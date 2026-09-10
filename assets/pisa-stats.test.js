/* Unit-Tests für PisaStats — Aufruf: node assets/pisa-stats.test.js (Exit 0 = alle Tests bestanden) */
const S = require('./pisa-stats.js');
const assert = require('assert');
let n = 0;
const t = (name, fn) => { fn(); n++; console.log('✓', name); };
t('ci95 symmetrisch, ±1.96·SE', () => { const c = S.ci95(486, 3.1); assert.ok(Math.abs(c.half - 6.0759) < 1e-3); assert.ok(Math.abs(c.lo - 479.924) < 1e-2); });
t('diffIndependent: SE = sqrt(SEa²+SEb²)', () => { const d = S.diffIndependent(486, 3.1, 504, 2.4); assert.strictEqual(d.diff, -18); assert.ok(Math.abs(d.se - Math.sqrt(3.1*3.1+2.4*2.4)) < 1e-9); assert.strictEqual(d.significant, true); });
t('diffIndependent: kleine Differenz nicht signifikant', () => { const d = S.diffIndependent(486, 3.1, 483, 2.9); assert.strictEqual(d.significant, false); assert.strictEqual(S.classify(d), 'equal'); });
t('diffVsReference nutzt publizierten SE, sonst approx', () => { const a = S.diffVsReference(486, 3.1, 482, 0.5, 3.0); assert.strictEqual(a.approx, false); assert.strictEqual(a.se, 3.0); const b = S.diffVsReference(486, 3.1, 482, 0.5); assert.strictEqual(b.approx, true); });
t('trend: Linking Error erhöht SE', () => { const noLE = S.trend(465, 3.1, 480, 3.2, 0); const withLE = S.trend(465, 3.1, 480, 3.2, 3.0); assert.ok(withLE.se > noLE.se); assert.strictEqual(withLE.diff, -15); assert.ok(Math.abs(withLE.se - Math.sqrt(3.1**2+3.2**2+9)) < 1e-9); });
t('trend: Signifikanz kann durch LE kippen', () => { const a = S.trend(486, 3.1, 492, 3.2, 0); const b = S.trend(486, 3.1, 492, 3.2, 3.0); assert.strictEqual(a.significant, false); assert.strictEqual(b.significant, false); const c = S.trend(475, 1.0, 482, 1.0, 0); const d = S.trend(475, 1.0, 482, 1.0, 5.0); assert.strictEqual(c.significant, true); assert.strictEqual(d.significant, false); });
t('classify: above / below / equal', () => { assert.strictEqual(S.classify(S.diffIndependent(560, 1.5, 482, 0.5)), 'above'); assert.strictEqual(S.classify(S.diffIndependent(456, 2.6, 461, 0.5)), 'equal'); assert.strictEqual(S.classify(S.diffIndependent(440, 2.0, 461, 0.5)), 'below'); });
t('interdecile: P90−P10 = 289, SE nur publiziert', () => { const g = S.interdecile(630, 341, undefined); assert.strictEqual(g.gap, 289); assert.strictEqual(g.se, null); });
t('phi: Φ(0)=0.5, Φ(1.96)≈0.975', () => { assert.ok(Math.abs(S._phi(0)-0.5) < 1e-9); assert.ok(Math.abs(S._phi(1.959964)-0.975) < 1e-4); });
t('p-Wert zweiseitig', () => { const d = S.diffIndependent(10, 5, 0, 0); assert.ok(Math.abs(d.p - 0.0455) < 1e-3); });
console.log(n + ' Tests bestanden');
