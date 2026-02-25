/* Menu responsive (hamburger) */
(function() {
  const nav = document.querySelector('nav');
  const toggle = document.getElementById('navToggle');
  const menu = document.getElementById('navMenu');
  if (!nav || !toggle || !menu) return;
  function openMenu() {
    nav.classList.add('nav-open');
    toggle.setAttribute('aria-expanded', 'true');
    toggle.setAttribute('aria-label', 'Fermer le menu');
    document.body.style.overflow = 'hidden';
  }
  function closeMenu() {
    nav.classList.remove('nav-open');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'Ouvrir le menu');
    document.body.style.overflow = '';
  }
  toggle.addEventListener('click', function() {
    if (nav.classList.contains('nav-open')) closeMenu();
    else openMenu();
  });
  menu.querySelectorAll('.nav-link').forEach(function(link) {
    link.addEventListener('click', closeMenu);
  });
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && nav.classList.contains('nav-open')) closeMenu();
  });
})();
