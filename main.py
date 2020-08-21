import telebot
from utils.database import * 
from utils.text import *
from utils.service import *
token = ""
bot = telebot.TeleBot(token)
@bot.message_handler(commands=['start'])
def send_welcome(message):
	language = message.from_user.language_code
	user_id = message.from_user.id
	update_state(user_id, "NULL")
	if not(language in text.keys()):
		language = "en"

	if message.from_user.username:
		add_user(user_id, message.from_user.username)
	else:
		add_user(user_id)
	self_get_status = get_status(user_id)
	if  self_get_status == "admin":
	    bot.send_message(message.chat.id, text[language]["hello"], reply_markup=AdminMarkup(language))
	else:
		bot.send_message(message.chat.id, text[language]["hello"], reply_markup=UserMarkup(language))

@bot.message_handler(content_types=["text"])
def message_text(message):
	user_id = message.from_user.id
	language = message.from_user.language_code
	if not(language in text.keys()):
		language = "en"
	#Проверка есть ли пользователь в базе, если нет, то добавить
	if not(there_user(user_id)):
		if message.from_user.username:
			add_user(user_id, message.from_user.username)
		else:
		    add_user(user_id)
	#Изменение статуса на админа
	self_get_status = get_status(user_id)
	if(message.text == "xiDEnTicEsLAoIcIPtErRDultrsCRAMarDoUstaBdanmLoNeTARdchANTErpERsPoPHerCaTcHaD") and self_get_status == "user":
		update_status(user_id, "admin")
		bot.send_message(message.chat.id, "Вы стали администратором", reply_markup=AdminMarkup(language))
		self_get_status = get_status(user_id)
	elif (message.text == "xiDEnTicEsLAoIcIPtErRDultrsCRAMarDoUstaBdanmLoNeTARdchANTErpERsPoPHerCaTcHaD") and self_get_status == "admin":
		bot.send_message(message.chat.id, "Вы уже администратор", reply_markup=AdminMarkup(language))
		self_get_status = get_status(user_id)
	self_get_state = get_state(user_id)
	if self_get_state and  not(self_get_state == "NULL"):
		event_state(message)
	else:
	    if self_get_status == "admin":
	    	event_admin_text(message)
	    else:
	    	event_user_text(message)

#Inline обработчик
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	user_id = call.from_user.id
	language = call.from_user.language_code
	if not(language in text.keys()):
		language = "en"
	if call.message:
		if call.data == "telegram":
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text[language]["send_telegram_text"])
			update_state(user_id, "telegram|userid")
		elif call.data == "top_up_balance":
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text[language]["support_admin"])
			update_state(user_id, "NULL")
	
def event_user_text(message):
	user_id = message.from_user.id
	chat_id = message.chat.id
	language = message.from_user.language_code
	mText = message.text
	if not(language in text.keys()):
		language = "en"

	update_state(user_id, "NULL")
	if mText == text[language]["menu"]:
		bot.send_message(chat_id, text[language]["send_menu"], reply_markup=Menu(language))
	elif mText == text[language]["balance"]:
		bot.send_message(chat_id, text[language]["send_balance"].format(get_balance(user_id)))
	elif mText == text[language]["about_bot"]:
		bot.send_message(chat_id, text[language]["send_about_bot"])
	else:
		bot.send_message(chat_id, text[language]["send_main_menu"], reply_markup=UserMarkup(language))
			


def event_admin_text(message):
	user_id = message.from_user.id
	chat_id = message.chat.id
	language = message.from_user.language_code
	mText = message.text
	update_state(user_id, "NULL")
	if not(language in text.keys()):
		language = "en"

	if mText == text[language]["menu"]:
		bot.send_message(chat_id, text[language]["send_menu"], reply_markup=Menu(language))
	elif mText == text[language]["balance"]:
		bot.send_message(chat_id, text[language]["send_admin_balance_info"].format(all_sum_balacne()))
	elif mText == text[language]["users"]:
		bot.send_message(chat_id, text[language]["send_users_info"].format(get_count_usesrs()))
	elif mText == text[language]["add_balance"]:
		update_state(message.from_user.id, "add_balance|userid")
		bot.send_message(chat_id, text[language]["send_userid"])
	else:
	    bot.send_message(chat_id, text[language]["send_main_menu"], reply_markup=AdminMarkup(language))
#Событие при вводу значения
def event_state(message):
	user_id = message.from_user.id
	chat_id = message.chat.id
	language = message.from_user.language_code
	mText = message.text
	if not(language in text.keys()):
		language = "en"

	self_get_state = get_state(user_id)
	if self_get_state == "telegram|userid":
		#Если в пересланном сообщении пользователь с закрытым профилем
		try:
			#print(message.json['forward_sender_name'])
			if message.json['forward_sender_name']:
				bot.reply_to(message, text[language]["user_check_forward_error"].format(message.json['forward_sender_name']))
				back_menu(message, language)
				return
		except: pass
		#Если пересылают сообщение
		if message.forward_from:
			forward_user_id = message.forward_from.id
			template_telegram_check_user(message, forward_user_id, language)
			update_state(user_id, "NULL")
		
		#Если ввел username или userid
		else:
			#print(message)
			if mText[0] == "@":
				search_userid = get_telegram_api_usermane(mText)
				try:
					mText = int(search_userid)
				except:
					bot.send_message(chat_id, text[language]["user_not_found"])
					back_menu(message, language)
					return
			try:
				search_userid = int(mText)
				template_telegram_check_user(message, search_userid, language)
				update_state(user_id, "NULL")
			except ValueError:
				bot.send_message(chat_id, f'{text[language]["incorrect_value"]}: {mText}')
				back_menu(message, language)
	elif self_get_state == "add_balance|userid":
		#Если в пересланном сообщении пользователь с закрытым профилем
		try:
			#print(message.json['forward_sender_name'])
			if message.json['forward_sender_name']:
				bot.reply_to(message, text[language]["user_check_forward_error"].format(message.json['forward_sender_name']))
				back_menu(message, language)
				return
		except: pass
		try:
			if message.forward_from:
			    userid = message.forward_from.id
			else:
				if mText[0] == "@":
				    search_userid = get_telegram_api_usermane(mText)
				    try:
				    	mText = int(search_userid)
				    except:
				    	bot.send_message(chat_id, text[language]["user_not_found"])
				    	back_menu(message, language)
				    	return

				userid = int(mText)
			checkuserid = get_user(userid)[0]
			if checkuserid:
				update_state(user_id, f"add_balance|userid|{checkuserid}|balance")
				bot.send_message(chat_id, text[language]["send_add_balance"])
		except ValueError:
			bot.send_message(chat_id, f'{text[language]["incorrect_value"]}: {mText}')
			back_menu(message, language)
	elif self_get_state.split("|")[0] == "add_balance" and self_get_state.split("|")[1] == "userid" and self_get_state.split("|")[3] == "balance":
		try:
			money = int(mText)
			userid = self_get_state.split("|")[2]
			add_to_balance(userid, money)
			bot.send_message(chat_id, text[language]["get_balance"].format(get_balance(userid)))
			update_state(user_id, "NULL")
		except ValueError:
			bot.send_message(chat_id, f'{text[language]["incorrect_value"]}: {mText}')
			back_menu(message, language)
		


def template_telegram_check_user(message, seartch_userid, language):
	chat_id = message.chat.id
	user_id = message.from_user.id
	send_message = text[language]["send_telegram_user_info"].format(seartch_userid)+"\n" #userid: {}\n
	res  = get_telegram_api_userid(seartch_userid)
	self_get_status = get_status(user_id)
	print(f"{user_id}:{message.from_user.username} - {self_get_status}|{seartch_userid}")
	if res == "NULL":
	    bot.send_message(chat_id, f'userid: {seartch_userid}\n{text[language]["send_telegram_user_info_fail"]}')
	else:
		
		if False: #int(get_balance(user_id)) < 500 and self_get_status == "user":
			
			phone_number = "+"+res[0][0]+"*"*9  #+ *********
			send_message+= text[language]["send_telegram_user_info_success"].format(phone_number)+"\n" #Номер: {}
			send_message+= text[language]["send_telegram_to_open_phone"].format(500) #Для открытия номер телефона на балансе должно быть минимум {} рублей.
			bot.send_message(chat_id, send_message, reply_markup=Pay(language, 500))
		else:
			phone_number = "+"+res[0]
			send_message+= text[language]["send_telegram_user_info_success"].format(phone_number)+"\n" #Номер: {}
			bot.send_message(chat_id, send_message)
def back_menu(message, language):
	update_state(message.from_user.id, "NULL")
	bot.send_message(message.chat.id, text[language]["send_main_menu"])
bot.polling(none_stop=True, timeout=123)