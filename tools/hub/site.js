/* SiteSprintPro hub motion layer. Loaded after assets/vendor.js (GSAP, ScrollTrigger, Lenis).
   Everything here is decoration: the pages read and work without it. Page transitions and the phone menu
   live inline in each page so they never wait on this file. */
(function () {
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = matchMedia('(pointer: fine)').matches;
  var G = window.gsap, ST = window.ScrollTrigger;
  if (G && ST) G.registerPlugin(ST);

  /* Smooth wheel scrolling on desktop only. Touch keeps native scrolling. */
  if (G && ST && window.Lenis && fine && !reduce) {
    var lenis = new Lenis({ lerp: 0.12, wheelMultiplier: 1 });
    lenis.on('scroll', ST.update);
    G.ticker.add(function (t) { lenis.raf(t * 1000); });
    G.ticker.lagSmoothing(0);
    window.__lenis = lenis;
  }

  /* Hero: topographic contour field that bends toward the pointer. One WebGL pass, paused offscreen. */
  var cv = document.querySelector('.topo');
  if (cv && fine && matchMedia('(min-width: 901px)').matches) topo(cv); else if (cv) cv.remove();
  function topo(canvas) {
    var gl = canvas.getContext('webgl', { alpha: true, antialias: false, premultipliedAlpha: true });
    if (!gl || !gl.getExtension('OES_standard_derivatives')) { canvas.remove(); return; }
    var vs = 'attribute vec2 p;void main(){gl_Position=vec4(p,0.,1.);}';
    var fs = '#extension GL_OES_standard_derivatives : enable\nprecision highp float;uniform vec2 r;uniform float t;uniform vec2 m;uniform float k;' +
      'float h(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}' +
      'float n(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(h(i),h(i+vec2(1.,0.)),f.x),mix(h(i+vec2(0.,1.)),h(i+vec2(1.,1.)),f.x),f.y);}' +
      'float fbm(vec2 p){float v=0.,a=.5;for(int i=0;i<5;i++){v+=a*n(p);p=p*2.03+vec2(1.7,9.2);a*=.5;}return v;}' +
      'void main(){vec2 uv=gl_FragCoord.xy/r.y;vec2 mm=m*vec2(r.x/r.y,1.);float d=distance(uv,mm);' +
      'float e=fbm(uv*1.35+vec2(t*.018,-t*.011))+.42*exp(-d*d*5.)*k;float lv=e*16.;' +
      'float g=abs(fract(lv)-.5)/fwidth(lv);float line=1.-min(g,1.);float major=1.-step(.5,abs(mod(floor(lv),5.)));' +
      'float hot=exp(-d*d*3.2)*k;vec3 base=vec3(.93,.92,.89);vec3 acc=vec3(.94,.48,.27);' +
      'vec3 col=mix(base,acc,clamp(hot*1.3+major*.15,0.,1.));float a=line*(.10+major*.09+hot*.38);' +
      'float fx=smoothstep(.0,.55,gl_FragCoord.x/r.x);float fy=smoothstep(0.,.25,gl_FragCoord.y/r.y);' +
      'float o=a*fx*fy;gl_FragColor=vec4(col*o,o);}';
    function sh(type, src) { var s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s); return gl.getShaderParameter(s, gl.COMPILE_STATUS) ? s : null; }
    var v = sh(gl.VERTEX_SHADER, vs), f = sh(gl.FRAGMENT_SHADER, fs);
    if (!v || !f) { canvas.remove(); return; }
    var pr = gl.createProgram(); gl.attachShader(pr, v); gl.attachShader(pr, f); gl.linkProgram(pr); gl.useProgram(pr);
    var buf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buf);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, -1, 1, 1, -1, 1, 1]), gl.STATIC_DRAW);
    var loc = gl.getAttribLocation(pr, 'p'); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
    var uR = gl.getUniformLocation(pr, 'r'), uT = gl.getUniformLocation(pr, 't'), uM = gl.getUniformLocation(pr, 'm'), uK = gl.getUniformLocation(pr, 'k');
    var host = canvas.parentElement, mx = .72, my = .55, tx = mx, ty = my, kk = fine ? 1 : .6, t0 = performance.now(), on = true, raf = 0, last = 0;
    function size() {
      var s = Math.min(devicePixelRatio || 1, 1.5) * (fine ? .8 : .6);
      canvas.width = Math.max(2, Math.round(canvas.clientWidth * s)); canvas.height = Math.max(2, Math.round(canvas.clientHeight * s));
      gl.viewport(0, 0, canvas.width, canvas.height);
    }
    size(); addEventListener('resize', size);
    if (fine) host.addEventListener('pointermove', function (e) {
      var b = canvas.getBoundingClientRect(); tx = (e.clientX - b.left) / b.width; ty = 1 - (e.clientY - b.top) / b.height;
    });
    function frame(now) {
      raf = 0;
      if (!on || document.hidden) return;
      if (now - last < 33) { raf = requestAnimationFrame(frame); return; }
      last = now;
      var t = (now - t0) / 1000;
      if (!fine) { tx = .62 + Math.cos(t * .23) * .18; ty = .5 + Math.sin(t * .19) * .2; }
      mx += (tx - mx) * .06; my += (ty - my) * .06;
      gl.uniform2f(uR, canvas.width, canvas.height); gl.uniform1f(uT, reduce ? 0 : t); gl.uniform2f(uM, mx, my); gl.uniform1f(uK, kk);
      gl.clearColor(0, 0, 0, 0); gl.clear(gl.COLOR_BUFFER_BIT); gl.drawArrays(gl.TRIANGLES, 0, 6);
      if (!reduce) raf = requestAnimationFrame(frame);
    }
    function start() { if (!raf) raf = requestAnimationFrame(frame); }
    if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { on = es[0].isIntersecting; if (on) start(); }).observe(canvas);
    document.addEventListener('visibilitychange', start);
    canvas.classList.add('on'); start();
  }

  /* Hero stage: slight 3D tilt toward the pointer on desktop. */
  var stage = document.querySelector('.stage');
  if (stage && fine && !reduce) {
    var hero = stage.closest('.hero');
    hero.addEventListener('pointermove', function (e) {
      var b = hero.getBoundingClientRect(), x = (e.clientX - b.left) / b.width - .5, y = (e.clientY - b.top) / b.height - .5;
      stage.style.transform = 'perspective(1400px) rotateY(' + (x * 7).toFixed(2) + 'deg) rotateX(' + (-y * 5).toFixed(2) + 'deg)';
    });
    hero.addEventListener('pointerleave', function () { stage.style.transform = ''; });
  }

  /* Magnetic primary buttons on desktop. */
  if (fine && !reduce) document.querySelectorAll('.btn-hot, .call-pill').forEach(function (b) {
    b.addEventListener('pointermove', function (e) {
      var r = b.getBoundingClientRect(), x = e.clientX - r.left - r.width / 2, y = e.clientY - r.top - r.height / 2;
      b.style.transform = 'translate(' + (x * .18).toFixed(1) + 'px,' + (y * .3).toFixed(1) + 'px)';
    });
    b.addEventListener('pointerleave', function () { b.style.transform = ''; });
  });

  if (!G || !ST) return;

  /* Built under the Peak: the photo settles as it scrolls in, and first light rises behind the summit. */
  var ridge = document.querySelector('.ridge');
  if (ridge && !reduce) {
    var glow = ridge.querySelector('.r-glow'), media = ridge.querySelector('.ridge-media');
    G.set(glow, { opacity: 0 });
    G.fromTo(media, { scale: 1.16 }, { scale: 1, ease: 'none', scrollTrigger: { trigger: ridge, start: 'top bottom', end: 'bottom bottom', scrub: true } });
    G.to(glow, { opacity: 1, ease: 'none', scrollTrigger: { trigger: ridge, start: 'top 70%', end: 'center 40%', scrub: true } });
    var h2 = ridge.querySelector('h2');
    if (h2) {
      h2.innerHTML = h2.textContent.split(' ').map(function (w) { return '<span class="w"><span>' + w + '</span></span>'; }).join(' ');
      G.from(h2.querySelectorAll('.w > span'), { yPercent: 110, duration: 1.1, ease: 'expo.out', stagger: .08, scrollTrigger: { trigger: ridge, start: 'top 45%' } });
    }
  }

  /* Footer horizon drifts a little slower than the page. */
  document.querySelectorAll('.horizon img').forEach(function (img) {
    if (reduce) return;
    G.fromTo(img, { yPercent: -10 }, { yPercent: 0, ease: 'none', scrollTrigger: { trigger: img.closest('.horizon'), start: 'top bottom', end: 'bottom bottom', scrub: true } });
  });

  /* The phone reel: a real sample scrolls inside the phone as you scroll the list. */
  var reel = document.querySelector('.reel');
  if (reel) {
    var tall = reel.querySelector('.tall'), items = reel.querySelectorAll('.reel-list li'), phone = reel.querySelector('.reel-phone');
    reel.classList.add('live');
    var desk = matchMedia('(min-width: 861px)').matches;
    var run = function () {
      var shift = function () { return -(tall.offsetHeight - phone.querySelector('.reel-screen').offsetHeight); };
      G.to(tall, { y: shift, ease: 'none', scrollTrigger: { trigger: desk ? reel : phone, start: desk ? 'top 20%' : 'top 85%', end: desk ? 'bottom 80%' : 'bottom 15%', scrub: .6, invalidateOnRefresh: true } });
    };
    if (tall.complete && tall.naturalHeight) run(); else tall.addEventListener('load', function () { run(); ST.refresh(); });
    items.forEach(function (li) {
      ST.create({ trigger: li, start: 'top 62%', end: 'bottom 38%', toggleClass: { targets: li, className: 'on' } });
    });
  }

  /* About: the production line fills in as you read it. */
  var pipe = document.querySelector('.pipe');
  if (pipe && !reduce) G.fromTo(pipe, { '--fill': 0 }, { '--fill': 1, ease: 'none', scrollTrigger: { trigger: pipe, start: 'top 75%', end: 'bottom 55%', scrub: true } });

  addEventListener('load', function () { ST.refresh(); });
})();
