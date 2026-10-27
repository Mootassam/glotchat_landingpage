/* Text of the demo scenes, per website language.
   The "agent" (the GlotChat user) reads and writes in the page language; customers write in another
   language, so the visitor always sees messages translated INTO their own language.
   GlotChat's own interface exists in English and Chinese only, so app labels are English except on /zh/. */
window.DEMO_TEXTS = (function () {
  const UI_EN = {
    addTitle: 'Add a WhatsApp account',
    addSub: 'It gets its own isolated space in GlotChat. Then scan the QR code with the phone of this WhatsApp number.',
    sbAccounts: 'WhatsApp accounts', sbTgAccounts: 'Telegram accounts', sbAll: 'All', sbUnread: 'Unread', sbAdd: 'Add account', navAllApps: 'All apps',
    theyRead: '↩ They will read:', other: '🔁 Other wording', transPct: (p) => '🎤 Transcribing… ' + p + '%', translatingV: '🌐 Translating…',
    navAll: 'All accounts', navTpl: 'Templates', navLang: 'Languages', navSet: 'Settings',
    name: 'Name', color: 'Color', iWrite: 'I write in', custSpeak: 'Customers speak', autoDetect: 'Auto-detect',
    iWriteHint: 'Messages are translated into this language for you.', custHint: 'Auto-detect learns each chat’s language.',
    cancel: 'Cancel', create: 'Add & connect WhatsApp', scanQr: 'Scan the QR code with WhatsApp on your phone → Linked devices',
    linkTitle: 'Scan to log in', linkSteps: ['Scan the QR code with your phone’s camera', 'Tap the link to open WhatsApp', 'Scan the QR code again to link your account'],
    linkStay: 'Stay logged in on this browser', linkPhone: 'Log in with phone number',
    connected: 'Connected', loading: 'Loading your chats…', qrState: 'Scan the QR code', addApp: 'Add app',
    search: 'Search or start a new chat', type: 'Type a message', online: 'online',
    chipAuto: (n) => 'Auto · ' + n, tpl: '⚡ Templates', mode: '👁 Send: Preview',
    sendIn: (n) => 'Send in ' + n, change: 'Change language', wrote: 'You wrote:',
    hint: 'Enter to send · Esc to edit', edit: 'Edit', orig: 'Send original', send: 'Send ➤', youWrote: '✎ You wrote',
    transcribe: '🎤 Transcribe', transcribing: '🎤 Transcribing…', readText: '🔤 Read text', reading: '🔤 Reading the photo…',
    yesterday: 'Yesterday', photo: '📷 Photo',
    lang: { en: 'English', zh: 'Chinese', ar: 'Arabic', tr: 'Turkish', es: 'Spanish', pt: 'Portuguese', ru: 'Russian', fr: 'French', de: 'German', it: 'Italian' },
    sbApp: (n) => n + ' accounts',
  };
  const UI_ZH = {
    addTitle: '添加 WhatsApp 账号',
    addSub: '账号在 GlotChat 中拥有独立的空间。然后用该 WhatsApp 号码的手机扫描二维码。',
    sbAccounts: 'WhatsApp 账号', sbTgAccounts: 'Telegram 账号', sbAll: '所有', sbUnread: '未读', sbAdd: '添加账号', navAllApps: '所有应用',
    theyRead: '↩ 对方将读到：', other: '🔁 换个说法', transPct: (p) => '🎤 正在转写… ' + p + '%', translatingV: '🌐 正在翻译…',
    navAll: '所有账号', navTpl: '快捷回复', navLang: '语言', navSet: '设置',
    name: '名称', color: '颜色', iWrite: '我使用的语言', custSpeak: '客户使用的语言', autoDetect: '自动检测',
    iWriteHint: '消息会为你翻译成这种语言。', custHint: '自动检测会记住每个聊天的语言。',
    cancel: '取消', create: '添加并连接 WhatsApp', scanQr: '请用手机 WhatsApp 扫描二维码 → 已关联的设备',
    linkTitle: '扫码登录', linkSteps: ['用手机相机扫描二维码', '点按链接打开 WhatsApp', '再次扫描二维码以关联你的账号'],
    linkStay: '在此浏览器上保持登录', linkPhone: '使用手机号登录',
    connected: '已连接', loading: '正在加载聊天…', qrState: '请扫描二维码', addApp: '添加应用',
    search: '搜索或开始新的聊天', type: '输入消息', online: '在线',
    chipAuto: (n) => '自动 · ' + n, tpl: '⚡ 快捷回复', mode: '👁 发送：预览',
    sendIn: (n) => '以' + n + '发送', change: '更改语言', wrote: '你写的是：',
    hint: 'Enter 发送 · Esc 编辑', edit: '编辑', orig: '发送原文', send: '发送 ➤', youWrote: '✎ 你写的是',
    transcribe: '🎤 转文字', transcribing: '🎤 正在转写…', readText: '🔤 识别文字', reading: '🔤 正在识别图片…',
    yesterday: '昨天', photo: '📷 照片',
    lang: { en: '英语', zh: '中文', ar: '阿拉伯语', tr: '土耳其语', es: '西班牙语', pt: '葡萄牙语', ru: '俄语', fr: '法语', de: '德语', it: '意大利语' },
    sbApp: (n) => n + ' 账号',
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

  /* ---- Telegram: a buyer in Kazakhstan asks about delivery (Russian), or in Turkish on the Russian site ---- */
  const TG_RU = {
    who: ['Айгерим', 'А', '#0ea5e9'], src: 'ru',
    in1: 'Здравствуйте! Сколько стоит доставка в Алматы?',
    in2: 'Можно оплатить при получении?',
    out: 'Доставка в Алматы — 12 $. Да, можно оплатить при получении.',
    tr: {
      en: ['Hello! How much is delivery to Almaty?', 'Can I pay on delivery?', 'Delivery to Almaty is $12. Yes, you can pay on delivery.', 'Delivery to Almaty is $12. Yes, you can pay upon receipt.'],
      zh: ['你好！寄到阿拉木图的运费是多少？', '可以货到付款吗？', '寄到阿拉木图的运费是 12 美元。可以，支持货到付款。', '寄到阿拉木图的运费是 12 美元。可以，收货时付款。'],
      ar: ['مرحبًا! كم تكلفة التوصيل إلى ألماتي؟', 'هل يمكنني الدفع عند الاستلام؟', 'التوصيل إلى ألماتي 12 دولارًا. نعم، يمكنك الدفع عند الاستلام.', 'التوصيل إلى ألماتي 12 دولارًا. نعم، يمكن الدفع عند الاستلام.'],
      tr: ['Merhaba! Almatı’ya kargo ne kadar?', 'Kapıda ödeme yapabilir miyim?', 'Almatı’ya kargo 12 $. Evet, kapıda ödeme yapabilirsiniz.', 'Almatı’ya teslimat 12 $. Evet, teslimatta ödeme yapılabilir.'],
      es: ['¡Hola! ¿Cuánto cuesta el envío a Almaty?', '¿Puedo pagar contra entrega?', 'El envío a Almaty cuesta 12 $. Sí, puede pagar contra entrega.', 'La entrega en Almaty cuesta 12 $. Sí, se puede pagar al recibirlo.'],
      pt: ['Olá! Quanto custa o frete para Almaty?', 'Posso pagar na entrega?', 'O frete para Almaty custa US$ 12. Sim, você pode pagar na entrega.', 'A entrega em Almaty custa US$ 12. Sim, é possível pagar ao receber.'],
    },
  };
  const TG_TR = {
    who: ['Elif Kaya', 'E', '#0ea5e9'], src: 'tr',
    in1: 'Merhaba! İstanbul’a kargo ne kadar?',
    in2: 'Kapıda ödeme yapabilir miyim?',
    out: 'İstanbul’a kargo 12 $. Evet, kapıda ödeme yapabilirsiniz.',
    tr: { ru: ['Здравствуйте! Сколько стоит доставка в Стамбул?', 'Можно оплатить при получении?', 'Доставка в Стамбул — 12 $. Да, можно оплатить при получении.', 'Доставка в Стамбул стоит 12 $. Да, оплата при получении возможна.'] },
  };

  /* ---- Messenger: a Facebook-shop customer in Germany; Instagram: a buyer in France; Discord: a client in Italy ----
     [incoming 1, incoming 2, the agent's reply in the page language, what the customer will read (back-translation)] */
  const MS_DE = {
    who: ['Lena Schmidt', 'L', '#2563eb'], src: 'de',
    in1: 'Hallo! Ist die Lampe noch verfügbar?',
    in2: 'Was kostet der Versand nach München?',
    out: 'Ja, die Lampe ist verfügbar! Der Versand nach München kostet 8 €.',
    tr: {
      en: ['Hello! Is the lamp still available?', 'How much is shipping to Munich?', 'Yes, the lamp is available! Shipping to Munich costs €8.', 'Yes, the lamp is available! Shipping to Munich is €8.'],
      zh: ['你好！这盏灯还有货吗？', '寄到慕尼黑的运费是多少？', '有货！寄到慕尼黑的运费是 8 欧元。', '是的，这盏灯有货！寄到慕尼黑的运费为 8 欧元。'],
      ar: ['مرحبًا! هل المصباح لا يزال متوفرًا؟', 'كم تكلفة الشحن إلى ميونخ؟', 'نعم، المصباح متوفر! الشحن إلى ميونخ 8 يورو.', 'نعم، المصباح متوفر! تكلفة الشحن إلى ميونخ 8 يورو.'],
      tr: ['Merhaba! Lamba hâlâ mevcut mu?', 'Münih’e kargo ne kadar?', 'Evet, lamba mevcut! Münih’e kargo 8 €.', 'Evet, lamba mevcut! Münih’e gönderim 8 € tutuyor.'],
      es: ['¡Hola! ¿La lámpara sigue disponible?', '¿Cuánto cuesta el envío a Múnich?', '¡Sí, la lámpara está disponible! El envío a Múnich cuesta 8 €.', '¡Sí, la lámpara está disponible! El envío a Múnich son 8 €.'],
      pt: ['Olá! A luminária ainda está disponível?', 'Quanto custa o frete para Munique?', 'Sim, a luminária está disponível! O frete para Munique custa 8 €.', 'Sim, a luminária está disponível! O envio para Munique custa 8 €.'],
      ru: ['Здравствуйте! Лампа ещё в наличии?', 'Сколько стоит доставка в Мюнхен?', 'Да, лампа в наличии! Доставка в Мюнхен стоит 8 €.', 'Да, лампа есть в наличии! Доставка в Мюнхен — 8 €.'],
    },
  };
  const IG_FR = {
    who: ['Chloé Bernard', 'C', '#c026d3'], src: 'fr',
    in1: 'Coucou ! Le sac noir est dispo ?',
    in2: 'Vous livrez en Belgique ?',
    out: 'Oui, le sac noir est disponible ! Nous livrons en Belgique en 3 jours.',
    tr: {
      en: ['Hi! Is the black bag available?', 'Do you deliver to Belgium?', 'Yes, the black bag is available! We deliver to Belgium in 3 days.', 'Yes, the black bag is available! We deliver in Belgium in 3 days.'],
      zh: ['嗨！黑色的包有货吗？', '你们送货到比利时吗？', '黑色的包有货！我们 3 天内送到比利时。', '是的，黑色的包有货！我们在 3 天内送达比利时。'],
      ar: ['مرحبًا! هل الحقيبة السوداء متوفرة؟', 'هل توصلون إلى بلجيكا؟', 'نعم، الحقيبة السوداء متوفرة! نوصل إلى بلجيكا خلال 3 أيام.', 'نعم، الحقيبة السوداء متوفرة! نقوم بالتوصيل إلى بلجيكا خلال 3 أيام.'],
      tr: ['Selam! Siyah çanta var mı?', 'Belçika’ya gönderim yapıyor musunuz?', 'Evet, siyah çanta mevcut! Belçika’ya 3 günde teslim ediyoruz.', 'Evet, siyah çanta mevcut! Belçika’ya 3 gün içinde teslimat yapıyoruz.'],
      es: ['¡Hola! ¿Está disponible el bolso negro?', '¿Hacen envíos a Bélgica?', '¡Sí, el bolso negro está disponible! Enviamos a Bélgica en 3 días.', '¡Sí, el bolso negro está disponible! Entregamos en Bélgica en 3 días.'],
      pt: ['Oi! A bolsa preta está disponível?', 'Vocês entregam na Bélgica?', 'Sim, a bolsa preta está disponível! Entregamos na Bélgica em 3 dias.', 'Sim, a bolsa preta está disponível! Fazemos entregas na Bélgica em 3 dias.'],
      ru: ['Привет! Чёрная сумка есть в наличии?', 'Вы доставляете в Бельгию?', 'Да, чёрная сумка в наличии! Доставим в Бельгию за 3 дня.', 'Да, чёрная сумка есть в наличии! Доставка в Бельгию — 3 дня.'],
    },
  };
  const DC_IT = {
    who: ['Marco Rossi', 'M', '#16a34a'], src: 'it',
    in1: 'Ciao! Quanto costa il logo animato?',
    in2: 'Posso pagare con USDT?',
    out: 'Il logo animato costa 40 $. Sì, accettiamo USDT.',
    tr: {
      en: ['Hi! How much is the animated logo?', 'Can I pay with USDT?', 'The animated logo costs $40. Yes, we accept USDT.', 'The animated logo is $40. Yes, we accept USDT.'],
      zh: ['你好！动态 logo 多少钱？', '可以用 USDT 付款吗？', '动态 logo 价格是 40 美元。可以，我们接受 USDT。', '动态 logo 售价 40 美元。是的，我们接受 USDT。'],
      ar: ['مرحبًا! كم سعر الشعار المتحرك؟', 'هل يمكنني الدفع بـ USDT؟', 'سعر الشعار المتحرك 40 دولارًا. نعم، نقبل USDT.', 'الشعار المتحرك بـ 40 دولارًا. نعم، نقبل USDT.'],
      tr: ['Merhaba! Animasyonlu logo ne kadar?', 'USDT ile ödeyebilir miyim?', 'Animasyonlu logo 40 $. Evet, USDT kabul ediyoruz.', 'Animasyonlu logonun fiyatı 40 $. Evet, USDT kabul ediyoruz.'],
      es: ['¡Hola! ¿Cuánto cuesta el logo animado?', '¿Puedo pagar con USDT?', 'El logo animado cuesta 40 $. Sí, aceptamos USDT.', 'El logo animado vale 40 $. Sí, aceptamos USDT.'],
      pt: ['Oi! Quanto custa o logo animado?', 'Posso pagar com USDT?', 'O logo animado custa US$ 40. Sim, aceitamos USDT.', 'O logo animado sai por US$ 40. Sim, aceitamos USDT.'],
      ru: ['Привет! Сколько стоит анимированный логотип?', 'Можно оплатить в USDT?', 'Анимированный логотип стоит 40 $. Да, мы принимаем USDT.', 'Анимированный логотип — 40 $. Да, принимаем USDT.'],
    },
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
      chat, chatTr: chat.tr[lang], tg: lang === 'ru' ? TG_TR : TG_RU, tgTr: (lang === 'ru' ? TG_TR : TG_RU).tr[lang], ms: MS_DE, msTr: MS_DE.tr[lang], ig: IG_FR, igTr: IG_FR.tr[lang], dc: DC_IT, dcTr: DC_IT.tr[lang],
      voice, voiceTr: voice.tr[lang], photo: PHOTO, photoTr: PHOTO.tr[lang],
      notes: [pick(N_UAE, N_UAE_RU), pick(N_SUP, N_SUP_DE), pick(N_EXP, N_EXP_ES)],
      rows: ROWS.map((r) => r.map((c) => (c === '*' ? ui.yesterday : c))),
    };
  };
})();
