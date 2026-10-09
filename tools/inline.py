"""Inline the motion libraries into a page so it stays one self-contained HTML file (images sit beside it in ./img/).

Usage: python3 inline.py src.html out/index.html [libs]
  libs: comma list from gsap,scrolltrigger,splittext,drawsvg,lenis (default gsap,scrolltrigger,splittext,lenis)
The source must contain exactly one <!--@LIBS@--> placeholder, placed before the page's own <script>.
"""
import pathlib, re, sys

KIT = pathlib.Path(__file__).parent / "vendor"
FILES = {"gsap": "gsap.min.js", "scrolltrigger": "ScrollTrigger.min.js", "splittext": "SplitText.min.js",
         "drawsvg": "DrawSVGPlugin.min.js", "lenis": "lenis.min.js"}

def main():
    src, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    libs = (sys.argv[3] if len(sys.argv) > 3 else "gsap,scrolltrigger,splittext,lenis").split(",")
    s = src.read_text()
    assert s.count("<!--@LIBS@-->") == 1, "need exactly one <!--@LIBS@--> placeholder"
    parts = []
    for name in libs:
        js = (KIT / FILES[name]).read_text()
        js = re.sub(r"//# sourceMappingURL=.*$", "", js, flags=re.M)
        parts.append(f"<script>/* {FILES[name]} */\n{js}\n</script>")
    s = s.replace("<!--@LIBS@-->", "\n".join(parts))
    bad = [m for m in re.findall(r'<script[^>]+src="([^"]+)"', s)]
    assert not bad, f"external scripts not allowed: {bad}"
    css = [m for m in re.findall(r'<link[^>]+rel="stylesheet"[^>]+href="([^"]+)"', s) if "fonts.googleapis.com" not in m]
    assert not css, f"external stylesheets not allowed (Google Fonts only): {css}"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(s)
    print(out, round(len(s) / 1024), "KB")

if __name__ == "__main__":
    main()
