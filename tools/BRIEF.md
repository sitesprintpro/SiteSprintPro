# SiteSprintPro sample rebuild brief

You are rebuilding ONE sample website for SiteSprintPro, a one-person web design business in Colorado Springs that sells $697 to $1,197 websites to local businesses. The sample is for a FICTIONAL business and lives in the public portfolio. The owner (Don) will pull it up on his phone in front of real business owners and text the link, so it must look like a $5,000 site on a phone first, then on a laptop.

## Read first (required)
1. The design rules: `cat /root/.claude/skills/synced/*/ssp-design/SKILL.md` (follow sections 1 to 5; where this brief is more specific, this brief wins).
2. The content rules: the "Content rules" section of `cat /root/.claude/skills/synced/*/ssp-build/SKILL.md`.
3. Your niche section at the bottom of this file.

## Hard rules
- One HTML file per sample: all CSS and JS inline. Write your source to `/home/claude/ssp-kit/src/<slug>.html` with one `<!--@LIBS@-->` placeholder before your own `<script>`, then build with `python3 /home/claude/ssp-kit/inline.py /home/claude/ssp-kit/src/<slug>.html /home/claude/ssp-site/<slug>/index.html` (inlines GSAP, ScrollTrigger, SplitText, Lenis). Photos are the only separate files, in `/home/claude/ssp-site/<slug>/img/`.
- Fonts: Google Fonts `<link>` is allowed, with a full fallback stack. Banned faces: Inter, Inter Tight, Fraunces, Instrument Serif, Bebas Neue. One family (two only if you can say why). Emphasis is italic or weight of the same family.
- Every link is relative and works from the folder: the SAMPLE BUILD badge links to `../work/index.html`; the footer credit "Sample build by SiteSprintPro" links to `../index.html`. No `href="#"` placeholders anywhere. In-page anchors must resolve.
- Copy: plain, specific, local. Zero em dashes and zero en dashes anywhere on the page (use hyphens or rewrite). No filler verbs (elevate, seamless, unleash, premier, top-notch, world-class, cutting-edge). No invented reviews, ratings, review counts, years in business, job counts, awards or team names. Policies are fine ("Free estimates", "Upfront written pricing", "Licensed and insured" is acceptable on a labeled sample).
- Reviews section: a sample layout clearly labeled "Sample layout. On your site these are your real Google reviews, quoted word for word." Placeholder quotes describe what goes there, they never pretend to be real customers.
- Trust row under the hero with labeled placeholders a real client fills in (e.g. "Your Google rating", "Years in business", "Licensed and insured").
- Keep the SAMPLE BUILD badge, exactly this CSS and HTML (move it to the top-left under the header on phones so it never covers the call bar):
  ```
  .ssp-sample{position:fixed;left:12px;bottom:12px;z-index:9999;display:flex;align-items:center;gap:8px;background:rgba(17,17,17,0.92);color:#fff;font:700 12px/1.3 -apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif;letter-spacing:.02em;padding:9px 13px;border-radius:999px;box-shadow:0 4px 18px rgba(0,0,0,.35);text-decoration:none;max-width:calc(100vw - 24px)}
  .ssp-sample b{background:#7ed957;color:#111;border-radius:999px;padding:2px 8px;font-weight:800}
  <a class="ssp-sample" href="../work/index.html" title="Back to the SiteSprintPro portfolio"><b>SAMPLE BUILD</b><span>Fictional business. Reviews and numbers are placeholders.</span></a>
  ```
- Banned visual tells (from ssp-design): neon glows, gradient-text headlines, custom cursors, section numbers (01, 02), decorative status dots, "scroll" cues, slogan strips, labels laid over photos, three equal feature cards, eyebrow labels on every section (max one per three sections), poetic section names, fake app screenshots, pure #000 or #fff, more than 3 corner-radius values.

## Required structure (adapt order and layout families to the niche, never a generic template)
1. Header: an original SVG wordmark/mark (inline), nav (phones: no hamburger needed if the page is one scroll; if you add one it must work), and a tap-to-call pill. Max 72px tall.
2. Hero photo slider: 3 or 4 real photos crossfading. Each holds about 5.5 s, crossfades over 1.2 s with a slow scale from 1.0 to 1.08 (transform only). Dark gradient overlay for contrast (text must pass 4.5:1). Headline (max 2 lines desktop), at most 20 words of subtext, primary button = Call with the phone number (tel:), secondary = Book or Directions or Menu. Headline and buttons stay FIXED over the slides (never animate out per slide). Use `<picture>` with a portrait crop for phones (`media="(max-width: 700px)"`). The first slide loads eagerly with `fetchpriority="high"`; under `prefers-reduced-motion: reduce` show only the first slide, no zoom. Use `100dvh`-based heights with a sensible max (e.g. `min(92dvh, 860px)`), never bare `100vh`. Pause the slider when the hero is off screen (IntersectionObserver).
3. Trust row (placeholders, labeled).
4. Services: real copy for this trade, 4 to 6 services, in a layout that is NOT three equal cards (e.g. a photo-led split list, an asymmetric grid, a two-column list with one feature photo).
5. One section that only someone local would write (the niche section gives you the hook). This is what makes it feel built for Colorado Springs.
6. How it works or why us: short, specific, plain.
7. Reviews sample layout (labeled).
8. Service area or hours and location, with a Google Maps directions link (see niche for the exact link).
9. Contact: a short quote/booking form with Netlify attributes (`data-netlify="true"`, hidden honeypot field, `name` on every input, phone input `type="tel"`, inputs at least 16px font) whose submit is intercepted in JS for the sample and shows: "Sample form. On your site this sends the lead straight to your phone and email." Plus a big tap-to-call.
10. Footer: business name, phone, area, hours, "Kestrel ... is a fictional business. Sample build by SiteSprintPro." (with your business name), link to ../index.html. Footer links at least 44px tall on phones.
11. Sticky call bar on phones (max-width 760px): Call (primary) plus one secondary action; add bottom padding to the body so it never covers content or the form button; respect `env(safe-area-inset-bottom)`.
12. `var CONFIG = { phone, phoneDisplay, email, ... }` at the bottom of the script, and populate tel links from it.

## Motion (Don asked for premium motion; keep it purposeful)
- GSAP + ScrollTrigger reveals (transform and opacity only, staggered, once), SplitText on the H1 only, Lenis smooth scroll wired as: `lenis.on('scroll', ScrollTrigger.update); gsap.ticker.add(t => lenis.raf(t * 1000)); gsap.ticker.lagSmoothing(0);`
- SplitText masking clips descenders (g, y, p) unless the mask has padding: use `SplitText.create(el, {type:'lines,words', mask:'lines', linesClass:'ln'})` and CSS `.ln-mask{padding-bottom:.14em;margin-bottom:-.14em}`, then animate words `yPercent: 110 -> 0`.
- Never hide content without JS: only the hero headline may be hidden before init, under `html.js:not(.ready)` with a 2.5 s timeout that adds `ready`. Initial states are set by GSAP at runtime.
- Everything static under `prefers-reduced-motion: reduce` (no Lenis, no slider, no reveals).
- Working reference for wiring (not for look; its cursor, numbered sections, scroll cue and status dot are banned): `/home/claude/ssp-work/premium/src/hvac.html`.

## Photos (you source them)
- Source: Pexels only (free commercial use, no attribution required). Find IDs by using WebFetch on `https://www.pexels.com/search/<url-encoded query>/` and asking for the photo page URLs (they end in `-<ID>/`). Download with `curl -sL "https://images.pexels.com/photos/<ID>/pexels-photo-<ID>.jpeg?auto=compress&cs=tinysrgb&w=2400" -o raw/<ID>.jpg` (pexels.com pages themselves block curl; the image CDN does not).
- Rules: no identifiable faces (backs, hands and out-of-focus people are fine), no readable brand names or logos (tool brands, appliance logos, bottle labels), no watermarks or text, no obvious non-US settings (European radiators, foreign signage). Consistent color grade across the set. Look at every candidate yourself (build a contact sheet with PIL and Read it) before choosing.
- Need: 4 hero slides plus 2 to 4 section photos.
- Process with PIL: hero landscape crop 1920x1080 and 960x540, portrait crop 900x1350 for phones; section photos 1400w and 700w. Save WebP quality 72 to 76. Every `<img>` gets width and height attributes and `alt` text. Keep total image weight under 2.5 MB.
- License log: write `/home/claude/ssp-kit/licenses/<slug>.csv` with columns `file,pexels_id,page_url,photographer,license,date` (license = "Pexels License", date = 2026-10-08).

## Name check
Before writing copy, WebSearch "<business name> Colorado Springs". If a real business in Colorado (or a well-known one nationally) uses that exact name, rename to a distinctive fictional name, report it, and keep the folder slug.

## Done means (run all, fix, rerun)
- `python3 /home/claude/ssp-kit/preflight.py /home/claude/ssp-site/<slug>/index.html /home/claude/ssp-kit/qa/<slug>/preflight` prints ALL PASS.
- `python3 /home/claude/ssp-kit/mobile.py /home/claude/ssp-site/<slug>/index.html /home/claude/ssp-kit/qa/<slug>/mobile` prints ALL PASS.
- You have LOOKED at `qa/<slug>/mobile/contact-sheet.png`, `desktop-1440.png`, and the full-page phone shot `iphone-390-full.png`, and fixed anything that looks off: cramped spacing, text over busy photo areas, clipped letters, orphaned words, sections that read as template.
- Write `/home/claude/ssp-kit/design/<slug>.md` (the DESIGN.md: 9 sections per ssp-design, short).
- Final reply (under 150 words): business name (and any rename), fonts and accent, the local section's hook, photo IDs used, preflight and mobile results, total image weight, anything you could not solve.

Do not touch any other sample's folder, the hub files, or anything outside your slug's paths and the shared kit outputs listed above. Do not push to git or publish anything.

---
## Niche sections
