/* GlotChat website: Telegram links with a pre-filled message in the visitor's language, menus,
   language redirect (first visit only), demo player + lazy demo clips, plan finder, time-saved
   calculator, sticky contact buttons, exit offer, copy buttons and click tracking.
   Page language + texts come from window.GC (written by src/build.py). */
(function () {
  'use strict';
  var GC = window.GC || { lang: 'en', tg: 'GlotChat', msg: {}, plans: {}, langs: ['en'], alts: {} };
  var lang = GC.lang, vlang = GC.vlang || lang;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var contacted = false;
  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } return null; }
  function track(name, data) { try { if (window.va) window.va('event', { name: name, data: data }); } catch (e) { /* optional */ } }

  /* -------- first visit: send people to their language (once; a manual choice always wins) -------- */
  (function () {
    if (lang !== GC['default'] || store('gc-lang') || /[?&]nolang/.test(location.search)) return;
    var prefs = (navigator.languages && navigator.languages.length ? navigator.languages : [navigator.language || '']);
    for (var i = 0; i < prefs.length; i++) {
      var tag = String(prefs[i]).toLowerCase(), code = tag.split('-')[0];
      if (code === 'en') return;
      if (/^zh-(tw|hk|mo|hant)/.test(tag)) code = 'zh-hant';        // Taiwan / Hong Kong / Macau read 繁體
      if (GC.alts && GC.alts[code]) { store('gc-lang', code); location.replace(GC.alts[code] + location.hash); return; }
    }
  })();
  $$('[data-lang]').forEach(function (a) { a.addEventListener('click', function () { store('gc-lang', a.getAttribute('data-lang')); track('language', { lang: a.getAttribute('data-lang') }); }); });

  /* -------- Telegram links -------- */
  function links() {
    $$('[data-tg]').forEach(function (a) {
      var kind = a.getAttribute('data-tg');
      var text = GC.msg[kind] || GC.msg.general || '';
      var plan = a.getAttribute('data-plan'), price = a.getAttribute('data-price');
      if (plan) text = text.replace('{plan}', GC.plans[plan] || plan).replace('{price}', price || '');
      text = text.replace('{n}', a.getAttribute('data-n') || '');
      a.href = 'https://t.me/' + GC.tg + (text ? '?text=' + encodeURIComponent(text) : '');
    });
  }
  links();

  /* -------- header menus -------- */
  var dds = $$('.dd');
  function closeDd(except) { dds.forEach(function (d) { if (d !== except) { d.classList.remove('open'); var b = $('.dd-b', d); if (b) b.setAttribute('aria-expanded', 'false'); } }); }
  dds.forEach(function (d) {
    var b = $('.dd-b', d);
    b.addEventListener('click', function (e) { e.stopPropagation(); var on = !d.classList.contains('open'); closeDd(d); d.classList.toggle('open', on); b.setAttribute('aria-expanded', String(on)); });
    if (window.matchMedia && window.matchMedia('(hover: hover)').matches && !d.classList.contains('lang-dd')) {
      var t;
      d.addEventListener('mouseenter', function () { clearTimeout(t); closeDd(d); d.classList.add('open'); b.setAttribute('aria-expanded', 'true'); });
      d.addEventListener('mouseleave', function () { t = setTimeout(function () { d.classList.remove('open'); b.setAttribute('aria-expanded', 'false'); }, 180); });
    }
  });
  document.addEventListener('click', function (e) { if (!(e.target.closest && e.target.closest('.dd'))) closeDd(); });
  var burger = $('.burger'), mnav = $('#mnav');
  if (burger && mnav) burger.addEventListener('click', function () { var on = mnav.hidden; mnav.hidden = !on; burger.setAttribute('aria-expanded', String(on)); });

  /* -------- demo clips: the phone or desktop version, loaded when visible, paused when not -------- */
  var PORT = window.matchMedia ? window.matchMedia('(max-width: 700px)') : null;
  function fmt() { return PORT && PORT.matches ? 'port' : 'land'; }
  function srcOf(scene) { return '/assets/media/' + scene + '-' + vlang + '-' + fmt() + '.mp4'; }
  function setSrc(v, scene) { var s = srcOf(scene); if (v.getAttribute('src') !== s) { v.classList.remove('on'); v.src = s; } }
  function play(v) { var p = v.play(); if (p && p.catch) p.catch(function () {}); }
  var clips = $$('video.vid');
  clips.forEach(function (v) { v.addEventListener('playing', function () { v.classList.add('on'); }); });
  if ('IntersectionObserver' in window) {
    var vo = new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        var v = en.target; v.dataset.visible = en.isIntersecting ? '1' : '';
        if (en.isIntersecting) { setSrc(v, v.dataset.scene); if (!reduce) play(v); } else v.pause();
      });
    }, { threshold: 0.3 });
    clips.forEach(function (v) { vo.observe(v); });
  }
  clips.forEach(function (v) { v.parentNode.addEventListener('click', function () { setSrc(v, v.dataset.scene); if (v.paused) play(v); else v.pause(); }); });

  /* -------- hero demo player: 5 chapters in a row, progress per chapter, full-screen view -------- */
  var pl = $('.player');
  if (pl) (function () {
    var tabs = $$('[data-ch]', pl), vids = $$('video.pv', pl), cap = $('.cap', pl);
    var cur = 0, k = 0, started = false, full = false, shown = '';
    function show(v) { vids.forEach(function (x) { x.classList.toggle('on', x === v); }); }
    vids.forEach(function (v) {
      v.addEventListener('playing', function () { if (v === vids[k]) show(v); });
      v.addEventListener('ended', function () { if (v === vids[k]) go(cur + 1); });
    });
    function go(i, user) {
      cur = (i + tabs.length) % tabs.length;
      var prev = vids[k], next = vids[1 - k];
      k = 1 - k;
      var s = srcOf(tabs[cur].dataset.ch); shown = fmt();
      if (next.getAttribute('src') !== s) next.src = s;   // keeps showing the old picture until the new one plays
      try { next.currentTime = 0; } catch (e) { /* not loaded yet */ }
      prev.pause();
      tabs.forEach(function (t, j) {
        t.setAttribute('aria-selected', String(j === cur));
        var bar = $('.bar i', t); if (bar) bar.style.width = j < cur ? '100%' : '0';
      });
      if (cap) cap.textContent = tabs[cur].dataset.cap;
      var strip = tabs[cur].parentNode;                          // keep the current chapter in view on phones
      if (strip.scrollWidth > strip.clientWidth) {
        var x = tabs[cur].offsetLeft - strip.offsetLeft - 16;
        if (getComputedStyle(strip).direction === 'rtl') x = tabs[cur].offsetLeft + tabs[cur].offsetWidth - strip.offsetLeft + 16 - strip.scrollWidth;
        strip.scrollTo({ left: x, behavior: reduce ? 'auto' : 'smooth' });
      }
      if (!reduce || user) play(next);
      // get the following chapter ready in the hidden video once the cross-fade is over
      setTimeout(function () {
        if (vids[1 - k] !== prev) return;
        var n = srcOf(tabs[(cur + 1) % tabs.length].dataset.ch);
        if (prev.getAttribute('src') !== n) { prev.preload = 'auto'; prev.src = n; }
      }, 900);
      if (user) track('demo_chapter', { ch: tabs[cur].dataset.ch });
    }
    (function tick() {
      var v = vids[k], bar = $('.bar i', tabs[cur]);
      if (bar && v.duration && started) bar.style.width = Math.min(100, v.currentTime / v.duration * 100) + '%';
      requestAnimationFrame(tick);
    })();
    tabs.forEach(function (t, j) { t.addEventListener('click', function () { started = true; go(j, true); }); });
    function setFull(on) {
      full = on; pl.classList.toggle('full', on); document.body.classList.toggle('noscroll', on);
      if (on) { play(vids[k]); track('demo_fullscreen', {}); }
    }
    $$('[data-expand]', pl).forEach(function (b) { b.addEventListener('click', function (e) { e.stopPropagation(); setFull(!full); }); });
    $('.screen', pl).addEventListener('click', function () { if (!full) { if (!started) { started = true; go(0, true); } setFull(true); } });
    pl.addEventListener('click', function (e) { if (full && e.target === pl) setFull(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && full) setFull(false); });
    $$('[data-watch]').forEach(function (a) {
      a.addEventListener('click', function (e) { e.preventDefault(); started = true; go(0, true); setFull(true); });
    });
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) {
        var on = es[0].isIntersecting;
        if (on && !started && !reduce) { started = true; go(0); }
        else if (on && started && !reduce) play(vids[k]);
        else if (!on && !full) vids[k].pause();
      }, { threshold: 0.25 }).observe($('.screen', pl));
    }
    // phone <-> computer layout (rotation, resizing): restart the chapter in the other format
    if (PORT && PORT.addEventListener) PORT.addEventListener('change', function () { if (started && fmt() !== shown) go(cur, true); });
  })();
  if (PORT && PORT.addEventListener) PORT.addEventListener('change', function () { clips.forEach(function (v) { if (v.dataset.visible) { setSrc(v, v.dataset.scene); play(v); } }); });

  /* -------- sticky contact: after the hero, hidden over the final contact block -------- */
  var fab = $('.fab'), mbar = $('.mbar'), hero = $('.hero') || $('.phero'), fin = $('.final');
  var heroOut = false, finIn = false;
  function stick() { var on = heroOut && !finIn; if (fab) fab.classList.toggle('show', on); if (mbar) mbar.classList.toggle('show', on); }
  if ('IntersectionObserver' in window && hero) {
    new IntersectionObserver(function (es) { heroOut = !es[0].isIntersecting; stick(); }, { threshold: 0.05 }).observe(hero);
    if (fin) new IntersectionObserver(function (es) { finIn = es[0].isIntersecting; stick(); }, { threshold: 0.2 }).observe(fin);
  }

  /* -------- plan finder -------- */
  var chips = $$('.chips [role="radio"]');
  chips.forEach(function (c) {
    c.addEventListener('click', function () {
      chips.forEach(function (x) { x.setAttribute('aria-checked', String(x === c)); });
      var plan = c.dataset.plan, btn = $('#finderBtn');
      btn.setAttribute('data-plan', plan); btn.setAttribute('data-n', c.dataset.n);
      $('#finderPlan').textContent = GC.plans[plan] || plan;
      $('#finderA').hidden = false;
      $$('[data-plan-card]').forEach(function (p) { p.classList.toggle('pick', p.dataset.planCard === plan); });
      links();
      track('plan_finder', { accounts: c.dataset.n, plan: plan });
    });
  });

  /* -------- time-saved calculator -------- */
  $$('[data-calc]').forEach(function (box) {
    var loc = document.documentElement.lang;
    function get(k) { return +$('[data-c="' + k + '"]', box).value; }
    function out(k, v) { $$('[data-o="' + k + '"]', box).forEach(function (o) { o.textContent = v; }); }
    function calc() {
      var msgs = get('msgs'), secs = get('secs'), people = get('people');
      out('msgs', msgs); out('secs', secs); out('people', people);
      var hours = msgs * secs * people * 22 / 3600;          // 22 working days a month
      out('hours', Math.round(hours).toLocaleString(loc));
      out('days', (hours / 8).toLocaleString(loc, { maximumFractionDigits: 1 }));
    }
    $$('input', box).forEach(function (i) {
      i.addEventListener('input', calc);
      i.addEventListener('change', function () { track('calculator', { msgs: get('msgs'), people: get('people') }); });
    });
    calc();
  });

  /* -------- leaving without contacting? one gentle offer (desktop) -------- */
  var leave = $('#leave'), start = Date.now();
  function closeLeave() { if (leave) leave.hidden = true; }
  if (leave && window.matchMedia && window.matchMedia('(pointer: fine)').matches) {
    document.addEventListener('mouseout', function (e) {
      if (e.relatedTarget || e.clientY > 8 || contacted || Date.now() - start < 12000) return;
      try { if (sessionStorage.getItem('gc-leave') === '1') return; sessionStorage.setItem('gc-leave', '1'); } catch (er) { /* ignore */ }
      leave.hidden = false; track('exit_popup', {});
    });
    leave.addEventListener('click', function (e) { if (e.target === leave || (e.target.closest && e.target.closest('[data-close]'))) closeLeave(); });
  }
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('[data-tg]');
    if (a) { contacted = true; closeLeave(); track('telegram_click', { place: a.getAttribute('data-place') || '', plan: a.getAttribute('data-plan') || '', lang: lang }); }
  });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { closeLeave(); closeDd(); } });

  /* -------- copy buttons -------- */
  var toast = $('#toast');
  $$('[data-copy]').forEach(function (b) {
    b.addEventListener('click', function (e) {
      e.preventDefault();
      var txt = b.getAttribute('data-copy');
      // "send the link to my PC": the phone's share sheet (WhatsApp, WeChat, mail…) when there is one
      if (b.hasAttribute('data-share') && navigator.share) {
        navigator.share({ title: document.title, url: b.getAttribute('data-share') }).catch(function () {});
        track('share', { place: b.getAttribute('data-place') || '' });
        return;
      }
      var done = function () {
        if (!toast) return;
        toast.textContent = (GC.copied || 'Copied') + ' ' + txt; toast.classList.add('show');
        setTimeout(function () { toast.classList.remove('show'); }, 1800);
      };
      if (navigator.clipboard) navigator.clipboard.writeText(txt).then(done, done); else done();
      track('copy', { what: txt });
    });
  });

  /* -------- reveal on scroll -------- */
  if ('IntersectionObserver' in window && !reduce) {
    var ro = new IntersectionObserver(function (es) { es.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); ro.unobserve(en.target); } }); }, { threshold: 0.1 });
    $$('.card, .steps li, .plan, .vs .col, .shot, .srow, .head, .calc, .tbl-wrap, .extras').forEach(function (el) { el.classList.add('rv'); ro.observe(el); });
  }
  $$('.year').forEach(function (y) { y.textContent = new Date().getFullYear(); });
})();
