"""Build the SiteSprintPro hub pages into /home/claude/ssp-site.

Every page is one self-contained HTML file (CSS and JS inline). Links are relative so the site works on
GitHub Pages (project path), on sitesprintpro.live, and in a local preview.
Edit CONFIG and the copy below, then run: python3 build_hub.py
"""
import json, pathlib, html

SITE = pathlib.Path("/home/claude/ssp-site")

CONFIG = {
    "phone": "+17194287932",
    "phoneDisplay": "(719) 428-7932",
    "email": "sitesprintproteam@gmail.com",
    "owner": "Don",
    "ownerPhoto": "",  # e.g. "assets/don.jpg" once Don sends the Mt. Parish photo
    "domain": "https://sitesprintpro.live/",
    # Google Form wiring for /start. Fill after the form exists (see the spec, Inquiry form).
    "form": {"action": "", "fields": {}},
}

SAMPLES = [
    {"slug": "hvac", "niche": "HVAC", "group": "trades", "name": "Kestrel Heating & Air",
     "line": "Furnace and AC repair. Winter photo hero, the 6,035 ft altitude section, tune-up booking."},
    {"slug": "plumbing", "niche": "Plumbing", "group": "trades", "name": "Dipper Plumbing",
     "line": "Burst pipes and water heaters. Text-a-photo button and a before-the-freeze checklist."},
    {"slug": "contractor", "niche": "Contractor", "group": "trades", "name": "Ledgerline Builders",
     "line": "Remodels and decks. Permits through Pikes Peak Regional, a season planner, written quotes."},
    {"slug": "lawn", "niche": "Lawn care", "group": "trades", "name": "Shortgrass Lawn Co",
     "line": "Mowing, aeration, sprinkler blowouts. A fall checklist and a service-area map."},
    {"slug": "salon", "niche": "Salon", "group": "beauty", "name": "Oriel Hair Studio",
     "line": "Cuts and color downtown. Editorial look, sample pricing, hours and a booking request."},
    {"slug": "restaurant", "niche": "Restaurant", "group": "food", "name": "Sawbuck Fire Grill",
     "line": "Wood-fired dinner in Old Colorado City. Full sample menu, hours, table requests."},
]

FONT = "https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:ital,wght@0,400..900;1,400..900&display=swap"

CSS = r"""
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#121417;--bg2:#171a1e;--bg3:#1e2227;--line:rgba(237,234,228,.12);--line2:rgba(237,234,228,.22);
  --text:#edeae4;--muted:rgba(237,234,228,.68);--faint:rgba(237,234,228,.5);
  --accent:#e2622a;--accent2:#f07a45;--accent-ink:#1c0d05;
  --r1:8px;--r2:16px;--r3:999px;
  --pad:clamp(20px,5vw,64px);--max:1240px;
  --font:'Schibsted Grotesk',ui-sans-serif,system-ui,-apple-system,'Segoe UI',Roboto,Arial,sans-serif;
  --ease:cubic-bezier(.2,.7,.1,1);
}
html{-webkit-text-size-adjust:100%;scrollbar-color:#3a3f45 var(--bg);caret-color:var(--accent2)}
html.lenis,html.lenis body{height:auto}.lenis.lenis-smooth{scroll-behavior:auto!important}.lenis.lenis-stopped{overflow:hidden}
body{font-family:var(--font);background:var(--bg);color:var(--text);font-size:17px;line-height:1.55;-webkit-font-smoothing:antialiased;overflow-x:clip}
html.menu-open,html.menu-open body{overflow:hidden}
a{color:inherit}
img{display:block;max-width:100%;height:auto}
:focus-visible{outline:2px solid var(--accent2);outline-offset:3px;border-radius:4px}
::selection{background:var(--accent);color:var(--accent-ink)}
.wrap{width:100%;max-width:var(--max);margin:0 auto;padding:0 var(--pad)}
.skip{position:absolute;left:-9999px}.skip:focus{left:12px;top:12px;z-index:200;background:var(--text);color:var(--bg);padding:10px 14px;border-radius:var(--r1)}

/* header */
.hdr{position:sticky;top:0;z-index:50;background:rgba(18,20,23,.86);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}
.hdr .wrap{display:flex;align-items:center;justify-content:space-between;gap:20px;height:64px}
.brand{display:flex;align-items:center;gap:10px;text-decoration:none;font-weight:800;font-size:1.12rem;letter-spacing:-.02em;min-height:44px}
.brand svg{width:30px;height:30px;flex:none}
.brand b{color:var(--accent2);font-weight:800}
.nav{display:flex;align-items:center;gap:6px;list-style:none}
.nav a{display:inline-flex;align-items:center;min-height:44px;padding:0 12px;text-decoration:none;color:var(--muted);font-weight:600;font-size:.95rem;border-radius:var(--r1)}
.nav a:hover,.nav a[aria-current=page]{color:var(--text)}
.nav a[aria-current=page]{text-decoration:underline;text-decoration-color:var(--accent);text-underline-offset:6px;text-decoration-thickness:2px}
.call-pill{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:0 16px;border-radius:var(--r3);background:var(--text);color:var(--bg);text-decoration:none;font-weight:700;font-size:.95rem;white-space:nowrap}
.call-pill svg{width:16px;height:16px}
.hdr-r{display:flex;align-items:center;gap:8px}
.menu-btn{display:none;place-items:center;width:48px;height:48px;border-radius:var(--r3);border:1px solid var(--line2);background:transparent;color:var(--text);cursor:pointer}
.menu-btn .bars{display:grid;gap:5px;width:18px}
.menu-btn .bars span{display:block;height:2px;border-radius:2px;background:currentColor;transition:transform .45s var(--ease)}
.menu-btn[aria-expanded=true] .bars span:first-child{transform:translateY(3.5px) rotate(45deg)}
.menu-btn[aria-expanded=true] .bars span:last-child{transform:translateY(-3.5px) rotate(-45deg)}
@media (max-width:900px){.nav{display:none}.menu-btn{display:grid}}
@media (max-width:420px){.call-pill .num{display:none}.call-pill{width:48px;padding:0;justify-content:center}}

/* phone menu: full screen, opens downward from the header */
.menu{position:fixed;inset:0;z-index:45;background:var(--bg);display:flex;flex-direction:column;padding:calc(88px + env(safe-area-inset-top)) var(--pad) calc(28px + env(safe-area-inset-bottom));clip-path:inset(0 0 100% 0);visibility:hidden;transition:clip-path .6s var(--ease),visibility 0s linear .6s}
.menu.open{clip-path:inset(0);visibility:visible;transition:clip-path .6s var(--ease),visibility 0s}
.menu ul{list-style:none;display:grid}
.menu li{opacity:0;transform:translateY(22px);transition:opacity .35s,transform .6s var(--ease)}
.menu.open li{opacity:1;transform:none;transition-delay:calc(.12s + var(--i) * .05s)}
.menu li a{display:flex;align-items:center;justify-content:space-between;min-height:64px;font-size:clamp(2rem,9vw,2.9rem);font-weight:850;letter-spacing:-.035em;text-decoration:none;border-bottom:1px solid var(--line)}
.menu li a svg{width:26px;height:26px;color:var(--faint)}
.menu li a[aria-current=page]{color:var(--accent2)}
.menu-foot{margin-top:auto;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;padding-top:24px}
.menu-foot .btn{width:100%}
@media (min-width:901px){.menu{display:none}}
html.menu-open .callbar{display:none}

/* page change curtain */
.curtain{position:fixed;inset:0;z-index:1000;background:#0b0c0e;display:grid;place-items:center;transform:translateY(101%);pointer-events:none;visibility:hidden}
html.cur-in .curtain,.curtain.go{visibility:visible}
.curtain svg{width:58px;height:58px}
html.cur-in .curtain{transform:none}

/* buttons */
.btns{display:flex;flex-wrap:wrap;gap:12px}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:10px;min-height:52px;padding:0 24px;border-radius:var(--r1);text-decoration:none;font-weight:700;font-size:1rem;border:1px solid transparent;white-space:nowrap;cursor:pointer;font-family:inherit;transition:transform .2s,background .2s,border-color .2s}
.btn svg{width:18px;height:18px;flex:none}
.btn-hot{background:var(--accent);color:var(--accent-ink)}
.btn-hot:hover{background:var(--accent2);transform:translateY(-1px)}
.btn-line{border-color:var(--line2);color:var(--text);background:transparent}
.btn-line:hover{border-color:var(--text)}
.small-note{color:var(--faint);font-size:.9rem;margin-top:14px}

/* type */
h1,h2,h3{letter-spacing:-.025em;line-height:1.04;font-weight:800}
h1{font-size:clamp(2.6rem,5.6vw,5rem);letter-spacing:-.04em;line-height:.98}
h2{font-size:clamp(1.8rem,3.2vw,2.7rem)}
h3{font-size:1.25rem;line-height:1.2}
.lede{color:var(--muted);font-size:clamp(1.05rem,1.5vw,1.22rem);max-width:34em}
em{font-style:italic}
.eyebrow{display:inline-block;font-size:.8rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--accent2);margin-bottom:18px}

section{padding:clamp(72px,10vw,128px) 0}
.sec-head{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,.8fr);gap:24px 48px;align-items:end;margin-bottom:clamp(36px,5vw,60px)}
@media (max-width:800px){.sec-head{grid-template-columns:minmax(0,1fr)}}

/* hero */
.hero{padding:clamp(48px,7vw,96px) 0 clamp(64px,8vw,104px);position:relative;overflow:hidden}
.topo{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;opacity:0;transition:opacity 1.6s ease}
.topo.on{opacity:1}
.hero .wrap{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,.8fr);gap:clamp(32px,5vw,72px);align-items:center;position:relative}
.stage{transition:transform .6s var(--ease);transform-style:preserve-3d}
.hero h1{font-size:clamp(2.6rem,3.9vw,3.9rem)}
.hero .lede{margin:24px 0 32px}
.stage{position:relative;aspect-ratio:1/1.02;max-width:560px;justify-self:end;width:100%}
.stage .desk{position:absolute;right:0;top:4%;width:88%;border-radius:var(--r2);overflow:hidden;border:1px solid var(--line2);background:var(--bg3);box-shadow:0 30px 80px -30px rgba(0,0,0,.8);aspect-ratio:16/10}
.stage .phone{position:absolute;left:0;bottom:0;width:41%;aspect-ratio:390/844;border-radius:28px;border:7px solid #0a0b0d;background:#0a0b0d;overflow:hidden;box-shadow:0 30px 70px -20px rgba(0,0,0,.85),0 0 0 1px var(--line2)}
.stage img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:top;opacity:0;transition:opacity .9s ease}
.stage img.on{opacity:1}
.stage-cap{position:absolute;right:0;bottom:2%;width:52%;font-size:.92rem;color:var(--muted)}
.stage-cap b{display:block;color:var(--text);font-size:1rem}
.stage-cap a{display:inline-flex;align-items:center;min-height:44px;color:var(--accent2);font-weight:700;text-decoration:none}
@media (max-width:900px){
  .hero .wrap{grid-template-columns:minmax(0,1fr)}
  .stage{justify-self:stretch;max-width:520px;margin:8px auto 0}
}

/* work grid */
.work{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:20px}
.card{grid-column:span 6;position:relative;display:flex;flex-direction:column;border:1px solid var(--line);border-radius:var(--r2);background:var(--bg2);text-decoration:none;overflow:hidden;transition:border-color .3s,transform .3s}
.card:hover{border-color:var(--line2);transform:translateY(-3px)}
.card.w7{grid-column:span 7}.card.w5{grid-column:span 5}
.shot{position:relative;aspect-ratio:16/10;overflow:hidden;background:var(--bg3)}
.shot .d{width:100%;height:100%;object-fit:cover;object-position:top;transition:transform .8s cubic-bezier(.2,.7,.1,1)}
.card:hover .shot .d{transform:scale(1.03)}
.shot .p{position:absolute;right:4%;bottom:-18%;width:24%;aspect-ratio:390/844;object-fit:cover;object-position:top;border-radius:14px;border:4px solid #0a0b0d;box-shadow:0 18px 40px -10px rgba(0,0,0,.8)}
.card-body{display:flex;flex-wrap:wrap;align-items:baseline;justify-content:space-between;gap:6px 16px;padding:18px 20px 20px}
.card-body .niche{display:inline-flex;align-items:center;min-height:28px;padding:0 12px;border:1px solid rgba(240,122,69,.45);border-radius:var(--r3);font-size:.86rem;font-weight:700;color:var(--accent2)}
.card-body h3{flex-basis:100%;font-size:1.3rem}
.card-body p{flex-basis:100%;color:var(--muted);font-size:.97rem}
.card-body .go{display:inline-flex;align-items:center;gap:6px;min-height:44px;font-weight:700}
.card-actions{display:flex;flex-wrap:wrap;gap:10px;padding:0 20px 20px}
.card-actions .btn{min-height:46px;padding:0 18px;font-size:.95rem}
@media (max-width:860px){.card,.card.w7,.card.w5{grid-column:1/-1}}
.filters{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:24px}
.filters button{min-height:44px;padding:0 18px;border-radius:var(--r3);border:1px solid var(--line2);background:transparent;color:var(--muted);font:600 .95rem var(--font);cursor:pointer}
.filters button[aria-pressed=true]{background:var(--text);color:var(--bg);border-color:var(--text)}
.sample-note{color:var(--faint);font-size:.92rem;margin-top:18px}
.card.more{position:relative;justify-content:flex-end;min-height:0;overflow:hidden;background:var(--bg3)}
/* every card fills its row: the narrow card's picture grows to match its neighbor, so no empty space */
.work .card.w5 .shot{flex:1 1 auto;min-height:0}
.work .card.w5 .shot .d{position:absolute;inset:0;height:100%;object-position:left top}
.more-mosaic{position:absolute;inset:0 0 auto 0;height:58%;pointer-events:none}
.more-mosaic img{position:absolute;width:44%;height:auto;border-radius:12px;border:1px solid var(--line2);box-shadow:0 26px 50px -18px rgba(0,0,0,.9);transition:transform .7s cubic-bezier(.2,.7,.1,1)}
.more-mosaic img:nth-child(1){left:6%;top:14%;transform:rotate(-3deg)}
.more-mosaic img:nth-child(2){left:28%;top:5%;transform:rotate(1.5deg);z-index:2}
.more-mosaic img:nth-child(3){left:50%;top:16%;transform:rotate(4deg);z-index:3}
@media (hover:hover) and (prefers-reduced-motion:no-preference){
  .card.more:hover .more-mosaic img:nth-child(1){transform:rotate(-5deg) translate(-8px,-6px)}
  .card.more:hover .more-mosaic img:nth-child(2){transform:rotate(1.5deg) translateY(-12px)}
  .card.more:hover .more-mosaic img:nth-child(3){transform:rotate(6deg) translate(8px,-6px)}
}
@media (max-width:860px){.card.more{min-height:340px}}
.card.more .more-in{position:relative;z-index:4;display:grid;gap:10px;padding:clamp(56px,5vw,64px) clamp(22px,3vw,32px) clamp(22px,3vw,32px);background:linear-gradient(to bottom,transparent,var(--bg3) 46%)}
.card.more b{font-size:clamp(1.7rem,3vw,2.5rem);letter-spacing:-.03em;line-height:1.05}
.card.more span{color:var(--muted)}
.card.more .go{display:inline-flex;align-items:center;gap:6px;min-height:44px;color:var(--accent2);font-weight:700}

/* steps: cards that stack on each other as you scroll */
.steps{list-style:none;display:grid;gap:18px}
.steps li{position:sticky;top:calc(92px + var(--i) * 18px);display:grid;grid-template-columns:minmax(0,.42fr) minmax(0,1fr);gap:10px 40px;align-items:start;padding:clamp(26px,4vw,44px);border:1px solid var(--line);border-radius:var(--r2);background:var(--bg2);box-shadow:0 -18px 40px -24px rgba(0,0,0,.9)}
.steps .when{font-size:clamp(1.6rem,3.2vw,2.6rem);font-weight:850;letter-spacing:-.03em;line-height:1;color:var(--accent2)}
.steps h3{font-size:clamp(1.3rem,2.2vw,1.7rem);margin-bottom:10px}
.steps p{color:var(--muted);max-width:36em}
@media (max-width:760px){.steps li{grid-template-columns:minmax(0,1fr);top:calc(78px + var(--i) * 12px)}}


/* phone hero: first light comes up behind Pikes Peak, a phone rises playing a real sample */
.hx-bg,.hx-phone{display:none}
@keyframes glowup{from{opacity:0}to{opacity:1}}
@keyframes rise{from{transform:translateY(80%)}to{transform:translateY(46%)}}
@keyframes reelup{from{transform:translateY(0)}to{transform:translateY(-76%)}}
@media (max-width:760px){
  .hero{min-height:calc(100svh - 64px);padding:30px 0 0;display:flex;flex-direction:column}
  .hero .stage{display:none}
  .hero .wrap{position:relative;z-index:1}
  .hero h1{font-size:clamp(2.6rem,11.5vw,4.2rem);line-height:.95;letter-spacing:-.045em}
  .hero .lede{margin:16px 0 22px}
  .hero .btns .btn{flex:1 1 auto}
  .hero .small-note{color:var(--muted);text-shadow:0 1px 14px rgba(0,0,0,.75)}
  .hx-bg{display:block;position:absolute;inset:0;z-index:0}
  .hx-bg picture{position:absolute;inset:0}
  .hx-bg img{position:absolute;left:0;top:0;width:100%;height:124%;object-fit:cover;object-position:45% 0%}
  .hx-bg .g img{opacity:0;animation:glowup 2.8s .35s ease-out forwards}
  .hx-phone{display:block;position:absolute;left:50%;bottom:0;width:52%;margin-left:-26%;aspect-ratio:390/844;border-radius:40px;border:9px solid #07080a;background:#07080a;overflow:hidden;z-index:1;box-shadow:0 40px 90px -30px rgba(0,0,0,.95),0 0 0 1px var(--line2);transform:translateY(46%);animation:rise 1.4s .55s cubic-bezier(.2,.7,.1,1) both}
  .hx-phone img{position:absolute;left:0;top:0;width:100%;height:auto;max-width:none;animation:reelup 24s 2s linear infinite alternate}
  html.cur-in .hx-bg .g img,html.cur-in .hx-phone,html.cur-in .hx-phone img{animation-play-state:paused}
}
@media (max-width:760px) and (prefers-reduced-motion:reduce){.hx-bg .g img{opacity:1;animation:none}.hx-phone,.hx-phone img{animation:none}}

/* towns we serve */
.towns{border-top:1px solid var(--line);border-bottom:1px solid var(--line);overflow:hidden;padding:16px 0;position:relative}
.towns .track{display:flex;width:max-content;animation:marq 48s linear infinite}
.towns ul{display:flex;list-style:none}
.towns li{display:flex;align-items:center;gap:22px;padding-right:22px;font-weight:700;font-size:1.02rem;color:var(--muted);white-space:nowrap}
.towns li svg{width:14px;height:10px;color:var(--accent2);flex:none}
.towns:hover .track{animation-play-state:paused}
@keyframes marq{to{transform:translateX(-50%)}}

/* Built under the Peak */
.ridge{position:relative;min-height:clamp(560px,94svh,920px);display:grid;align-items:end;overflow:hidden;padding:0;isolation:isolate}
.ridge-media{position:absolute;inset:0;z-index:-1;transform-origin:50% 60%}
.ridge-media picture{position:absolute;inset:0}
.ridge-media img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:46% 52%}
.ridge-copy{padding-bottom:clamp(56px,8vw,112px)}
.ridge h2{font-size:clamp(2.7rem,7.4vw,6rem);letter-spacing:-.04em;line-height:.94;max-width:8.5em}
.ridge h2 .w{display:inline-block;overflow:hidden;vertical-align:top;padding-bottom:.06em}
.ridge h2 .w>span{display:inline-block}
.ridge p{color:var(--muted);max-width:31em;margin-top:20px;font-size:clamp(1.05rem,1.5vw,1.22rem)}

/* the ridge at the bottom of every page */
.horizon{position:relative;height:clamp(300px,44vw,680px);overflow:hidden;margin-top:clamp(32px,5vw,64px);pointer-events:none}
.horizon img{position:absolute;left:0;top:0;width:100%;height:112%;object-fit:cover;object-position:46% 62%}
.horizon+.foot{margin-top:clamp(-210px,-13vw,-90px);position:relative;border-top:0}

/* a real sample scrolling inside a phone */
.reel{display:grid;grid-template-columns:minmax(0,.85fr) minmax(0,1.15fr);gap:clamp(32px,6vw,104px);align-items:start}
.reel-phone{position:sticky;top:104px;justify-self:center;width:min(100%,330px);aspect-ratio:390/844;border-radius:46px;border:10px solid #07080a;background:#07080a;box-shadow:0 50px 100px -40px rgba(0,0,0,.95),0 0 0 1px var(--line2)}
.reel-screen{position:absolute;inset:0;overflow:hidden;border-radius:36px;background:var(--bg3)}
.reel-screen .tall{position:absolute;left:0;top:0;width:100%;height:auto;max-width:none}
.reel-screen .bar{position:absolute;left:0;bottom:0;width:100%;height:auto}
.reel-list{list-style:none}
.reel-list li{display:grid;grid-template-columns:28px minmax(0,1fr);gap:16px;padding:clamp(26px,6vh,60px) 0;border-bottom:1px solid var(--line);transition:opacity .45s}
.reel-list li:first-child{border-top:1px solid var(--line)}
.reel.live .reel-list li{opacity:.38}
.reel.live .reel-list li.on{opacity:1}
.reel-list svg{width:24px;height:24px;color:var(--accent2);margin-top:4px}
.reel-list b{display:block;font-size:clamp(1.2rem,2vw,1.5rem);letter-spacing:-.02em;margin-bottom:6px}
.reel-list span{color:var(--muted)}
@media (max-width:860px){.reel{grid-template-columns:minmax(0,1fr)}.reel-phone{position:relative;top:auto;width:min(74%,300px)}.reel.live .reel-list li{opacity:1}}

/* about: the production line */
.pipe{--fill:1;list-style:none;display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:24px;position:relative;padding-top:30px}
.pipe::before,.pipe::after{content:'';position:absolute;left:0;right:0;top:6px;height:2px;background:var(--line)}
.pipe::after{background:var(--accent);transform:scaleX(var(--fill));transform-origin:0 50%}
.pipe li{position:relative}
.pipe li::before{content:'';position:absolute;top:-30px;left:0;width:14px;height:14px;border-radius:var(--r3);background:var(--bg);border:2px solid var(--accent2);z-index:1}
.pipe b{display:block;font-size:1.25rem;margin-bottom:6px}
.pipe span{color:var(--muted);font-size:.98rem}
.pipe .who{display:block;margin-top:10px;font-size:.85rem;font-weight:700;color:var(--accent2)}
@media (max-width:900px){.pipe{grid-template-columns:minmax(0,1fr);padding:0 0 0 34px;gap:28px}.pipe::before,.pipe::after{left:6px;right:auto;top:0;bottom:0;width:2px;height:auto}.pipe::after{transform:scaleY(var(--fill));transform-origin:50% 0}.pipe li::before{top:4px;left:-34px}}

/* pricing: the monthly plan math */
.calc{display:grid;grid-template-columns:minmax(0,.8fr) minmax(0,1.2fr);gap:clamp(24px,5vw,64px);align-items:center;border:1px solid var(--line);border-radius:var(--r2);background:var(--bg2);padding:clamp(22px,4vw,40px)}
.calc .fld label{display:flex;justify-content:space-between;gap:12px}
.calc output{color:var(--accent2);font-variant-numeric:tabular-nums}
.calc input[type=range]{width:100%;height:44px;accent-color:var(--accent);background:transparent;font-size:16px}
.calc .ctl{display:grid;gap:18px}
.bars{display:grid;gap:18px}
.bar-row{display:grid;gap:8px}
.bar-row .top{display:flex;justify-content:space-between;gap:12px;font-weight:700}
.bar-row .top b{font-size:1.3rem;letter-spacing:-.02em}
.bar{height:16px;border-radius:var(--r3);background:var(--bg3);overflow:hidden}
.bar i{display:block;height:100%;border-radius:var(--r3);background:var(--faint);transform-origin:0 50%;transition:transform .5s var(--ease)}
.bar.us i{background:var(--accent)}
.calc .fine{color:var(--faint);font-size:.9rem}
.save{font-size:clamp(1.3rem,2.4vw,1.8rem);font-weight:850;letter-spacing:-.02em}
.save b{color:var(--accent2);font-variant-numeric:tabular-nums}
@media (max-width:860px){.calc{grid-template-columns:minmax(0,1fr)}}

/* faq search */
.faq-find{display:flex;align-items:center;gap:10px;max-width:900px;margin-bottom:22px;border:1px solid var(--line2);border-radius:var(--r1);padding:0 14px;background:var(--bg2)}
.faq-find svg{width:18px;height:18px;color:var(--faint);flex:none}
.faq-find input{flex:1;min-height:52px;border:0;background:transparent;color:var(--text);font:500 16px var(--font);outline:none}
.faq-none{color:var(--muted);padding:18px 0}
.faq .ans{overflow:hidden}

/* pricing */
.prices{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);gap:20px}
.price{border:1px solid var(--line);border-radius:var(--r2);padding:28px;background:var(--bg2)}
.price.main{grid-row:span 2;border-color:rgba(226,98,42,.55);background:var(--bg2)}
.price .tag{display:inline-block;font-size:.8rem;font-weight:700;color:var(--accent-ink);background:var(--accent2);border-radius:var(--r3);padding:4px 10px;margin-bottom:14px}
.price h3{font-size:1.15rem;color:var(--muted);font-weight:700}
.price .amt{font-size:clamp(2.6rem,5vw,3.6rem);font-weight:850;letter-spacing:-.04em;line-height:1;margin:8px 0 6px}
.price .amt small{font-size:1rem;font-weight:600;color:var(--muted);letter-spacing:0;margin-left:6px}
.price ul{list-style:none;margin-top:18px;display:grid;gap:10px}
.price li{display:flex;gap:10px;color:var(--muted)}
.price li::before{content:'';flex:none;width:7px;height:7px;margin-top:.62em;border-radius:2px;background:var(--accent2)}
.price .btn{margin-top:22px}
.price-extra{grid-column:1/-1;display:flex;flex-wrap:wrap;gap:10px 28px;color:var(--muted);padding:6px 2px 0}
.price-extra b{color:var(--text)}
@media (max-width:860px){.prices{grid-template-columns:minmax(0,1fr)}.price.main{grid-row:auto}}
.terms{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 40px;list-style:none;margin-top:12px}
.terms li{padding:16px 0;border-bottom:1px solid var(--line);color:var(--muted)}
.terms li b{color:var(--text)}
@media (max-width:760px){.terms{grid-template-columns:minmax(0,1fr)}}
.cost-table{width:100%;border-collapse:collapse;margin-top:8px}
.cost-table th,.cost-table td{text-align:left;padding:16px 12px 16px 0;border-bottom:1px solid var(--line);vertical-align:top}
.cost-table th{font-size:.82rem;letter-spacing:.08em;text-transform:uppercase;color:var(--faint);font-weight:700}
.cost-table td:first-child{font-weight:700}
.cost-table td.n{white-space:nowrap;font-weight:800}
.cost-table td.s{color:var(--muted)}

/* features list */
.feat{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 48px;list-style:none}
.feat li{display:grid;grid-template-columns:28px minmax(0,1fr);gap:14px;padding:22px 0;border-bottom:1px solid var(--line)}
.feat svg{width:24px;height:24px;color:var(--accent2);margin-top:2px}
.feat b{display:block;font-size:1.08rem;margin-bottom:4px}
.feat span{color:var(--muted)}
@media (max-width:760px){.feat{grid-template-columns:minmax(0,1fr)}}

/* founder */
.founder.solo{grid-template-columns:minmax(0,1fr)}
.founder{display:grid;grid-template-columns:minmax(0,.8fr) minmax(0,1.2fr);gap:clamp(28px,5vw,72px);align-items:center}
.portrait[hidden]{display:none}
.portrait{position:relative;aspect-ratio:4/5;border-radius:var(--r2);overflow:hidden;background:var(--bg3);border:1px solid var(--line)}
.portrait img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:1}
.portrait .art{position:absolute;inset:0}
.founder blockquote{font-size:clamp(1.35rem,2.4vw,1.8rem);font-weight:650;letter-spacing:-.02em;line-height:1.3;margin:18px 0 22px}
.founder p{color:var(--muted);max-width:34em}
.founder .sig{color:var(--text);font-weight:700;margin-top:18px}
@media (max-width:860px){.founder{grid-template-columns:minmax(0,1fr)}.portrait{max-width:420px;aspect-ratio:16/10}}

/* faq */
.faq{border-top:1px solid var(--line);max-width:900px}
.faq details{border-bottom:1px solid var(--line)}
.faq summary{list-style:none;display:flex;justify-content:space-between;align-items:center;gap:16px;min-height:64px;padding:16px 0;cursor:pointer;font-weight:700;font-size:1.1rem}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:'';flex:none;width:12px;height:12px;border-right:2px solid var(--muted);border-bottom:2px solid var(--muted);transform:rotate(45deg) translateY(-3px);transition:transform .25s}
.faq details[open] summary::after{transform:rotate(225deg) translateY(-3px)}
.faq .ans{padding:0 0 22px;color:var(--muted);max-width:44em}
.faq .ans p+p{margin-top:10px}

/* cta band */
.band{border-top:1px solid var(--line);border-bottom:1px solid var(--line);background:var(--bg2)}
.band .wrap{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,.8fr);gap:28px;align-items:center}
.band .big-tel{font-size:clamp(2rem,4.5vw,3.4rem);font-weight:850;letter-spacing:-.03em;text-decoration:none;display:inline-flex;min-height:56px;align-items:center}
@media (max-width:860px){.band .wrap{grid-template-columns:minmax(0,1fr)}}

/* page head */
.phead{padding:clamp(56px,8vw,104px) 0 clamp(28px,4vw,48px)}
.phead h1{font-size:clamp(2.4rem,5.4vw,4.4rem)}
.phead .lede{margin-top:18px}

/* form */
.form-wrap{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,.85fr);gap:clamp(28px,5vw,64px);align-items:start}
@media (max-width:900px){.form-wrap{grid-template-columns:minmax(0,1fr)}}
form.ask{display:grid;gap:18px;padding:clamp(20px,3vw,32px);border:1px solid var(--line);border-radius:var(--r2);background:var(--bg2)}
.fld{display:grid;gap:8px}
.fld>label,.fld legend{font-weight:700;font-size:.98rem}
.fld .hint{color:var(--faint);font-weight:500;font-size:.9rem}
.fld input[type=text],.fld input[type=tel],.fld input[type=email],.fld select{width:100%;min-height:52px;font:500 16px var(--font);color:var(--text);background:var(--bg);border:1px solid var(--line2);border-radius:var(--r1);padding:0 14px}
.fld select{appearance:none;background-image:linear-gradient(45deg,transparent 50%,var(--muted) 50%),linear-gradient(135deg,var(--muted) 50%,transparent 50%);background-position:calc(100% - 20px) 50%,calc(100% - 14px) 50%;background-size:6px 6px;background-repeat:no-repeat}
.fld select option{color:#111}
.fld input:focus,.fld select:focus{outline:none;border-color:var(--accent2)}
fieldset.fld{border:0}
.choices{display:flex;flex-wrap:wrap;gap:8px;margin-top:4px}
.choices label{display:inline-flex;align-items:center;gap:10px;min-height:48px;padding:0 16px;border:1px solid var(--line2);border-radius:var(--r1);cursor:pointer;font-size:16px;font-weight:600}
.choices input{accent-color:var(--accent);width:18px;height:18px}
.choices label:has(input:checked){border-color:var(--accent2);background:rgba(226,98,42,.08)}
.hp{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden}
.form-msg{min-height:1.4em;color:var(--accent2);font-weight:600}
.privacy-line{color:var(--faint);font-size:.9rem}
.side-card{border:1px solid var(--line);border-radius:var(--r2);padding:24px;display:grid;gap:14px}
.side-card .big-tel{font-size:1.8rem;font-weight:850;letter-spacing:-.02em;text-decoration:none;min-height:48px;display:inline-flex;align-items:center}

/* prose */
.prose{max-width:46em;color:var(--muted)}
.prose h2{color:var(--text);font-size:1.6rem;margin:40px 0 12px}
.prose p+p{margin-top:12px}
.prose ul{margin:12px 0 0 20px}
.prose li{margin:6px 0}

/* footer */
.foot{border-top:1px solid var(--line);padding:56px 0 40px;color:var(--muted);font-size:.95rem}
.foot .wrap{display:grid;grid-template-columns:minmax(0,1.4fr) repeat(2,minmax(0,1fr));gap:32px}
.foot h4{color:var(--text);font-size:.82rem;letter-spacing:.1em;text-transform:uppercase;margin-bottom:10px}
.foot ul{list-style:none}
.foot li a{display:inline-flex;align-items:center;min-height:44px;text-decoration:none}
.foot li a:hover{color:var(--text)}
.foot .base{grid-column:1/-1;display:flex;flex-wrap:wrap;justify-content:space-between;gap:12px;border-top:1px solid var(--line);padding-top:22px;margin-top:8px;color:var(--faint);font-size:.88rem}
@media (max-width:760px){.foot .wrap{grid-template-columns:minmax(0,1fr)}}

/* phone call bar */
.callbar{display:none}
@media (max-width:760px){
  .callbar{position:fixed;left:0;right:0;bottom:0;z-index:60;display:flex;gap:8px;padding:10px 12px calc(10px + env(safe-area-inset-bottom));background:rgba(18,20,23,.94);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);border-top:1px solid var(--line)}
  .callbar a{flex:1;min-height:50px;display:flex;align-items:center;justify-content:center;gap:8px;border-radius:var(--r1);font-weight:700;text-decoration:none}
  .callbar .c1{background:var(--accent);color:var(--accent-ink)}
  .callbar .c2{border:1px solid var(--line2)}
  .callbar svg{width:18px;height:18px}
  body{padding-bottom:calc(74px + env(safe-area-inset-bottom))}
}

/* motion */
.js [data-r]{opacity:0;transform:translateY(22px)}
.js [data-r].in{opacity:1;transform:none;transition:opacity .8s cubic-bezier(.2,.7,.1,1),transform .8s cubic-bezier(.2,.7,.1,1)}
.js .load{opacity:0;transform:translateY(16px);animation:up .9s cubic-bezier(.2,.7,.1,1) forwards}
.js .load.d1{animation-delay:.08s}.js .load.d2{animation-delay:.16s}.js .load.d3{animation-delay:.24s}.js .load.d4{animation-delay:.34s}
@keyframes up{to{opacity:1;transform:none}}
@media (prefers-reduced-motion:reduce){
  .js [data-r],.js .load{opacity:1;transform:none;animation:none;transition:none}
  .stage img{transition:none}
  .towns .track{animation:none;width:auto}.towns .track ul+ul{display:none}.towns ul{flex-wrap:wrap;row-gap:8px}
  .menu,.menu li{transition:none}
  html.cur-in .curtain{transform:translateY(101%)}
}
"""

ICON = {
    "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>',
    "chat": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/></svg>',
    "arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" style="width:18px;height:18px"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    "share": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v13M7 8l5-5 5 5M5 14v5a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-5"/></svg>',
    "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>',
}
LOGO = ('<svg viewBox="0 0 32 32" aria-hidden="true"><rect x="1" y="1" width="30" height="30" rx="8" fill="#1e2227" stroke="rgba(237,234,228,.22)"/>'
        '<path d="M7 20.5h7.5M9 15.5h11M11 10.5h14" stroke="#edeae4" stroke-width="2.4" stroke-linecap="round"/>'
        '<path d="M18.5 20.5l3 0 4-4" stroke="#e2622a" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg>')

def esc(s):
    return html.escape(s, quote=True)

ARROW_UR = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7M8 7h9v9"/></svg>'
PEAK_SEP = '<svg viewBox="0 0 14 10" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" aria-hidden="true"><path d="M1 9 5 4l2 2 2.5-4.5L13 9"/></svg>'

def peak_pic(root, name, alt, pos="46% 52%", lazy=True, cls="", phone="p"):
    """Pikes Peak photo: portrait crop on phones, wide crop elsewhere."""
    p = f"{root}assets/peak/peak-{name}"
    load = ' loading="lazy"' if lazy else ""
    return (f'<picture class="{cls}"><source media="(max-width:700px)" srcset="{p}-{phone}.webp">'
            f'<img src="{p}-1600.webp" srcset="{p}-900.webp 900w, {p}-1600.webp 1600w, {p}-2400.webp 2400w" sizes="100vw" '
            f'alt="{alt}" width="2400" height="1260"{load} decoding="async" style="object-position:{pos}"></picture>')

HEAD_JS = """<script>
(function(h){h.className+=' js';
 try{var t=+sessionStorage.getItem('ssp-nav');sessionStorage.removeItem('ssp-nav');
  if(t&&Date.now()-t<6000&&!matchMedia('(prefers-reduced-motion: reduce)').matches){h.className+=' cur-in';h.setAttribute('data-fresh','1');}}catch(e){}
})(document.documentElement);
</script>
<script type="speculationrules">{"prefetch":[{"where":{"selector_matches":"a[href$='index.html']"},"eagerness":"moderate"}]}</script>"""

# Page change: curtain sweeps up, the next page loads behind it, the curtain leaves off the top.
# Lives inline on every page so it never waits on the motion file.
NAV_JS = r"""
(function(){
  var html=document.documentElement, cur=document.querySelector('.curtain'), reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  var EASE='cubic-bezier(.76,0,.24,1)';
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
  function reveal(){
    if(!html.classList.contains('cur-in')) return;
    var done=function(){ html.classList.remove('cur-in'); };
    if(!cur.animate){ done(); return; }
    var a=cur.animate([{transform:'translateY(0)'},{transform:'translateY(-101%)'}],{duration:640,easing:EASE,fill:'forwards'});
    a.onfinish=function(){ done(); a.cancel(); };
  }
  var fontsIn=document.fonts&&document.fonts.ready?Promise.race([document.fonts.ready,new Promise(function(r){setTimeout(r,350);})]):Promise.resolve();
  fontsIn.then(function(){ requestAnimationFrame(function(){ requestAnimationFrame(reveal); }); });
  addEventListener('pageshow',function(e){ if(e.persisted){ html.classList.remove('cur-in'); cur.classList.remove('go'); if(cur.getAnimations) cur.getAnimations().forEach(function(x){x.cancel();}); setMenu(false); } });
  function internal(a){
    if(!a||(a.target&&a.target!=='_self')||a.hasAttribute('download')) return null;
    var h=a.getAttribute('href'); if(!h||h.charAt(0)==='#'||/^(tel|sms|mailto|javascript):/i.test(h)) return null;
    var u; try{ u=new URL(a.href,location.href); }catch(e){ return null; }
    return u.origin===location.origin?u:null;
  }
  document.addEventListener('click',function(e){
    if(e.defaultPrevented||e.button!==0||e.metaKey||e.ctrlKey||e.shiftKey||e.altKey) return;
    var a=e.target.closest&&e.target.closest('a'), u=internal(a); if(!u) return;
    if(u.pathname===location.pathname&&u.search===location.search){
      if(u.hash) return;
      e.preventDefault(); setMenu(false); if(window.__lenis) window.__lenis.scrollTo(0); else scrollTo({top:0,behavior:reduce?'auto':'smooth'}); return;
    }
    if(reduce||!cur.animate) return;
    e.preventDefault();
    try{ sessionStorage.setItem('ssp-nav',String(Date.now())); }catch(x){}
    var went=false, go=function(){ if(went) return; went=true; toTop(); location.href=u.href; };
    cur.classList.add('go'); var a2=cur.animate([{transform:'translateY(101%)'},{transform:'translateY(0)'}],{duration:440,easing:EASE,fill:'forwards'});
    a2.onfinish=go; setTimeout(go,560);
  });
  var seen={};
  function pf(e){ var u=internal(e.target.closest&&e.target.closest('a')); if(!u||seen[u.href]||u.pathname===location.pathname) return; seen[u.href]=1;
    var l=document.createElement('link'); l.rel='prefetch'; l.href=u.href; document.head.appendChild(l); }
  document.addEventListener('touchstart',pf,{passive:true}); document.addEventListener('pointerover',pf,{passive:true}); document.addEventListener('focusin',pf);
  var btn=document.querySelector('.menu-btn'), menu=document.getElementById('menu');
  function setMenu(open){
    if(!menu||!btn) return;
    menu.classList.toggle('open',open); html.classList.toggle('menu-open',open);
    btn.setAttribute('aria-expanded',String(open)); btn.setAttribute('aria-label',open?'Close menu':'Open menu');
    if(open){ menu.removeAttribute('inert'); if(window.__lenis) window.__lenis.stop(); setTimeout(function(){ var f=menu.querySelector('a'); if(f) f.focus({preventScroll:true}); },80); }
    else { menu.setAttribute('inert',''); if(window.__lenis) window.__lenis.start(); }
  }
  if(btn) btn.addEventListener('click',function(){ setMenu(!menu.classList.contains('open')); });
  document.addEventListener('keydown',function(e){
    if(!menu||!menu.classList.contains('open')) return;
    if(e.key==='Escape'){ setMenu(false); btn.focus(); return; }
    if(e.key==='Tab'){
      var f=[btn].concat([].slice.call(menu.querySelectorAll('a'))), i=f.indexOf(document.activeElement);
      if(e.shiftKey&&i<=0){ e.preventDefault(); f[f.length-1].focus(); } else if(!e.shiftKey&&i===f.length-1){ e.preventDefault(); f[0].focus(); }
    }
  });
  addEventListener('resize',function(){ if(innerWidth>900) setMenu(false); });
  var io='IntersectionObserver' in window?new IntersectionObserver(function(es){ es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); } }); },{rootMargin:'0px 0px -8% 0px'}):null;
  document.querySelectorAll('[data-r]').forEach(function(el){ io?io.observe(el):el.classList.add('in'); });
  setTimeout(function(){ document.querySelectorAll('[data-r]').forEach(function(el){ if(el.getBoundingClientRect().top<innerHeight) el.classList.add('in'); }); },60);
})();
"""

def page(path, title, desc, body, active="", head_extra="", script_extra="", horizon=True):
    depth = path.count("/")
    root = "../" * depth
    nav = [("index", "Home"), ("work", "Work"), ("pricing", "Pricing"), ("about", "About"), ("faq", "FAQ"), ("start", "Get started")]
    href = lambda k: f"{root}index.html" if k == "index" else f"{root}{k}/index.html"
    cur = lambda k: ' aria-current="page"' if active == k else ""
    nav_html = "".join(f'<li><a href="{href(k)}"{cur(k)}>{v}</a></li>' for k, v in nav)
    menu_html = "".join(f'<li style="--i:{i}"><a href="{href(k)}"{cur(k)}>{v}{ARROW_UR}</a></li>' for i, (k, v) in enumerate(nav))
    canonical = CONFIG["domain"] + (path.replace("index.html", "") if path != "index.html" else "")
    hz = (f'<div class="horizon" aria-hidden="true">{peak_pic(root, "glow", "", "46% 62%")}</div>') if horizon else ""
    out = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="SiteSprintPro">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{CONFIG['domain']}assets/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#121417">
<link rel="icon" href="data:image/svg+xml,{esc(LOGO.replace('"', "'").replace('#', '%23'))}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONT}">
{HEAD_JS}
<style>{CSS}</style>
{head_extra}
</head>
<body>
<div class="curtain" aria-hidden="true">{LOGO}</div>
<a class="skip" href="#main">Skip to content</a>
<header class="hdr"><div class="wrap">
  <a class="brand" href="{root}index.html" aria-label="SiteSprintPro home">{LOGO}<span>SiteSprint<b>Pro</b></span></a>
  <nav aria-label="Main"><ul class="nav">{nav_html}</ul></nav>
  <div class="hdr-r">
    <a class="call-pill" href="tel:{CONFIG['phone']}" aria-label="Call {CONFIG['phoneDisplay']}">{ICON['phone']}<span class="num">{CONFIG['phoneDisplay']}</span></a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu" aria-label="Open menu"><span class="bars"><span></span><span></span></span></button>
  </div>
</div></header>
<div class="menu" id="menu" inert>
  <nav aria-label="Menu"><ul>{menu_html}</ul></nav>
  <div class="menu-foot"><a class="btn btn-hot" href="tel:{CONFIG['phone']}">{ICON['phone']}Call</a><a class="btn btn-line" href="sms:{CONFIG['phone']}">{ICON['chat']}Text</a></div>
</div>
<main id="main">
{body.replace('{root}', root)}
</main>
{hz}
<footer class="foot"><div class="wrap">
  <div>
    <a class="brand" href="{root}index.html">{LOGO}<span>SiteSprint<b>Pro</b></span></a>
    <p style="margin-top:12px;max-width:30em">Websites for Colorado businesses. Live in 2 to 3 days, yours to keep.</p>
  </div>
  <div><h4>Site</h4><ul>
    <li><a href="{root}index.html">Home</a></li>
    <li><a href="{root}work/index.html">Sample sites</a></li>
    <li><a href="{root}pricing/index.html">Pricing</a></li>
    <li><a href="{root}about/index.html">About</a></li>
    <li><a href="{root}faq/index.html">FAQ</a></li>
  </ul></div>
  <div><h4>Contact</h4><ul>
    <li><a href="tel:{CONFIG['phone']}">Call {CONFIG['phoneDisplay']}</a></li>
    <li><a href="sms:{CONFIG['phone']}">Text {CONFIG['phoneDisplay']}</a></li>
    <li><a href="mailto:{CONFIG['email']}">{CONFIG['email']}</a></li>
    <li><a href="{root}start/index.html">Get started</a></li>
  </ul></div>
  <div class="base"><span>Colorado Springs, Colorado</span><span><a href="{root}privacy/index.html" style="display:inline-flex;min-height:44px;align-items:center">Privacy</a></span><span>&copy; 2026 SiteSprintPro</span></div>
</div></footer>
<div class="callbar" aria-label="Quick contact">
  <a class="c1" href="tel:{CONFIG['phone']}">{ICON['phone']}Call</a>
  <a class="c2" href="sms:{CONFIG['phone']}">{ICON['chat']}Text</a>
  <a class="c2" href="{root}start/index.html">Get started</a>
</div>
<script>{NAV_JS}
{script_extra}
</script>
<script src="{root}assets/vendor.js" defer></script>
<script src="{root}assets/site.js" defer></script>
</body>
</html>
"""
    dest = SITE / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(out)
    return dest

def tel_btn(cls="btn btn-hot"):
    return f'<a class="{cls}" href="tel:{CONFIG["phone"]}">{ICON["phone"]}Call {CONFIG["phoneDisplay"]}</a>'

def card(s, size="", actions=False):
    acts = ""
    if actions:
        acts = (f'<div class="card-actions"><a class="btn btn-hot" href="{{root}}{s["slug"]}/index.html">Open the site {ICON["arrow"]}</a>'
                f'<button class="btn btn-line share" type="button" data-slug="{s["slug"]}" data-name="{esc(s["name"])}">{ICON["share"]}Share</button></div>')
        tag_open, tag_close = '<article class="card %s" data-group="%s">' % (size, s["group"]), "</article>"
        title = f'<h3><a href="{{root}}{s["slug"]}/index.html" style="text-decoration:none">{esc(s["name"])}</a></h3>'
    else:
        tag_open, tag_close = f'<a class="card {size}" href="{{root}}{s["slug"]}/index.html" data-r>', "</a>"
        title = f'<h3>{esc(s["name"])}</h3>'
    return (f'{tag_open}<div class="shot"><img class="d" src="{{root}}assets/shots/{s["slug"]}-desktop.webp" width="1200" height="750" alt="{esc(s["name"])} sample site on a laptop" loading="lazy" decoding="async">'
            f'<img class="p" src="{{root}}assets/shots/{s["slug"]}-phone.webp" width="600" height="1298" alt="" loading="lazy" decoding="async"></div>'
            f'<div class="card-body"><span class="niche">{s["niche"]}</span>{"" if actions else "<span class=go>Open the site " + ICON["arrow"] + "</span>"}{title}<p>{esc(s["line"])}</p></div>{acts}{tag_close}')

FAQS = [
    ("Who will I be working with?", ["Don, from the first call to launch day. He plans your site, reviews every page and answers the phone. A production system handles the build and testing behind him, which is how the price stays flat and the timeline stays short."]),
    ("Do I own the website?", ["Yes. Once the balance is paid, the site, the files and the domain are yours. If you ever want to leave, you take everything with you."]),
    ("Are there monthly fees?", ["No. The only recurring cost is your domain name, about $12 a year, paid to the registrar. A care plan is optional: $100 a quarter if you want us to handle changes."]),
    ("How fast is it?", ["Standard sites go live 2 to 3 days after the deposit and your info. Pro builds get priority, usually 1 to 2 days."]),
    ("What do you need from me?", ["Your services, hours, service area, your logo if you have one, and 10 to 20 photos from your phone of real work, your crew or your space. We write all the words."]),
    ("I only have a Facebook page. Which option is that?", ["Starter, $697. We build up to 3 pages from what's already on your Facebook or Instagram page: your photos, hours, services and reviews. You don't have to write anything."]),
    ("I already have a website. Can you fix it?", ["Often, yes. A refresh of an existing site is $300 to $400 when the bones are good. If it's cheaper to rebuild, we'll tell you."]),
    ("Will it help me show up on Google?", ["We connect the site to your Google Business Profile and set it up with the business details Google reads. Where you rank depends on your profile, your reviews and your competition, so nobody can honestly promise first place."]),
    ("Can you use my Google reviews?", ["Yes, your real reviews, quoted word for word with the reviewer's first name. Never made-up ones."]),
    ("Where do the photos come from?", ["Your own photos first. When a section needs more, we license stock photos for your business so you're covered. Never random images pulled off the internet."]),
    ("Do you use AI?", ["Yes, for the repetitive build and testing work. That's how you get a custom site in days at this price. Every site is planned and reviewed by Don, written for your business, and checked on real phone sizes before you see it."]),
    ("How do I pay?", ["Half to start and half when you approve the finished site, by invoice. You see it working before you pay the second half."]),
]

def faq_html(items):
    return '<div class="faq">' + "".join(
        f'<details><summary>{esc(q)}</summary><div class="ans">{"".join("<p>" + esc(p) + "</p>" for p in a)}</div></details>' for q, a in items) + "</div>"

FEATURES = [
    ("Tap to call on every page", "Your number is one tap from anywhere on the site, with a call bar that stays on screen on phones."),
    ("Built for phones first", "Most people find you on a phone. Every site is checked on four phone sizes and a desktop before you see it."),
    ("Your real Google reviews", "Quoted word for word with first names. Nothing invented, ever."),
    ("Leads that reach you", "A quote or booking form that lands in your email the second someone sends it."),
    ("Set up for Google", "Your name, number, hours and service area written the way search engines read them, and linked to your Google profile."),
    ("Yours to keep", "No monthly platform, no lock-in. You own the site, the files and the domain."),
]

def build():
    s = SAMPLES
    stage_imgs = "".join(
        f'<img src="assets/shots/{x["slug"]}-desktop.webp" width="1200" height="750" alt="" class="{"on" if i == 0 else ""}" {"" if i == 0 else "loading=lazy"} decoding="async">' for i, x in enumerate(s))
    stage_phone = "".join(
        f'<img src="assets/shots/{x["slug"]}-phone.webp" width="600" height="1298" alt="" class="{"on" if i == 0 else ""}" {"" if i == 0 else "loading=lazy"} decoding="async">' for i, x in enumerate(s))
    feats = "".join(f'<li>{ICON["check"]}<div><b>{esc(a)}</b><span>{esc(b)}</span></div></li>' for a, b in FEATURES)
    towns = ["Colorado Springs", "Monument", "Fountain", "Manitou Springs", "Woodland Park", "Falcon", "Black Forest", "Peyton",
             "Security-Widefield", "Palmer Lake", "Cripple Creek", "Cañon City", "Pueblo", "Castle Rock"]
    town_items = "".join(f'<li>{esc(t)}{PEAK_SEP}</li>' for t in towns)
    town_ul = lambda hidden: ('<ul aria-hidden="true">' if hidden else '<ul>') + town_items + "</ul>"
    ld = {"@context": "https://schema.org", "@type": "ProfessionalService", "name": "SiteSprintPro",
          "description": "Websites for Colorado small businesses, built in Colorado Springs.", "url": CONFIG["domain"],
          "telephone": CONFIG["phone"], "email": CONFIG["email"],
          "areaServed": [{"@type": "City", "name": "Colorado Springs, Colorado"}, {"@type": "State", "name": "Colorado"}], "priceRange": "$697 to $1,197"}
    featured = [s[0], s[5], s[4]]
    home = f"""
<section class="hero"><canvas class="topo" aria-hidden="true"></canvas><div class="hx-bg" aria-hidden="true"><picture class="m"><source media="(max-width:760px)" srcset="assets/peak/peak-mist-p.webp"><img src="data:image/gif;base64,R0lGODlhAQABAAAAACw=" alt="" width="1588" height="1765"></picture><picture class="g"><source media="(max-width:760px)" srcset="assets/peak/peak-glow-p.webp"><img src="data:image/gif;base64,R0lGODlhAQABAAAAACw=" alt="" width="1588" height="1765"></picture></div><div class="hx-phone" aria-hidden="true"><picture><source media="(max-width:760px)" srcset="assets/reel/hvac-hero.webp"><img src="data:image/gif;base64,R0lGODlhAQABAAAAACw=" alt="" width="600" height="4200"></picture></div><div class="wrap">
  <div>
    <h1 class="load">Websites for Springs businesses.</h1>
    <p class="lede load d1">Live in 2 to 3 days. One flat price, no monthly fees, and the site is yours.</p>
    <div class="btns load d2">{tel_btn()}<a class="btn btn-line" href="work/index.html">See the work {ICON['arrow']}</a></div>
    <p class="small-note load d3">Or text the same number. You get Don, not a call center.</p>
  </div>
  <div class="stage load d2" aria-label="Sample sites, cycling">
    <div class="desk">{stage_imgs}</div>
    <div class="phone">{stage_phone}</div>
    <div class="stage-cap" aria-live="polite"><span id="capNiche">{s[0]['niche']} sample</span><b id="capName">{esc(s[0]['name'])}</b><a id="capLink" href="{s[0]['slug']}/index.html">Open it {ICON['arrow']}</a></div>
  </div>
</div></section>

<div class="towns" aria-label="Towns we build for"><div class="track">{town_ul(False)}{town_ul(True)}</div></div>

<section id="work"><div class="wrap">
  <div class="sec-head"><h2 data-r>Find the one closest to your business.</h2><p class="lede" data-r>Six live samples. Open one on your phone, that's how your customers will see yours.</p></div>
  <div class="work">{card(featured[0],'w7')}{card(featured[1],'w5')}{card(featured[2],'w5')}<a class="card w7 more" href="work/index.html" data-r><div class="more-mosaic" aria-hidden="true"><img src="{{root}}assets/shots/plumbing-desktop.webp" width="1200" height="750" alt="" loading="lazy" decoding="async"><img src="{{root}}assets/shots/contractor-desktop.webp" width="1200" height="750" alt="" loading="lazy" decoding="async"><img src="{{root}}assets/shots/lawn-desktop.webp" width="1200" height="750" alt="" loading="lazy" decoding="async"></div><div class="more-in"><b>See all six samples</b><span>HVAC, plumbing, contractor, lawn care, salon and restaurant.</span><span class="go">Open the work {ICON['arrow']}</span></div></a></div>
</div></section>

<section class="ridge" aria-labelledby="ridge-h">
  <div class="ridge-media" aria-hidden="true">{peak_pic("", "mist", "", "46% 52%", cls="r-mist", phone="s")}{peak_pic("", "glow", "", "46% 52%", cls="r-glow", phone="s")}</div>
  <div class="wrap ridge-copy">
    <h2 id="ridge-h">Built under the Peak.</h2>
    <p>We're in Colorado Springs. We know the 10pm furnace call, the first hard freeze and Pikes Peak Regional permits. Your site will too.</p>
  </div>
</section>

<section><div class="wrap">
  <div class="sec-head"><h2 data-r>How it works</h2><p class="lede" data-r>Three steps, one point of contact from the first call to launch day.</p></div>
  <ol class="steps">
    <li style="--i:0"><span class="when">Same day</span><div><h3>Call, text, or send the form.</h3><p>Tell us what you do and where. We send back the sample closest to your business and a flat quote.</p></div></li>
    <li style="--i:1"><span class="when">2 to 3 days</span><div><h3>Half down, and we build it.</h3><p>Your services, hours, real Google reviews and photos. You check it on your phone and tell us what to change.</p></div></li>
    <li style="--i:2"><span class="when">Yours</span><div><h3>It goes live on your domain.</h3><p>Tap to call everywhere, a form that reaches your inbox, connected to your Google profile. Then you own it.</p></div></li>
  </ol>
</div></section>

<section style="padding-top:0"><div class="wrap">
  <div class="sec-head"><h2 data-r>Built for the phone in your customer's hand.</h2><p class="lede" data-r>Scroll and watch a sample site run on a phone. Every site gets these.</p></div>
  <div class="reel">
    <div class="reel-phone" aria-hidden="true"><div class="reel-screen"><img class="tall" src="assets/reel/hvac-tall.webp" width="600" height="12845" alt="" loading="lazy" decoding="async"><img class="bar" src="assets/reel/hvac-bar.webp" width="600" height="117" alt="" loading="lazy" decoding="async"></div></div>
    <ul class="reel-list">{feats}</ul>
  </div>
</div></section>

<section class="band"><div class="wrap">
  <div><h2 data-r>Want to see yours?</h2><p class="lede" data-r style="margin-top:14px">Call or text, or send the one-minute form. We'll send the closest sample and a flat price the same day.</p></div>
  <div data-r><a class="big-tel" href="tel:{CONFIG['phone']}">{CONFIG['phoneDisplay']}</a><div class="btns" style="margin-top:14px"><a class="btn btn-hot" href="start/index.html">Get started</a><a class="btn btn-line" href="sms:{CONFIG['phone']}">{ICON['chat']}Text us</a></div></div>
</div></section>
"""
    names = json.dumps([[x["slug"], x["niche"], x["name"]] for x in s])
    stage_js = f"""
(function(){{
  var S = {names}, i = 0, reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var d = document.querySelectorAll('.stage .desk img'), p = document.querySelectorAll('.stage .phone img');
  var n = document.getElementById('capNiche'), nm = document.getElementById('capName'), l = document.getElementById('capLink');
  if (!d.length || reduce) return;
  var visible = true;
  if ('IntersectionObserver' in window) new IntersectionObserver(function(e){{ visible = e[0].isIntersecting; }}).observe(document.querySelector('.stage'));
  setInterval(function(){{
    if (!visible || document.hidden) return;
    d[i].classList.remove('on'); p[i].classList.remove('on');
    i = (i + 1) % S.length;
    d[i].classList.add('on'); p[i].classList.add('on');
    n.textContent = S[i][1] + ' sample'; nm.textContent = S[i][2]; l.setAttribute('href', S[i][0] + '/index.html');
  }}, 3600);
}})();
"""
    page("index.html", "SiteSprintPro | Websites for Colorado Springs businesses",
         "Websites for Colorado Springs businesses. Live in 2 to 3 days, one flat price, no monthly fees, and you own it.",
         home, head_extra=f'<script type="application/ld+json">{json.dumps(ld)}</script>', script_extra=stage_js)

    # WORK
    cards = "".join(card(x, "", actions=True) for x in s)
    work = f"""
<section class="phead"><div class="wrap">
  <h1 class="load">Sample sites</h1>
  <p class="lede load d1">Six live samples for six kinds of business. Open one on your phone, or share it with someone who needs a site.</p>
</div></section>
<section style="padding-top:0"><div class="wrap">
  <div class="filters" role="group" aria-label="Filter samples">
    <button type="button" aria-pressed="true" data-f="all">All</button><button type="button" aria-pressed="false" data-f="trades">Trades</button><button type="button" aria-pressed="false" data-f="beauty">Beauty</button><button type="button" aria-pressed="false" data-f="food">Food</button>
  </div>
  <div class="work">{cards}</div>
  <p class="sample-note">Every sample is a fictional business. Reviews and numbers on them are placeholders. Your site uses your real ones.</p>
</div></section>
<section class="band"><div class="wrap">
  <div><h2>Don't see your trade?</h2><p class="lede" style="margin-top:14px">These are starting points, not templates. Every site is written and designed for one business.</p></div>
  <div><div class="btns">{tel_btn()}<a class="btn btn-line" href="../start/index.html">Get started</a></div></div>
</div></section>
"""
    work_js = """
(function(){
  var bs = document.querySelectorAll('.filters button'), cs = document.querySelectorAll('.work .card');
  bs.forEach(function(b){ b.addEventListener('click', function(){
    bs.forEach(function(x){ x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
    var f = b.getAttribute('data-f');
    var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
    cs.forEach(function(c){
      var show = f === 'all' || c.getAttribute('data-group') === f;
      if (show && c.style.display === 'none') { c.style.display = ''; if (!reduce && c.animate) c.animate([{opacity:0, transform:'translateY(16px) scale(.98)'},{opacity:1, transform:'none'}], {duration:480, easing:'cubic-bezier(.2,.7,.1,1)'}); }
      else if (!show) c.style.display = 'none';
    });
  }); });
  document.querySelectorAll('.share').forEach(function(btn){ btn.addEventListener('click', function(){
    var url = new URL('../' + btn.getAttribute('data-slug') + '/index.html', location.href).href.replace(/index\\.html$/, '');
    var data = { title: btn.getAttribute('data-name') + ' (sample site)', text: 'A sample site by SiteSprintPro', url: url };
    if (navigator.share) { navigator.share(data).catch(function(){}); return; }
    if (navigator.clipboard) { navigator.clipboard.writeText(url).then(function(){ btn.lastChild.textContent = 'Link copied'; }); }
    else { prompt('Copy this link', url); }
  }); });
})();
"""
    page("work/index.html", "Sample sites | SiteSprintPro",
         "Live sample websites for HVAC, plumbing, contractors, lawn care, salons and restaurants in Colorado Springs.",
         work, active="work", script_extra=work_js)

    # PRICING
    pricing = f"""
<section class="phead"><div class="wrap">
  <h1 class="load">Pricing</h1>
  <p class="lede load d1">Flat prices, written down. Half to start, half when you approve the finished site. No monthly fees.</p>
</div></section>
<section style="padding-top:0"><div class="wrap">
  <div class="prices">
    <div class="price main"><span class="tag">Most picked</span><h3>Standard</h3><div class="amt">$897</div>
      <ul><li>Up to 5 pages: home, services, about, gallery or hiring, contact</li><li>All the writing done for you</li><li>Live in 2 to 3 days after the deposit and your info</li><li>Tap to call on every page and a phone call bar</li><li>Quote or booking form that reaches your email</li><li>Google-ready setup and linked to your Google profile</li><li>2 rounds of changes, plus 2 free updates after launch</li></ul>
      <a class="btn btn-hot" href="../start/index.html">Get started</a></div>
    <div class="price"><h3>Pro</h3><div class="amt">$1,197</div><ul><li>Everything in Standard, up to 8 pages</li><li>Priority build, usually 1 to 2 days</li><li>Photo gallery, reviews section, booking link</li><li>A simple text logo if you don't have one</li><li>4 rounds of changes</li></ul></div>
    <div class="price"><h3>Starter: Facebook to website</h3><div class="amt">$697</div><ul><li>For a business with no website yet, only a Facebook or Instagram page</li><li>Up to 3 pages: home, services, contact</li><li>Built from what's already on your page: photos, hours, services, reviews. You don't write anything</li><li>Tap to call and a quote form, live in 2 to 3 days</li></ul></div>
  </div>
</div></section>
<section style="padding-top:0"><div class="wrap">
  <div class="sec-head"><h2>What a monthly plan really costs</h2><p class="lede">A lot of website companies charge by the month. Move the sliders to see the total next to a one-time site.</p></div>
  <div class="calc" id="calc">
    <div class="ctl">
      <div class="fld"><label for="c-fee">Monthly fee <output id="c-fee-o" for="c-fee">$30</output></label><input id="c-fee" type="range" min="10" max="100" step="5" value="30"></div>
      <div class="fld"><label for="c-yrs">Years <output id="c-yrs-o" for="c-yrs">3</output></label><input id="c-yrs" type="range" min="1" max="5" step="1" value="3"></div>
      <p class="fine">Monthly plan total is the fee times 12 times the years. SiteSprintPro Standard is $897 once, plus about $12 a year for your domain.</p>
    </div>
    <div class="bars" aria-live="polite">
      <div class="bar-row"><div class="top"><span>Monthly plan</span><b id="t-them">$1,080</b></div><div class="bar"><i id="b-them"></i></div></div>
      <div class="bar-row"><div class="top"><span>SiteSprintPro Standard</span><b id="t-us">$933</b></div><div class="bar us"><i id="b-us"></i></div></div>
      <p class="save" id="save">You keep <b>$147</b> and own the site.</p>
    </div>
  </div>
</div></section>
<section style="padding-top:0" id="care"><div class="wrap">
  <h2 style="margin-bottom:12px">Everything it can cost</h2>
  <table class="cost-table">
    <thead><tr><th scope="col">What</th><th scope="col">Price</th><th scope="col">Notes</th></tr></thead>
    <tbody>
      <tr><td>Standard site</td><td class="n">$897</td><td class="s">One time</td></tr>
      <tr><td>Pro site</td><td class="n">$1,197</td><td class="s">One time</td></tr>
      <tr><td>Starter (Facebook to website)</td><td class="n">$697</td><td class="s">One time. Up to 3 pages built from your Facebook or Instagram page</td></tr>
      <tr><td>Refresh of a site you have</td><td class="n">$300 to $400</td><td class="s">When the existing site is worth keeping</td></tr>
      <tr><td>Care plan</td><td class="n">$100 a quarter</td><td class="s">Optional. Text us changes (hours, prices, photos, a new service) and we make them. Cancel anytime.</td></tr>
      <tr><td>Domain name</td><td class="n">About $12 a year</td><td class="s">Paid to the registrar, in your name</td></tr>
      <tr><td>Extra changes</td><td class="n">$75 an hour</td><td class="s">Only after the included rounds</td></tr>
    </tbody>
  </table>
</div></section>
<section style="padding-top:0"><div class="wrap">
  <h2 style="margin-bottom:12px">The terms, in plain words</h2>
  <ul class="terms">
    <li><b>Deposit:</b> half to start, by invoice.</li>
    <li><b>Balance:</b> due when you approve the finished site.</li>
    <li><b>Ownership:</b> the site, files and domain are yours once paid in full.</li>
    <li><b>Domain:</b> registered for you and moved into your own account when the balance clears.</li>
    <li><b>Photos:</b> yours first, licensed stock when needed, never random internet images.</li>
    <li><b>Reviews:</b> only your real Google reviews, word for word.</li>
  </ul>
</div></section>
<section class="band"><div class="wrap">
  <div><h2>Questions about price?</h2><p class="lede" style="margin-top:14px">Call or text and you'll get a straight answer from Don.</p></div>
  <div><div class="btns">{tel_btn()}<a class="btn btn-line" href="../start/index.html">Get started</a></div></div>
</div></section>
"""
    pricing_js = """
(function(){
  var fee=document.getElementById('c-fee'), yrs=document.getElementById('c-yrs'); if(!fee) return;
  var $=function(n){ return '$'+Math.round(n).toLocaleString('en-US'); };
  function upd(){
    var f=+fee.value, y=+yrs.value, them=f*12*y, us=897+12*y, max=Math.max(them,us);
    document.getElementById('c-fee-o').textContent=$(f); document.getElementById('c-yrs-o').textContent=y;
    document.getElementById('t-them').textContent=$(them); document.getElementById('t-us').textContent=$(us);
    document.getElementById('b-them').style.transform='scaleX('+(them/max).toFixed(3)+')'; document.getElementById('b-us').style.transform='scaleX('+(us/max).toFixed(3)+')';
    document.getElementById('save').innerHTML = them>us ? 'You keep <b>'+$(them-us)+'</b> and own the site.' : 'Close on price, and with us <b>you own the site</b>.';
  }
  fee.addEventListener('input',upd); yrs.addEventListener('input',upd); upd();
})();
"""
    page("pricing/index.html", "Pricing | SiteSprintPro",
         "Flat prices: $897 Standard, $1,197 Pro, $697 Starter for businesses that only have a Facebook page. No monthly fees.", pricing, active="pricing", script_extra=pricing_js)

    # ABOUT
    pipe = [("Plan", "Don learns your business, your service area and who calls you.", "Don"),
            ("Write", "Every word written for your trade and your town, the way people search for it.", "Production system"),
            ("Build", "Designed for phones first, with tap to call on every page and a form that reaches you.", "Production system"),
            ("Test", "Checked on four phone sizes and a desktop, plus every link, the form and the load speed.", "Production system"),
            ("Launch", "You approve it on your phone, then it goes live on your domain and your Google profile.", "Don")]
    pipe_html = "".join(f'<li><b>{a}</b><span>{esc(b)}</span><span class="who">{c}</span></li>' for a, b, c in pipe)
    about = f"""
<section class="phead"><div class="wrap">
  <h1 class="load">One point of contact. A full production system behind it.</h1>
  <p class="lede load d1">SiteSprintPro is a web studio in Colorado Springs. {CONFIG['owner']} runs every project and answers the phone. Behind him, a production system writes, builds and tests every site before you see it.</p>
</div></section>
<section style="padding-top:0"><div class="wrap">
  <h2 style="margin-bottom:clamp(28px,4vw,44px)" data-r>How every site gets made</h2>
  <ol class="pipe">{pipe_html}</ol>
</div></section>
<section style="padding-top:0"><div class="wrap founder{"" if CONFIG["ownerPhoto"] else " solo"}">
  <div class="portrait"{"" if CONFIG["ownerPhoto"] else " hidden"}>
    {('<img src="../' + CONFIG['ownerPhoto'] + '" alt="' + CONFIG['owner'] + ' outdoors near Colorado Springs" width="800" height="1000" loading="lazy" decoding="async">') if CONFIG['ownerPhoto'] else ''}
  </div>
  <div class="prose">
    <h2 style="margin-top:0">Why we do this</h2>
    <p>Most small businesses here run on referrals and a Google listing. When a homeowner's furnace quits at 10pm, they search, they look at the first few listings on their phone, and they call whoever looks legit. A listing with no website loses that call more often than it should.</p>
    <p>We build the website that wins it: your number one tap away, your real reviews, your work, and nothing that makes a customer hesitate.</p>
    <h2>How we work</h2>
    <ul><li>You deal with {CONFIG['owner']} from the first call to launch day.</li><li>Flat prices, written down before anything starts.</li><li>No monthly packages. You own what you pay for.</li><li>Every site is tested on four phone sizes and a desktop before you see it.</li></ul>
    <div class="btns" style="margin-top:26px">{tel_btn()}<a class="btn btn-line" href="../work/index.html">See the work</a></div>
  </div>
</div></section>
"""
    page("about/index.html", "About | SiteSprintPro",
         "SiteSprintPro is a Colorado Springs web studio. One point of contact, and a production system that writes, builds and tests every site.", about, active="about")

    # FAQ
    search_icon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>'
    faq = f"""
<section class="phead"><div class="wrap"><h1 class="load">Questions</h1><p class="lede load d1">Straight answers. If yours isn't here, call or text.</p></div></section>
<section style="padding-top:0"><div class="wrap">
  <label class="faq-find" for="faq-q">{search_icon}<span class="sr-only" style="position:absolute;left:-9999px">Search questions</span><input id="faq-q" type="search" placeholder="Search: price, Google, photos" autocomplete="off"></label>
  {faq_html(FAQS)}
  <p class="faq-none" id="faq-none" hidden>Nothing matches that. Call or text {CONFIG['phoneDisplay']} and ask.</p>
</div></section>
<section class="band"><div class="wrap">
  <div><h2>Still wondering?</h2><p class="lede" style="margin-top:14px">Ask directly. Don answers the phone.</p></div>
  <div><div class="btns">{tel_btn()}<a class="btn btn-line" href="../start/index.html">Get started</a></div></div>
</div></section>
"""
    faq_js = """
(function(){
  var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('.faq details').forEach(function(d){
    var sum=d.querySelector('summary'), ans=d.querySelector('.ans');
    sum.addEventListener('click',function(e){
      if(reduce||!ans.animate) return; e.preventDefault();
      if(d.open){ var h=ans.offsetHeight; var a=ans.animate([{height:h+'px',opacity:1},{height:'0px',opacity:0}],{duration:280,easing:'cubic-bezier(.4,0,.2,1)'}); a.onfinish=function(){ d.open=false; }; }
      else { d.open=true; var h2=ans.offsetHeight; ans.animate([{height:'0px',opacity:0},{height:h2+'px',opacity:1}],{duration:380,easing:'cubic-bezier(.2,.7,.1,1)'}); }
    });
  });
  var q=document.getElementById('faq-q'), none=document.getElementById('faq-none');
  if(q) q.addEventListener('input',function(){
    var v=q.value.trim().toLowerCase(), n=0;
    document.querySelectorAll('.faq details').forEach(function(d){ var hit=!v||d.textContent.toLowerCase().indexOf(v)>-1; d.hidden=!hit; if(hit) n++; if(v&&hit) d.open=true; });
    none.hidden=n>0;
  });
})();
"""
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": " ".join(a)}} for q, a in FAQS]}
    page("faq/index.html", "FAQ | SiteSprintPro", "Ownership, pricing, timing, AI, and what you need to get a SiteSprintPro website.",
         faq, active="faq", head_extra=f'<script type="application/ld+json">{json.dumps(faq_ld)}</script>', script_extra=faq_js)

    # START
    kinds = ["HVAC", "Plumbing", "Contractor or remodel", "Lawn and landscaping", "Salon, barber or spa", "Restaurant or food", "Other"]
    sources = ["Facebook group", "SiteSprintPro Facebook Page", "Someone told me", "Google", "Other"]
    start = f"""
<section class="phead"><div class="wrap"><h1 class="load">Get started</h1><p class="lede load d1">Takes a minute. We'll get back to you the same day with the closest sample and a flat price.</p></div></section>
<section style="padding-top:0"><div class="wrap form-wrap">
  <form class="ask" id="ask" novalidate>
    <div class="fld"><label for="f-name">Your name</label><input id="f-name" name="name" type="text" autocomplete="name" required></div>
    <div class="fld"><label for="f-biz">Business name</label><input id="f-biz" name="business" type="text" autocomplete="organization" required></div>
    <div class="fld"><label for="f-phone">Best phone number</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" required></div>
    <div class="fld"><label for="f-kind">What kind of business?</label><select id="f-kind" name="kind" required><option value="">Choose one</option>{''.join(f'<option>{esc(k)}</option>' for k in kinds)}</select></div>
    <fieldset class="fld"><legend>Do you have a website now?</legend><div class="choices">
      <label><input type="radio" name="site" value="No" required>No</label><label><input type="radio" name="site" value="Yes, it needs work">Yes, it needs work</label><label><input type="radio" name="site" value="Only Facebook or Instagram">Only Facebook or Instagram</label></div></fieldset>
    <div class="fld"><label for="f-link">Link to your current site or Facebook page <span class="hint">(optional)</span></label><input id="f-link" name="link" type="text" inputmode="url"></div>
    <fieldset class="fld"><legend>Best way to reach you</legend><div class="choices">
      <label><input type="radio" name="reach" value="Call" required>Call</label><label><input type="radio" name="reach" value="Text">Text</label><label><input type="radio" name="reach" value="Email">Email</label></div></fieldset>
    <div class="fld" id="email-row" hidden><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email"></div>
    <div class="fld"><label for="f-src">Where did you find us? <span class="hint">(optional)</span></label><select id="f-src" name="source"><option value="">Choose one</option>{''.join(f'<option>{esc(k)}</option>' for k in sources)}</select></div>
    <div class="hp" aria-hidden="true"><label>Company<input name="company" tabindex="-1" autocomplete="off"></label></div>
    <button class="btn btn-hot" type="submit">Send it</button>
    <p class="form-msg" id="msg" role="status"></p>
    <p class="privacy-line">Used only to contact you about your website. Never sold or shared. <a href="../privacy/index.html" style="display:inline-flex;align-items:center;min-height:44px">Privacy</a></p>
  </form>
  <aside class="side-card">
    <h2 style="font-size:1.5rem">Rather talk?</h2>
    <p style="color:var(--muted)">Call or text. You get Don.</p>
    <a class="big-tel" href="tel:{CONFIG['phone']}">{CONFIG['phoneDisplay']}</a>
    <div class="btns">{tel_btn()}<a class="btn btn-line" href="sms:{CONFIG['phone']}">{ICON['chat']}Text us</a></div>
    <p style="color:var(--muted)">Want to look around first? <a href="../work/index.html" style="color:var(--accent2);font-weight:700">See the sample sites</a></p>
  </aside>
</div></section>
"""
    start_js = f"""
(function(){{
  var FORM = {json.dumps(CONFIG['form'])}, PHONE = {json.dumps(CONFIG['phone'])}, EMAIL = {json.dumps(CONFIG['email'])};
  var f = document.getElementById('ask'), el = function(n){{ return f.elements[n]; }}, msg = document.getElementById('msg'), er = document.getElementById('email-row');
  var q = new URLSearchParams(location.search);
  if (q.get('src')) {{ var s = document.getElementById('f-src'); for (var i = 0; i < s.options.length; i++) if (s.options[i].text === q.get('src')) s.selectedIndex = i; }}
  if (q.get('kind')) {{ var k = document.getElementById('f-kind'); for (var j = 0; j < k.options.length; j++) if (k.options[j].text === q.get('kind')) k.selectedIndex = j; }}
  f.querySelectorAll('input[name=reach]').forEach(function(r){{ r.addEventListener('change', function(){{ er.hidden = r.value !== 'Email' || !r.checked; }}); }});
  f.addEventListener('submit', function(e){{
    e.preventDefault();
    if (el('company').value) return;
    var bad = [];
    ['name','business','phone','kind'].forEach(function(n){{ if (!el(n).value.trim()) bad.push(n); }});
    if (!f.querySelector('input[name=site]:checked')) bad.push('site');
    if (!f.querySelector('input[name=reach]:checked')) bad.push('reach');
    if (bad.length) {{ msg.textContent = 'Please fill in the highlighted questions.'; var first = f.querySelector('[name=' + bad[0] + ']'); first && first.focus(); return; }}
    var data = {{ name: el('name').value, business: el('business').value, phone: el('phone').value, kind: el('kind').value,
      site: f.querySelector('input[name=site]:checked').value, link: el('link').value,
      reach: f.querySelector('input[name=reach]:checked').value, email: el('email').value, source: el('source').value }};
    if (FORM.action) {{
      var body = new URLSearchParams();
      Object.keys(FORM.fields).forEach(function(key){{ if (data[key]) body.append(FORM.fields[key], data[key]); }});
      fetch(FORM.action, {{ method: 'POST', mode: 'no-cors', body: body }}).then(function(){{
        f.reset(); msg.textContent = 'Got it. We will reach out today. If it is urgent, call or text ' + {json.dumps(CONFIG['phoneDisplay'])} + '.';
      }}).catch(function(){{ fallback(data); }});
    }} else {{ fallback(data); }}
  }});
  function fallback(d){{
    var text = 'New website request: ' + d.name + ', ' + d.business + ' (' + d.kind + '), ' + d.phone + '. Site: ' + d.site + (d.link ? ' ' + d.link : '') + '. Reach by ' + d.reach + (d.email ? ' ' + d.email : '') + '.';
    msg.innerHTML = 'Tap to send this to us: <a href="sms:' + PHONE + '?&body=' + encodeURIComponent(text) + '">by text</a> or <a href="mailto:' + EMAIL + '?subject=Website%20request&body=' + encodeURIComponent(text) + '">by email</a>.';
  }}
}})();
"""
    page("start/index.html", "Get started | SiteSprintPro",
         "Tell us about your business and get the closest sample site and a flat price the same day.", start, active="start", script_extra=start_js)

    # PRIVACY
    privacy = f"""
<section class="phead"><div class="wrap"><h1 class="load">Privacy</h1><p class="lede load d1">Short version: what you send us is used to contact you about a website, and nothing else.</p></div></section>
<section style="padding-top:0"><div class="wrap prose">
  <h2 style="margin-top:0">What the form collects</h2>
  <p>Your name, business name, phone number, the kind of business, whether you have a website, how you'd like to be reached, an email address if you choose email, and where you found me.</p>
  <h2>How it's used</h2>
  <p>Only to contact you about a website for your business. It is stored in SiteSprintPro's Google account. It is never sold, rented or shared with anyone else.</p>
  <h2>Cookies and tracking</h2>
  <p>This site does not use advertising trackers. The fonts load from Google Fonts.</p>
  <h2>Removing your info</h2>
  <p>Call or text {CONFIG['phoneDisplay']} or email <a href="mailto:{CONFIG['email']}" style="display:inline-block;padding:11px 0">{CONFIG['email']}</a> and it will be deleted.</p>
  <p style="margin-top:28px">Updated October 2026.</p>
</div></section>
"""
    page("privacy/index.html", "Privacy | SiteSprintPro", "How SiteSprintPro uses the information you send.", privacy)

    # 404
    page("404.html", "Page not found | SiteSprintPro", "That page moved.",
         f'<section class="phead"><div class="wrap"><h1>That page moved.</h1><p class="lede" style="margin-top:16px">Try the sample sites or the home page.</p><div class="btns" style="margin-top:24px"><a class="btn btn-hot base-link" data-to="work/index.html" href="/work/index.html">Sample sites</a><a class="btn btn-line base-link" data-to="index.html" href="/">Home</a></div></div></section>',
         script_extra="(function(){var b=location.pathname.indexOf('/SiteSprintPro/')===0?'/SiteSprintPro/':'/';document.querySelectorAll('.base-link').forEach(function(a){a.href=b+a.getAttribute('data-to');});})();")

    # Redirects for every old page name, so links already sent still open
    old = {"packages.html": "pricing/index.html", "maintenance.html": "pricing/index.html#care", "faq.html": "faq/index.html",
           "careers.html": "index.html", "portfolio-plumber.html": "plumbing/index.html", "portfolio-salon.html": "salon/index.html",
           "sample-contractor.html": "contractor/index.html", "sample-lawncare.html": "lawn/index.html",
           "sample-restaurant.html": "restaurant/index.html", "portfolio-hvac.html": "hvac/index.html"}
    for name, to in old.items():
        (SITE / name).write_text(f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>Moved | SiteSprintPro</title>'
                                 f'<meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url={to}"><link rel="canonical" href="{CONFIG["domain"]}{to.replace("index.html", "")}">'
                                 f'</head><body><p>This page moved. <a href="{to}">Continue</a>.</p></body></html>')
    (SITE / ".nojekyll").write_text("")
    print("hub built")

if __name__ == "__main__":
    build()
