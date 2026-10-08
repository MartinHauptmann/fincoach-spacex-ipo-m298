/* Tailwind v3 – selbst gehostet statt cdn.tailwindcss.com (Lehre L20).
 * Neu bauen nach jeder Klassenänderung:  sh vendor/build-tailwind.sh
 * Neue Modulseiten in `content` aufnehmen. */
module.exports = {
  content: ['./m300.html'],
  theme: { extend: {
    colors: { tngb: { bg:'#0A0F1A', card:'#121A2E', cyan:'#00CFFF', emerald:'#00CC7A', magenta:'#E6399A', orange:'#FF6B00',
      lavender:'#9933FF', gold:'#DFAF0F', indigo:'#4472C4', coral:'#E040A0', muted:'#64748B', border:'#1E293B' } },
    fontFamily: { sans:['Inter','system-ui','sans-serif'], head:['Space Grotesk','sans-serif'], mono:['JetBrains Mono','monospace'] }
  } }
};
