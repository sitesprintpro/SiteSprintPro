"""SiteSprintPro mobile QA: four phones plus desktop, one contact sheet, PASS/FAIL per check.

Usage: python3 mobile.py path/to/index.html outdir
Engine: Chromium with phone emulation (user agent, touch, pixel ratio). WebKit is not installed in this
workspace, so the final iPhone check happens on a real phone during sign-off.
"""
import json, pathlib, sys
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw

IPHONE = "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1"
ANDROID = "Mozilla/5.0 (Linux; Android 14; SM-S911B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Mobile Safari/537.36"
DEVICES = [
    ("android-360", 360, 800, 3, ANDROID, True),
    ("iphone-se-375", 375, 667, 2, IPHONE, True),
    ("iphone-390", 390, 844, 3, IPHONE, True),
    ("iphone-max-430", 430, 932, 3, IPHONE, True),
    ("desktop-1440", 1440, 900, 1, None, False),
]

PROBE = r"""
() => {
  const vis = el => { const r = el.getBoundingClientRect(), s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none' && parseFloat(s.opacity) > 0.05; };
  const H = innerHeight, W = innerWidth;
  const overflow = document.documentElement.scrollWidth - W;
  const tel = [...document.querySelectorAll('a[href^="tel:"]')].filter(vis);
  const telFirst = tel.filter(a => { const r = a.getBoundingClientRect(); return r.top >= 0 && r.bottom <= H; }).length;
  const onscreen = el => { const r = el.getBoundingClientRect(); return r.right > 0 && r.left < W && !el.closest('[aria-hidden=true]'); };
  const target = el => (/^(radio|checkbox)$/.test(el.type) && el.closest('label')) ? el.closest('label') : el;
  const small = [...document.querySelectorAll('a[href], button, input:not([type=hidden]), select, textarea, [role=button]')].filter(vis).filter(onscreen).filter(el => {
    const r = target(el).getBoundingClientRect(); return (r.height < 44 && r.width < 44) || r.height < 24; })
    .map(el => (el.innerText || el.getAttribute('aria-label') || el.name || el.tagName).trim().slice(0, 24));
  const inputs = [...document.querySelectorAll('input:not([type=hidden]):not([type=radio]):not([type=checkbox]), select, textarea')].filter(vis).filter(onscreen)
    .filter(el => parseFloat(getComputedStyle(el).fontSize) < 16).map(el => el.name || el.type);
  const telInputs = [...document.querySelectorAll('input')].filter(el => /phone|tel/i.test(el.name + el.id + (el.placeholder||'')) && el.type !== 'tel').map(el => el.name);
  const fixedBottom = [...document.querySelectorAll('body *')].filter(el => { const s = getComputedStyle(el);
    if (s.position !== 'fixed' || !vis(el)) return false; const r = el.getBoundingClientRect(); return r.bottom >= H - 48 && r.height < H / 3 && r.width > W / 2; });
  const barH = fixedBottom.length ? Math.max(...fixedBottom.map(el => el.getBoundingClientRect().height)) : 0;
  const soft = [...document.images].filter(vis).filter(img => {
    const r = img.getBoundingClientRect(); if (r.width < 200 || !img.naturalWidth) return false;
    // naturalWidth is density-corrected for srcset picks, so read the real pixel width from the chosen candidate
    let px = img.naturalWidth; const cur = (img.currentSrc || img.src).split('/').pop();
    const srcs = [img.srcset, ...[...(img.parentElement && img.parentElement.tagName === 'PICTURE' ? img.parentElement.querySelectorAll('source') : [])].map(s => s.srcset)].filter(Boolean).join(',');
    for (const c of srcs.split(',')) { const [u, d] = c.trim().split(/\s+/); if (u && u.split('/').pop() === cur && /w$/.test(d || '')) px = parseInt(d); }
    const box = getComputedStyle(img).objectFit === 'cover' ? Math.max(r.width, r.height * (img.naturalWidth / Math.max(img.naturalHeight, 1))) : r.width;
    return px < box * Math.min(devicePixelRatio, 2) * 0.7; }).map(img => (img.currentSrc || img.src).split('/').pop());
  const unsized = [...document.images].filter(i => !i.getAttribute('width') && !getComputedStyle(i).aspectRatio.includes('/')).length;
  let vh100 = 0; for (const sh of document.styleSheets) { try { for (const r of sh.cssRules) { if (/100vh/.test(r.cssText) && !/dvh|svh/.test(r.cssText)) vh100++; } } catch (e) {} }
  const dashes = (document.body.innerText.match(/[–—]/g) || []).length;
  return {overflow, tel: tel.length, telFirst, small: [...new Set(small)].slice(0, 6), inputs, telInputs, barH, soft: [...new Set(soft)].slice(0, 6), unsized, vh100, dashes};
}
"""

def scroll_through(pg):
    h = pg.evaluate("document.documentElement.scrollHeight")
    y = 0
    while y < h:
        pg.evaluate(f"window.scrollTo(0, {y})")
        pg.wait_for_timeout(120)
        y += 500
        h = pg.evaluate("document.documentElement.scrollHeight")
    pg.wait_for_timeout(900)
    pg.evaluate("window.scrollTo(0, 0)")
    pg.wait_for_timeout(700)

def main():
    page = pathlib.Path(sys.argv[1]).resolve()
    out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
    results, shots, fails = {}, [], 0
    with sync_playwright() as p:
        b = p.chromium.launch()
        for name, w, h, dpr, ua, mobile in DEVICES:
            ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=dpr, is_mobile=mobile,
                                has_touch=mobile, user_agent=ua) if ua else b.new_context(viewport={"width": w, "height": h})
            pg = ctx.new_page()
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)[:160]))
            pg.on("console", lambda m: errs.append(m.text[:160]) if m.type == "error" else None)
            pg.on("requestfailed", lambda r: None if "ERR_ABORTED" in (r.failure or "") else errs.append("failed: " + r.url[-60:] + " " + (r.failure or "")))
            pg.goto(page.as_uri(), wait_until="load")
            pg.wait_for_timeout(3200)
            first = out / f"{name}.png"
            pg.screenshot(path=str(first))
            scroll_through(pg)
            r = pg.evaluate(PROBE)
            pg.screenshot(path=str(out / f"{name}-full.png"), full_page=True)
            checks = [
                ("no sideways scroll", r["overflow"] <= 1, r["overflow"]),
                ("Call visible in first screen", r["telFirst"] > 0, f'{r["tel"]} tel links'),
                ("tap targets 44px+", (not mobile) or not r["small"], r["small"]),
                ("inputs 16px+ (no iOS zoom)", not r["inputs"], r["inputs"]),
                ("phone inputs typed tel", not r["telInputs"], r["telInputs"]),
                ("images sharp at this density", not r["soft"], r["soft"]),
                ("images reserve space", r["unsized"] == 0, r["unsized"]),
                ("no bare 100vh", r["vh100"] == 0, r["vh100"]),
                ("zero em/en dashes", r["dashes"] == 0, r["dashes"]),
                ("no JS errors or failed loads", not errs, errs[:3]),
            ]
            if mobile:
                checks.append(("sticky call bar present", r["barH"] >= 44, r["barH"]))
            results[name] = [{"check": c, "pass": ok, "detail": d} for c, ok, d in checks]
            fails += sum(1 for _, ok, _ in checks if not ok)
            shots.append((name, first))
            ctx.close()
        b.close()
    # contact sheet: the four phones' first screens side by side, scaled to the same height
    phones = [(n, Image.open(s)) for n, s in shots if not n.startswith("desktop")]
    H = 900
    scaled = [(n, im.resize((int(im.width * H / im.height), H))) for n, im in phones]
    sheet = Image.new("RGB", (sum(im.width for _, im in scaled) + 40 * (len(scaled) + 1), H + 90), (24, 24, 27))
    d = ImageDraw.Draw(sheet); x = 40
    for n, im in scaled:
        sheet.paste(im, (x, 60)); d.text((x, 24), n, fill=(230, 230, 230)); x += im.width + 40
    sheet.save(out / "contact-sheet.png")
    (out / "mobile.json").write_text(json.dumps(results, indent=1))
    for n, rows in results.items():
        print(f"== {n}")
        for row in rows:
            if not row["pass"]:
                print(f"  FAIL  {row['check']}  {row['detail']}")
    print(f"contact sheet: {out / 'contact-sheet.png'}")
    print("ALL PASS" if fails == 0 else f"{fails} FAIL(S)")

if __name__ == "__main__":
    main()
