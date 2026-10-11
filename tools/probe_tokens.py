"""Read each sample's real colors and display type so the injected page heads, menu and curtain match it."""
import json
from playwright.sync_api import sync_playwright
JS = r"""() => {
  const cs = el => el ? getComputedStyle(el) : null;
  const opaque = c => c && !/rgba\(0, 0, 0, 0\)|transparent/.test(c);
  const h2 = document.querySelector('main section:not(.hero) h2') || document.querySelector('h2');
  const tel = [...document.querySelectorAll('.callbar a[href^="tel:"], a.btn[href^="tel:"], a[href^="tel:"]')].find(a => opaque(cs(a).backgroundColor));
  const hdr = document.querySelector('header');
  const brand = document.querySelector('header a[href="#top"]') || document.querySelector('header a');
  let bg = cs(document.body).backgroundColor; if (!opaque(bg)) bg = cs(document.documentElement).backgroundColor;
  return { bg, fg: cs(document.body).color, font: cs(document.body).fontFamily,
    dfont: cs(h2).fontFamily, dweight: cs(h2).fontWeight, dls: cs(h2).letterSpacing, dtt: cs(h2).textTransform, dstyle: cs(h2).fontStyle,
    acc: tel ? cs(tel).backgroundColor : cs(document.body).color, accFg: tel ? cs(tel).color : cs(document.body).backgroundColor,
    hdrBg: cs(hdr).backgroundColor, hdrH: hdr.getBoundingClientRect().height, radius: tel ? cs(tel).borderTopLeftRadius : '8px',
    brand: (brand && brand.textContent || '').replace(/\s+/g, ' ').trim() };
}"""
out = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    for slug in ["hvac", "plumbing", "contractor", "lawn", "salon", "restaurant", "barber"]:
        pg = b.new_page(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
        pg.goto(f"file:///home/claude/ssp-work/full/{slug}.html"); pg.wait_for_timeout(1500)
        out[slug] = pg.evaluate(JS); pg.close()
        print(slug, out[slug])
    b.close()
json.dump(out, open("/home/claude/ssp-work/full/tokens.json", "w"), indent=1)
