// Modern Sponsorship Form JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Get form elements
    const sponsorshipForm = document.getElementById('sponsorshipForm');
    const formSteps = document.querySelectorAll('.form-step');
    const progressFill = document.querySelector('.progress-fill');
    const progressSteps = document.querySelectorAll('.step');
    const nextButtons = document.querySelectorAll('.next-btn');
    const prevButtons = document.querySelectorAll('.prev-btn');
    const submitButton = document.querySelector('.submit-btn');
    const formSuccess = document.getElementById('formSuccess');
    const resetFormButton = document.getElementById('resetForm');
    const sponsorshipLevel = document.getElementById('sponsorshipLevel');
    const customAmountContainer = document.getElementById('customAmountContainer');
    
    // Current step tracker
    let currentStep = 1;
    
    // Initialize form
    updateFormProgress(currentStep);
    
    // Handle "Next" button clicks
    nextButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Validate current step before proceeding
            if (validateStep(currentStep)) {
                if (currentStep < formSteps.length) {
                    currentStep++;
                    updateFormProgress(currentStep);
                }
            }
        });
    });
    
    // Handle "Previous" button clicks
    prevButtons.forEach(button => {
        button.addEventListener('click', function() {
            if (currentStep > 1) {
                currentStep--;
                updateFormProgress(currentStep);
            }
        });
    });
    
    // Handle sponsorship level change
    sponsorshipLevel.addEventListener('change', function() {
        if (this.value === 'platinum') {
            customAmountContainer.style.display = 'block';
        } else {
            customAmountContainer.style.display = 'none';
        }
    });
    
    // Handle form submission
    sponsorshipForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Validate the final step
        if (validateStep(currentStep)) {
            // Get form data
            const formData = new FormData(sponsorshipForm);
            const formDataObj = {};
            
            formData.forEach((value, key) => {
                formDataObj[key] = value;
            });
            
            // Log form data (in a real application, you would send this to your server)
            console.log('Sponsorship Form Submission:', formDataObj);
            
            // Show success message
            currentStep++;
            updateFormProgress(currentStep);
            
            // Add animation to success icon
            document.querySelector('.success-icon').classList.add('animated');
        }
    });
    
    // Handle form reset
    resetFormButton.addEventListener('click', function() {
        window.location.href = 'index.html';
    });
    
    // Function to update form progress
    function updateFormProgress(step) {
        // Hide all steps
        formSteps.forEach(formStep => {
            formStep.classList.remove('active');
        });
        
        // Show current step
        document.querySelector(`.form-step[data-step="${step}"]`).classList.add('active');
        
        // Update progress bar
        progressFill.style.width = `${((step - 1) / (formSteps.length - 1)) * 100}%`;
        
        // Update progress steps
        progressSteps.forEach((progressStep, idx) => {
            if (idx + 1 <= step) {
                progressStep.classList.add('active');
            } else {
                progressStep.classList.remove('active');
            }
        });
    }
    
    // Function to validate each step
    function validateStep(step) {
        document.getElementById('formError').style.display = 'none';
        const currentStepEl = document.querySelector(`.form-step[data-step="${step}"]`);
        const requiredFields = currentStepEl.querySelectorAll('[required]');
        let isValid = true;

        // ✅ Validación personalizada del paso 1: al menos un producto seleccionado
        if (step === 1) {
            const checkboxes = document.querySelectorAll('.product-checkbox');
            const algunoSeleccionado = Array.from(checkboxes).some(cb => cb.checked);
            if (!algunoSeleccionado) {
                const errorBox = document.getElementById('formError');
                errorBox.textContent = 'Debés seleccionar al menos un producto para continuar.';
                errorBox.style.display = 'block';
                return false;
            }
        }

        // Validar campos requeridos
        requiredFields.forEach(field => {
            field.style.borderColor = '';

            if (!field.checkValidity() || field.value.trim() === '') {
                field.style.borderColor = 'var(--danger-color)';
                isValid = false;

                // Shake animation
                field.classList.add('shake');
                setTimeout(() => {
                    field.classList.remove('shake');
                }, 500);
            }
        });

        // Validación personalizada para USA (platinum)
        if (step === 2 && sponsorshipLevel.value === 'platinum') {
            const customAmount = document.getElementById('customAmount');
            if (!customAmount.value || parseInt(customAmount.value) < 10000) {
                customAmount.style.borderColor = 'var(--danger-color)';
                isValid = false;

                customAmount.classList.add('shake');
                setTimeout(() => {
                    customAmount.classList.remove('shake');
                }, 500);
            }
        }

        return isValid;
    }


  const productCheckboxes = document.querySelectorAll('.product-checkbox');
  const totalAmountDisplay = document.getElementById('totalAmount');

  function updateTotalAmount() {
    let total = 0;
    productCheckboxes.forEach(cb => {
      if (cb.checked) {
        total += parseFloat(cb.getAttribute('data-price'));
      }
    });
    totalAmountDisplay.innerHTML = `<strong>Total: $${total}</strong>`;
  }

  productCheckboxes.forEach(cb => {
    cb.addEventListener('change', updateTotalAmount);
  });




document.addEventListener('DOMContentLoaded', () => {
  const radios = document.querySelectorAll('.plan');
  const totalDisplay = document.getElementById('totalAmount');

  radios.forEach(radio => {
    radio.addEventListener('change', () => {
      const selected = document.querySelector('.plan:checked');
      const price = selected ? parseInt(selected.dataset.price || 0, 10) : 0;
      totalDisplay.innerHTML = `<strong>Total: $${price.toLocaleString()}</strong>`;
    });
  });
});

});