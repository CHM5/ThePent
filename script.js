// Pricing Toggle Functionality
document.addEventListener('DOMContentLoaded', () => {
  const plans = [
    {
      name: 'Base',
      prices: { monthly: 'GRATIS', yearly: 'GRATIS' },
      features: [
        { label: 'Actualizaciones', info: 'Actualizaciones automáticas del sistema' },
        { label: 'Datos negocio', info: 'Carga y edición de información básica del local' },
        { label: 'Seguridad Sitio Seguro', info: 'Certificado SSL incluido' },
        { label: 'Máx. 25 productos', info: 'Podés cargar hasta 25 ítems en tu carta' },
        { label: 'Hosting limitado', info: 'Conexión restringida al plan gratuito' }
      ]
    },
    {
      name: 'Emprendedor',
      prices: { monthly: '$18.000', yearly: '$180.000' },
      features: [
        { label: 'Actualizaciones', info: 'Actualizaciones automáticas del sistema' },
        { label: 'Datos negocio', info: 'Carga y edición de información básica del local' },
        { label: 'Productos ilimitados', info: 'Sin límite de carga de productos' },
        { label: 'Botón redes', info: 'Enlaces a redes sociales desde tu carta' },
        { label: 'Sin publicidad', info: 'Carta sin banners ni anuncios externos' },
        { label: 'Hosting 24/7', info: 'Acceso permanente a la carta online' }
      ]
    },
    {
      name: 'Profesional',
      prices: { monthly: '$36.000', yearly: '$360.000' },
      features: [
        { label: 'Todo lo anterior', info: 'Incluye todas las características previas' },
        { label: 'Botón WhatsApp', info: 'Contacto directo vía WhatsApp desde la carta' },
        { label: 'Dominio propio', info: 'URL personalizada con el nombre de tu local' },
        { label: 'Fotos platos', info: 'Galería fotográfica para mostrar tus productos' },
        { label: 'Diseño carta física 20% OFF', info: 'Descuento exclusivo en impresiones físicas' }
      ]
    },
    {
      name: 'Corporativo',
      prices: { monthly: '$72.000', yearly: '$720.000' },
      features: [
        { label: 'Todo lo anterior', info: 'Incluye todas las características previas' },
        { label: 'Promos x temporada', info: 'Asistencia para crear promociones estacionales' },
        { label: 'Informe mensual', info: 'Reporte con métricas de uso y visitas' },
        { label: 'Atención prioritaria', info: 'Soporte técnico rápido y personalizado' },
        { label: 'Diseño carta física 30% OFF', info: 'Descuento exclusivo en impresiones físicas' }
      ]
    }
  ];

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
              ✓ ${f.label}
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