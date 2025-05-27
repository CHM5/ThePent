// Modern Sponsorship Form JavaScript

document.addEventListener('DOMContentLoaded', function () {
    // Get form elements
    const sponsorshipForm = document.getElementById('sponsorshipForm');
    const formSteps = document.querySelectorAll('.form-step');
    const progressFill = document.querySelector('.progress-fill');
    const progressSteps = document.querySelectorAll('.step');
    const nextButtons = document.querySelectorAll('.next-btn');
    const prevButtons = document.querySelectorAll('.prev-btn');
    const submitButton = document.querySelector('.submit-btn');
    const resetFormButton = document.getElementById('resetForm');
    const sponsorshipLevel = document.getElementById('sponsorshipLevel');
    const customAmountContainer = document.getElementById('customAmountContainer');

    let currentStep = 1;
    updateFormProgress(currentStep);

    nextButtons.forEach(button => {
        button.addEventListener('click', function () {
            if (validateStep(currentStep)) {
                if (currentStep < formSteps.length) {
                    currentStep++;
                    updateFormProgress(currentStep);
                }
            }
        });
    });

    prevButtons.forEach(button => {
        button.addEventListener('click', function () {
            if (currentStep > 1) {
                currentStep--;
                updateFormProgress(currentStep);
            }
        });
    });

    sponsorshipLevel.addEventListener('change', function () {
        customAmountContainer.style.display = this.value === 'platinum' ? 'block' : 'none';
    });

    sponsorshipForm.addEventListener('submit', function (e) {
        e.preventDefault();
        if (validateStep(currentStep)) {
            const formData = new FormData(sponsorshipForm);
            const formDataObj = {};
            formData.forEach((value, key) => {
                formDataObj[key] = value;
            });

            console.log('Sponsorship Form Submission:', formDataObj);
            currentStep++;
            updateFormProgress(currentStep);
            document.querySelector('.success-icon').classList.add('animated');
        }
    });

    resetFormButton.addEventListener('click', function () {
        window.location.href = 'index.html';
    });

    function updateFormProgress(step) {
        formSteps.forEach(formStep => formStep.classList.remove('active'));
        document.querySelector(`.form-step[data-step="${step}"]`).classList.add('active');
        progressFill.style.width = `${((step - 1) / (formSteps.length - 1)) * 100}%`;

        progressSteps.forEach((progressStep, idx) => {
            progressStep.classList.toggle('active', idx + 1 <= step);
        });

        // Actualiza la info del plan en el paso 4
        if (step === 4) {
            updatePlanInfo();
        }
    }

    function validateStep(step) {
        document.getElementById('formError').style.display = 'none';
        const currentStepEl = document.querySelector(`.form-step[data-step="${step}"]`);
        const requiredFields = currentStepEl.querySelectorAll('[required]');
        let isValid = true;

        if (step === 1) {
            const selectedPlan = document.querySelector('input.plan[type="radio"]:checked');
            const errorBox = document.getElementById('formError');

            if (!selectedPlan) {
                errorBox.textContent = 'Seleccioná un plan para continuar.';
                errorBox.style.display = 'block';
                return false;
            } else {
                errorBox.style.display = 'none';
            }
        }

        requiredFields.forEach(field => {
            field.style.borderColor = '';
            if (!field.checkValidity() || field.value.trim() === '') {
                field.style.borderColor = 'var(--danger-color)';
                isValid = false;
                field.classList.add('shake');
                setTimeout(() => field.classList.remove('shake'), 500);
            }
        });

        if (step === 2 && sponsorshipLevel.value === 'platinum') {
            const customAmount = document.getElementById('customAmount');
            if (!customAmount.value || parseInt(customAmount.value) < 10000) {
                customAmount.style.borderColor = 'var(--danger-color)';
                customAmount.classList.add('shake');
                setTimeout(() => customAmount.classList.remove('shake'), 500);
                return false;
             }
            }        

        if (step === 3) {
            const agreeTerms = document.getElementById('agreeTerms');
            if (!agreeTerms.checked) {
                const errorBox = document.getElementById('termsError');
                errorBox.textContent = 'Debes aceptar los términos y condiciones para continuar.';
                errorBox.style.display = 'block';
                customAmount.classList.add('shake');
                setTimeout(() => customAmount.classList.remove('shake'), 500);
                return false;
            }
            }
        return isValid; // <-- AGREGA ESTA LÍNEA
    }

    // Actualización del total dinámico según plan seleccionado
    const radios = document.querySelectorAll('.plan');
    const totalDisplay = document.getElementById('totalAmount');

    function updateTotal() {
        const selected = document.querySelector('.plan:checked');
        const price = parseInt(selected?.dataset.price || 0, 10);

        if (!selected) {
            totalDisplay.innerHTML = `<strong>Total: $0</strong>`;
            return;
        }
        // Actualiza todos los spans con class="priceValue"
        document.querySelectorAll('.priceValue').forEach(el => {
            el.textContent = price.toLocaleString();
        });
        if (priceValue) {
            priceValue.textContent = price.toLocaleString();
        }
    }


    
    radios.forEach(radio => {
        radio.addEventListener('change', function() {
            updateTotal();
            updatePlanInfo();
        });
    });

    updateTotal(); // Mostrar al cargar

    // Si querés que al volver del pago de MercadoPago se pase al paso 6:
    window.addEventListener('message', function (event) {
        // Verificamos que venga de MercadoPago y que tenga la estructura esperada (puede variar según tu integración real)
        if (event.origin.includes("mercadopago")) {
            console.log("💬 Mensaje recibido desde Mercado Pago:", event.data);

            if (event.data && event.data.preapproval_id) {
                console.log("🔁 Suscripción confirmada:", event.data.preapproval_id);
                currentStep = 6;
                updateFormProgress(currentStep);
            }
        }

    });



// Paso 5: redirigir a MercadoPago si el plan es pago
const mpRedirectBtn = document.getElementById('mpRedirectBtn');
if (mpRedirectBtn) {
    mpRedirectBtn.addEventListener('click', function () {
        const selected = document.querySelector('.plan:checked');
        const price = parseInt(selected?.dataset.price || 0, 10);

        const mpLinks = {
            18000: "https://www.mercadopago.com.ar/subscriptions/checkout?preapproval_plan_id=2c938084968c9eaa01969982254c05d0",
            36000: "https://www.mercadopago.com.ar/subscriptions/checkout?preapproval_plan_id=2c938084968c9eaa01969982254c05d0",
            72000: "https://www.mercadopago.com.ar/subscriptions/checkout?preapproval_plan_id=2c938084968c9eaa01969982254c05d0",
            180000: "https://www.mercadopago.com.ar/subscriptions/checkout?preapproval_plan_id=2c938084968c9eaa01969982254c05d0",
            360000: "hhttps://www.mercadopago.com.ar/subscriptions/checkout?preapproval_plan_id=2c938084968c9eaa01969982254c05d0",
            720000: "https://www.mercadopago.com.ar/subscriptions/checkout?preapproval_plan_id=2c938084968c9eaa01969982254c05d0"
        };

        if (price === 0) {
            currentStep = 6;
            updateFormProgress(currentStep);
        } else if (mpLinks[price]) {
            window.location.href = mpLinks[price];
        } else {
            alert("No se encontró el enlace de pago para el plan seleccionado.");
        }
    });
}

    function updatePlanInfo() {
        const selected = document.querySelector('.plan:checked');
        const planInfo = document.getElementById('planInfo');

        if (!selected || !planInfo) {
            if (planInfo) planInfo.innerHTML = '';
            return;
        }

        let planKey = selected.value || selected.id || '';
        let planName = '';
        let planDesc = '';

        // Intenta obtener el nombre del plan desde el label
        let label = selected.closest('label') || document.querySelector(`label[for="${selected.id}"]`);
        if (label) {
            planName = label.textContent.split('(')[0].trim();
        } else {
            planName = planKey;
        }

        const nameLower = planName.toLowerCase();

        if (nameLower.includes('base')) {
            planDesc = `
                <ul>
                    <li>✅ Actualizaciones del software limitadas</li>
                    <li>✅ Carga y edición de información básica del local</li>
                    <li>✅ Certificado SSL incluido</li>
                    <li>✅ Hasta 25 ítems en tu carta</li>
                    <li>⚠️ Hosting limitado</li>
                </ul>
            `;
        } else if (nameLower.includes('emprendedor')) {
            planDesc = `
                <ul>
                    <li>✅ Actualizaciones automáticas ilimitadas</li>
                    <li>✅ Carga y edición completa</li>
                    <li>✅ Certificado SSL incluido</li>
                    <li>✅ Productos ilimitados</li>
                    <li>✅ Dominio personalizado</li>
                    <li>✅ Soporte estándar</li>
                    <li>✅ Sin publicidad</li>
                    <li>✅ Hosting 24/7</li>
                    <li>
                        <strong>Extra:</strong>
                        <ul>
                            <li>⚠️ 5% de descuento en productos</li>
                        </ul>
                    </li>
                </ul>
            `;
        } else if (nameLower.includes('profesional')) {
            planDesc = `
                <ul>
                    <li><strong>Incluye todo lo del plan Emprendedor, más:</strong></li>
                    <li>✅ Diseño personalizado</li>
                    <li>✅ Galería de fotos</li>
                    <li>✅ Soporte prioritario</li>
                    <li>✅ Botón de WhatsApp</li>
                    <li>✅ Dominio personalizado</li>
                    <li>
                        <strong>Extras:</strong>
                        <ul>
                            <li>⚠️ 10% de descuento en productos</li>
                        </ul>
                    </li>
                </ul>
            `;
        } else if (nameLower.includes('corporativo')) {
            planDesc = `
                <ul>
                    <li><strong>Incluye todo lo del plan Profesional, más:</strong></li>
                    <li>✅ Gestión multisucursal</li>
                    <li>✅ Atención personalizada 1 a 1</li>
                    <li>✅ Edición avanzada</li>
                    <li>✅ Informe mensual de visitas</li>
                    <li>
                        <strong>Extras:</strong>
                        <ul>
                            <li>⚠️ 20% de descuento en productos</li>
                        </ul>
                    </li>
                </ul>
            `;
        } else {
            planDesc = `<em>Este producto no tiene descripción detallada.</em>`;
        }

        planInfo.innerHTML = `Plan <h3>${planName}</h3>${planDesc}`;
    }


});


