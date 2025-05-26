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
