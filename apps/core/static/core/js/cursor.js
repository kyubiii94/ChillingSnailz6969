/* Custom Cursor */
const cur = document.getElementById('cursor');
const fol = document.getElementById('cursor-follower');
let mx=0, my=0, fx=0, fy=0;
document.addEventListener('mousemove', e => {
  mx = e.clientX; my = e.clientY;
  cur.style.left = mx + 'px';
  cur.style.top  = my + 'px';
});
function animFol() {
  fx += (mx - fx) * 0.15;
  fy += (my - fy) * 0.15;
  fol.style.left = fx + 'px';
  fol.style.top  = fy + 'px';
  requestAnimationFrame(animFol);
}
animFol();

const _hoverSel = 'a,button,.faction-card,.nft-card,.game-entry,.promo-card,.wallet-btn,.console-btn';
document.addEventListener('mouseover', e => { if (e.target.closest(_hoverSel)) document.body.classList.add('hovering'); });
document.addEventListener('mouseout',  e => { if (e.target.closest(_hoverSel)) document.body.classList.remove('hovering'); });
