document.addEventListener('DOMContentLoaded', () => {

  function togglePricing(mode) {
  currentMode = mode;
    document.querySelectorAll('.pricing-toggle button').forEach(btn => {
      btn.classList.remove('active');
    });
    document.getElementById(`${mode}Btn`).classList.add('active');
    renderPricing(mode);
  }

function renderPricing(mode) {
  const container = document.getElementById('pricingContainer');
  container.innerHTML = '';

  plans.forEach(plan => {
    const card = document.createElement('div');
    card.className = 'pricing-card';

    const planId = plan.ids[mode];

    // Acá filtramos por modes (o incluimos si no tiene definido)
    const filteredFeatures = plan.features
      .filter(f => !f.modes || f.modes.includes(mode))
      .map(f => `
        <li>
          ✓ ${f.label}
          <span class="info-icon" title="${f.info}">i</span>
        </li>
      `).join('');

    card.innerHTML = `
      <h3>${plan.name}</h3>
      <div class="price">${plan.prices[mode]}</div>
      <ul class="feature-list">
        ${plan.features
          .filter(f => !f.modes || f.modes.includes(mode))
          .map(f => `
            <li>
              ✓ ${f.label}
              <span class="info-icon" title="${f.info}">i</span>
            </li>
          `).join('')}
      </ul>
      <button class="select-btn" data-plan="${planId}">Seleccionar</button>
    `;

    container.appendChild(card);
  });

  document.querySelectorAll('.select-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const planId = e.currentTarget.getAttribute('data-plan');
      window.location.href = `plansForm.html?plan=${planId}`;
    });
  });
}



  // Toggle buttons
  document.getElementById('monthlyBtn').addEventListener('click', () => togglePricing('monthly'));
  document.getElementById('yearlyBtn').addEventListener('click', () => togglePricing('yearly'));
  togglePricing('monthly'); // default

  // Mobile menu toggle
  const burger = document.querySelector('.navbar8-burger-menu');
  const closeBtn = document.querySelector('.navbar8-close-menu');
  const mobileMenu = document.querySelector('.navbar8-mobile-menu');

  // Cerrar menú al hacer clic en cualquier link dentro del menú móvil
  mobileMenu.addEventListener('click', (e) => {
    const link = e.target.closest('a');
    if (link && mobileMenu.contains(link)) {
      mobileMenu.classList.remove('active');
    }
  });

  burger.addEventListener('click', () => {
    mobileMenu.classList.toggle('active');
  });

  closeBtn.addEventListener('click', () => {
    mobileMenu.classList.remove('active');
  });

  // Botones generales
  document.querySelectorAll('.navbar8-action11, .navbar8-action21, .hero17-button1, .hero17-button2').forEach(button => {
    button.addEventListener('click', function () {
      const text = this.textContent.trim();
      alert(`Botón "${text}" clickeado - Agrega aquí la funcionalidad deseada`);
    });
  });

  // Debugging (podés borrar esto después de testear)
  document.querySelectorAll('button, a').forEach(element => {
    element.addEventListener('click', function () {
      console.log('Elemento clickeado:', this);
    });
  });
});
