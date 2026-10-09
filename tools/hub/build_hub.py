"""Build the SiteSprintPro hub pages into /home/claude/ssp-site.

Every page is one self-contained HTML file (CSS and JS inline). Links are relative so the site works on
GitHub Pages (project path), on sitesprintpro.com, and in a local preview.
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
    "domain": "https://sitesprintpro.com/",
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
}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
body{font-family:var(--font);background:var(--bg);color:var(--text);font-size:17px;line-height:1.55;-webkit-font-smoothing:antialiased;overflow-x:clip}
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
@media (max-width:900px){.nav{display:none}}
@media (max-width:420px){.call-pill .num{display:none}}

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
.hero::before{content:'';position:absolute;inset:-20% -10% auto auto;width:70vw;height:70vw;max-width:900px;max-height:900px;background:radial-gradient(closest-side,rgba(226,98,42,.16),transparent 70%);pointer-events:none}
.hero .wrap{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,.8fr);gap:clamp(32px,5vw,72px);align-items:center;position:relative}
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
.card-body .niche{font-size:.82rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--accent2)}
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

/* steps */
.steps{list-style:none;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:0;border-top:1px solid var(--line)}
.steps li{padding:28px 28px 8px 0;position:relative}
.steps li+li{padding-left:28px;border-left:1px solid var(--line)}
.steps h3{margin-bottom:10px}
.steps p{color:var(--muted)}
.steps .when{display:block;margin-top:14px;font-size:.88rem;font-weight:700;color:var(--accent2)}
@media (max-width:860px){.steps{grid-template-columns:minmax(0,1fr)}.steps li,.steps li+li{padding:24px 0;border-left:0;border-bottom:1px solid var(--line)}}

/* pricing */
.prices{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);gap:20px}
.price{border:1px solid var(--line);border-radius:var(--r2);padding:28px;background:var(--bg2)}
.price.main{grid-row:span 2;border-color:rgba(226,98,42,.55);background:linear-gradient(180deg,rgba(226,98,42,.10),rgba(226,98,42,0) 55%),var(--bg2)}
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
.founder.solo{grid-template-columns:minmax(0,1fr);max-width:820px}
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
.band{border-top:1px solid var(--line);border-bottom:1px solid var(--line);background:linear-gradient(120deg,rgba(226,98,42,.14),rgba(226,98,42,0) 60%),var(--bg2)}
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

def page(path, title, desc, body, active="", head_extra="", script_extra=""):
    depth = path.count("/")
    root = "../" * depth
    nav = [("work", "Work"), ("pricing", "Pricing"), ("about", "About"), ("faq", "FAQ"), ("start", "Get started")]
    nav_html = "".join(
        f'<li><a href="{root}{k}/index.html"{" aria-current=\"page\"" if active == k else ""}>{v}</a></li>' for k, v in nav)
    canonical = CONFIG["domain"] + (path.replace("index.html", "") if path != "index.html" else "")
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
<script>document.documentElement.className+=' js';</script>
<style>{CSS}</style>
{head_extra}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="hdr"><div class="wrap">
  <a class="brand" href="{root}index.html" aria-label="SiteSprintPro home">{LOGO}<span>SiteSprint<b>Pro</b></span></a>
  <nav aria-label="Main"><ul class="nav">{nav_html}</ul></nav>
  <a class="call-pill" href="tel:{CONFIG['phone']}">{ICON['phone']}<span class="num">{CONFIG['phoneDisplay']}</span><span class="sr-only" style="position:absolute;left:-9999px">Call</span></a>
</div></header>
<main id="main">
{body.replace('{root}', root)}
</main>
<footer class="foot"><div class="wrap">
  <div>
    <a class="brand" href="{root}index.html">{LOGO}<span>SiteSprint<b>Pro</b></span></a>
    <p style="margin-top:12px;max-width:30em">Websites for Colorado Springs businesses. Built by one person, live in 2 to 3 days, yours to keep.</p>
  </div>
  <div><h4>Site</h4><ul>
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
<script>
(function(){{
  var io = 'IntersectionObserver' in window ? new IntersectionObserver(function(es){{ es.forEach(function(e){{ if(e.isIntersecting){{ e.target.classList.add('in'); io.unobserve(e.target); }} }}); }}, {{rootMargin:'0px 0px -8% 0px'}}) : null;
  document.querySelectorAll('[data-r]').forEach(function(el){{ io ? io.observe(el) : el.classList.add('in'); }});
  setTimeout(function(){{ document.querySelectorAll('[data-r]').forEach(function(el){{ if(el.getBoundingClientRect().top < innerHeight) el.classList.add('in'); }}); }}, 60);
}})();
{script_extra}
</script>
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
    ("Do I own the website?", ["Yes. Once the balance is paid, the site, the files and the domain are yours. If you ever want to leave, you take everything with you."]),
    ("Are there monthly fees?", ["No. The only recurring cost is your domain name, about $12 a year, paid to the registrar. A care plan is optional: $100 a quarter if you want me to handle changes."]),
    ("How fast is it?", ["Standard sites go live 2 to 3 days after the deposit and your info. Pro builds get priority, usually 1 to 2 days."]),
    ("What do you need from me?", ["Your services, hours, service area, your logo if you have one, and 10 to 20 photos from your phone of real work, your crew or your space. I write all the words."]),
    ("I already have a website. Can you fix it?", ["Often, yes. A refresh of an existing site is $300 to $400 when the bones are good. If it's cheaper to rebuild, I'll tell you."]),
    ("Will it help me show up on Google?", ["I connect the site to your Google Business Profile and set it up with the business details Google reads. Where you rank depends on your profile, your reviews and your competition, so nobody can honestly promise first place."]),
    ("Can you use my Google reviews?", ["Yes, your real reviews, quoted word for word with the reviewer's first name. Never made-up ones."]),
    ("Where do the photos come from?", ["Your own photos first. When a section needs more, I license stock photos for your business so you're covered. Never random images pulled off the internet."]),
    ("How do I pay?", ["Half to start and half when you approve the finished site, by invoice. You see it working before you pay the second half."]),
]

def faq_html(items):
    return '<div class="faq">' + "".join(
        f'<details data-r><summary>{esc(q)}</summary><div class="ans">{"".join("<p>" + esc(p) + "</p>" for p in a)}</div></details>' for q, a in items) + "</div>"

FEATURES = [
    ("Tap to call on every page", "Your number is one tap from anywhere on the site, with a call bar that stays on screen on phones."),
    ("Built for phones first", "Most people find you on a phone. Every site is checked on four phone sizes before you see it."),
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
    feats = "".join(f'<li data-r>{ICON["check"]}<div><b>{esc(a)}</b><span>{esc(b)}</span></div></li>' for a, b in FEATURES)
    ld = {"@context": "https://schema.org", "@type": "ProfessionalService", "name": "SiteSprintPro",
          "description": "Websites for Colorado Springs small businesses.", "url": CONFIG["domain"],
          "telephone": CONFIG["phone"], "email": CONFIG["email"],
          "areaServed": {"@type": "City", "name": "Colorado Springs, Colorado"}, "priceRange": "$697 to $1,197"}
    home = f"""
<section class="hero"><div class="wrap">
  <div>
    <span class="eyebrow load">Colorado Springs web design</span>
    <h1 class="load d1">Websites for Springs businesses.</h1>
    <p class="lede load d2">Live in 2 to 3 days. One flat price, no monthly fees, and the site is yours.</p>
    <div class="btns load d3">{tel_btn()}<a class="btn btn-line" href="work/index.html">See the work {ICON['arrow']}</a></div>
    <p class="small-note load d4">Or text the same number. I answer it myself.</p>
  </div>
  <div class="stage load d2" aria-label="Sample sites, cycling">
    <div class="desk">{stage_imgs}</div>
    <div class="phone">{stage_phone}</div>
    <div class="stage-cap" aria-live="polite"><span id="capNiche">{s[0]['niche']} sample</span><b id="capName">{esc(s[0]['name'])}</b><a id="capLink" href="{s[0]['slug']}/index.html">Open it {ICON['arrow']}</a></div>
  </div>
</div></section>

<section id="work" style="padding-top:0"><div class="wrap">
  <div class="sec-head"><h2 data-r>Find the one closest to your business.</h2><p class="lede" data-r>Six sample sites, all live. Open one on your phone, that's how your customers will see yours.</p></div>
  <div class="work">{card(s[0],'w7')}{card(s[1],'w5')}{card(s[2],'w5')}{card(s[3],'w7')}{card(s[4])}{card(s[5])}</div>
  <p class="sample-note">Every sample is a fictional business, built to show what yours would look like. Reviews and numbers on them are placeholders.</p>
</div></section>

<section style="padding-top:0"><div class="wrap">
  <div class="sec-head"><h2 data-r>How it works</h2><p class="lede" data-r>Three steps, and you deal with one person the whole way.</p></div>
  <ol class="steps">
    <li data-r><h3>Call, text, or send the form.</h3><p>Tell me what you do and where. I send back the sample closest to your business and a flat quote.</p><span class="when">Same day</span></li>
    <li data-r><h3>Half down, and I build it.</h3><p>Your services, hours, real Google reviews and photos. You check it on your phone and tell me what to change.</p><span class="when">2 to 3 days</span></li>
    <li data-r><h3>It goes live on your domain.</h3><p>Tap to call everywhere, a form that reaches your inbox, connected to your Google profile. Then it's yours.</p><span class="when">You own it</span></li>
  </ol>
</div></section>

<section style="padding-top:0"><div class="wrap">
  <div class="sec-head"><h2 data-r>One price. No monthly.</h2><p class="lede" data-r>Half to start, half when you approve it. All the writing is included.</p></div>
  <div class="prices">
    <div class="price main" data-r><span class="tag">Most picked</span><h3>Standard</h3><div class="amt">$897</div><ul><li>Up to 5 pages, live in 2 to 3 days</li><li>All the writing done for you</li><li>Tap to call, quote form, Google-ready setup</li><li>2 rounds of changes, plus 2 free updates after launch</li></ul><a class="btn btn-hot" href="start/index.html">Get started</a></div>
    <div class="price" data-r><h3>Pro</h3><div class="amt">$1,197</div><ul><li>Up to 8 pages, priority 1 to 2 days</li><li>Gallery, booking link, reviews section</li><li>4 rounds of changes</li></ul></div>
    <div class="price" data-r><h3>Facebook-only businesses</h3><div class="amt">$697</div><ul><li>For businesses whose only page today is Facebook or Instagram</li></ul></div>
    <div class="price-extra"><span><b>$300 to $400</b> to refresh a site you already have</span><span><b>$100 a quarter</b> optional care plan</span><span><b>About $12 a year</b> for your domain</span><a href="pricing/index.html" style="display:inline-flex;align-items:center;gap:6px;min-height:44px;color:var(--accent2);font-weight:700;text-decoration:none">Full pricing {ICON['arrow']}</a></div>
  </div>
</div></section>

<section style="padding-top:0"><div class="wrap">
  <div class="sec-head"><h2 data-r>In every site</h2><p class="lede" data-r>The parts that turn a visit into a phone call.</p></div>
  <ul class="feat">{feats}</ul>
</div></section>

<section style="padding-top:0"><div class="wrap founder{"" if CONFIG["ownerPhoto"] else " solo"}">
  <div class="portrait" data-r{"" if CONFIG["ownerPhoto"] else " hidden"}>
    {('<img src="' + CONFIG['ownerPhoto'] + '" alt="' + CONFIG['owner'] + ', who builds every SiteSprintPro site" width="800" height="1000" loading="lazy" decoding="async">') if CONFIG['ownerPhoto'] else ''}
    <svg class="art" viewBox="0 0 400 500" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a3038"/><stop offset="1" stop-color="#16191d"/></linearGradient></defs><rect width="400" height="500" fill="url(#sky)"/><path d="M0 380 L70 330 L120 350 L190 250 L230 285 L270 215 L320 290 L400 250 L400 500 L0 500Z" fill="#1d2126"/><path d="M190 250 L230 285 L270 215 L320 290" fill="none" stroke="#e2622a" stroke-width="3" stroke-linejoin="round"/></svg>
  </div>
  <div>
    <span class="eyebrow" data-r>Who builds it</span>
    <h2 data-r>You call me. I build it.</h2>
    <blockquote data-r>No call center, no sales team, no outsourcing. The person who answers is the person who builds your site.</blockquote>
    <p data-r>I live in Colorado Springs and build every site myself. Most businesses here run on referrals and a Google listing, and when that listing has no website, the call goes to whoever looks more legit. I build the site that makes you the obvious call.</p>
    <p class="sig" data-r>{CONFIG['owner']}, SiteSprintPro</p>
    <div class="btns" style="margin-top:22px" data-r>{tel_btn()}<a class="btn btn-line" href="about/index.html">More about me</a></div>
  </div>
</div></section>

<section style="padding-top:0"><div class="wrap">
  <div class="sec-head"><h2 data-r>Questions owners ask</h2><p class="lede" data-r><a href="faq/index.html" style="display:inline-flex;align-items:center;gap:6px;min-height:44px;color:var(--accent2);font-weight:700;text-decoration:none">All questions {ICON['arrow']}</a></p></div>
  {faq_html(FAQS[:5])}
</div></section>

<section class="band"><div class="wrap">
  <div><h2 data-r>Want to see yours?</h2><p class="lede" data-r style="margin-top:14px">Call or text, or send the one-minute form. I'll send the closest sample and a flat price the same day.</p></div>
  <div data-r><a class="big-tel" href="tel:{CONFIG['phone']}">{CONFIG['phoneDisplay']}</a><div class="btns" style="margin-top:14px"><a class="btn btn-hot" href="start/index.html">Get started</a><a class="btn btn-line" href="sms:{CONFIG['phone']}">{ICON['chat']}Text me</a></div></div>
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
    cs.forEach(function(c){ c.style.display = (f === 'all' || c.getAttribute('data-group') === f) ? '' : 'none'; });
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
    <div class="price"><h3>Facebook-only businesses</h3><div class="amt">$697</div><ul><li>For businesses whose only page today is Facebook or Instagram</li><li>Up to 3 pages, built from what's already on your page</li></ul></div>
  </div>
</div></section>
<section style="padding-top:0" id="care"><div class="wrap">
  <h2 style="margin-bottom:12px">Everything it can cost</h2>
  <table class="cost-table">
    <thead><tr><th scope="col">What</th><th scope="col">Price</th><th scope="col">Notes</th></tr></thead>
    <tbody>
      <tr><td>Standard site</td><td class="n">$897</td><td class="s">One time</td></tr>
      <tr><td>Pro site</td><td class="n">$1,197</td><td class="s">One time</td></tr>
      <tr><td>Facebook-only business</td><td class="n">$697</td><td class="s">One time</td></tr>
      <tr><td>Refresh of a site you have</td><td class="n">$300 to $400</td><td class="s">When the existing site is worth keeping</td></tr>
      <tr><td>Care plan</td><td class="n">$100 a quarter</td><td class="s">Optional. Text me changes (hours, prices, photos, a new service) and I make them. Cancel anytime.</td></tr>
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
  <div><h2>Questions about price?</h2><p class="lede" style="margin-top:14px">Call or text and you'll get a straight answer.</p></div>
  <div><div class="btns">{tel_btn()}<a class="btn btn-line" href="../start/index.html">Get started</a></div></div>
</div></section>
"""
    page("pricing/index.html", "Pricing | SiteSprintPro",
         "Flat prices: $897 standard, $1,197 pro, $697 for Facebook-only businesses. No monthly fees.", pricing, active="pricing")

    # ABOUT
    about = f"""
<section class="phead"><div class="wrap">
  <h1 class="load">One person. Your whole site.</h1>
  <p class="lede load d1">SiteSprintPro is me, {CONFIG['owner']}. I live in Colorado Springs and I build every site myself.</p>
</div></section>
<section style="padding-top:0"><div class="wrap founder{"" if CONFIG["ownerPhoto"] else " solo"}">
  <div class="portrait"{"" if CONFIG["ownerPhoto"] else " hidden"}>
    {('<img src="../' + CONFIG['ownerPhoto'] + '" alt="' + CONFIG['owner'] + ' outdoors near Colorado Springs" width="800" height="1000" loading="lazy" decoding="async">') if CONFIG['ownerPhoto'] else ''}
    <svg class="art" viewBox="0 0 400 500" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><rect width="400" height="500" fill="#20252b"/><path d="M0 380 L70 330 L120 350 L190 250 L230 285 L270 215 L320 290 L400 250 L400 500 L0 500Z" fill="#1a1d22"/><path d="M190 250 L230 285 L270 215 L320 290" fill="none" stroke="#e2622a" stroke-width="3" stroke-linejoin="round"/></svg>
  </div>
  <div class="prose">
    <h2 style="margin-top:0">Why I do this</h2>
    <p>Most small businesses here run on referrals and a Google listing. When a homeowner's furnace quits at 10pm, they search, they look at the first few listings on their phone, and they call whoever looks legit. A listing with no website loses that call more often than it should.</p>
    <p>I build the website that wins it: your number one tap away, your real reviews, your work, and nothing that makes a customer hesitate.</p>
    <h2>How I work</h2>
    <ul><li>You deal with me from the first call to launch day.</li><li>Flat prices, written down before anything starts.</li><li>No monthly packages. You own what you pay for.</li><li>I test every site on four phone sizes before you see it.</li></ul>
    <div class="btns" style="margin-top:26px">{tel_btn()}<a class="btn btn-line" href="../work/index.html">See the work</a></div>
  </div>
</div></section>
"""
    page("about/index.html", "About | SiteSprintPro",
         "SiteSprintPro is one person in Colorado Springs building websites for local businesses.", about, active="about")

    # FAQ
    faq = f"""
<section class="phead"><div class="wrap"><h1 class="load">Questions</h1><p class="lede load d1">Straight answers. If yours isn't here, call or text.</p></div></section>
<section style="padding-top:0"><div class="wrap">{faq_html(FAQS)}</div></section>
<section class="band"><div class="wrap">
  <div><h2>Still wondering?</h2><p class="lede" style="margin-top:14px">Ask me directly. I answer my own phone.</p></div>
  <div><div class="btns">{tel_btn()}<a class="btn btn-line" href="../start/index.html">Get started</a></div></div>
</div></section>
"""
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": " ".join(a)}} for q, a in FAQS]}
    page("faq/index.html", "FAQ | SiteSprintPro", "Ownership, pricing, timing and what you need to get a SiteSprintPro website.",
         faq, active="faq", head_extra=f'<script type="application/ld+json">{json.dumps(faq_ld)}</script>')

    # START
    kinds = ["HVAC", "Plumbing", "Contractor or remodel", "Lawn and landscaping", "Salon, barber or spa", "Restaurant or food", "Other"]
    sources = ["Facebook group", "SiteSprintPro Facebook Page", "Someone told me", "Google", "Other"]
    start = f"""
<section class="phead"><div class="wrap"><h1 class="load">Get started</h1><p class="lede load d1">Takes a minute. I'll get back to you the same day with the closest sample and a flat price.</p></div></section>
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
    <div class="fld"><label for="f-src">Where did you find me? <span class="hint">(optional)</span></label><select id="f-src" name="source"><option value="">Choose one</option>{''.join(f'<option>{esc(k)}</option>' for k in sources)}</select></div>
    <div class="hp" aria-hidden="true"><label>Company<input name="company" tabindex="-1" autocomplete="off"></label></div>
    <button class="btn btn-hot" type="submit">Send it</button>
    <p class="form-msg" id="msg" role="status"></p>
    <p class="privacy-line">Used only to contact you about your website. Never sold or shared. <a href="../privacy/index.html" style="display:inline-flex;align-items:center;min-height:44px">Privacy</a></p>
  </form>
  <aside class="side-card">
    <h2 style="font-size:1.5rem">Rather talk?</h2>
    <p style="color:var(--muted)">Call or text. I answer it myself.</p>
    <a class="big-tel" href="tel:{CONFIG['phone']}">{CONFIG['phoneDisplay']}</a>
    <div class="btns">{tel_btn()}<a class="btn btn-line" href="sms:{CONFIG['phone']}">{ICON['chat']}Text me</a></div>
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
        f.reset(); msg.textContent = 'Got it. I will reach out today. If it is urgent, call or text ' + {json.dumps(CONFIG['phoneDisplay'])} + '.';
      }}).catch(function(){{ fallback(data); }});
    }} else {{ fallback(data); }}
  }});
  function fallback(d){{
    var text = 'New website request: ' + d.name + ', ' + d.business + ' (' + d.kind + '), ' + d.phone + '. Site: ' + d.site + (d.link ? ' ' + d.link : '') + '. Reach by ' + d.reach + (d.email ? ' ' + d.email : '') + '.';
    msg.innerHTML = 'Tap to send this to me: <a href="sms:' + PHONE + '?&body=' + encodeURIComponent(text) + '">by text</a> or <a href="mailto:' + EMAIL + '?subject=Website%20request&body=' + encodeURIComponent(text) + '">by email</a>.';
  }}
}})();
"""
    page("start/index.html", "Get started | SiteSprintPro",
         "Tell me about your business and get the closest sample site and a flat price the same day.", start, active="start", script_extra=start_js)

    # PRIVACY
    privacy = f"""
<section class="phead"><div class="wrap"><h1 class="load">Privacy</h1><p class="lede load d1">Short version: what you send me is used to contact you about a website, and nothing else.</p></div></section>
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
