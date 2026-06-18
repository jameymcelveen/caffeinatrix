// Caffeinatrix rain.
// Full-motion by design: every pixel cycles constantly, so there is nothing
// static to burn into an OLED/mini-LED panel over a long overnight run.

const canvas = document.getElementById('matrix');
const ctx = canvas.getContext('2d', { alpha: false });

const FONT_SIZE = 18;          // logical px
const HEAD = '#cfffd0';        // bright leading glyph
const BODY = '#00ff41';        // classic matrix green
const FPS = 26;                // capped to keep the laptop cool all night

// Glyph set: half-width katakana (U+FF66..U+FF9D) + digits.
const GLYPHS = (() => {
  const arr = [];
  for (let c = 0xff66; c <= 0xff9d; c++) arr.push(String.fromCharCode(c));
  for (let d = 0; d <= 9; d++) arr.push(String(d));
  return arr;
})();
const glyph = () => GLYPHS[(Math.random() * GLYPHS.length) | 0];

let dpr, cellW, cols, drops;

function setup() {
  dpr = window.devicePixelRatio || 1;
  const w = window.innerWidth;
  const h = window.innerHeight;

  canvas.width = Math.floor(w * dpr);
  canvas.height = Math.floor(h * dpr);
  canvas.style.width = w + 'px';
  canvas.style.height = h + 'px';

  cellW = FONT_SIZE * dpr;
  ctx.font = `${cellW}px ui-monospace, "SF Mono", Menlo, Consolas, monospace`;
  ctx.textBaseline = 'top';

  cols = Math.ceil(canvas.width / cellW);
  // Stagger starting rows so columns do not march in lockstep.
  drops = Array.from({ length: cols }, () => Math.random() * -40);

  ctx.fillStyle = '#000';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
}

setup();
window.addEventListener('resize', setup);

const slow = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const interval = 1000 / (slow ? 10 : FPS);
let last = 0;

function frame(now) {
  requestAnimationFrame(frame);
  if (now - last < interval) return;
  last = now;

  // Translucent black wash leaves fading tails instead of a hard clear.
  ctx.fillStyle = 'rgba(0, 0, 0, 0.07)';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  for (let i = 0; i < cols; i++) {
    const x = i * cellW;
    const y = drops[i] * cellW;

    ctx.fillStyle = HEAD;
    ctx.fillText(glyph(), x, y);

    ctx.fillStyle = BODY;
    ctx.fillText(glyph(), x, y - cellW);

    if (y > canvas.height && Math.random() > 0.975) {
      drops[i] = Math.random() * -20;
    }
    drops[i]++;
  }
}

requestAnimationFrame(frame);
