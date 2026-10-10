"""Capture hub card screenshots of each sample: desktop first screen and phone first screen (badge hidden)."""
import sys, pathlib
from playwright.sync_api import sync_playwright
from PIL import Image
SITE = pathlib.Path("/home/claude/ssp-site"); OUT = SITE / "assets/shots"; OUT.mkdir(parents=True, exist_ok=True)
SLUGS = sys.argv[1:] or ["hvac", "plumbing", "contractor", "lawn", "salon", "restaurant"]
HIDE = ".ssp-sample,.sspx-fab{display:none!important}"
with sync_playwright() as p:
    b = p.chromium.launch()
    for s in SLUGS:
        for kind, vp, dpr, mobile in [("desktop", (1440, 900), 1, False), ("phone", (390, 844), 2, True)]:
            ctx = b.new_context(viewport={"width": vp[0], "height": vp[1]}, device_scale_factor=dpr, is_mobile=mobile, has_touch=mobile)
            pg = ctx.new_page(); pg.goto((SITE / s / "index.html").as_uri()); pg.add_style_tag(content=HIDE)
            pg.wait_for_timeout(4200)
            tmp = OUT / f"{s}-{kind}.png"; pg.screenshot(path=str(tmp)); ctx.close()
            im = Image.open(tmp).convert("RGB")
            if kind == "desktop":
                im = im.resize((1200, 750), Image.LANCZOS)
            else:
                im = im.resize((600, int(600 * im.height / im.width)), Image.LANCZOS)
            im.save(OUT / f"{s}-{kind}.webp", "WEBP", quality=78); tmp.unlink()
            print(s, kind, im.size)
    b.close()
