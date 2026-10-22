/* Text of the demo scenes, per website language.
   The "agent" (the GlotChat user) reads and writes in the page language; customers write in another
   language, so the visitor always sees messages translated INTO their own language.
   GlotChat's own interface exists in English and Chinese only, so app labels are English except on /zh/. */
window.DEMO_TEXTS = (function () {
  const UI_EN = {
    addTitle: 'Add a WhatsApp account',
    addSub: 'It gets its own isolated space in GlotChat. Then scan the QR code with the phone of this WhatsApp number.',
    sbAccounts: 'WhatsApp accounts', sbAll: 'All', sbUnread: 'Unread', sbAdd: 'Add account',
    navAll: 'All accounts', navTpl: 'Templates', navLang: 'Languages', navSet: 'Settings',
    name: 'Name', color: 'Color', iWrite: 'I write in', custSpeak: 'Customers speak', autoDetect: 'Auto-detect',
    iWriteHint: 'Messages are translated into this language for you.', custHint: 'Auto-detect learns each chat’s language.',
    cancel: 'Cancel', create: 'Add & connect WhatsApp', scanQr: 'Scan the QR code with WhatsApp on your phone → Linked devices',
    linkTitle: 'Use WhatsApp on your computer', linkSteps: ['Open WhatsApp on your phone', 'Tap Menu → Linked devices', 'Point your phone at this screen'],
    connected: 'Connected', loading: 'Loading your chats…',
    search: 'Search or start a new chat', type: 'Type a message', online: 'online',
    chipAuto: (n) => 'Auto · ' + n, tpl: '⚡ Templates', mode: '👁 Send: Preview',
    sendIn: (n) => 'Send in ' + n, change: 'Change language', wrote: 'You wrote:',
    hint: 'Enter to send · Esc to edit', edit: 'Edit', orig: 'Send original', send: 'Send ➤', youWrote: '✎ You wrote',
    transcribe: '🎤 Transcribe', transcribing: '🎤 Transcribing…', readText: '🔤 Read text', reading: '🔤 Reading the photo…',
    yesterday: 'Yesterday', photo: '📷 Photo',
    lang: { en: 'English', zh: 'Chinese', ar: 'Arabic', tr: 'Turkish', es: 'Spanish', pt: 'Portuguese', ru: 'Russian', fr: 'French', de: 'German' },
  };
  const UI_ZH = {
    addTitle: '添加 WhatsApp 账号',
    addSub: '账号在 GlotChat 中拥有独立的空间。然后用该 WhatsApp 号码的手机扫描二维码。',
    sbAccounts: 'WhatsApp 账号', sbAll: '所有', sbUnread: '未读', sbAdd: '添加账号',
    navAll: '所有账号', navTpl: '快捷回复', navLang: '语言', navSet: '设置',
    name: '名称', color: '颜色', iWrite: '我使用的语言', custSpeak: '客户使用的语言', autoDetect: '自动检测',
    iWriteHint: '消息会为你翻译成这种语言。', custHint: '自动检测会记住每个聊天的语言。',
    cancel: '取消', create: '添加并连接 WhatsApp', scanQr: '请用手机 WhatsApp 扫描二维码 → 已关联的设备',
    linkTitle: '在电脑上使用 WhatsApp', linkSteps: ['在手机上打开 WhatsApp', '点按 菜单 → 已关联的设备', '将手机对准此屏幕'],
    connected: '已连接', loading: '正在加载聊天…',
    search: '搜索或开始新的聊天', type: '输入消息', online: '在线',
    chipAuto: (n) => '自动 · ' + n, tpl: '⚡ 快捷回复', mode: '👁 发送：预览',
    sendIn: (n) => '以' + n + '发送', change: '更改语言', wrote: '你写的是：',
    hint: 'Enter 发送 · Esc 编辑', edit: '编辑', orig: '发送原文', send: '发送 ➤', youWrote: '✎ 你写的是',
    transcribe: '🎤 转文字', transcribing: '🎤 正在转写…', readText: '🔤 识别文字', reading: '🔤 正在识别图片…',
    yesterday: '昨天', photo: '📷 照片',
    lang: { en: '英语', zh: '中文', ar: '阿拉伯语', tr: '土耳其语', es: '西班牙语', pt: '葡萄牙语', ru: '俄语', fr: '法语', de: '德语' },
  };

  /* ---- chat: a customer asks about a shirt, the agent answers in their own language ---- */
  const CHAT_ES = {
    who: ['María López', 'M', '#db2777'], src: 'es',
    in1: 'Hola, ¿tienen esta camisa en talla L?',
    in2: '¿Cuánto cuesta el envío a Madrid?',
    out: '¡Sí, tenemos la talla L! El envío a Madrid es gratis esta semana.',
    tr: {
      en: ['Hi, do you have this shirt in size L?', 'How much is shipping to Madrid?', 'Yes, we have size L! Shipping to Madrid is free this week.'],
      zh: ['你好，这件衬衫有 L 码吗？', '寄到马德里的运费是多少？', '有 L 码！本周寄到马德里免运费。'],
      ar: ['مرحبًا، هل لديكم هذا القميص بمقاس L؟', 'كم تكلفة الشحن إلى مدريد؟', 'نعم، لدينا مقاس L! الشحن إلى مدريد مجاني هذا الأسبوع.'],
      tr: ['Merhaba, bu gömleğin L bedeni var mı?', 'Madrid’e kargo ne kadar?', 'Evet, L bedeni var! Bu hafta Madrid’e kargo ücretsiz.'],
      pt: ['Olá, vocês têm esta camisa no tamanho L?', 'Quanto custa o frete para Madri?', 'Sim, temos no tamanho L! O frete para Madri é grátis esta semana.'],
      ru: ['Здравствуйте, есть эта рубашка размера L?', 'Сколько стоит доставка в Мадрид?', 'Да, размер L есть! Доставка в Мадрид на этой неделе бесплатная.'],
    },
  };
  const CHAT_FR = {
    who: ['Sophie Martin', 'S', '#15803d'], src: 'fr',
    in1: 'Bonjour, vous avez cette chemise en taille L ?',
    in2: 'Combien coûte la livraison à Paris ?',
    out: 'Oui, nous avons la taille L ! La livraison à Paris est gratuite cette semaine.',
    tr: { es: ['Hola, ¿tienen esta camisa en talla L?', '¿Cuánto cuesta el envío a París?', '¡Sí, tenemos la talla L! El envío a París es gratis esta semana.'] },
  };

  /* ---- voice note ---- */
  const VOICE_TR = {
    who: ['Ahmet Yılmaz', 'A', '#c2410c'], src: 'tr',
    text: 'Merhaba, yarın sabah ofis temizliğine gelebilir misiniz? Fiyat ne kadar?',
    tr: {
      en: 'Hello, can you come tomorrow morning to clean the office? How much is it?',
      zh: '你好，你们明天上午可以来打扫办公室吗？价格是多少？',
      ar: 'مرحبًا، هل يمكنكم القدوم صباح الغد لتنظيف المكتب؟ كم السعر؟',
      es: 'Hola, ¿pueden venir mañana por la mañana a limpiar la oficina? ¿Cuánto cuesta?',
      pt: 'Olá, vocês podem vir amanhã de manhã limpar o escritório? Quanto custa?',
      ru: 'Здравствуйте, можете прийти завтра утром убрать офис? Сколько это стоит?',
    },
  };
  const VOICE_DE = {
    who: ['Lukas Weber', 'L', '#0369a1'], src: 'de',
    text: 'Hallo, können Sie morgen früh zur Büroreinigung kommen? Was kostet das?',
    tr: { tr: 'Merhaba, yarın sabah ofis temizliğine gelebilir misiniz? Fiyatı ne kadar?' },
  };

  /* ---- photo of a German invoice ---- */
  const PHOTO = {
    who: ['Jonas Becker', 'J', '#0f766e'], src: 'de',
    lines: ['Rechnung Nr. 2381', '3 × Hemd Größe L – 75 €', 'Versand nach Berlin – 6 €', 'Gesamt: 81 €'],
    tr: {
      en: ['Invoice No. 2381', '3 × Shirt size L – €75', 'Shipping to Berlin – €6', 'Total: €81'],
      zh: ['发票号 2381', '3 × L 码衬衫 – 75 €', '寄往柏林 – 6 €', '合计：81 €'],
      ar: ['فاتورة رقم 2381', '3 × قميص مقاس L – 75 €', 'الشحن إلى برلين – 6 €', 'المجموع: 81 €'],
      tr: ['Fatura No. 2381', '3 × L beden gömlek – 75 €', 'Berlin’e kargo – 6 €', 'Toplam: 81 €'],
      es: ['Factura n.º 2381', '3 × Camisa talla L – 75 €', 'Envío a Berlín – 6 €', 'Total: 81 €'],
      pt: ['Fatura nº 2381', '3 × Camisa tamanho L – 75 €', 'Frete para Berlim – 6 €', 'Total: 81 €'],
      ru: ['Счёт № 2381', '3 × Рубашка, размер L – 75 €', 'Доставка в Берлин – 6 €', 'Итого: 81 €'],
    },
  };

  /* ---- notifications from three different accounts ---- */
  const N_UAE = { acc: 'Shop UAE', who: ['Fatima Al Zahra', 'F', '#7e22ce'], first: 'Fatima', src: 'ar', text: 'هل الطلب جاهز؟',
    chat: ['مرحبا، هل الطلب جاهز؟', 'سأدفع اليوم'],
    tr: { en: ['Is the order ready?', 'Hello, is the order ready?', 'I’ll pay today'],
          zh: ['订单准备好了吗？', '你好，订单准备好了吗？', '我今天付款'],
          tr: ['Sipariş hazır mı?', 'Merhaba, sipariş hazır mı?', 'Bugün ödeyeceğim'],
          es: ['¿El pedido está listo?', 'Hola, ¿el pedido está listo?', 'Hoy pago'],
          pt: ['O pedido está pronto?', 'Olá, o pedido está pronto?', 'Vou pagar hoje'],
          ru: ['Заказ готов?', 'Здравствуйте, заказ готов?', 'Оплачу сегодня'] } };
  const N_UAE_RU = { acc: 'Shop UAE', who: ['Ivan Petrov', 'I', '#7e22ce'], first: 'Ivan', src: 'ru', text: 'Заказ готов?',
    chat: ['Здравствуйте, заказ готов?', 'Оплачу сегодня'],
    tr: { ar: ['هل الطلب جاهز؟', 'مرحبًا، هل الطلب جاهز؟', 'سأدفع اليوم'] } };
  const N_SUP = { acc: 'Support', first: 'Ahmet', src: 'tr', text: 'Yarın gelebilir misiniz?',
    tr: { en: ['Can you come tomorrow?'], zh: ['你们明天能来吗？'], ar: ['هل يمكنكم القدوم غدًا؟'], es: ['¿Pueden venir mañana?'],
          pt: ['Vocês podem vir amanhã?'], ru: ['Можете прийти завтра?'] } };
  const N_SUP_DE = { acc: 'Support', first: 'Lukas', src: 'de', text: 'Können Sie morgen kommen?', tr: { tr: ['Yarın gelebilir misiniz?'] } };
  const N_EXP = { acc: 'Export', first: 'Wang Lei', src: 'zh', text: '好的，明天发货',
    tr: { en: ['OK, it ships tomorrow'], ar: ['حسنًا، سيتم الشحن غدًا'], tr: ['Tamam, yarın kargoya verilecek'], es: ['Vale, se envía mañana'],
          pt: ['Ok, será enviado amanhã'], ru: ['Хорошо, отправим завтра'] } };
  const N_EXP_ES = { acc: 'Export', first: 'Carlos', src: 'es', text: 'Perfecto, se envía mañana', tr: { zh: ['好的，明天发货'] } };

  /* chat-list rows behind the scenes (other customers, kept in their own language) */
  const ROWS = [
    ['Ahmet Yılmaz', 'A', '#c2410c', 'Merhaba, fiyat ne kadar?', '10:41', '2'],
    ['Lukas Weber', 'L', '#0369a1', 'Danke! Bis morgen.', '10:12', ''],
    ['Fatima Al Zahra', 'F', '#7e22ce', 'شكرا جزيلا', '09:58', '1'],
    ['Wang Lei', 'W', '#be123c', '好的，明天发货', '09:30', ''],
    ['Sophie Martin', 'S', '#15803d', 'Merci beaucoup !', '*', ''],
    ['João Silva', 'J', '#a16207', 'Obrigado!', '*', ''],
  ];

  return function (lang) {
    const ui = lang === 'zh' ? UI_ZH : UI_EN;
    const pick = (a, b) => (a.src === lang ? b : a);
    const chat = pick(CHAT_ES, CHAT_FR), voice = pick(VOICE_TR, VOICE_DE);
    return {
      lang, ui, rtl: lang === 'ar', my: ui.lang[lang], code: lang.toUpperCase(),
      chat, chatTr: chat.tr[lang], voice, voiceTr: voice.tr[lang], photo: PHOTO, photoTr: PHOTO.tr[lang],
      notes: [pick(N_UAE, N_UAE_RU), pick(N_SUP, N_SUP_DE), pick(N_EXP, N_EXP_ES)],
      rows: ROWS.map((r) => r.map((c) => (c === '*' ? ui.yesterday : c))),
    };
  };
})();
