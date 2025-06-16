// Pricing Toggle Functionality
document.addEventListener('DOMContentLoaded', () => {
  
  function togglePricing(mode) {
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
      card.innerHTML = `
        <h3>${plan.name}</h3>
        <div class="price">${plan.prices[mode]}</div>
        <ul class="feature-list">
          ${plan.features.map(f => `
            <li>
              ${f.label}
              <span class="info-icon" title="${f.info}">i</span>
            </li>
          `).join('')}
        </ul>
        <button class="select-btn">Seleccionar</button>
      `;
      container.appendChild(card);
    });
  }

  // Event listeners for pricing buttons
  document.getElementById('monthlyBtn').addEventListener('click', () => togglePricing('monthly'));
  document.getElementById('yearlyBtn').addEventListener('click', () => togglePricing('yearly'));
  
  // Initialize with monthly pricing
  togglePricing('monthly');

  // General button handlers
  document.querySelectorAll('.navbar8-action11, .navbar8-action21, .hero17-button1, .hero17-button2').forEach(button => {
    button.addEventListener('click', function() {
      const text = this.textContent.trim();
      alert(`Botón "${text}" clickeado - Agrega aquí la funcionalidad deseada`);
    });
  });

  // Mobile menu handlers
  document.querySelector('.navbar8-burger-menu').addEventListener('click', function() {
    const mobileMenu = document.querySelector('.navbar8-mobile-menu');
    mobileMenu.style.display = mobileMenu.style.display === 'block' ? 'none' : 'block';
  });

  document.querySelector('.navbar8-close-menu').addEventListener('click', function() {
    document.querySelector('.navbar8-mobile-menu').style.display = 'none';
  });

  // Debugging all buttons
  document.querySelectorAll('button, a').forEach(element => {
    element.addEventListener('click', function(e) {
      console.log('Elemento clickeado:', this);
    });
  });

});
