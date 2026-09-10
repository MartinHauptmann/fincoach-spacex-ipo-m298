/* FinCoach AI · PisaStats v1.0.0 — Statistik-Engine für den PISA Explorer (M301)
   Reine Funktionen, keine Abhängigkeiten. Läuft im Browser (window.PisaStats) und in Node (module.exports).
   Konventionen: SE = Standardfehler; 95-%-KI = ±1.96·SE; Linking Error (LE) nur bei Zyklusvergleichen. */
(function(root){
  const Z95 = 1.959964;
  const S = {
    /** 95-%-Konfidenzintervall um einen Mittelwert. */
    ci95(mean, se){ return {lo: mean - Z95*se, hi: mean + Z95*se, half: Z95*se}; },
    /** Differenz zweier unabhängiger Stichproben (Land A vs. Land B). */
    diffIndependent(a, seA, b, seB){
      const d = a - b, se = Math.sqrt(seA*seA + seB*seB);
      return S._finish(d, se);
    },
    /** Differenz Land vs. OECD-Mittel. Das Land ist Teil des Mittels; die OECD nutzt daher den publizierten SE der Differenz.
        Fehlt dieser, approximieren wir mit dem unabhängigen Fall und kennzeichnen das (approx=true). */
    diffVsReference(a, seA, ref, seRef, sePublished){
      if (typeof sePublished === 'number') return Object.assign(S._finish(a - ref, sePublished), {approx:false});
      return Object.assign(S._finish(a - ref, Math.sqrt(seA*seA + seRef*seRef)), {approx:true});
    },
    /** Veränderung zwischen zwei Zyklen desselben Landes: SE enthält den Linking Error. */
    trend(later, seLater, earlier, seEarlier, linkError){
      const le = linkError || 0;
      const d = later - earlier, se = Math.sqrt(seLater*seLater + seEarlier*seEarlier + le*le);
      return Object.assign(S._finish(d, se), {linkError: le});
    },
    /** Dreiteilung wie in OECD-Tabellen: 'above' | 'equal' | 'below' (95-%-Niveau). */
    classify(diffObj){ return diffObj.significant ? (diffObj.diff > 0 ? 'above' : 'below') : 'equal'; },
    /** Interdezilbereich P90−P10 (Spannweite der Verteilung). SE nur mit publiziertem Wert; sonst null. */
    interdecile(p90, p10, sePublished){ return {gap: p90 - p10, se: (typeof sePublished==='number') ? sePublished : null}; },
    _finish(d, se){
      const z = se > 0 ? d/se : NaN;
      const p = se > 0 ? 2*(1 - S._phi(Math.abs(z))) : NaN;
      return {diff: d, se, z, p, ci: S.ci95(d, se), significant: se > 0 && Math.abs(z) >= Z95};
    },
    /** Standard-Normalverteilung Φ(x) (Abramowitz-Stegun 26.2.17, |ε| < 7.5e-8). */
    _phi(x){
      const t = 1/(1+0.2316419*Math.abs(x));
      const poly = t*(0.319381530 + t*(-0.356563782 + t*(1.781477937 + t*(-1.821255978 + t*1.330274429))));
      const pdf = Math.exp(-0.5*x*x)/Math.sqrt(2*Math.PI);
      const cdf = 1 - pdf*poly;
      return x >= 0 ? cdf : 1 - cdf;
    },
    Z95
  };
  if (typeof module !== 'undefined' && module.exports) module.exports = S; else root.PisaStats = S;
})(typeof window !== 'undefined' ? window : globalThis);
