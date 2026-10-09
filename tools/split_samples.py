"""Turn each one-page sample into real pages: Home, Services (or Menu), Area or Visit, and Contact/Quote/Book.

Input:  /home/claude/ssp-work/full/<slug>.html  (the single-file build from inline.py)
        /home/claude/ssp-work/full/tokens.json  (colors and type read from each sample by probe_tokens.py)
Output: /home/claude/ssp-site/<slug>/index.html plus one .html per extra page, same folder, same img/.

Each page keeps the sample's own header, footer, call bar and scripts. Sections are moved, not copied:
a page only holds its own content. Subpages get a page head (two hero photos crossfading), a phone menu
in the call bar, and the same curtain page change the hub uses.
"""
import json, re, html, pathlib

FULL = pathlib.Path("/home/claude/ssp-work/full")
SITE = pathlib.Path("/home/claude/ssp-site")
TOK = json.loads((FULL / "tokens.json").read_text())

# slug -> name, pages [(file, nav label, page title, lede, [section keys])], hero images [(desktop, phone)]
PLAN = {
 "hvac": ("Kestrel Heating & Air", [
    ("index.html", "Home", None, None, ["hero", "trust", "altitude", "reviews"]),
    ("services.html", "Services", "Services", "Furnace and AC repair, tune-ups and new systems, with the price in writing before any work starts.", ["services", "process"]),
    ("area.html", "Service area", "Service area", "Colorado Springs and El Paso County, 7 days a week.", ["area"]),
    ("contact.html", "Book", "Book service", "Call, text, or send a request. A technician answers, not a call center.", ["contact"])],
    [(f"img/hero-{n}-1920.webp", f"img/hero-{n}-p.webp") for n in (1, 2, 3, 4)]),
 "plumbing": ("Dipper Plumbing", [
    ("index.html", "Home", None, None, ["hero", "trust", "freeze", "reviews"]),
    ("services.html", "Services", "Services", "Burst pipes, water heaters, drains and leaks, fixed the same day when we can.", ["services", "how"]),
    ("area.html", "Service area", "Service area", "Colorado Springs and the towns around it.", ["area"]),
    ("contact.html", "Book a visit", "Book a visit", "Call, text a photo of the problem, or book a time.", ["contact"])],
    [(f"img/hero-{n}.webp", f"img/hero-{n}-p.webp") for n in (1, 2, 3, 4)]),
 "contractor": ("Ledgerline Builders", [
    ("index.html", "Home", None, None, ["hero", "trust", "local", "season", "reviews"]),
    ("services.html", "Services", "Services", "Kitchens, baths, basements and decks, with written quotes and permits handled.", ["services", "process"]),
    ("area.html", "Area", "Where we build", "From Monument to Fountain, and the neighborhoods in between.", ["area"]),
    ("quote.html", "Quote", "Start your project", "Tell us about the project. You get a written quote.", ["quote"])],
    [(f"img/hero-{k}-1920.webp", f"img/hero-{k}-900.webp") for k in ("basement", "framing", "kitchen", "porch")]),
 "lawn": ("Shortgrass Lawn Co", [
    ("index.html", "Home", None, None, ["hero", "trust", "fall", "reviews"]),
    ("services.html", "Services", "Services", "Mowing, aeration, fertilizing and sprinkler blowouts.", ["services", "how"]),
    ("area.html", "Service area", "Where we mow", "The neighborhoods on our weekly routes.", ["area"]),
    ("quote.html", "Get a quote", "Price your yard", "Send your address and what you need. We quote it the same day.", ["quote"])],
    [(f"img/hero-{k}-1920.webp", f"img/hero-{k}-900x1350.webp") for k in ("backyard", "mowing", "ranch", "stripes")]),
 "salon": ("Oriel Hair Studio", [
    ("index.html", "Home", None, None, ["hero", "trust", "color-care", "reviews"]),
    ("services.html", "Services", "Services", "Cuts, color and styling, with starting prices.", ["services", "first-visit"]),
    ("visit.html", "Hours", "Hours and visit", "When we're open and where to park downtown.", ["hours"]),
    ("book.html", "Book a chair", "Booking", "Send a booking request and we'll confirm your time.", ["book"])],
    [(f"img/hero-{n}-1920.webp", f"img/hero-{n}-p.webp") for n in (1, 2, 3, 4)]),
 "restaurant": ("Sawbuck Fire Grill", [
    ("index.html", "Home", None, None, ["hero", "trust", "local", "why", "reviews"]),
    ("menu.html", "Menu", "Menu", "Wood-fired dinner, cooked over oak.", ["menu"]),
    ("visit.html", "Hours", "Hours and directions", "Find us in Old Colorado City.", ["hours"]),
    ("book.html", "Reservations", "Reservations", "Call to book, or send a table request.", ["book"])],
    [(f"img/hero-{k}-1920.webp", f"img/hero-{k}-portrait.webp") for k in ("fire", "grill", "plate", "room")]),
}

def rgb(s):
    return tuple(int(x) for x in re.findall(r"[\d.]+", s)[:3])

def rgba(s, a):
    r, g, b = rgb(s); return f"rgba({r},{g},{b},{a})"

def light(s):
    r, g, b = rgb(s); return (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255 > 0.5

def sections(doc):
    """Top-level <section> blocks: list of (start, end, opening tag)."""
    out, i, depth, start = [], 0, 0, None
    for m in re.finditer(r"<section\b[^>]*>|</section>", doc):
        if m.group(0).startswith("<section"):
            if depth == 0: start = m
            depth += 1
        else:
            depth -= 1
            if depth == 0: out.append((start.start(), m.end(), start.group(0)))
    return out

def key_of(tag):
    m = re.search(r'\bid="([^"]+)"', tag)
    cls = re.search(r'class="([^"]+)"', tag).group(1).split()[0]
    if cls in ("hero", "trust"): return cls
    return m.group(1) if m else cls

def css(t, hdr_h):
    dark_site = not light(t["bg"])
    cur_bg = "#26221e" if dark_site else t["fg"]
    cur_fg = t["fg"] if dark_site else t["bg"]
    return f"""<style id="sspx-css">
.sspx-ph{{position:relative;min-height:clamp(320px,48svh,540px);display:flex;align-items:flex-end;overflow:hidden;background:#111;color:#fff;isolation:isolate;padding:calc({hdr_h}px + 48px) clamp(20px,5vw,64px) clamp(34px,5vw,60px)}}
.sspx-ph .sx{{position:absolute;inset:0;z-index:-2}}
.sspx-ph .sx picture,.sspx-ph .sx img{{position:absolute;inset:0;width:100%;height:100%}}
.sspx-ph .sx img{{object-fit:cover}}
.sspx-ph .sx picture:nth-child(1) img{{animation:sspxA 14s infinite,sspxZ 7s ease-out infinite alternate}}
.sspx-ph .sx picture:nth-child(2) img{{opacity:0;animation:sspxB 14s infinite,sspxZ 7s ease-out infinite alternate-reverse}}
@keyframes sspxA{{0%,42%{{opacity:1}}50%,92%{{opacity:0}}100%{{opacity:1}}}}
@keyframes sspxB{{0%,42%{{opacity:0}}50%,92%{{opacity:1}}100%{{opacity:0}}}}
@keyframes sspxZ{{from{{transform:scale(1.09)}}to{{transform:scale(1)}}}}
.sspx-ph::after{{content:'';position:absolute;inset:0;z-index:-1;background:linear-gradient(180deg,rgba(0,0,0,.62),rgba(0,0,0,.22) 42%,rgba(0,0,0,.74))}}
.sspx-ph-in{{width:100%;max-width:1240px;margin:0 auto}}
.sspx-crumb{{display:flex;flex-wrap:wrap;gap:6px 10px;align-items:center;font:600 .95rem/1.2 {t['font']};margin:0 0 10px}}
.sspx-crumb a{{color:#fff;min-height:44px;display:inline-flex;align-items:center;text-decoration:underline;text-underline-offset:4px}}
.sspx-crumb span{{opacity:.8}}
.sspx-ph h1{{font-family:{t['dfont']};font-weight:{t['dweight']};letter-spacing:{t['dls']};text-transform:{t['dtt']};font-size:clamp(2.6rem,7.4vw,5.4rem);line-height:.98;margin:0;color:#fff;text-wrap:balance}}
.sspx-ph p{{font-family:{t['font']};font-size:clamp(1.04rem,1.4vw,1.22rem);line-height:1.5;max-width:34em;margin:14px 0 0;color:rgba(255,255,255,.9)}}
.sspx-ph .rule{{display:block;width:64px;height:4px;background:{t['acc']};margin-top:20px}}
.sspx-mb{{display:none;align-items:center;justify-content:center;gap:8px;min-height:48px;min-width:56px;padding:0 14px;border-radius:{t['radius']};border:1px solid currentColor;background:transparent;color:inherit;font:700 1rem/1 {t['font']};cursor:pointer;flex:0 0 auto}}
.sspx-mb svg{{width:18px;height:18px}}
.sspx-mb.on{{display:inline-flex}}
.sspx-fab{{position:fixed;right:14px;bottom:calc(16px + env(safe-area-inset-bottom));z-index:80;background:{t['bg']};color:{t['fg']};border-color:{rgba(t['fg'], .35)};border-radius:999px;box-shadow:0 12px 30px -10px rgba(0,0,0,.55);transition:bottom .3s}}
.sspx-menu{{position:fixed;inset:0;z-index:2147483600;background:{t['bg']};color:{t['fg']};display:flex;flex-direction:column;padding:calc(18px + env(safe-area-inset-top)) clamp(20px,6vw,40px) calc(24px + env(safe-area-inset-bottom));transform:translateY(100%);visibility:hidden;transition:transform .55s cubic-bezier(.2,.7,.1,1),visibility 0s linear .55s}}
.sspx-menu.open{{transform:none;visibility:visible;transition:transform .55s cubic-bezier(.2,.7,.1,1)}}
.sspx-menu .top{{display:flex;justify-content:space-between;align-items:center;gap:16px;min-height:56px;font-family:{t['dfont']};font-weight:{t['dweight']};font-size:1.15rem}}
.sspx-menu .x{{display:grid;place-items:center;width:48px;height:48px;border-radius:999px;border:1px solid {rgba(t['fg'], .3)};background:transparent;color:inherit;cursor:pointer}}
.sspx-menu .x svg{{width:20px;height:20px}}
.sspx-menu ul{{list-style:none;margin:18px 0 0;padding:0}}
.sspx-menu li{{opacity:0;transform:translateY(16px);transition:opacity .3s,transform .5s cubic-bezier(.2,.7,.1,1)}}
.sspx-menu.open li{{opacity:1;transform:none;transition-delay:calc(.14s + var(--i) * .05s)}}
.sspx-menu li a{{display:flex;align-items:center;justify-content:space-between;min-height:66px;border-bottom:1px solid {rgba(t['fg'], .16)};font-family:{t['dfont']};font-weight:{t['dweight']};letter-spacing:{t['dls']};text-transform:{t['dtt']};font-size:clamp(1.9rem,8vw,2.6rem);color:inherit;text-decoration:none}}
.sspx-menu li a[aria-current=page]{{box-shadow:inset 5px 0 0 {t['acc']};padding-left:16px}}
.sspx-menu .call{{margin-top:auto;display:flex;align-items:center;justify-content:center;gap:10px;min-height:56px;border-radius:{t['radius']};background:{t['acc']};color:{t['accFg']};font:700 1.05rem/1 {t['font']};text-decoration:none}}
.sspx-menu .call svg{{width:18px;height:18px}}
html.sspx-open,html.sspx-open body{{overflow:hidden}}
.sspx-cur{{position:fixed;inset:0;z-index:2147483646;background:{cur_bg};color:{cur_fg};display:grid;place-items:center;text-align:center;padding:24px;transform:translateY(101%);visibility:hidden;pointer-events:none;font-family:{t['dfont']};font-weight:{t['dweight']};letter-spacing:{t['dls']};text-transform:{t['dtt']};font-size:clamp(1.7rem,5vw,2.8rem);line-height:1}}
.sspx-cur span{{display:block;width:48px;height:4px;margin:16px auto 0;background:{t['acc']}}}
html.cur-in .sspx-cur,.sspx-cur.go{{visibility:visible}}
html.cur-in .sspx-cur{{transform:none}}
@media (prefers-reduced-motion:reduce){{.sspx-ph .sx img{{animation:none}}.sspx-ph .sx picture:nth-child(2) img{{opacity:0}}.sspx-menu,.sspx-menu li{{transition:none}}html.cur-in .sspx-cur{{transform:translateY(101%)}}}}
</style>"""

HEAD_JS = """<script>(function(h){try{var t=+sessionStorage.getItem('ssp-nav');sessionStorage.removeItem('ssp-nav');
if(t&&Date.now()-t<6000&&!matchMedia('(prefers-reduced-motion: reduce)').matches){h.className+=' cur-in';h.setAttribute('data-fresh','1');}}catch(e){}})(document.documentElement);</script>"""

MENU_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h10"/></svg>'
X_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>'
PHONE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>'

NAV_JS = r"""<script>
(function(){
  var html=document.documentElement, cur=document.querySelector('.sspx-cur'), reduce=matchMedia('(prefers-reduced-motion: reduce)').matches, EASE='cubic-bezier(.76,0,.24,1)';
  var navEntry=performance.getEntriesByType?performance.getEntriesByType('navigation')[0]:null;
  var fromSite=false; try{ fromSite=!!document.referrer&&new URL(document.referrer).origin===location.origin; }catch(e){}
  var fresh=html.hasAttribute('data-fresh')||(navEntry&&navEntry.type==='navigate'&&fromSite)||(top!==self&&!(navEntry&&navEntry.type==='back_forward'));
  function toTop(){ if(scrollY!==0) scrollTo(0,0); try{ if(top!==self) html.scrollIntoView({block:'start',inline:'nearest'}); }catch(e){} }
  if(fresh&&!location.hash){
    var held=true, stop=function(){ held=false; };
    addEventListener('touchstart',stop,{once:true,passive:true}); addEventListener('wheel',stop,{once:true,passive:true}); addEventListener('keydown',stop,{once:true});
    toTop(); [60,180,400,800].forEach(function(ms){ setTimeout(function(){ if(held) toTop(); },ms); });
    addEventListener('load',function(){ if(held) toTop(); setTimeout(stop,300); });
  }
  function reveal(){ if(!html.classList.contains('cur-in')) return; var done=function(){ html.classList.remove('cur-in'); };
    if(!cur.animate){ done(); return; } var a=cur.animate([{transform:'translateY(0)'},{transform:'translateY(-101%)'}],{duration:640,easing:EASE,fill:'forwards'}); a.onfinish=function(){ done(); a.cancel(); }; }
  var fontsIn=document.fonts&&document.fonts.ready?Promise.race([document.fonts.ready,new Promise(function(r){setTimeout(r,350);})]):Promise.resolve();
  fontsIn.then(function(){ requestAnimationFrame(function(){ requestAnimationFrame(reveal); }); });
  addEventListener('pageshow',function(e){ if(e.persisted){ html.classList.remove('cur-in'); cur.classList.remove('go'); if(cur.getAnimations) cur.getAnimations().forEach(function(x){x.cancel();}); setMenu(false); } });
  function internal(a){ if(!a||(a.target&&a.target!=='_self')||a.hasAttribute('download')) return null; var h=a.getAttribute('href');
    if(!h||h.charAt(0)==='#'||/^(tel|sms|mailto|javascript):/i.test(h)) return null; var u; try{ u=new URL(a.href,location.href); }catch(e){ return null; } return u.origin===location.origin?u:null; }
  document.addEventListener('click',function(e){
    if(e.defaultPrevented||e.button!==0||e.metaKey||e.ctrlKey||e.shiftKey||e.altKey) return;
    var a=e.target.closest&&e.target.closest('a'), u=internal(a); if(!u) return;
    if(u.pathname===location.pathname&&u.search===location.search){ if(u.hash) return; e.preventDefault(); setMenu(false); scrollTo({top:0,behavior:reduce?'auto':'smooth'}); return; }
    if(reduce||!cur.animate) return; e.preventDefault(); setMenu(false);
    try{ sessionStorage.setItem('ssp-nav',String(Date.now())); }catch(x){}
    var went=false, go=function(){ if(went) return; went=true; toTop(); location.href=u.href; };
    cur.classList.add('go'); var a2=cur.animate([{transform:'translateY(101%)'},{transform:'translateY(0)'}],{duration:440,easing:EASE,fill:'forwards'}); a2.onfinish=go; setTimeout(go,560);
  },true);
  var seen={}; function pf(e){ var u=internal(e.target.closest&&e.target.closest('a')); if(!u||seen[u.href]||u.pathname===location.pathname) return; seen[u.href]=1;
    var l=document.createElement('link'); l.rel='prefetch'; l.href=u.href; document.head.appendChild(l); }
  document.addEventListener('touchstart',pf,{passive:true}); document.addEventListener('pointerover',pf,{passive:true});
  var menu=document.getElementById('sspx-menu'), mb=null, fab=document.querySelector('.sspx-fab'), opener=null;
  function setMenu(open){ if(!menu) return; menu.classList.toggle('open',open); html.classList.toggle('sspx-open',open);
    [mb,fab].forEach(function(b){ if(b) b.setAttribute('aria-expanded',String(open)); });
    if(open){ menu.removeAttribute('inert'); setTimeout(function(){ var f=menu.querySelector('a'); if(f) f.focus({preventScroll:true}); },80); }
    else { menu.setAttribute('inert',''); if(opener){ opener.focus({preventScroll:true}); opener=null; } } }
  [mb,fab].forEach(function(b){ if(b) b.addEventListener('click',function(){ opener=b; setMenu(true); }); });
  var x=menu&&menu.querySelector('.x'); if(x) x.addEventListener('click',function(){ setMenu(false); });
  document.addEventListener('keydown',function(e){ if(!menu||!menu.classList.contains('open')) return; if(e.key==='Escape'){ setMenu(false); return; }
    if(e.key==='Tab'){ var f=[].slice.call(menu.querySelectorAll('a,button')), i=f.indexOf(document.activeElement);
      if(e.shiftKey&&i<=0){ e.preventDefault(); f[f.length-1].focus(); } else if(!e.shiftKey&&i===f.length-1){ e.preventDefault(); f[0].focus(); } } });
  function place(){
    var links=[].slice.call(document.querySelectorAll('header [data-sspx]'));
    var hidden=!links.length||links.every(function(a){ var r=a.getBoundingClientRect(); return !a.offsetParent||r.width===0||r.height===0; });
    var cb=document.querySelector('.callbar'), cbOn=cb&&getComputedStyle(cb).display!=='none'&&cb.getBoundingClientRect().height>0;
    if(fab){ fab.classList.toggle('on',hidden); fab.style.bottom=(cbOn?Math.round(innerHeight-cb.getBoundingClientRect().top)+12:16)+'px'; }
    if(!hidden) setMenu(false);
  }
  place(); addEventListener('resize',place); addEventListener('load',place);
})();
</script>"""

def build(slug):
    name, pages, heroes = PLAN[slug]
    t = TOK[slug]
    doc = (FULL / f"{slug}.html").read_text()
    secs = sections(doc)
    # each section carries whatever sits between it and the next one (a decorative photo band, for example)
    starts = [a for a, _, _ in secs] + [secs[-1][1]]
    by_key = {key_of(tag): doc[a:starts[i + 1]] for i, (a, b, tag) in enumerate(secs)}
    first, last = secs[0][0], secs[-1][1]
    pre, post = doc[:first], doc[last:]
    keys_all = [key_of(tag) for _, _, tag in secs]
    for _, _, _, _, ks in pages:
        for k in ks: assert k in by_key, f"{slug}: no section {k} (have {keys_all})"
    # which page holds each section id, so every #anchor can point at the right file
    where = {}
    for fname, _, _, _, ks in pages:
        for i, k in enumerate(ks):
            m = re.search(r'\bid="([^"]+)"', by_key[k][:300])
            if m: where[m.group(1)] = (fname, i == 0)
    where["top"] = ("index.html", True)
    tel = re.search(r'href="(tel:[^"]+)"', doc).group(1)
    phone_disp = re.search(r'\((\d{3})\) (\d{3})-(\d{4})', doc)
    phone_disp = phone_disp.group(0) if phone_disp else "Call"

    for pi, (fname, label, ptitle, lede, ks) in enumerate(pages):
        def fix_href(m):
            tag = m.group(0); hid = m.group(1)
            if hid.startswith("i-") or hid not in where: return tag
            f, is_first = where[hid]
            if f == fname: dest = f"#{hid}" if (not is_first or hid == "top") else f
            else: dest = f if is_first else f"{f}#{hid}"
            return tag.replace(f'href="#{hid}"', f'href="{dest}"')
        head = pre
        # the header nav lists pages, not sections
        def nav_sub(m):
            inner = m.group(2)
            links = "".join(f'<a href="{f}" data-sspx{" aria-current=\"page\"" if f == fname else ""}>{html.escape(l)}</a>' for f, l, *_ in pages)
            if '<ul class="nav-links">' in inner:
                lis = "".join(f'<li><a href="{f}" data-sspx{" aria-current=\"page\"" if f == fname else ""}>{html.escape(l)}</a></li>' for f, l, *_ in pages)
                inner = re.sub(r'<ul class="nav-links">.*?</ul>', f'<ul class="nav-links">{lis}</ul>', inner, flags=re.S)
            else:
                inner = re.sub(r'(\s*<a href="#[^"]*"[^>]*>.*?</a>)+', links, inner, count=1, flags=re.S)
            return m.group(1) + inner + "</nav>"
        head = re.sub(r'(<nav class="nav"[^>]*>)(.*?)</nav>', nav_sub, head, count=1, flags=re.S)
        body = "".join(by_key[k] for k in ks)
        if ptitle:
            d1, p1 = heroes[pi % len(heroes)]; d2, p2 = heroes[(pi + 1) % len(heroes)]
            pic = lambda d, p, lazy: (f'<picture><source media="(max-width:700px)" srcset="{p}"><img src="{d}" alt="" width="1920" height="1080"'
                                      f'{" loading=\"lazy\"" if lazy else ""} decoding="async"></picture>')
            ph = (f'<section class="sspx-ph" aria-labelledby="sspx-h1"><div class="sx" aria-hidden="true">{pic(d1, p1, False)}{pic(d2, p2, True)}</div>'
                  f'<div class="sspx-ph-in"><nav class="sspx-crumb" aria-label="Breadcrumb"><a href="index.html">{html.escape(name)}</a><span aria-hidden="true">/</span><span>{html.escape(ptitle)}</span></nav>'
                  f'<h1 id="sspx-h1">{html.escape(ptitle)}</h1><p>{html.escape(lede)}</p><span class="rule" aria-hidden="true"></span></div></section>')
            body = ph + body
            # the moved section's own h1, if any, steps down so the page has one h1
            head = re.sub(r"<title>.*?</title>", f"<title>{html.escape(ptitle)} | {html.escape(name)} (Sample)</title>", head, count=1, flags=re.S)
        out = head + body + post
        out = re.sub(r'<a\b[^>]*href="#([a-z0-9-]+)"[^>]*>', fix_href, out)
        # phone menu sheet, curtain, styles and the page-change script
        menu_items = "".join(f'<li style="--i:{i}"><a href="{f}"{" aria-current=\"page\"" if f == fname else ""}>{html.escape(l)}</a></li>' for i, (f, l, *_) in enumerate(pages))
        sheet = (f'<div class="sspx-menu" id="sspx-menu" inert role="dialog" aria-modal="true" aria-label="Menu">'
                 f'<div class="top"><span>{html.escape(name)}</span><button class="x" type="button" aria-label="Close menu">{X_ICON}</button></div>'
                 f'<ul>{menu_items}</ul><a class="call" href="{tel}">{PHONE}Call {phone_disp}</a></div>'
                 f'<button class="sspx-mb sspx-fab" type="button" aria-controls="sspx-menu" aria-expanded="false">{MENU_ICON}Menu</button>'
                 f'<div class="sspx-cur" aria-hidden="true">{html.escape(name)}<span></span></div>')
        out = out.replace("</head>", HEAD_JS + css(t, int(t["hdrH"])) + "</head>", 1)
        out = out.replace("</body>", sheet + NAV_JS + "</body>", 1)
        (SITE / slug / fname).write_text(out)
    return [p[0] for p in pages]

if __name__ == "__main__":
    import sys
    for slug in (sys.argv[1:] or PLAN):
        print(slug, build(slug))
