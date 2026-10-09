#!/usr/bin/env python3
"""ssp preflight: mechanical design checks on a local SiteSprintPro page.
Usage: python3 preflight.py path/to/index.html [outdir]
Prints PASS/FAIL per check and saves screenshots at 390x844 and 1440x900.
"""
import json, pathlib, sys
from playwright.sync_api import sync_playwright

JS = r"""
() => {
  const vis = el => { const r = el.getBoundingClientRect(), s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none'; };
  const text = document.body.innerText;
  const dashes = (text.match(/[—–]/g) || []).length;
  const sections = [...document.querySelectorAll('section, header, footer')].filter(vis).length;
  const eyebrows = [...document.querySelectorAll('body *')].filter(el => {
    if (!vis(el) || el.children.length > 0) return false;
    const s = getComputedStyle(el), fs = parseFloat(s.fontSize), ls = parseFloat(s.letterSpacing) || 0;
    const next = el.nextElementSibling;
    return s.textTransform === 'uppercase' && fs <= 14 && ls / fs >= 0.05 && el.innerText.trim().length > 0
      && next && /^H[1-3]$/.test(next.tagName);
  }).length;
  const tel = [...document.querySelectorAll('a[href^="tel:"]')].filter(vis);
  const telAbove = tel.some(a => a.getBoundingClientRect().top < innerHeight && a.getBoundingClientRect().bottom > 0);
  const small = [...document.querySelectorAll('a, button')].filter(vis).filter(el => {
    const r = el.getBoundingClientRect(); return r.height < 44 && r.width < 44; }).map(el => el.innerText.trim().slice(0, 30));
  const radii = new Set([...document.querySelectorAll('a, button, img, section *')].filter(vis)
    .map(el => getComputedStyle(el).borderTopLeftRadius).filter(r => r !== '0px'));
  const overflow = document.documentElement.scrollWidth > innerWidth + 1;
  const maps = [...document.querySelectorAll('a[href*="maps"]')].length;
  const internal = [...document.querySelectorAll('a[href^="#"]')].map(a => a.getAttribute('href'))
    .filter(h => h.length > 1 && !document.getElementById(decodeURIComponent(h.slice(1))));
  const imgsNoSize = [...document.images].filter(i => !i.getAttribute('width') && !i.style.aspectRatio && !getComputedStyle(i).aspectRatio.includes('/')).length;
  const filler = (text.match(/\b(elevate|seamless(ly)?|unleash|next-gen|revolutioni[sz]e|world-class|top-notch|premier|cutting-edge|game-?changer)\b/gi) || []);
  const fonts = [document.body, document.querySelector('h1')].filter(Boolean).map(el => getComputedStyle(el).fontFamily.split(',')[0].replace(/["']/g, '').trim());
  return {filler, fonts, dashes, sections, eyebrows, telCount: tel.length, telAbove, small, radii: [...radii], overflow, maps, internal, imgsNoSize};
}
"""

def main():
    page_path = pathlib.Path(sys.argv[1]).resolve()
    out = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else page_path.parent / "preflight")
    out.mkdir(parents=True, exist_ok=True)
    fails = 0
    with sync_playwright() as p:
        b = p.chromium.launch()
        for w, h in [(390, 844), (1440, 900)]:
            pg = b.new_page(viewport={"width": w, "height": h})
            errors = []
            pg.on("pageerror", lambda e: errors.append(str(e)))
            pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
            pg.goto(page_path.as_uri(), wait_until="networkidle")
            r = pg.evaluate(JS)
            pg.screenshot(path=str(out / f"shot_{w}.png"))
            pg.screenshot(path=str(out / f"full_{w}.png"), full_page=True)
            checks = [
                ("zero em/en dashes", r["dashes"] == 0, r["dashes"]),
                ("eyebrows <= ceil(sections/3)", r["eyebrows"] <= -(-r["sections"] // 3), f'{r["eyebrows"]} for {r["sections"]} sections'),
                ("tap-to-call visible in first screen", r["telAbove"], f'{r["telCount"]} tel links'),
                ("directions link present", r["maps"] > 0, r["maps"]),
                ("no horizontal overflow", not r["overflow"], ""),
                ("tap targets >= 44px", not r["small"], r["small"][:5]),
                ("radius values <= 3 (one system)", len(r["radii"]) <= 3, r["radii"]),
                ("internal anchors resolve", not r["internal"], r["internal"]),
                ("images reserve space (CLS)", r["imgsNoSize"] == 0, r["imgsNoSize"]),
                ("no filler verbs (ignore if it is the business name)", not r["filler"], r["filler"][:5]),
                ("Inter is not the default face", all(f.lower() != "inter" for f in r["fonts"]), r["fonts"]),
                ("no JS/console errors", not errors, errors[:3]),
            ]
            print(f"== {w}px")
            for name, ok, detail in checks:
                fails += 0 if ok else 1
                print(f"  {'PASS' if ok else 'FAIL'}  {name}  {detail if not ok else ''}")
        b.close()
    print(f"screenshots: {out}\n{'ALL PASS' if fails == 0 else f'{fails} FAIL(S): fix, rerun once, then look at the screenshots'}")

if __name__ == "__main__":
    main()