#!/usr/bin/env node
// The banner: one schematic claim, not a rendering of the documentation.
//
// THE CLAIM: the clock lives outside every agent, and the loop closes through a
// fixed contract. Nothing else belongs in this figure. The handoff fields, the
// seven phases, the two ladders and the nine ledgers are tables in the README
// and in docs/. Repeating them here costs the legibility and buys nothing.
//
// THE RULES THIS SCRIPT ENFORCES (it exits non-zero rather than emit a figure
// that breaks them, because the first version of this diagram failed by growing
// the canvas to fit the text instead of cutting the text):
//   * banner proportions, so it reads in a README column;
//   * a hard word budget for the whole figure;
//   * a minimum type size, measured at the width GitHub actually renders;
//   * no label wider than the box it sits in.
//
//   node docs/figures/workflow.mjs
//     -> docs/figures/workflow-light.svg
//        docs/figures/workflow-dark.svg

import { writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const HERE = dirname(fileURLToPath(import.meta.url));

const W = 1600, H = 560;          // 2.86 : 1
const COLUMN = 850;               // what a README column gives the figure
const MAX_WORDS = 50;
const MIN_SIZE = 22;              // on canvas -> 11.7px rendered at COLUMN
const MIN_RATIO = 2.4;            // anything squarer is not a banner

const THEMES = {
  light: {
    bg: '#ffffff', card: '#ffffff', ghost: '#f6f8fa', border: '#d0d7de',
    text: '#1f2328', muted: '#59636e', wire: '#424a53',
    coord: '#0550ae', exec: '#6639ba', sec: '#1a7f37', aud: '#a40e26',
  },
  dark: {
    bg: '#0d1117', card: '#161b22', ghost: '#12181f', border: '#30363d',
    text: '#e6edf3', muted: '#9198a1', wire: '#9198a1',
    coord: '#79c0ff', exec: '#d2a8ff', sec: '#56d364', aud: '#ff7b72',
  },
};

const SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif";
const MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace";

const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

function width(s, size, mono) {
  let w = 0;
  for (const ch of s) {
    const c = ch.codePointAt(0);
    let f;
    if (c > 0x2000) f = 1.1;
    else if (mono) f = 0.602;
    else if (/[A-Z]/.test(ch)) f = 0.68;
    else if (/[ilt.,'!|:;]/.test(ch)) f = 0.31;
    else if (/[mwMW]/.test(ch)) f = 0.86;
    else f = 0.545;
    w += size * f;
  }
  return w;
}

// ------------------------------------------------------------------ content

const NODE_W = 360, NODE_H = 140, ROW1 = 110, ROW2 = 320, CHECK_H = 120;
const X = [50, 620, 1190];
const MID1 = ROW1 + NODE_H / 2;

const TITLE = 'The Descartes loop';
const THESIS = 'the clock lives outside every agent';

const ACTORS = [
  { x: X[0], y: ROW1, h: NODE_H, accent: 'coord', title: 'Coordinator', sub: 'holds the clock' },
  { x: X[1], y: ROW1, h: NODE_H, accent: 'exec', title: 'Descartes', sub: 'Executor, runs one pass' },
  { x: X[1], y: ROW2, h: CHECK_H, accent: 'sec', title: 'Secretary', sub: 'marks the phases' },
  { x: X[2], y: ROW2, h: CHECK_H, accent: 'aud', title: 'Doubt auditor', sub: 'can only kill a doubt' },
];

const HANDOFF = { x: X[2], y: ROW1, h: NODE_H, mono: '=== LOOP HANDOFF ===', sub: 'fixed fields' };

const EDGES = ['fires one pass', 'returns', 'also fires', 'decides the next tick'];

// ------------------------------------------------------------------ render

function render(t) {
  const out = [];
  const warn = [];
  const words = [];
  const push = (s) => out.push(s);

  const text = (x, y, s, o = {}) => {
    const { size = 23, color = t.text, weight = 400, mono = false, anchor = 'start', limit = null } = o;
    words.push(...s.split(/\s+/).filter(Boolean));
    if (size < MIN_SIZE) warn.push(`type too small (${size}px < ${MIN_SIZE}px): "${s}"`);
    if (limit != null) {
      const w = width(s, size, mono);
      const left = anchor === 'middle' ? x - w / 2 : x;
      if (left + w > limit) warn.push(`overflow ${Math.round(left + w - limit)}px: "${s}"`);
    }
    push(`<text x="${x}" y="${y}" font-family="${mono ? MONO : SANS}" font-size="${size}" `
      + `font-weight="${weight}" fill="${color}" text-anchor="${anchor}">${esc(s)}</text>`);
  };

  const wire = (d, o = {}) => {
    const { dash = null, w = 2.4 } = o;
    push(`<path d="${d}" fill="none" stroke="${t.wire}" stroke-width="${w}" stroke-linecap="round" `
      + `stroke-linejoin="round"${dash ? ` stroke-dasharray="${dash}"` : ''} marker-end="url(#head)"/>`);
  };

  push(`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" `
    + `role="img" aria-label="The Descartes loop. A coordinator holds the clock and fires the executor, Descartes, `
    + `which runs one pass and returns a fixed handoff block; the coordinator also fires a secretary that `
    + `marks the phases and a doubt auditor that can only kill a doubt. The handoff decides the next tick.">`);
  push(`<defs><marker id="head" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" `
    + `orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="${t.wire}"/></marker></defs>`);
  push(`<rect width="${W}" height="${H}" fill="${t.bg}"/>`);

  // title
  text(50, 62, TITLE, { size: 32, weight: 700 });
  text(50 + width(TITLE, 32, false) + 22, 62, THESIS, { size: 23, color: t.muted, limit: W - 50 });

  // actors
  for (const a of ACTORS) {
    const accent = t[a.accent];
    push(`<rect x="${a.x}" y="${a.y}" width="${NODE_W}" height="${a.h}" rx="12" fill="${t.card}" `
      + `stroke="${t.border}" stroke-width="1.5"/>`);
    push(`<path d="M ${a.x + 2} ${a.y + 14} V ${a.y + a.h - 14}" stroke="${accent}" stroke-width="5" `
      + `stroke-linecap="round"/>`);
    const cy = a.y + a.h / 2;
    text(a.x + 30, cy - 6, a.title, { size: 33, weight: 600, limit: a.x + NODE_W - 20 });
    text(a.x + 30, cy + 28, a.sub, { size: 23, color: t.muted, limit: a.x + NODE_W - 20 });
  }

  // the contract is an artefact, not an actor: dashed, monospaced
  push(`<rect x="${HANDOFF.x}" y="${HANDOFF.y}" width="${NODE_W}" height="${HANDOFF.h}" rx="12" `
    + `fill="${t.ghost}" stroke="${t.border}" stroke-width="1.5" stroke-dasharray="7 6"/>`);
  text(HANDOFF.x + NODE_W / 2, MID1 - 4, HANDOFF.mono,
    { size: 24, mono: true, weight: 600, anchor: 'middle', limit: HANDOFF.x + NODE_W - 16 });
  text(HANDOFF.x + NODE_W / 2, MID1 + 30, HANDOFF.sub, { size: 23, color: t.muted, anchor: 'middle' });

  // the single reading path, left to right
  wire(`M ${X[0] + NODE_W} ${MID1} H ${X[1] - 10}`);
  text((X[0] + NODE_W + X[1]) / 2, MID1 - 16, EDGES[0], { size: 23, color: t.muted, anchor: 'middle' });
  wire(`M ${X[1] + NODE_W} ${MID1} H ${X[2] - 10}`);
  text((X[1] + NODE_W + X[2]) / 2, MID1 - 16, EDGES[1], { size: 23, color: t.muted, anchor: 'middle' });

  // the coordinator also fires the two checks
  const trunk = X[0] + 250, branch = ROW2 - 36;
  wire(`M ${trunk} ${ROW1 + NODE_H} V ${branch} H ${X[1] + NODE_W / 2} V ${ROW2 - 10}`, { w: 2 });
  wire(`M ${trunk} ${ROW1 + NODE_H} V ${branch} H ${X[2] + NODE_W / 2} V ${ROW2 - 10}`, { w: 2 });
  text(trunk + 16, branch - 14, EDGES[2], { size: 23, color: t.muted });

  // and the handoff closes the tick
  const ret = H - 52;
  wire(`M ${X[2] + NODE_W} ${MID1} H ${W - 34} V ${ret} H ${X[0] + 110} V ${ROW1 + NODE_H + 10}`, { dash: '8 7' });
  text(X[0] + 130, ret - 16, EDGES[3], { size: 24, color: t.muted });

  push('</svg>');

  const ratio = W / H;
  if (ratio < MIN_RATIO) warn.push(`aspect ${ratio.toFixed(2)}:1 is squarer than the ${MIN_RATIO}:1 banner minimum`);
  if (words.length > MAX_WORDS) warn.push(`${words.length} words, budget is ${MAX_WORDS}: cut text, do not grow the canvas`);

  return { svg: out.join('\n'), warn, words: words.length };
}

let bad = 0;
for (const [name, t] of Object.entries(THEMES)) {
  const { svg, warn, words } = render(t);
  for (const w of warn) { console.error(`[${name}] ${w}`); bad++; }
  writeFileSync(join(HERE, `workflow-${name}.svg`), svg + '\n');
  console.log(`wrote workflow-${name}.svg  ${W}x${H} (${(W / H).toFixed(2)}:1)  ${words} words  `
    + `smallest type renders at ${(MIN_SIZE * COLUMN / W).toFixed(1)}px in a ${COLUMN}px column`);
}
if (bad) { console.error(`\n${bad} violation(s).`); process.exit(1); }
