/* GlotChat website: Telegram links with a pre-filled message in the visitor's language, menus,
   language redirect (first visit only), lazy demo videos, demo tabs, plan finder, time-saved
   calculator, sticky contact buttons, exit offer, copy buttons and click tracking.
   Page language + texts come from window.GC (written by src/build.py). */
(function () {
  'use strict';
  var GC = window.GC || { lang: 'en', tg: 'GlotChat', msg: {}, plans: {}, langs: ['en'], alts: {} };
  var lang = GC.lang, vlang = lang === 'zh' ? 'zh' : 'en';
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
      var code = String(prefs[i]).toLowerCase().split('-')[0];
      if (code === 'en') return;
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

  /* -------- videos: load when visible, pause when not -------- */
  function setScene(v, scene) {
    v.dataset.scene = scene;
    var base = '/assets/media/' + scene + '-' + vlang, src = $('source', v);
    v.poster = base + '.webp';
    if (v.dataset.loaded === '1') {
      if (src.getAttribute('src') !== base + '.mp4') { src.setAttribute('src', base + '.mp4'); v.load(); if (v.dataset.visible === '1' && !reduce) v.play().catch(function () {}); }
    } else src.setAttribute('data-src', base + '.mp4');
  }
  function loadVid(v) { if (v.dataset.loaded !== '1') { var s = $('source', v); s.setAttribute('src', s.getAttribute('data-src')); v.dataset.loaded = '1'; v.load(); } }
  if ('IntersectionObserver' in window) {
    var vo = new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        var v = en.target; v.dataset.visible = en.isIntersecting ? '1' : '0';
        if (en.isIntersecting) { loadVid(v); if (!reduce) v.play().catch(function () {}); } else v.pause();
      });
    }, { threshold: 0.25 });
    $$('video.vid').forEach(function (v) { vo.observe(v); });
  }

  /* -------- demo tabs -------- */
  var tabs = $$('.tabs [role="tab"]');
  tabs.forEach(function (t) {
    t.addEventListener('click', function () {
      var k = t.dataset.tab;
      tabs.forEach(function (x) { x.setAttribute('aria-selected', String(x === t)); });
      $$('.pane').forEach(function (p) { p.hidden = p.dataset.pane !== k; });
      var v = $('#demoVid'); if (!v) return;
      loadVid(v); setScene(v, k); v.currentTime = 0;
      if (!reduce) v.play().catch(function () {});
      track('demo_tab', { tab: k });
    });
  });

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
    $$('.card, .steps li, .plan, .vs .col, .shot, .demo, .head, .calc, .tbl-wrap').forEach(function (el) { el.classList.add('rv'); ro.observe(el); });
  }
  $$('.year').forEach(function (y) { y.textContent = new Date().getFullYear(); });
})();
