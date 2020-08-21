text = {
    "ru": {
        "hello": "Добро Пожаловать странник, я попробую раскрыть тебе все тайны, найти твоих обидчиков и должников...", 
        "balance": '💸 Баланс',
        "menu": '📱 Меню', 
        "about_bot": '💬 О боте',
        "users": "👫 Пользователи",
        "send_main_menu": "Главное меню: ",
        "send_balance": "Ваш баланс: {} рублей",
        "send_admin_balance_info": "Сумма баланса всех пользователей: {} рублей",
        "send_menu": "Выберите поиск:", 
        "send_about_bot": 'Ирландский бот, который поможет Вам раздобыть информацию на пользователя сети.',
        "not enough balance": "У вас недостаточно средств на балансе",
        "pay": "Пополнить",
        "incorrect_value": "Некорректное значение", 
        "send_telegram_text": "Введите userid, username или пришлите сюда сообщение человека, которого нужно найти",
        "send_telegram_to_open_phone":"Для открытия номера телефона на балансе должно быть минимум {} рублей.",
        "send_telegram_user_info": "userid: {}",
        "send_telegram_user_info_success": "Номер: {}",
        "send_telegram_user_info_fail": "К сожалению пользователя нет в базе",
        "send_users_info": "Количество пользователей: {}",
        "add_balance": "Добавить баланс пользователю",
        "get_balance": "Баланс пользователя составляет:  {} рублей",
        "send_userid": "Введите userid пользователя или перешлите его сообщение",
        "send_add_balance": "На сколько пополнить баланс: ",
        "support_admin": "Чтобы пополнить баланс, свяжитесь с администрацией: @user_na_me, @prometheus_service, @Proper_Admin",
        "user_not_found": "Пользователь не найден",
        "user_check_forward_error": "К сожалению не удалось узнать userid пользователя {}. Пожалуйста используйте username или userid."
    },
    "en": {
        "hello": "Welcome wanderer, I will try to reveal all the secrets to you, to find your offenders and debtors ...", 
        "balance": '💸 Balance',
        "menu": '📱 Menu', 
        "about_bot": '💬 About bot',
        "users": "👫 Users",
        "send_main_menu": "Main menu: ",
        "send_balance": "Your balance: {} RUB",
        "send_admin_balance_info": "The sum of the balance of all users: {} RUB",
        "send_menu": "Select search:", 
        "send_about_bot": 'An Irish bot that will help you get information on a network user.',
        "not enough balance": "Not enough funds in the balance",
        "pay": "Pay",
        "incorrect_value": "Incorrect value", 
        "send_telegram_text": "Enter userid or username send the message of the person you want to find here",
        "send_telegram_to_open_phone":"To open a phone number, the balance must be {} RUB.",
        "send_telegram_user_info": "userid: {}",
        "send_telegram_user_info_success": "Phone: {}",
        "send_telegram_user_info_fail": "Unfortunately the user is not in the database",
        "send_users_info": "Count users: {}",
        "add_balance": "Add balance",
        "get_balance": "The user's balance is:  {} RUB",
        "send_userid": "Enter the user's userid or forward their message",
        "send_add_balance": "How much to top up the balance: ",
        "support_admin": "To top up the balance, contact the administration: {}",
        "user_not_found":"User is not found",
        "user_check_forward_error": "Unfortunately, we could not find out the userid of user {}. Please use username or userid."
    }
}
from telebot import types
#User
def UserMarkup(language):
    MarkupUser = types.ReplyKeyboardMarkup(resize_keyboard=True)
    Balance = types.KeyboardButton(text[language]["balance"])
    Menu = types.KeyboardButton(text[language]["menu"])
    AboutBot = types.KeyboardButton(text[language]["about_bot"])
    MarkupUser.row(Menu)
    MarkupUser.row(Balance, AboutBot)
    return MarkupUser
#Admin
def AdminMarkup(language):
    MarkupAdmin = types.ReplyKeyboardMarkup(resize_keyboard=True)
    Balance = types.KeyboardButton(text[language]["balance"]) 
    Menu = types.KeyboardButton(text[language]["menu"])
    AboutBot = types.KeyboardButton(text[language]["users"])
    AddBalance = types.KeyboardButton(text[language]["add_balance"])
    MarkupAdmin.row(Menu, AddBalance)
    MarkupAdmin.row(Balance, AboutBot)
    return MarkupAdmin



def Menu(language):
    menu = types.InlineKeyboardMarkup()
    menu.add(types.InlineKeyboardButton(text="Телеграмм", callback_data="telegram"))
    return menu

def Pay(lang, money):
    shop = types.InlineKeyboardMarkup()
    shop.add(types.InlineKeyboardButton(text=text[lang]["pay"], callback_data="top_up_balance"))
    return shop