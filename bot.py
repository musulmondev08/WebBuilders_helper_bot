from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, CommandHandler, CallbackQueryHandler, CallbackContext
import logging
import requests

TOKEN = '7757609154:AAEFn8Xs4NnvBzbTovhLv8cDD1ZpuUIEhP8'
ADMIN_CHAT_ID = '6428294967'  # Adminning chat ID'si
CHANNEL_USERNAMES = ['@S_WebBuilders','@R_Webbuilders']  # Kanal nomlari ro'yxati

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(level)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Global variables to store the previous states
current_state = {}
previous_state = {}

# faq savollarga avto javob berish start
FAQ_CONTENT = { 
    # salom javobi
    "salom": "Salom",
    "salm":"Salom",
    "slom":"Salom",
    "hello": "Hello", 
    "hi": "Hii",
    "hii":"Hii",
    "assalomu alaykum": "Va alaykum assalom", 
    # Yaxshi raxmat javobi
    "qandaysiz": "Yaxshi, rahmat!",
    "qandaysz":"Yaxshi, raxmat!",
    "qanday":"Yaxshi, raxmat!",
    "qalesiz": "Yaxshi, rahmat!", 
    "qalaysan": "Yaxshi, rahmat!",
    "qandaysan": "Yaxshi, rahmat!",
    "qandaysn": "Yaxshi, rahmat!",
    "qandaysan": "Yaxshi, rahmat!",
    "qalay": "Zo'r",
    "qale":"Zo'r",
    # tinclikmi savoliga javob
    "tinchmi":"Tinch o'zizda nima gap",
    "tincmi":"Tinch o'zizda nima gap",
    "tinch":"Tinch bo'lsa yaxshi, mendan qanday yordam kerak!",
    "tinc":"Tinch bo'lsa yaxshi, mendan qanday yordam kerak!",
    # saytda xatolik bo'yicha savol javoblar
    "saytda muammo chiqdi":"Saytda muammo chiqdimi, siz menga qaysi saytdan va saytni qayeridan muammo chiqanini aytsangiz men sizga aniqroq yordam berishga harakat qilaman.",
    "saytda hatolik chiqdi":"Saytda muammo chiqdimi, siz menga qaysi saytdan va saytni qayeridan muammo chiqanini aytsangiz men sizga aniqroq yordam berishga harakat qilaman.",
    "saytda xatolik chiqdi":"Saytda muammo chiqdimi, siz menga qaysi saytdan va saytni qayeridan muammo chiqanini aytsangiz men sizga aniqroq yordam berishga harakat qilaman.",
    "saytda xatolik":"Saytda muammo chiqdimi, siz menga qaysi saytdan va saytni qayeridan muammo chiqanini aytsangiz men sizga aniqroq yordam berishga harakat qilaman.",
    "saytda hatolik":"Saytda muammo chiqdimi, siz menga qaysi saytdan va saytni qayeridan muammo chiqanini aytsangiz men sizga aniqroq yordam berishga harakat qilaman.",
    "saytda xatolik bor":"Saytda muammo chiqdimi, siz menga qaysi saytdan va saytni qayeridan muammo chiqanini aytsangiz men sizga aniqroq yordam berishga harakat qilaman.",
    "saytda hatolik bor":"Saytda muammo chiqdimi, siz menga qaysi saytdan va saytni qayeridan muammo chiqanini aytsangiz men sizga aniqroq yordam berishga harakat qilaman.",
    "webbuilders saytida":"Yaxshi menga qanday xatolik ekanligini aytsangiz men sizga aniqroq ma'lumot bera olishim mumkin",
    # Bot haqida savol javoblar
    "sen kimsan":"men kim emas nimasan degan savolga to'g'ri kelaman va men WebBuilders_helper_bot man agar men haqimda qiziqayotgan bolsangiz sen nimasan deb savol bering.",
    "sen nimasan":"Men 'WebBuilders_helper_bot'man va men sizning ko'plab savollaringizga javob beraman. Ogohlantirish! taqiqlangan va mavzuga oid bo'lmagan savollarga javob bera olmayman.",
    "o'zing haqingda ma'lumot ber":"Men 'WebBuilders_helper_bot'man va men sizning ko'plab savollaringizga javob beraman. Ogohlantirish! taqiqlangan va mavzuga oid bo'lmagan savollarga javob bera olmayman.",
    "ozing haqingda malumot ber":"Men 'WebBuilders_helper_bot'man va men sizning ko'plab savollaringizga javob beraman. Ogohlantirish! taqiqlangan va mavzuga oid bo'lmagan savollarga javob bera olmayman.",
    "ozing haqingda ma'lumot ber":"Men 'WebBuilders_helper_bot'man va men sizning ko'plab savollaringizga javob beraman. Ogohlantirish! taqiqlangan va mavzuga oid bo'lmagan savollarga javob bera olmayman.",
    "o'zing haqingda malumot ber":"Men 'WebBuilders_helper_bot'man va men sizning ko'plab savollaringizga javob beraman. Ogohlantirish! taqiqlangan va mavzuga oid bo'lmagan savollarga javob bera olmayman.",
    "o'zing haqingda aytib ber":"Men 'WebBuilders_helper_bot'man va men sizning ko'plab savollaringizga javob beraman. Ogohlantirish! taqiqlangan va mavzuga oid bo'lmagan savollarga javob bera olmayman.",
    "o'zing haqingda ayt":"Men 'WebBuilders_helper_bot'man va men sizning ko'plab savollaringizga javob beraman. Ogohlantirish! taqiqlangan va mavzuga oid bo'lmagan savollarga javob bera olmayman.",
    "ozing haqingda ayt":"Men 'WebBuilders_helper_bot'man va men sizning ko'plab savollaringizga javob beraman. Ogohlantirish! taqiqlangan va mavzuga oid bo'lmagan savollarga javob bera olmayman.",



    

    # Davom etirib toldirish kerak









    # Add more FAQs here 
}

# Foydalanuvchi xabarlarini qo'lga olish va javob berish uchun xabar handleri
async def handle_message(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user

        # Xabar kanaldan kelganligini tekshirish
    if update.message.chat.type in ['group', 'supergroup', 'channel']:
        return

    message_text = update.message.text.lower()  # Convert text to lowercase for case-insensitive matching
    if message_text in FAQ_CONTENT:
        response = FAQ_CONTENT[message_text]
        await update.message.reply_text(response)
    else:
        await update.message.reply_text("Kechirasiz, savolingizga tushunmadim.")
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"Foydalanuvchi {user.full_name} xabar yubordi: {message_text}")

  
# faq svollarga avto javob berish finish

# Start command handler
async def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    current_state[user.id] = 'main_menu'
    previous_state[user.id] = 'start'
    keyboard = [
        [InlineKeyboardButton("🔍 Tekshirish", callback_data='check_subscription')]
        ]

    for channel in CHANNEL_USERNAMES:
        keyboard.insert(0, [InlineKeyboardButton(f"Obuna bo'lish: {channel}", url=f"https://t.me/{channel[1:]}")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f"Assalomu alaykum, {user.full_name}! Botga xush kelibsiz! Davom etish uchun kanal(lar)ga obuna bo'ling. Obuna bo'lganingizni tekshiring. 😊", reply_markup=reply_markup)
    logger.info(f"User {user.full_name} started the bot.")

# Function to check channel subscription
def check_subscription(user_id: int) -> bool:
    for channel in CHANNEL_USERNAMES:
        response = requests.get(f"https://api.telegram.org/bot{TOKEN}/getChatMember?chat_id={channel}&user_id={user_id}")
        result = response.json()["result"]
        status = result["status"]
        if status not in ["member", "administrator", "creator"]:
            return False
    return True

# Callback query handler
async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    user = query.from_user

    if query.data == 'check_subscription':
        is_subscribed = check_subscription(user.id)
        if is_subscribed:
            current_state[user.id] = 'main_menu'
            previous_state[user.id] = 'start'
            keyboard = [
                [InlineKeyboardButton("📄 Ma'lumotlar", callback_data='info')],
                [InlineKeyboardButton("📋 Variantlar", callback_data='options')],
                [InlineKeyboardButton("🔧 Yordam olish", callback_data='help')],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text("Obuna bo'lganingiz tekshirildi. Quyidagi tugmachalardan birini tanlang: 😊", reply_markup=reply_markup)
            logger.info(f"User {user.full_name} subscribed to the channel(s).")

        else:
            keyboard = [[InlineKeyboardButton("🔍 Tekshirish", callback_data='check_subscription')]]
            for channel in CHANNEL_USERNAMES:
                keyboard.insert(0, [InlineKeyboardButton(f"Obuna bo'lish: {channel}", url=f"https://t.me/{channel[1:]}")])
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(f"❌ Iltimos, avval kanal(lar)ga obuna bo'ling. Obuna bo'lganingizni tekshiring. 😊", reply_markup=reply_markup)

            logger.info(f"User {user.full_name} is not subscribed to the channel(s).")

            # Ma'lumotlar bo'limi start
    elif query.data == 'info':
        previous_state[user.id] = current_state[user.id]
        current_state[user.id] = 'info'
        keyboard = [
            [InlineKeyboardButton("WebBuilders sayti haqida", callback_data='site1_info')],
            [InlineKeyboardButton("Sayt2 haqida ma'lumot", callback_data='site2_info')],
            [InlineKeyboardButton("Sayt3 haqida ma'lumot", callback_data='site3_info')],
            [InlineKeyboardButton("🔙 Orqaga", callback_data='back_to_main')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="📄 Ma'lumotlar bo'limi:", reply_markup=reply_markup)
        logger.info(f"User {user.full_name} selected 'Ma'lumotlar'.")
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"Foydalanuvchi {user.full_name} '📄 Ma'lumotlar' bo'limini tanladi.")
    elif query.data == 'site1_info':
        await query.edit_message_text(text="WebBuilders sayti 2025-yil 19-yanvarda tugatilgan va 25-yanvardan ishga tushirilgan", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Orqaga", callback_data='back_to_info')]]))
        logger.info(f"User {user.full_name} selected 'WebBuilders sayti haqidagi ma'lumot'.")
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"Foydalanuvchi {user.full_name} WebBuilders sayti haqidagi ma'lumotni tanladi.")
    elif query.data == 'site2_info':
        await query.edit_message_text(text="Bu sayt hali mavjud emas hozirda bizda WebBuilders sayti mavjud! Hamda bizning S_WebBuilders ommaviy guruhimizdan savollaringizga javob oling va R_WebBuilders kanalimizdan biz haqimizdagi yangiliklarni bilib boring.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Orqaga", callback_data='back_to_info')]]))
        logger.info(f"User {user.full_name} selected 'Sayt2 haqida ma'lumot'.")
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"Foydalanuvchi {user.full_name} 'Sayt2 haqida ma'lumot'ni tanladi.")
    elif query.data == 'site3_info':
        await query.edit_message_text(text="Bu sayt hali mavjud emas hozirda bizda WebBuilders sayti mavjud! Hamda bizning S_WebBuilders ommaviy guruhimizdan savollaringizga javob oling va R_WebBuilders kanalimizdan biz haqimizdagi yangiliklarni bilib boring.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Orqaga", callback_data='back_to_info')]]))
        logger.info(f"User {user.full_name} selected 'Sayt3 haqida ma'lumot'.")
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"Foydalanuvchi {user.full_name} 'Sayt3 haqida ma'lumot'ni tanladi.")
    elif query.data == 'back_to_info':
        keyboard = [
            [InlineKeyboardButton("WebBuilders sayti haqida", callback_data='site1_info')],
            [InlineKeyboardButton("Sayt2 haqida ma'lumot", callback_data='site2_info')],
            [InlineKeyboardButton("Sayt3 haqida ma'lumot", callback_data='site3_info')],
            [InlineKeyboardButton("🔙 Orqaga", callback_data='back_to_main')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="📄 Ma'lumotlar bo'limi:", reply_markup=reply_markup)

    # Ma'lumotlar bo'limi finish
    # Variyantlar bo'limi start 

    elif query.data == 'options':
        previous_state[user.id] = current_state[user.id]
        current_state[user.id] = 'options'
        keyboard = [
            [InlineKeyboardButton("📞 Telefon orqali bog'lanish", callback_data='phone_contact')],
            [InlineKeyboardButton("📩 Telegram orqali bog'lanish", callback_data='telegram_contact' )],
            [InlineKeyboardButton("🔙 Orqaga", callback_data='back_to_main')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="📋 Variantlar bo'limi: 😊", reply_markup=reply_markup)
        logger.info(f"User {user.full_name} selected 'Variantlar'.")
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"Foydalanuvchi {user.full_name} '📋 Variantlar' bo'limini tanladi.")
    elif query.data == 'phone_contact':
        keyboard = [[InlineKeyboardButton("🔙 Orqaga", callback_data='back_to_main')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="📞 Telefon orqali bog'lanish: +998979092508 shu nomerga murojaat qilishingiz mumkin. 😊", reply_markup=reply_markup)
        logger.info(f"User {user.full_name} selected 'Telefon orqali bog'lanish'.")
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"Foydalanuvchi {user.full_name} Telefon orqali bog'lanishni tanladi.")
        
    elif query.data == 'telegram_contact':
        keyboard = [[InlineKeyboardButton("🔙 Orqaga", callback_data='back_to_main')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="📩 Telegram orqali bog'lanish: url='https://t.me/Dasturchi2008' shu lichkaga murojaat qilishingiz mumkin. 😊", reply_markup=reply_markup)
        logger.info(f"User {user.full_name} selected 'Telefon orqali bog'lanish'.")
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"Foydalanuvchi {user.full_name} Telegram orqali bog'lanishni tanladi.")

        # Variantlar bo'limi finish

        # yordam olish bo'limi start 
    elif query.data == 'help':
        previous_state[user.id] = current_state[user.id]
        current_state[user.id] = 'help'
        keyboard = [
            [InlineKeyboardButton("🌐 Login page ishlamayapti", callback_data='login_issue')],
            [InlineKeyboardButton("🌐 Register page ishlamayapti", callback_data='register_issue')],
            [InlineKeyboardButton("🌐 Boshqa savol", callback_data='other_issue')],
            [InlineKeyboardButton("🔙 Orqaga", callback_data='back_to_main')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="🔧 Yordam olish bo'limi: 😊", reply_markup=reply_markup)
        logger.info(f"User {user.full_name} selected 'Yordam olish'.")
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"Foydalanuvchi {user.full_name} '🔧 Yordam olish' bo'lim tanladi.")
        
    elif query.data == 'login_issue':
        await query.edit_message_text(text="Agarda sizda Login page ishlamayotgan bo'lsa internet tarmog'ingizda muammo bor internet tarmog'ingizni tekshiring! Tekshirganingizdan keyin ham ishlamoytgan bo'lsa unda adminga murojat qiling.Adminga murojat qilish uchun variantlar bo'limiga o'ting va o'zingizga qulay yo'l orqali admin bilan aloqaga chiqing", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Orqaga", callback_data='back_to_help')]]))
        logger.info(f"User {user.full_name} selected 'Login_muammo'.")
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"Foydalanuvchi {user.full_name} Login page bo'yicha yordamni tanladi.")
    elif query.data == 'register_issue':
        await query.edit_message_text(text="Agarda sizda Register page ishlamayotgan bo'lsa registratsiyadan to'g'ri o'tayotganingizga ishonch hosil qilin va internet tarmog'ingizni tekshiring! Tekshirganingizdan keyin ham ishlamoytgan bo'lsa unda adminga murojat qiling.Adminga murojat qilish uchun variantlar bo'limiga o'ting va o'zingizga qulay yo'l orqali admin bilan aloqaga chiqing", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Orqaga", callback_data='back_to_help')]]))
        logger.info(f"User {user.full_name} selected 'Register_muammo'.")
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"Foydalanuvchi {user.full_name} Login page bo'yicha yordamni tanladi.")
    elif query.data == 'other_issue':
        await query.edit_message_text(text="Agarda sizda boshqa savollar mavjud bo'lsa bot ning o'ziga yozishingiz va savollaringizda javob olishingiz mumkin.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Orqaga", callback_data='back_to_main')]]))
        logger.info(f"User {user.full_name} selected 'Boshqa_muammo'.")
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"Foydalanuvchi {user.full_name} Boshqa savoli bor ekan botga yozishni boshlayapti.")


    elif query.data == 'back_to_help':
        current_state[user.id] = 'help'
        keyboard = [
            [InlineKeyboardButton("🌐 Login page ishlamayapti", callback_data='login_issue')],
            [InlineKeyboardButton("🌐 Register page ishlamayapti", callback_data='register_issue')],
            [InlineKeyboardButton("🌐 Boshqa savol", callback_data='other_issue')],
            [InlineKeyboardButton("🔙 Orqaga", callback_data='back_to_main')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("🔧 Yordam olish bo'limi: 😊", reply_markup=reply_markup)


    elif query.data == 'back_to_main':
        current_state[user.id] = 'main_menu'
        keyboard = [
            [InlineKeyboardButton("📄 Ma'lumotlar", callback_data='info')],
            [InlineKeyboardButton("📋 Variantlar", callback_data='options')],
            [InlineKeyboardButton("🔧 Yordam olish", callback_data='help')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Obuna bo'lganingiz tekshirildi ➕. Quyidagi tugmachalardan birini tanlang: 😊", reply_markup=reply_markup)

    

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button))

    # Message handler qo'shish
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

if __name__ == '__main__':
    main()
