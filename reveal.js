document.addEventListener('DOMContentLoaded', () => {
  const els = document.querySelectorAll('.reveal');
  const reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!('IntersectionObserver' in window) || reduced) {
    els.forEach(el => el.classList.add('visible'));
  } else {
    const io = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) { e.target.classList.add('visible'); io.unobserve(e.target); }
      });
    }, { threshold: 0.01, rootMargin: '0px 0px 200px 0px' });
    els.forEach(el => io.observe(el));
    setTimeout(() => document.querySelectorAll('.reveal:not(.visible)').forEach(el => el.classList.add('visible')), 3000);
  }

  // Photo carousel on animal pages
  document.querySelectorAll('.gallery-wrap').forEach(wrap => {
    const track = wrap.querySelector('.gallery-track');
    const slides = wrap.querySelectorAll('.gallery-slide');
    const dots = wrap.querySelectorAll('.gallery-dot');
    const prev = wrap.querySelector('.gallery-prev');
    const next = wrap.querySelector('.gallery-next');
    if (!track || slides.length < 2) {
      if (prev) prev.style.display = 'none';
      if (next) next.style.display = 'none';
      const dotsWrap = wrap.querySelector('.gallery-dots');
      if (dotsWrap) dotsWrap.style.display = 'none';
      return;
    }
    let idx = 0;
    const total = slides.length;
    const goTo = (i) => {
      idx = (i + total) % total;
      track.style.transform = `translateX(-${idx * 100}%)`;
      dots.forEach((d, di) => d.classList.toggle('active', di === idx));
    };
    prev && prev.addEventListener('click', () => goTo(idx - 1));
    next && next.addEventListener('click', () => goTo(idx + 1));
    dots.forEach((d, di) => d.addEventListener('click', () => goTo(di)));
    // Keyboard support
    wrap.setAttribute('tabindex', '0');
    wrap.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowLeft') goTo(idx - 1);
      if (e.key === 'ArrowRight') goTo(idx + 1);
    });
    // Touch swipe
    let startX = 0;
    track.addEventListener('touchstart', (e) => { startX = e.touches[0].clientX; }, { passive: true });
    track.addEventListener('touchend', (e) => {
      const dx = e.changedTouches[0].clientX - startX;
      if (Math.abs(dx) > 40) goTo(idx + (dx < 0 ? 1 : -1));
    });
  });
});
