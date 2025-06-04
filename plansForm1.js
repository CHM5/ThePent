document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('sponsorshipForm');
  const formSteps = document.querySelectorAll('.form-step');
  const nextButtons = document.querySelectorAll('.next-btn');
  const prevButtons = document.querySelectorAll('.prev-btn');
  let currentStep = 1;

  // Muestra únicamente el paso actual
  function showStep(step) {
    formSteps.forEach(stepDiv => {
      if (parseInt(stepDiv.getAttribute('data-step'), 10) === step) {
        stepDiv.classList.add('active');
      } else {
        stepDiv.classList.remove('active');
      }
    });
  }
  showStep(currentStep);

  // Validación para el paso 1: todos los campos [required]
  function validateStep1() {
    let isValid = true;
    const step1 = document.querySelector('.form-step[data-step="1"]');
    if (!step1) return false;
    const requiredFields = step1.querySelectorAll('[required]');
    requiredFields.forEach(field => {
      field.style.borderColor = '';
      if (!field.value.trim()) {
        field.style.borderColor = 'red';
        isValid = false;
      }
    });
    if (!isValid) {
      alert('Por favor complete todos los campos obligatorios del Paso 1.');
    }
    return isValid;
  }

  // Validación para el paso 2: checkbox debe estar marcado
  function validateStep2() {
    const agreeTerms = document.getElementById('agreeTerms');
    if (!agreeTerms || !agreeTerms.checked) {
      alert('Debe aceptar los términos y condiciones para continuar.');
      return false;
    }
    return true;
  }

  // Maneja el click en los botones "Siguiente"
  nextButtons.forEach(button => {
    button.addEventListener('click', function () {
      if (currentStep === 1) {
        // Validar paso 1
        if (!validateStep1()) return;
        currentStep++;
        showStep(currentStep);
      } else if (currentStep === 2) {
        // Validar checkbox en paso 2
        if (!validateStep2()) return;
        currentStep++;
        showStep(currentStep);
      } else if (currentStep === 3) {
        // En el paso 3 se dispara el push a Apps Script
        const formData = new FormData(form);
        const formDataObj = {};
        formData.forEach((value, key) => {
          formDataObj[key] = value;
        });
        // Puedes incluir información adicional, p.ej: plan, etc.
        // Llamada a Apps Script
        fetch("https://script.google.com/macros/s/AKfycbx2Gl5uAJm19Jn0duS6cbFLaJfZeslv7H6lLKFPWqGQjQpvBky_1HNKQqs2Nx7zeI7N/exec", {
          method: "POST",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded"
          },
          body: new URLSearchParams(formDataObj).toString()
        })
        .then(response => response.text())
        .then(text => {
          console.log("✅ Datos enviados a Apps Script:", text);
          currentStep++; // Avanza al paso 4 si la respuesta es exitosa
          showStep(currentStep);
        })
        .catch(err => {
          console.error("❌ Error al enviar a Apps Script:", err);
          alert("Ocurrió un error al enviar sus datos. Inténtelo nuevamente.");
        });
      }
    });
  });

  // Maneja el click en los botones "Atrás"
  prevButtons.forEach(button => {
    button.addEventListener('click', function () {
      if (currentStep > 1) {
        currentStep--;
        showStep(currentStep);
      }
    });
  });

  // Opcional: evitar el envío por defecto del formulario
  form.addEventListener('submit', function (e) {
    e.preventDefault();
  });
});