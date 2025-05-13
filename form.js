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
            sponsorshipForm.style.display = 'none';
            formSuccess.style.display = 'block';
            
            // Add animation to success icon
            document.querySelector('.success-icon').classList.add('animated');
        }
    });
    
    // Handle form reset
    resetFormButton.addEventListener('click', function() {
        // Reset form fields
        sponsorshipForm.reset();
        
        // Reset to first step
        currentStep = 1;
        updateFormProgress(currentStep);
        
        // Hide success message and show form
        formSuccess.style.display = 'none';
        sponsorshipForm.style.display = 'block';
        
        // Reset custom amount container
        customAmountContainer.style.display = 'none';
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
        const currentStepEl = document.querySelector(`.form-step[data-step="${step}"]`);
        const requiredFields = currentStepEl.querySelectorAll('[required]');
        let isValid = true;
        
        // Check each required field
        requiredFields.forEach(field => {
            // Clear previous error styling
            field.style.borderColor = '';
            
            // Check if field is empty or invalid
            if (!field.checkValidity() || field.value.trim() === '') {
                field.style.borderColor = 'var(--danger-color)';
                isValid = false;
                
                // Add shake animation
                field.classList.add('shake');
                setTimeout(() => {
                    field.classList.remove('shake');
                }, 500);
            }
        });
        
        // Custom validation for specific fields
        if (step === 2 && sponsorshipLevel.value === 'platinum') {
            const customAmount = document.getElementById('customAmount');
            if (!customAmount.value || parseInt(customAmount.value) < 10000) {
                customAmount.style.borderColor = 'var(--danger-color)';
                isValid = false;
                
                // Add shake animation
                customAmount.classList.add('shake');
                setTimeout(() => {
                    customAmount.classList.remove('shake');
                }, 500);
            }
        }
        
        return isValid;
    }
    
    // Add keypress event for enter key
    document.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && document.activeElement.type !== 'textarea') {
            e.preventDefault();
            // Trigger click on the appropriate button based on current step
            if (currentStep < formSteps.length) {
                document.querySelector(`.form-step[data-step="${currentStep}"] .next-btn`).click();
            } else {
                submitButton.click();
            }
        }
    });
    
    // Add animations for input fields
    const inputFields = document.querySelectorAll('input, select, textarea');
    
    inputFields.forEach(field => {
        // Focus effect
        field.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        field.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
        });
    });
    
    // Add CSS for shake animation
    const style = document.createElement('style');
    style.innerHTML = `
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
            20%, 40%, 60%, 80% { transform: translateX(5px); }
        }
        
        .shake {
            animation: shake 0.5s cubic-bezier(.36,.07,.19,.97) both;
        }
        
        .focused {
            transition: all 0.3s ease;
        }
        
        @keyframes successFade {
            0% { transform: scale(0.7); opacity: 0; }
            50% { transform: scale(1.1); }
            100% { transform: scale(1); opacity: 1; }
        }
        
        .success-icon.animated {
            animation: successFade 0.5s ease forwards;
        }
    `;
    document.head.appendChild(style);
});