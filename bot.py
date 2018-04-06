import const, base, temp, utils
import telebot
import request

bot = telebot.TeleBot(const.token)
phone = ""


@bot.message_handler(commands=['start'])
def start(message):
    text = message.text.split(" ")
    if len(text) == 2:
        if text[1].isdigit():
            initial_id = text[1]
            base.addInvitation(initial_id, int(message.chat.id))
    #base.add_user(message)
    main_message = "<b>Привет, " + message.from_user.first_name + "!</b>\n"\
                   "Меня зовут Анастасия, и я менеджер агентства <b>Intux Digital</b>.\n" \
                   "Сейчас, за меня конечно же пишет автоматический робот, но давайте познакомимся с Вами поближе, " \
                   "чтобы выяснить, чем и как мы можем быть Вам полезны.\n" \
                                                                  "<b>Согласны? :)</b>\n"
    if not base.is_in_base(message.chat.id):
        bot.send_message(message.chat.id, main_message, reply_markup=utils.step_1(), parse_mode="HTML")
    else:
        bot.send_message(message.chat.id, "<b>Привет</b>", parse_mode='HTML', reply_markup=utils.menu())


@bot.message_handler(regexp="Хочу также")
def want(message):
    sent = bot.send_message(message.chat.id, const.want_like_you, parse_mode="Markdown",
                            reply_markup=utils.phone())
    bot.register_next_step_handler(sent, ring)


def ring(message):
    bot.send_message(211439710, 'Привет, у вас новая заявка.\n\n {name}'.format(name=message.contact))
    bot.send_message(message.chat.id, 'Ваша заявка принята, в скором времени свяжемся с вами',
                     reply_markup=utils.menu())


@bot.message_handler(regexp="О нас")
def about(message):
    bot.send_message(message.chat.id, const.about_us, parse_mode="HTML")


@bot.message_handler(regexp="Примеры работ")
def example(message):
    bot.send_message(message.chat.id, "<b>Ознакомься с нашими крайними проектами</b>\n\n"
                                      "@mr2018Chatbot - криптобиржка\n"
                                      "@BestCryptoInsideBot - сигналы для торгов\n"
                                      "@Crytpoinside_bot\n"
                                      "https://vk.cc/7V8ZoM - учебный бот для Фоксфорда\n", parse_mode="HTML")


@bot.message_handler(regexp="Пригласить друзей")
def referalka(message):
    bot.send_message(message.chat.id, 'У вас рефералов: {0}\n'
                                      'Ваша реферальная ссылка:'
                                      ' https://t.me/intux_agency_bot?start={1}'.format(*base.getValuesPartnership(message.chat.id)))


@bot.message_handler(regexp="Назад")
def want(message):
    bot.send_message(message.chat.id, "*Меню*\n\n", parse_mode="Markdown",
                     reply_markup=utils.menu())


@bot.message_handler(regexp="Категория 1")
def first(message):
    bot.send_message(message.chat.id, "*Text about Категория 1*\n\n", parse_mode="Markdown",
                     reply_markup=utils.project())


@bot.message_handler(regexp="Категория 2")
def second(message):
    bot.send_message(message.chat.id, "*Text about Категория 2*\n\n", parse_mode="Markdown",
                     reply_markup=utils.project())


# Добавление телефона
@bot.callback_query_handler(func=lambda call: call.data == 'registr')
def want(call):
    new_item = temp.Item()
    const.new_items_user_adding.update([(call.message.chat.id, new_item)])
    sent = bot.send_message(call.message.chat.id, "Хорошо, в среднем это занимает всего 28 секунд\n"
                                                  "Нажми на кнопку",
                            reply_markup=utils.phone())
    bot.register_next_step_handler(sent, send_phone)


def send_phone(message):
    global phone
    try:
        phone = message.contact.phone_number
    except Exception:
        phone = message.text
    base.add_item_phone(message, phone)
    bot.send_message(211439710, 'Привет, у вас новая заявка на этапе регистрации.\n\n {name}'.format(name=message.contact))
    sent = bot.send_message(message.chat.id, "Напечатайте, как Вас зовут)")
    bot.register_next_step_handler(sent, base.add_item_name)
    const.user_adding_item_step[message.chat.id] = "Enter city"
    # const.user_adding_item_step.update([(message.chat.id, "Enter name")])


# Добавление имени
@bot.message_handler(func=lambda message: base.get_user_step(message.chat.id) == "Enter name")
def handle_add_item_phone(message):
    sent = bot.send_message(message.chat.id, "Напечатайте, как Вас зовут)")
    bot.register_next_step_handler(sent, base.add_item_name)
    const.user_adding_item_step[message.chat.id] = "Enter city"


# Добавление города
@bot.message_handler(func=lambda message: base.get_user_step(message.chat.id) == "Enter city")
def handle_add_item_phone(message):
    sent = bot.send_message(message.chat.id, "Из какого Вы города?")
    bot.register_next_step_handler(sent, base.add_item_city)
    const.user_adding_item_step[message.chat.id] = "Enter doing"


# Добавление группы
@bot.message_handler(func=lambda message: base.get_user_step(message.chat.id) == "Enter doing")
def handle_add_item_phone(message):
    sent = bot.send_message(message.chat.id, "Вы уже действующий предприниматель или "
                                             "только планируете запустить свой бизнес?", reply_markup=utils.doing())
    bot.register_next_step_handler(sent, base.add_item_who)
    const.user_adding_item_step[message.chat.id] = "Enter end"


# Добавление сферы
@bot.message_handler(regexp="Только планирую начать")
def about(message):
    sent = bot.send_message(message.chat.id, "У Вас всё получится, главное "
                                             "никогда не сдавайтесь! А Вы знаете уже сферу, которой хотите заняться "
                                             "или ещё не определились? Напишите)")
    bot.register_next_step_handler(sent, base.add_item_doing)
    const.user_adding_item_step[message.chat.id] = "well done"


# Добавление сферы
@bot.message_handler(regexp="Уже занимаюсь бизнесом")
def about(message):
    sent = bot.send_message(message.chat.id, "Превосходно, значит мы с Вами на одной волне:) "
                                             "Напишите сферу или направление, чем занимается Ваш бизнес")
    bot.register_next_step_handler(sent, base.add_item_doing)
    const.user_adding_item_step[message.chat.id] = "well done"


# Добавление группы
@bot.message_handler(func=lambda message: base.get_user_step(message.chat.id) == "well done")
def handle_add_item_phone(message):
    bot.send_message(message.chat.id, "Прекрасно, " + message.from_user.first_name + ", наша команда рада с Вами "
                                                                                     "познакомиться! :)\n\n"
                                             "Немного о нас. Цель нашей компании обеспечить каждому "
                                             "клиенту эффективный и стабильный поток заявок "
                                             "с помощью комплексных решений Digital Marketing’a."
                                             "Для нас наибольшая радость сопровождать клиента на всех этапах "
                                             "формирования своего интернет маркетинга: от создания логотипа и "
                                             "брендинга - до разработки крупных сайтов, тестирования рекламных "
                                             "компаний и внедрения CRM-системы в отдел продаж клиента.")

    bot.send_message(message.chat.id, "А ещё Вы можете заказать обратный звонок", reply_markup=utils.menu())


if __name__ == '__main__':
    bot.remove_webhook()
    bot.polling(none_stop=True)
