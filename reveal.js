document.addEventListener('DOMContentLoaded', () => {
  const els = document.querySelectorAll('.reveal');
  // If IntersectionObserver missing or user prefers reduced motion, just show all
  const reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!('IntersectionObserver' in window) || reduced) {
    els.forEach(el => el.classList.add('visible'));
    return;
  }
  const io = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('visible'); io.unobserve(e.target); }
    });
  }, { threshold: 0.01, rootMargin: '0px 0px 200px 0px' });
  els.forEach(el => io.observe(el));
  // Safety net: after 3s, force-show anything still hidden
  setTimeout(() => document.querySelectorAll('.reveal:not(.visible)').forEach(el => el.classList.add('visible')), 3000);
});
