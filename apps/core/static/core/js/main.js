/* Scroll Reveal */
const revObs = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.style.animation = 'reveal-up 0.7s cubic-bezier(0.16,1,0.3,1) both';
      revObs.unobserve(e.target);
    }
  });
}, { threshold: 0.05, rootMargin: '0px 0px -30px 0px' });
document.querySelectorAll('.reveal').forEach(r => revObs.observe(r));

/* NFT Filter */
const _filterBtns = document.querySelectorAll('.filter-btn');
const _nftCards   = document.querySelectorAll('.nft-card');
function setFilter(type, btn) {
  _filterBtns.forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  _nftCards.forEach(c => {
    const t = c.dataset.t || '';
    c.style.display = (type === 'all' || t.includes(type)) ? '' : 'none';
  });
}

/* Progress bar */
setTimeout(() => {
  const bar = document.getElementById('mintBar');
  if (bar) bar.style.width = '23%';
}, 800);

/* Console screen loop */
const screenTxts = ['PRESS START', 'CHOOSE SNAILZ', 'SELECT FACTION', 'ENTER ARENA', 'PLAY 2 EARN'];
let si = 0;
const screenEl = document.querySelector('.console-screen span');
if (screenEl) {
  screenEl.style.transition = 'opacity 0.4s';
  setInterval(() => {
    si = (si + 1) % screenTxts.length;
    screenEl.style.opacity = '0';
    setTimeout(() => { screenEl.textContent = screenTxts[si]; screenEl.style.opacity = '1'; }, 400);
  }, 2500);
}
