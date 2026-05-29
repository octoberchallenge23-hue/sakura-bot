import asyncio
import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# ========== الإعدادات ==========
BOT_TOKEN = "8805749137:AAGCA8zTxA_OpowLWpy_wX8pjPa9Q3wP-3Y"
WALLET_ADDRESS = "0x27af4d8bd1f755697c4b5a8ecc297ed6ea1df99d"
BIN_CHECK_URL = "https://cdpn.io/Kh4y/debug/qEqVPpj/full"

# ========== قوائم البيانات الوهمية ==========
BINS = [
    "400000", "411111", "510510", "545454",
    "601100", "378282", "400123", "511122",
    "545555", "601111", "378211", "400200",
]

FIRST_NAMES = ["James", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Charles", "Mary", "Patricia", "Jennifer", "Linda", "Barbara", "Elizabeth", "Susan", "Jessica", "Sarah", "Karen", "Nancy"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"]
STREETS = ["Main St", "Oak Ave", "Maple Dr", "Cedar Ln", "Pine Rd", "Elm St", "Washington Blvd", "Park Ave", "Lake Dr", "Hill Rd", "Forest Way", "River Rd", "Meadow Ln", "Sunset Blvd", "Valley Dr"]
CITIES = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "Miami", "Atlanta", "Boston", "Seattle", "Denver", "Portland"]
STATES = {"NY": "New York", "CA": "California", "IL": "Illinois", "TX": "Texas", "AZ": "Arizona", "PA": "Pennsylvania", "FL": "Florida", "OH": "Ohio", "GA": "Georgia", "MI": "Michigan", "NC": "North Carolina", "NJ": "New Jersey", "VA": "Virginia", "WA": "Washington", "MA": "Massachusetts"}
STATE_CODES = list(STATES.keys())

# ========== النصوص متعددة اللغات ==========
T = {
    "ar": {
        "lang_sel": "اختر لغتك / Choose your language",
        "welcome": "🌸 أهلاً بك في SakuraDigital\nنحن مزود خدمات رقمية موثوق. نقدم حلول دفع خاصة لعملائنا.\n\nاختر من القائمة أدناه:",
        "services": "🌸 باقات ساكورا الرقمية\n\nاختر الباقة التي تناسب احتياجك:\n\n🥉 الباقة البرونزية — 15 USDT\n🥈 الباقة الفضية — 25 USDT\n🥇 الباقة الذهبية — 40 USDT\n\n⚡️ جميع الباقات تشمل ضمان الاستبدال المجاني لمدة 24 ساعة.",
        "payment": "💳 طرق الدفع المتاحة:\n\nالعملة: USDT\nالشبكة: TRC20\nالحد الأدنى: 15 USDT\n\nلا نقبل أي عملات أخرى حاليًا.",
        "support": "📩 جميع طلبات الدعم تُعالج يدويًا.\nفريقنا سيتواصل معك في أقرب وقت.\n\nشكرًا لصبرك.",
        "bronze": "🥉 الباقة البرونزية\nالسعر: 15 USDT\nالرصيد المتوقع: 150-300$\n\nللتأكيد، اضغط على الزر أدناه.",
        "silver": "🥈 الباقة الفضية\nالسعر: 25 USDT\nالرصيد المتوقع: 500-800$\n\nللتأكيد، اضغط على الزر أدناه.",
        "gold": "🥇 الباقة الذهبية\nالسعر: 40 USDT\nالرصيد المتوقع: 1000-1500$\n\nللتأكيد، اضغط على الزر أدناه.",
        "confirm15": f"✅ تم تأكيد طلبك (15 USDT).\n\nللدفع، حول المبلغ على شبكة TRC20 إلى:\n`{WALLET_ADDRESS}`\n\nبعد التحويل، اضغط على زر 'تم التحويل'.",
        "confirm25": f"✅ تم تأكيد طلبك (25 USDT).\n\nللدفع، حول المبلغ على شبكة TRC20 إلى:\n`{WALLET_ADDRESS}`\n\nبعد التحويل، اضغط على زر 'تم التحويل'.",
        "confirm40": f"✅ تم تأكيد طلبك (40 USDT).\n\nللدفع، حول المبلغ على شبكة TRC20 إلى:\n`{WALLET_ADDRESS}`\n\nبعد التحويل، اضغط على زر 'تم التحويل'.",
        "paid": "📎 من فضلك، أرفق صورة إثبات التحويل (سكرين شوت) أو ملف PDF هنا في المحادثة.\n\nبعد الرفع، اضغط على الزر أدناه.",
        "proof": "📎 من فضلك، أرفق صورة إثبات التحويل (سكرين شوت) أو ملف PDF هنا في المحادثة.\n\n⏳ في انتظار الملف...",
        "received": "📥 تم استلام الملف. جاري الفحص...",
        "daily_15": "300$", "daily_25": "700$", "daily_40": "1500$",
        "exp_15": "150-300$", "exp_25": "500-800$", "exp_40": "1000-1500$",
        "pkg_15": "البرونزية", "pkg_25": "الفضية", "pkg_40": "الذهبية",
        "btn_services": "📦 عرض الخدمات", "btn_payment": "💳 طريقة الدفع", "btn_support": "🎧 الدعم الفني",
        "btn_back": "🔙 رجوع", "btn_confirm": "✅ تأكيد الطلب", "btn_paid": "💸 تم التحويل",
        "btn_proof": "✅ تم إرفاق الإثبات", "btn_check": "🔍 فحص البطاقة",
        "btn_bronze": "🥉 البرونزية (15$)", "btn_silver": "🥈 الفضية (25$)", "btn_gold": "🥇 الذهبية (40$)",
    },
    "en": {
        "lang_sel": "Choose your language / اختر لغتك",
        "welcome": "🌸 Welcome to SakuraDigital\nWe are a trusted digital services provider. We offer special payment solutions for our clients.\n\nChoose from the menu below:",
        "services": "🌸 SakuraDigital Packages\n\nChoose the package that suits your needs:\n\n🥉 Bronze Package — 15 USDT\n🥈 Silver Package — 25 USDT\n🥇 Gold Package — 40 USDT\n\n⚡️ All packages include free replacement guarantee for 24 hours.",
        "payment": "💳 Available Payment Methods:\n\nCurrency: USDT\nNetwork: TRC20\nMinimum: 15 USDT\n\nWe do not accept any other currencies at this time.",
        "support": "📩 All support requests are processed manually.\nOur team will contact you as soon as possible.\n\nThank you for your patience.",
        "bronze": "🥉 Bronze Package\nPrice: 15 USDT\nExpected Balance: 150-300$\n\nTo confirm, press the button below.",
        "silver": "🥈 Silver Package\nPrice: 25 USDT\nExpected Balance: 500-800$\n\nTo confirm, press the button below.",
        "gold": "🥇 Gold Package\nPrice: 40 USDT\nExpected Balance: 1000-1500$\n\nTo confirm, press the button below.",
        "confirm15": f"✅ Order Confirmed (15 USDT).\n\nTo pay, transfer the amount on TRC20 network to:\n`{WALLET_ADDRESS}`\n\nAfter transfer, press 'Paid' button.",
        "confirm25": f"✅ Order Confirmed (25 USDT).\n\nTo pay, transfer the amount on TRC20 network to:\n`{WALLET_ADDRESS}`\n\nAfter transfer, press 'Paid' button.",
        "confirm40": f"✅ Order Confirmed (40 USDT).\n\nTo pay, transfer the amount on TRC20 network to:\n`{WALLET_ADDRESS}`\n\nAfter transfer, press 'Paid' button.",
        "paid": "📎 Please attach payment proof (screenshot) or PDF file here in the chat.\n\nAfter uploading, press the button below.",
        "proof": "📎 Please attach payment proof (screenshot) or PDF file here in the chat.\n\n⏳ Waiting for file...",
        "received": "📥 File received. Checking...",
        "daily_15": "300$", "daily_25": "700$", "daily_40": "1500$",
        "exp_15": "150-300$", "exp_25": "500-800$", "exp_40": "1000-1500$",
        "pkg_15": "Bronze", "pkg_25": "Silver", "pkg_40": "Gold",
        "btn_services": "📦 Services", "btn_payment": "💳 Payment", "btn_support": "🎧 Support",
        "btn_back": "🔙 Back", "btn_confirm": "✅ Confirm Order", "btn_paid": "💸 Paid",
        "btn_proof": "✅ Proof Uploaded", "btn_check": "🔍 Check Card",
        "btn_bronze": "🥉 Bronze (15$)", "btn_silver": "🥈 Silver (25$)", "btn_gold": "🥇 Gold (40$)",
    },
    "ru": {
        "lang_sel": "Выберите язык / Choose your language",
        "welcome": "🌸 Добро пожаловать в SakuraDigital\nМы надежный поставщик цифровых услуг. Предлагаем специальные платежные решения для наших клиентов.\n\nВыберите из меню ниже:",
        "services": "🌸 Пакеты SakuraDigital\n\nВыберите подходящий пакет:\n\n🥉 Бронзовый пакет — 15 USDT\n🥈 Серебряный пакет — 25 USDT\n🥇 Золотой пакет — 40 USDT\n\n⚡️ Все пакеты включают бесплатную гарантию замены на 24 часа.",
        "payment": "💳 Доступные способы оплаты:\n\nВалюта: USDT\nСеть: TRC20\nМинимум: 15 USDT\n\nДругие валюты не принимаются.",
        "support": "📩 Все запросы обрабатываются вручную.\nНаша команда свяжется с вами как можно скорее.\n\nСпасибо за терпение.",
        "bronze": "🥉 Бронзовый пакет\nЦена: 15 USDT\nОжидаемый баланс: 150-300$\n\nДля подтверждения нажмите кнопку ниже.",
        "silver": "🥈 Серебряный пакет\nЦена: 25 USDT\nОжидаемый баланс: 500-800$\n\nДля подтверждения нажмите кнопку ниже.",
        "gold": "🥇 Золотой пакет\nЦена: 40 USDT\nОжидаемый баланс: 1000-1500$\n\nДля подтверждения нажмите кнопку ниже.",
        "confirm15": f"✅ Заказ подтвержден (15 USDT).\n\nДля оплаты переведите сумму в сети TRC20 на:\n`{WALLET_ADDRESS}`\n\nПосле перевода нажмите кнопку 'Оплачено'.",
        "confirm25": f"✅ Заказ подтвержден (25 USDT).\n\nДля оплаты переведите сумму в сети TRC20 на:\n`{WALLET_ADDRESS}`\n\nПосле перевода нажмите кнопку 'Оплачено'.",
        "confirm40": f"✅ Заказ подтвержден (40 USDT).\n\nДля оплаты переведите сумму в сети TRC20 на:\n`{WALLET_ADDRESS}`\n\nПосле перевода нажмите кнопку 'Оплачено'.",
        "paid": "📎 Пожалуйста, прикрепите доказательство оплаты (скриншот) или PDF файл сюда в чат.\n\nПосле загрузки нажмите кнопку ниже.",
        "proof": "📎 Пожалуйста, прикрепите доказательство оплаты (скриншот) или PDF файл сюда в чат.\n\n⏳ Ожидание файла...",
        "received": "📥 Файл получен. Проверка...",
        "daily_15": "300$", "daily_25": "700$", "daily_40": "1500$",
        "exp_15": "150-300$", "exp_25": "500-800$", "exp_40": "1000-1500$",
        "pkg_15": "Бронзовый", "pkg_25": "Серебряный", "pkg_40": "Золотой",
        "btn_services": "📦 Услуги", "btn_payment": "💳 Оплата", "btn_support": "🎧 Поддержка",
        "btn_back": "🔙 Назад", "btn_confirm": "✅ Подтвердить", "btn_paid": "💸 Оплачено",
        "btn_proof": "✅ Доказательство загружено", "btn_check": "🔍 Проверить карту",
        "btn_bronze": "🥉 Бронза (15$)", "btn_silver": "🥈 Серебро (25$)", "btn_gold": "🥇 Золото (40$)",
    },
    "ja": {
        "lang_sel": "言語を選んでください / Choose your language",
        "welcome": "🌸 SakuraDigitalへようこそ\n私たちは信頼できるデジタルサービスプロバイダーです。特別な支払いソリューションを提供します。\n\n下のメニューから選んでください:",
        "services": "🌸 SakuraDigitalパッケージ\n\nニーズに合ったパッケージを選んでください:\n\n🥉 ブロンズパッケージ — 15 USDT\n🥈 シルバーパッケージ — 25 USDT\n🥇 ゴールドパッケージ — 40 USDT\n\n⚡️ すべてのパッケージに24時間の無料交換保証が含まれます。",
        "payment": "💳 利用可能な支払い方法:\n\n通貨: USDT\nネットワーク: TRC20\n最低額: 15 USDT\n\n他の通貨は現在受け付けていません。",
        "support": "📩 すべてのサポートリクエストは手動で処理されます。\n私たちのチームができるだけ早く連絡します。\n\nお待ちいただきありがとうございます。",
        "bronze": "🥉 ブロンズパッケージ\n価格: 15 USDT\n予想残高: 150-300$\n\n確認するには下のボタンを押してください。",
        "silver": "🥈 シルバーパッケージ\n価格: 25 USDT\n予想残高: 500-800$\n\n確認するには下のボタンを押してください。",
        "gold": "🥇 ゴールドパッケージ\n価格: 40 USDT\n予想残高: 1000-1500$\n\n確認するには下のボタンを押してください。",
        "confirm15": f"✅ 注文確認 (15 USDT).\n\n支払うには、TRC20ネットワークで次のアドレスに送金してください:\n`{WALLET_ADDRESS}`\n\n送金後、「支払い完了」ボタンを押してください。",
        "confirm25": f"✅ 注文確認 (25 USDT).\n\n支払うには、TRC20ネットワークで次のアドレスに送金してください:\n`{WALLET_ADDRESS}`\n\n送金後、「支払い完了」ボタンを押してください。",
        "confirm40": f"✅ 注文確認 (40 USDT).\n\n支払うには、TRC20ネットワークで次のアドレスに送金してください:\n`{WALLET_ADDRESS}`\n\n送金後、「支払い完了」ボタンを押してください。",
        "paid": "📎 支払い証明（スクリーンショット）またはPDFファイルをここに添付してください。\n\nアップロード後、下のボタンを押してください。",
        "proof": "📎 支払い証明（スクリーンショット）またはPDFファイルをここに添付してください。\n\n⏳ ファイル待機中...",
        "received": "📥 ファイルを受信しました。確認中...",
        "daily_15": "300$", "daily_25": "700$", "daily_40": "1500$",
        "exp_15": "150-300$", "exp_25": "500-800$", "exp_40": "1000-1500$",
        "pkg_15": "ブロンズ", "pkg_25": "シルバー", "pkg_40": "ゴールド",
        "btn_services": "📦 サービス", "btn_payment": "💳 支払い", "btn_support": "🎧 サポート",
        "btn_back": "🔙 戻る", "btn_confirm": "✅ 注文確認", "btn_paid": "💸 支払い完了",
        "btn_proof": "✅ 証明アップロード", "btn_check": "🔍 カード確認",
        "btn_bronze": "🥉 ブロンズ (15$)", "btn_silver": "🥈 シルバー (25$)", "btn_gold": "🥇 ゴールド (40$)",
    }
}

# ========== دوال مساعدة ==========
def _(context, key):
    lang = context.user_data.get('lang', 'en')
    return T.get(lang, T['en']).get(key, T['en'].get(key, key))

def btn(context, key, callback_data):
    return InlineKeyboardButton(_(context, key), callback_data=callback_data)

def generate_fullz():
    bin_ = random.choice(BINS)
    length = 15 if bin_.startswith("3") else 16
    remaining = ''.join([str(random.randint(0,9)) for _ in range(length - len(bin_))])
    card_number = bin_ + remaining
    month = str(random.randint(1,12)).zfill(2)
    year = str(random.randint(27,31))  # 2027 إلى 2031
    cvv = ''.join([str(random.randint(0,9)) for _ in range(3)])
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    street = f"{random.randint(100,9999)} {random.choice(STREETS)}"
    city = random.choice(CITIES)
    state_code = random.choice(STATE_CODES)
    state = STATES[state_code]
    zip_code = f"{random.randint(10000,99999)}"
    return {
        "card": f"{card_number}|{month}|{year}|{cvv}",
        "name": f"{first} {last}",
        "address": street,
        "city": city,
        "state": state,
        "zip": zip_code,
    }

# ========== دوال البوت ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'lang' not in context.user_data:
        context.user_data['lang'] = 'en'
    keyboard = [
        [InlineKeyboardButton("🇸🇦 العربية", callback_data="lang_ar")],
        [InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")],
        [InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru")],
        [InlineKeyboardButton("🇯🇵 日本語", callback_data="lang_ja")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(_(context, "lang_sel"), reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("lang_"):
        lang = data.split("_")[1]
        context.user_data['lang'] = lang
        keyboard = [
            [btn(context, "btn_services", "services")],
            [btn(context, "btn_payment", "payment")],
            [btn(context, "btn_support", "support")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(_(context, "welcome"), reply_markup=reply_markup)

    elif data == "services":
        keyboard = [
            [btn(context, "btn_bronze", "bronze")],
            [btn(context, "btn_silver", "silver")],
            [btn(context, "btn_gold", "gold")],
            [btn(context, "btn_back", "start_menu")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(_(context, "services"), reply_markup=reply_markup)

    elif data == "payment":
        keyboard = [[btn(context, "btn_back", "start_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(_(context, "payment"), reply_markup=reply_markup)

    elif data == "support":
        keyboard = [[btn(context, "btn_back", "start_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(_(context, "support"), reply_markup=reply_markup)

    elif data in ["bronze", "silver", "gold"]:
        confirm_key = f"confirm{'15' if data == 'bronze' else '25' if data == 'silver' else '40'}"
        keyboard = [
            [btn(context, "btn_confirm", confirm_key)],
            [btn(context, "btn_back", "services")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(_(context, data), reply_markup=reply_markup)

    elif data in ["confirm15", "confirm25", "confirm40"]:
        keyboard = [
            [btn(context, "btn_paid", f"paid_{data}")],
            [btn(context, "btn_back", "services")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(_(context, data), reply_markup=reply_markup, parse_mode="Markdown")

    elif data.startswith("paid_"):
        keyboard = [
            [btn(context, "btn_proof", f"proof_{data}")],
            [btn(context, "btn_back", "services")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(_(context, "paid"), reply_markup=reply_markup)

    elif data.startswith("proof_"):
        keyboard = [[btn(context, "btn_back", "services")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(_(context, "proof"), reply_markup=reply_markup)
        context.user_data['awaiting_proof'] = True
        context.user_data['proof_data'] = data

    elif data == "start_menu":
        keyboard = [
            [btn(context, "btn_services", "services")],
            [btn(context, "btn_payment", "payment")],
            [btn(context, "btn_support", "support")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(_(context, "welcome"), reply_markup=reply_markup)

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get('awaiting_proof'):
        return
    proof_data = context.user_data.get('proof_data', '')
    if 'confirm15' in proof_data:
        daily_key, exp_key, pkg_key = "daily_15", "exp_15", "pkg_15"
    elif 'confirm25' in proof_data:
        daily_key, exp_key, pkg_key = "daily_25", "exp_25", "pkg_25"
    elif 'confirm40' in proof_data:
        daily_key, exp_key, pkg_key = "daily_40", "exp_40", "pkg_40"
    else:
        daily_key, exp_key, pkg_key = "daily_15", "exp_15", "pkg_15"
    
    await update.message.reply_text(_(context, "received"))
    await asyncio.sleep(90)
    
    fake = generate_fullz()
    text = f"""
✅ {_(context, exp_key)}

🎖 {_(context, pkg_key)}
📋 {fake['name']}
💳 `{fake['card']}`
🏠 {fake['address']}
🏙️ {fake['city']}, {fake['state']} {fake['zip']}
🇺🇸 United States
💰 {_(context, exp_key)}

🔍 {BIN_CHECK_URL}

📌 {_(context, daily_key)}
"""
    keyboard = [
        [InlineKeyboardButton(_(context, "btn_check"), url=BIN_CHECK_URL)],
        [btn(context, "btn_support", "support")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")
    context.user_data['awaiting_proof'] = False
    context.user_data['proof_data'] = ''

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL | filters.PHOTO, handle_document))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("🌸 Sakura is running...")
    app.run_polling()

if __name__ == "__main__":
    main()