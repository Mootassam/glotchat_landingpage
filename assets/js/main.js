/* GlotChat landing: language (EN / 中文), Telegram links with a ready-made message, demo tabs,
   lazy videos, sticky contact buttons, scroll reveal and click tracking. */
(function () {
  'use strict';
  var TG_USER = 'GlotChat';

  /* -------- Telegram messages (pre-filled, so visitors don't have to think what to write) -------- */
  var MSG = {
    en: {
      general: "Hi! I'm interested in GlotChat (many WhatsApp accounts + translation). Can you tell me more?",
      demo: 'Hi! Can I see a live demo of GlotChat?',
      trial: "Hi! I'd like the free 3-day GlotChat trial. I use about __ WhatsApp accounts.",
      usecase: "Hi! I'd like to try GlotChat free for 3 days. My business: __ · My customers speak: __",
      finder: "Hi! I use {n} WhatsApp accounts. I'd like to try GlotChat {plan} free for 3 days.",
      planTrial: "Hi! I'd like to try the GlotChat {plan} plan free for 3 days first.",
      plan: "Hi! I want the GlotChat {plan} plan ({price} USDT / year). How can I pay?",
      custom: "Hi! I need a custom GlotChat offer: __ computers, __ WhatsApp accounts (lifetime license?)."
    },
    zh: {
      general: '你好！我对 GlotChat（WhatsApp 多开 + 翻译）感兴趣，可以介绍一下吗？',
      demo: '你好！可以给我演示一下 GlotChat 吗？',
      trial: '你好！我想免费试用 GlotChat 3 天。我大约有 __ 个 WhatsApp 账号。',
      usecase: '你好！我想免费试用 GlotChat 3 天。我的行业：__ · 我的客户说：__',
      finder: '你好！我有 {n} 个 WhatsApp 账号，想先免费试用 GlotChat {plan} 3 天。',
      planTrial: '你好！我想先免费试用 GlotChat {plan} 3 天。',
      plan: '你好！我想购买 GlotChat {plan}（{price} USDT / 年），怎么付款？',
      custom: '你好！我需要 GlotChat 定制方案：__ 台电脑，__ 个 WhatsApp 账号（是否有终身授权？）。'
    }
  };
  var PLAN_ZH = { Starter: '入门版', Pro: '专业版', Business: '企业版' };

  /* -------- 中文 (English is written in the HTML) -------- */
  var ZH = {
    nav_demo: '演示', nav_features: '功能', nav_who: '适用行业', nav_pricing: '价格', nav_faq: '常见问题', cta_nav: '联系我们',
    promo: '<b>免费试用 3 天</b> — 全部功能，无需付款。', promo_go: '在 Telegram 领取 →',
    eyebrow: '为跨境卖家和客服团队打造',
    h1: '所有 WhatsApp 账号，一个窗口搞定。<span class="grad">每位客户，都用他的语言沟通。</span>',
    lead: 'GlotChat 让多个 WhatsApp 账号同时运行，每个账号完全隔离、通知独立；文字、语音和图片都能在你的电脑上即时翻译。',
    cta_hero: '免费试用 3 天', cta_demo: '观看演示',
    micro1: '3 天免费 · 无需付款', micro2: 'Telegram 快速回复', micro3: '低至 69 USDT / 年',
    float1: '即时翻译', float2: '个账号同屏运行',
    fact1: '个 WhatsApp 账号同时运行', fact2: '种翻译语言', fact3: '离线运行，不上传云端', fact4: '语音和图片翻译',
    demo_k: '实际演示', demo_h: '任何语言，都能看懂、能回复', demo_p: 'GlotChat 真实功能录屏，选择一个：',
    t_chat: '聊天翻译', t_voice: '语音消息', t_photo: '图片和文件', t_accounts: '多账号',
    p_chat_h: '双向聊天翻译',
    p_chat_1: '每条客户消息的译文都显示在原文下方。',
    p_chat_2: '用你自己的语言输入，发送前 GlotChat 会先显示译文。',
    p_chat_3: '客户收到地道的西班牙语、阿拉伯语、土耳其语……你保留自己写的原文。',
    p_voice_h: '语音秒变文字',
    p_voice_1: '在任意语音消息下点击 🎤 转文字。',
    p_voice_2: '立即看到客户说了什么，以及译文。',
    p_voice_3: '离线处理，音频不会离开你的电脑。',
    p_photo_h: '图片中的文字，直接翻译',
    p_photo_1: '订单、发票、价目表、截图——点击 🔤 识别文字。',
    p_photo_2: '支持拉丁文、阿拉伯文、西里尔文、中文、韩文、泰文等。',
    p_photo_3: '客户不会收到任何提示。',
    p_acc_h: '多账号，绝不混乱',
    p_acc_1: '每个账号都有独立的会话，登录永不混淆。',
    p_acc_2: '通知会显示属于哪个账号，点一下就打开对应聊天。',
    p_acc_3: 'Ctrl+K 一秒找到任意账号，切换瞬间完成。',
    cta_live: '预约在线演示',
    feat_k: '功能齐全', feat_h: '专为跨境销售和客服打造',
    f1_h: '多账号，一个窗口', f1_p: '每个号码一个标签页，已实测 27 个账号同时运行。',
    f2_h: '完全隔离', f2_p: '每个账号拥有独立的登录、Cookie 和存储，互不干扰、不会泄露。',
    f3_h: '按账号区分通知', f3_p: '“Shop UAE · Fatima”——你总能知道消息发到了哪个账号。',
    f4_h: '双向翻译', f4_p: '49 种语言。收到的消息自动翻译，发出的消息发送前可预览。',
    f5_h: '语音 → 文字', f5_p: '可转写并翻译约 100 种语言的语音消息。',
    f6_h: '图片 → 文字', f6_p: '识别并翻译图片、发票和截图中的文字。',
    f7_h: '快捷回复模板', f7_p: '自动带入客户名字的常用回复，并像你写的内容一样被翻译。',
    f8_h: '隐私 · 离线', f8_p: '翻译在你的电脑上运行，消息绝不会发送给谷歌、DeepL 或任何 AI 服务。',
    f9_h: '中英文界面', f9_p: '一键切换 GlotChat 的中文或英文界面。',
    who_k: '适用行业', who_h: '专为客户说其他语言的企业打造', who_p: '如果你用多个号码在 WhatsApp 上服务不同国家的客户，GlotChat 每天为你节省数小时。',
    u1_h: '外贸和批发商', u1_p: '用阿拉伯语、西班牙语、俄语或葡萄牙语给买家报价、谈判和跟进——你只需用中文输入。',
    u2_h: '房产中介', u2_p: '外国买家发来语音和证件照片，立即看懂，任何号码上的客户都不会漏掉。',
    u3_h: '诊所和医疗旅游', u3_p: '每位顾问的号码都在一个窗口里。患者用他们的语言咨询，团队用他们的语言回复。',
    u4_h: '旅游和旅行社', u4_p: '来自世界各地游客的预订、改期和咨询——一台电脑全部搞定。',
    u5_h: '电商和分销商', u5_p: '每个店铺或国家一个号码，快捷回复模板，订单和收据照片一键翻译。',
    u6_h: '客服和销售团队', u6_p: '客服用中文或英文工作，每位客户都收到他自己语言的回复。',
    cta_who: '告诉我们你的行业，免费试用',
    in_k: '软件内部', in_h: '全天候稳定运行',
    in_1: '<b>自动修复：</b>某个账号卡死或崩溃会自动重启，其他账号照常工作。',
    in_2: '<b>智能启动：</b>账号分批加载，电脑始终流畅。',
    in_3: '<b>内存监控：</b>查看每个账号的占用，让不常用的账号休眠。',
    in_4: '<b>真实的 WhatsApp 网页版：</b>GlotChat 绝不会自行发送任何内容，一切由你掌控。',
    in_cap: '账号切换器（Ctrl+K）：每个账号的状态、内存和未读消息一目了然。',
    zh_k: '中文 / English', zh_h: '团队可以用中文或英文使用',
    zh_p: 'GlotChat 的每个菜单、按钮和提示都有中英文两种版本；回复翻译同样支持中文——中文客服可以直接用西班牙语、阿拉伯语、德语或土耳其语服务客户。',
    zh_cap: '中文界面：客服用中文输入，客户收到的是西班牙语。',
    how_k: '先试用，再付款', how_h: '免费试用 3 天，10 分钟即可上手',
    s1_h: '在 Telegram 联系我们', s1_p: '告诉我们你有多少个 WhatsApp 账号。我们发给你安装程序，并解答所有问题。',
    s2_h: '领取免费试用密钥', s2_p: '安装 GlotChat，把软件显示的机器码发给我们，即可收到解锁全部功能的 3 天密钥。',
    s3_h: '满意？继续使用', s3_p: '用 USDT 付款，获取一年密钥。账号和设置保持不变，无需重新设置。',
    cta_steps: '在 Telegram 领取免费试用',
    why_k: '为什么选择 GlotChat', why_h: '不再来回复制粘贴到翻译器',
    bad_h: '没有 GlotChat', bad_1: '每个号码都要一部手机或一个浏览器配置', bad_2: '每条消息都要复制 → 粘贴 → 翻译 → 再粘贴回去',
    bad_3: '听不懂的语音消息', bad_4: '“另一个”账号上的消息常被漏掉', bad_5: '客户聊天内容被粘贴到在线翻译网站',
    good_h: '使用 GlotChat', good_1: '所有号码在一个窗口，一键切换', good_2: '每条消息下方自动显示译文',
    good_3: '语音消息转成你的语言的文字', good_4: '每条通知都标明属于哪个账号', good_5: '全部在你自己的电脑上离线翻译',
    pr_k: '价格', pr_h: '简单的年度套餐，先免费试用', pr_p: '每个套餐都包含全部功能和所有更新。先免费试用 3 天——满意再付款。',
    fd_q: '你使用多少个 WhatsApp 账号？', fd_a: '最适合你：', fd_btn: '免费试用 3 天', for_you: '为你推荐',
    per_year: '/ 年', about: '约', per_month: 'USDT / 月', pl_upd: '包含所有更新',
    try: '或先免费试用 3 天', buy2: '在 Telegram 购买', buy3: '在 Telegram 购买',
    custom: '<b>需要更多电脑、团队部署或终身授权？</b>告诉我们你的需求，我们为你定制报价。', custom_btn: '获取定制报价',
    pl1_n: '入门版', pl1_w: '适合个人卖家', pl2_n: '专业版', pl2_w: '适合成长中的店铺和团队', pl3_n: '企业版', pl3_w: '适合代理商和大型团队',
    pl1_1: '最多 <b>5</b> 个 WhatsApp 账号', pl2_1: '最多 <b>15</b> 个 WhatsApp 账号', pl3_1: '<b>不限</b> WhatsApp 账号数量',
    pl_all: '文字、语音和图片翻译', pl_tpl: '快捷回复 · 中英文界面',
    pl1_pc: '1 台电脑', pl2_pc: '1 台电脑 · 协助安装', pl3_pc: '最多 3 台电脑 · 优先支持',
    popular: '最受欢迎', buy: '在 Telegram 购买',
    paynote: '支持 USDT 付款（TRC20 · BEP20 · ERC20）。购买前有疑问？直接问我们——Telegram 上回复。',
    faq_k: '常见问题', faq_h: '你可能想知道',
    q9: '可以免费试用吗？', a9: '可以。在 Telegram 联系我们，即可获得解锁全部功能的 3 天试用密钥，无需付款。满意后购买套餐，所有账号和设置都会保留。',
    q10: '一年到期后怎么办？', a10: '按相同价格续费即可继续使用，不会中断。你的账号、聊天和设置都保存在你的电脑上。',
    q11: '以后可以升级吗？', a11: '可以。增加 WhatsApp 号码时联系我们，我们为你升级密钥——只需补差价。',
    q1: '会影响我的 WhatsApp 账号安全吗？', a1: 'GlotChat 为每个账号打开官方 WhatsApp 网页版，并放在各自独立的会话中——和浏览器一样，只是更有条理。它绝不会自行发送消息，所有内容都由你发送。',
    q2: '翻译需要联网吗？', a2: '不需要。翻译、语音转写和图片识别都在你的电脑上运行。语言包只需下载一次（英语已内置）。当然，WhatsApp 本身需要联网。',
    q3: '需要什么配置的电脑？', a3: 'Windows 10 或 11（64 位）。每个 WhatsApp 账号约占用 300–450 MB 内存：8 GB 内存约可运行 10 个账号，20–30 个账号建议 16 GB 或以上。',
    q4: '支持哪些语言？', a4: '49 种翻译语言，包括英语、中文、西班牙语、阿拉伯语、法语、德语、葡萄牙语、俄语、土耳其语、印地语、日语、韩语和越南语。语音消息可识别约 100 种语言。',
    q5: '如何付款和获取软件？', a5: '在 Telegram 联系我们，选择套餐并用 USDT（TRC20、BEP20 或 ERC20）付款。你会收到安装程序和授权密钥，如有需要我们会协助安装。',
    q6: '每个账号都需要扫码吗？', a6: '是的，每个账号扫一次——在对应手机的 WhatsApp → 已关联的设备 中扫码。之后账号会保持登录，重启电脑也不影响。',
    q7: '支持 Mac 或手机吗？', a7: 'GlotChat 是 Windows 桌面软件。你的手机照常使用——GlotChat 和 WhatsApp 网页版一样，是一个已关联的设备。',
    q8: '我的中文团队能用吗？', a8: '可以。整个界面都有中文版，客服用中文阅读和输入，客户收到的是他们自己的语言。',
    fin_h: '免费试用 GlotChat 3 天', fin_p: '在 Telegram 联系我们——我们发给你安装程序和免费试用密钥，解答问题并帮助你快速上手。',
    copy: '复制用户名', qr: '在电脑上浏览？用手机相机扫码即可打开 Telegram。',
    legal: 'WhatsApp 是 WhatsApp LLC 的商标。GlotChat 是独立产品，与 WhatsApp 或 Meta 无关联。',
    fab: '免费试用 · 联系我们', mbar: '免费试用 3 天 — 在 Telegram 联系我们', copied: '已复制 @GlotChat',
    lv_h: '先别走——免费试用一下', lv_p: '获取解锁全部功能的 GlotChat 3 天试用。无需付款、没有任何承诺——发条消息就行。', lv_btn: '在 Telegram 领取免费试用', lv_no: '不用了，谢谢'
  };
  var EN = {};                                  // filled from the HTML on first switch
  var lang = 'en';

  /* The language is the page: / = English, /zh/ = 中文 (static HTML, good for search engines).
     First-time visitors with a Chinese browser are sent to /zh/ once; a choice made with the
     EN / 中文 switch is remembered. ?lang=zh|en still works (used by the build script). */
  var PRERENDER = /[?&]prerender=1/.test(location.search);
  var ON_ZH = /^\/zh(\/|$)/.test(location.pathname);
  function saved() { try { return localStorage.getItem('gc-lang'); } catch (e) { return null; } }
  function pickLang() {
    var q = new URLSearchParams(location.search).get('lang');
    if (q === 'zh' || q === 'en') return q;
    if (ON_ZH) return 'zh';
    var s = saved();
    if (!PRERENDER && s !== 'en' && (s === 'zh' || /^zh/i.test(navigator.language || ''))) {
      location.replace('/zh/' + location.hash);
      return 'zh';
    }
    return 'en';
  }
  function setLang(l) {
    lang = l;
    document.documentElement.lang = l === 'zh' ? 'zh-CN' : 'en';
    document.querySelectorAll('[data-i18n]').forEach(function (el) {
      var k = el.getAttribute('data-i18n');
      if (!(k in EN)) EN[k] = el.textContent;
      el.textContent = l === 'zh' && ZH[k] ? ZH[k] : EN[k];
    });
    document.querySelectorAll('[data-i18n-html]').forEach(function (el) {
      var k = el.getAttribute('data-i18n-html');
      if (!(k in EN)) EN[k] = el.innerHTML;
      el.innerHTML = l === 'zh' && ZH[k] ? ZH[k] : EN[k];
    });
    document.querySelectorAll('.lang a').forEach(function (b) { if (b.dataset.lang === l) b.setAttribute('aria-current', 'page'); else b.removeAttribute('aria-current'); });
    links();
    swapVideos();
  }

  /* -------- Telegram links -------- */
  function links() {
    document.querySelectorAll('[data-tg]').forEach(function (a) {
      var kind = a.getAttribute('data-tg');
      var text = (MSG[lang][kind] || MSG[lang].general);
      var plan = a.getAttribute('data-plan'), price = a.getAttribute('data-price');
      if (plan) text = text.replace('{plan}', lang === 'zh' ? (PLAN_ZH[plan] || plan) : plan).replace('{price}', price || '');
      text = text.replace('{n}', a.getAttribute('data-n') || '');
      a.href = 'https://t.me/' + TG_USER + '?text=' + encodeURIComponent(text);
    });
  }
  function track(name, data) {
    try { if (window.va) window.va('event', { name: name, data: data }); } catch (e) { /* analytics optional */ }
  }
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('[data-tg]');
    if (a) track('telegram_click', { place: a.getAttribute('data-place') || '', plan: a.getAttribute('data-plan') || '', lang: lang });
  });

  /* -------- videos: load when visible, pause when not, language-specific -------- */
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function setScene(v, scene) {
    v.dataset.scene = scene;
    var base = '/assets/media/' + scene + '-' + lang;
    v.poster = base + '.webp';
    var src = v.querySelector('source');
    var want = base + '.mp4';
    if (v.dataset.loaded === '1') {
      if (src.getAttribute('src') !== want) { src.setAttribute('src', want); v.load(); if (v.dataset.visible === '1' && !reduce) v.play().catch(function () {}); }
    } else src.setAttribute('data-src', want);
  }
  function swapVideos() { document.querySelectorAll('video.vid').forEach(function (v) { setScene(v, v.dataset.scene); }); }
  if ('IntersectionObserver' in window) {
    var vo = new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        var v = en.target;
        v.dataset.visible = en.isIntersecting ? '1' : '0';
        if (en.isIntersecting) {
          if (v.dataset.loaded !== '1') {
            var s = v.querySelector('source'); s.setAttribute('src', s.getAttribute('data-src')); v.dataset.loaded = '1'; v.load();
          }
          if (!reduce) v.play().catch(function () {});
        } else v.pause();
      });
    }, { threshold: 0.25 });
    document.querySelectorAll('video.vid').forEach(function (v) { vo.observe(v); });
  }

  /* -------- demo tabs -------- */
  var tabs = document.querySelectorAll('.tabs [role="tab"]');
  tabs.forEach(function (t) {
    t.addEventListener('click', function () {
      var k = t.dataset.tab;
      tabs.forEach(function (x) { x.setAttribute('aria-selected', String(x === t)); });
      document.querySelectorAll('.pane').forEach(function (p) { p.hidden = p.dataset.pane !== k; });
      var v = document.getElementById('demoVid');
      if (v.dataset.loaded !== '1') { var s = v.querySelector('source'); s.setAttribute('src', s.getAttribute('data-src')); v.dataset.loaded = '1'; }
      setScene(v, k);
      v.currentTime = 0;
      if (!reduce) v.play().catch(function () {});
      track('demo_tab', { tab: k });
    });
  });

  /* -------- sticky contact: show after the hero, hide over the final contact block -------- */
  var fab = document.querySelector('.fab'), mbar = document.querySelector('.mbar');
  var hero = document.querySelector('.hero'), fin = document.querySelector('.final');
  var heroOut = false, finIn = false;
  function stick() { var on = heroOut && !finIn; fab.classList.toggle('show', on); mbar.classList.toggle('show', on); }
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (es) { heroOut = !es[0].isIntersecting; stick(); }, { threshold: 0.05 }).observe(hero);
    new IntersectionObserver(function (es) { finIn = es[0].isIntersecting; stick(); }, { threshold: 0.2 }).observe(fin);
  }

  /* -------- plan finder: highlight the right plan, pre-fill the trial message -------- */
  var chips = document.querySelectorAll('.chips [role="radio"]');
  chips.forEach(function (c) {
    c.addEventListener('click', function () {
      chips.forEach(function (x) { x.setAttribute('aria-checked', String(x === c)); });
      var plan = c.dataset.plan, btn = document.getElementById('finderBtn');
      btn.setAttribute('data-plan', plan); btn.setAttribute('data-n', c.dataset.n);
      var name = document.querySelector('[data-plan-card="' + plan + '"] h3');
      document.getElementById('finderPlan').textContent = name ? name.textContent : plan;
      document.getElementById('finderA').hidden = false;
      document.querySelectorAll('[data-plan-card]').forEach(function (p) { p.classList.toggle('pick', p.dataset.planCard === plan); });
      links();
      track('plan_finder', { accounts: c.dataset.n, plan: plan });
    });
  });

  /* -------- leaving without contacting? offer the free trial once (desktop, mouse leaves the top) -------- */
  var leave = document.getElementById('leave'), contacted = false, start = Date.now();
  function seen() { try { return sessionStorage.getItem('gc-leave') === '1'; } catch (e) { return false; } }
  function closeLeave() { leave.hidden = true; }
  document.addEventListener('click', function (e) { if (e.target.closest && e.target.closest('[data-tg]')) { contacted = true; closeLeave(); } });
  if (!PRERENDER && window.matchMedia && window.matchMedia('(pointer: fine)').matches) {
    document.addEventListener('mouseout', function (e) {
      if (e.relatedTarget || e.clientY > 8 || contacted || seen() || Date.now() - start < 8000) return;
      try { sessionStorage.setItem('gc-leave', '1'); } catch (er) { /* ignore */ }
      leave.hidden = false;
      track('exit_popup', {});
    });
  }
  leave.addEventListener('click', function (e) { if (e.target === leave || (e.target.closest && e.target.closest('[data-close]'))) closeLeave(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeLeave(); });

  /* -------- copy username -------- */
  var toast = document.getElementById('toast');
  document.getElementById('copyTg').addEventListener('click', function () {
    var done = function () { toast.textContent = lang === 'zh' ? ZH.copied : 'Copied @GlotChat'; toast.classList.add('show'); setTimeout(function () { toast.classList.remove('show'); }, 1800); };
    if (navigator.clipboard) navigator.clipboard.writeText('@' + TG_USER).then(done, done); else done();
    track('copy_username', {});
  });

  /* -------- reveal on scroll -------- */
  if ('IntersectionObserver' in window && !reduce && !PRERENDER) {
    var ro = new IntersectionObserver(function (es) { es.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); ro.unobserve(en.target); } }); }, { threshold: 0.12 });
    document.querySelectorAll('.card, .steps li, .plan, .vs .col, .shot, .demo, .head').forEach(function (el) { el.classList.add('rv'); ro.observe(el); });
  }

  document.querySelectorAll('.lang a').forEach(function (b) {
    b.addEventListener('click', function () { try { localStorage.setItem('gc-lang', b.dataset.lang); } catch (e) { /* ignore */ } track('language', { lang: b.dataset.lang }); });
  });
  document.getElementById('year').textContent = new Date().getFullYear();
  setLang(pickLang());
})();
