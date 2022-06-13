import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

import calc
import sqlite3


con = sqlite3.connect("food.db", check_same_thread=False)
cur = con.cursor()


bot = telebot.TeleBot('5510516119:AAFv8yr225_zo-Q9d8ao5QhBggFM7E9c44U')

global eaten_food
eaten_food = []

global parametrs
parametrs = []

def Search_name(a):
    s = []
    s.append(a)
    f = (a.split(' '))

    for x in f: s.append(x)
    for i in range(len(s)):
        if len(s[i]) >= 4 and (s[i][-1] == 'а' or s[i][-1] == 'и' or s[i][-1] == 'ы'):
            s[i] = s[i][:len(s[i]) - 1]

    for x in s:
        print(x)
        sql = f"SELECT * FROM food WHERE name LIKE '%{x}%'"
    cur.execute(sql)
    return (cur.fetchmany(10))

@bot.message_handler(commands=["start", 'help'])
def start(m):
    bot.send_message(m.chat.id, 'Введите любой продукт или блюдо или воспользуйтесь кнопками')

@bot.message_handler(commands=['add_norm_kcal'])
def norm_kcal(message):
    print(parametrs)

    def input_gender(message):
        if (message.text.lower() == 'отменить'):
            pass
        else:
            try:
                global gender
                if (message.text == 'м' or message.text == 'ж'):
                    gender = message.text
                    bot.send_message(message.chat.id,'ок', reply_markup=types.ReplyKeyboardRemove())
                else:
                    print(gender)
                bot.send_message(message.chat.id, 'Введите свой возраст')
                bot.register_next_step_handler(message, input_age)
            except:
                bot.send_message(message.chat.id, 'Пожалуйста, ответье буквой "м" или "ж"')
                bot.register_next_step_handler(message, input_gender)

    def input_age(message):
        if (message.text.lower() == 'отменить'):
            pass
        else:
            try:
                global age
                if (0 >= int(message.text) or int(message.text) >= 100):
                    bot.send_message(message.chat.id, f'Вам не может быть {message.text} лет.')
                    print(age)
                age = float(message.text)
                bot.send_message(message.chat.id, 'Введите свой вес (кг)')
                bot.register_next_step_handler(message, input_weight)
            except:
                bot.send_message(message.chat.id, 'Пожалуйста введите возраст целым числом')
                bot.register_next_step_handler(message, input_age)

    def input_weight(message):
        if (message.text.lower() == 'отменить'):
            pass
        else:
            try:
                global weight
                weight = float(message.text)
                bot.send_message(message.chat.id, 'Введите свой рост (см)')
                bot.register_next_step_handler(message, input_height)
            except:
                bot.send_message(message.chat.id, 'Пожалуйста введите свой вес в кг цифрами')
                bot.register_next_step_handler(message, input_weight)

    def input_height(message):
        if (message.text.lower() == 'отменить'):
            pass
        else:
            try:
                global height
                height = float(message.text)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton("1")
                btn2 = types.KeyboardButton("2")
                btn3 = types.KeyboardButton("3")
                btn4 = types.KeyboardButton("4")
                btn5 = types.KeyboardButton("5")
                markup.add(btn1, btn2, btn3, btn4, btn5)
                bot.send_message(message.chat.id, text="Введите свой уровень активности:",
                                 reply_markup=markup)
                bot.send_message(message.chat.id,
                                 'Минимальный уровень активности — 1,\nНизкий уровень активности — 2,\nСредний уровень активности — 3,\nВысокий уровень — 4,\nОчень высокий —  5:\n')

                bot.register_next_step_handler(message, input_kf)
            except:
                bot.send_message(message.chat.id, 'Пожалуйста, введите свой рост цифрами')
                bot.register_next_step_handler(message, input_height)

    def input_kf(message):
        if (message.text.lower() == 'отменить'):
            pass
        else:
            try:
                global kf
                if (int(message.text) == 1): kf = 1.2
                if (int(message.text) == 2): kf = 1.375
                if (int(message.text) == 3): kf = 1.55
                if (int(message.text) == 4): kf = 1.725
                if (int(message.text) == 5): kf = 1.9
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton("1")
                btn2 = types.KeyboardButton("2")
                btn3 = types.KeyboardButton("3")
                markup.add(btn1, btn2, btn2)
                bot.send_message(message.chat.id, text="Выберите и введите свою цель: ", reply_markup=markup)
                bot.send_message(message.chat.id, 'Похудеть - 1, \nПоддерживать свой вес - 2, \nНабрать массу - 3')
                bot.register_next_step_handler(message, input_mode)
            except:
                bot.send_message(message.chat.id, 'Пожалуйста, ответье числом от 1 до 5')
                bot.register_next_step_handler(message, input_kf)

    def input_mode(message):
        if (message.text.lower() == 'отменить'):
            pass
        else:
            try:
                global mode
                if (1 <= int(message.text) <= 3):
                    mode = int(message.text)
                bmr_mode = calc.Find_BMR_mode(calc.Find_BMR(gender, age, weight, height), mode)
                bot.send_message(message.chat.id, f'{calc.Day_kcal(gender, age, weight, height, mode)}')
                d = {'Пол: ': gender, 'Возраст:': age, 'Вес: ': weight, 'Рост: ': height, 'КФ: ': kf, 'Мод: ': mode,
                     'bmr: ': calc.Find_BMR(gender, age, weight, height), 'bmr_mode: ': bmr_mode}
                if (parametrs != [0]):
                    parametrs.clear()
                parametrs.append(d)

            except:
                bot.send_message(message.chat.id, 'Пожалуйста, ответье числом от 1 до 3')
                bot.register_next_step_handler(message, input_mode)

    global bmr_mode
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_m = types.KeyboardButton("м")
    btn_w = types.KeyboardButton("ж")
    markup.add(btn_m, btn_w)
    bot.send_message(message.chat.id, text="Введите свой пол (м/ж)", reply_markup=markup)
    bot.register_next_step_handler(message, input_gender)

@bot.message_handler(commands=['see_norm_kcal'])
def see_norm_kcal(message):
    if (parametrs != []):
        for par in parametrs:
            d = dict.copy(par)
            gender = d['Пол: ']
            age = d['Возраст:']
            weight = d['Вес: ']
            height = d['Рост: ']
            kf = d['КФ: ']
            mode = d['Мод: ']
            bmr = d['bmr: ']
            bmr_mode = d['bmr_mode: ']
            bot.send_message(message.chat.id, f'{calc.Day_kcal(gender, age, weight, height, mode)}')
    else:
        bot.send_message(message.chat.id, "Параметры не заполнены")

@bot.message_handler(commands=['add_my'])
def add_my(message):
    bot.send_message(message.chat.id, 'введите название')

    def input_name(message):
        if (message.text.lower() == 'отменить'):
            pass
        else:
            global name_self
            name_self = message.text
            print(name_self)
            bot.send_message(message.chat.id, 'введите калойрийность(ккал)')
            bot.register_next_step_handler(message, input_ccal)

    def input_ccal(message):
        if (message.text.lower() == 'отменить'):
            pass
        else:
            try:
                global ccal_self
                ccal_self = float(message.text)
                print(ccal_self)
                bot.send_message(message.chat.id, 'введите Белки на 100г (г)')
                bot.register_next_step_handler(message, input_prot)
            except:
                bot.send_message(message.chat.id, 'Пожалуйста введите калорийность цифрами и без пробелов')
                bot.register_next_step_handler(message, input_ccal)

    def input_prot(message):
        if (message.text.lower() == 'отменить'):
            pass
        else:
            try:
                global prot_self
                prot_self = float(message.text)
                print(prot_self)
                bot.send_message(message.chat.id, 'введите Жиры на 100г (г)')
                bot.register_next_step_handler(message, input_fats)
            except:
                bot.send_message(message.chat.id,
                                 'Пожалуйста введите Белки(г) цифрами и без пробелов или напишите "Отменить"')
                bot.register_next_step_handler(message, input_prot)

    def input_fats(message):
        if (message.text.lower() == 'отменить'):
            pass
        else:
            try:
                global fats_self
                fats_self = float(message.text)
                print(fats_self)
                bot.send_message(message.chat.id, 'введите Углеводы на 100г (г)')
                bot.register_next_step_handler(message, input_cbh)
            except:
                bot.send_message(message.chat.id,
                                 'Пожалуйста введите Жиры (г) цифрами и без пробелов или напишите "Отменить"')
                bot.register_next_step_handler(message, input_fats)

    def input_cbh(message):
        if (message.text.lower() == 'отменить'):
            pass
        else:
            try:
                global cbh_self
                cbh_self = float(message.text)
                print(cbh_self)
                bot.send_message(message.chat.id, 'введите вес (г)')
                bot.register_next_step_handler(message, input_weight)
            except:
                bot.send_message(message.chat.id,
                                 'Пожалуйста введите Углеводы (г) цифрами и без пробелов или напишите "Отменить"')
                bot.register_next_step_handler(message, input_cbh)

    def input_weight(message):
        if (message.text.lower() == 'отменить'):
            pass
        else:
            try:
                weight_self = float(message.text)
                print(weight_self)
                d = {"Название": name_self, 'ккал': ccal_self * weight_self / 100.0,
                     'Белки (г)': prot_self * weight_self / 100.0,
                     'Жиры (г)': fats_self * weight_self / 100.0,
                     'Углеводы (г)': cbh_self * weight_self / 100.0,
                     'вес (г)': weight_self}
                eaten_food.append(d)
                bot.send_message(message.chat.id, 'Записал :)')
                print(eaten_food)
            except:
                bot.send_message(message.chat.id,
                                 'Пожалуйста введите Вес (г) цифрами и без пробелов или напишите "Отменить"')
                bot.register_next_step_handler(message, input_weight)

    bot.register_next_step_handler(message, input_name)

@bot.message_handler(commands=['count_food'])
def count_food(message):
    bot.send_message(message.chat.id, 'ща скажу')
    ccal = 0
    prot = 0
    fat = 0
    cb = 0
    for food in eaten_food:
        d = dict.copy(food)
        ccal += d['ккал']
        prot += d['Белки (г)']
        fat += d['Жиры (г)']
        cb += d['Углеводы (г)']
        bot.send_message(message.chat.id,
                         f'Название: {d["Название"]}\n ккал: {d["ккал"]}\nБелки (г): {d["Белки (г)"]}\n Жиры (г): {d["Жиры (г)"]}\n Углеводы (г): {d["Углеводы (г)"]}\nВес (г): {d["вес (г)"]}')
    bot.send_message(message.chat.id,
                     f'итого: ккал: {ccal}\nБелки (г): {prot}\nЖиры (г): {fat}\n Углеводы (г): {cb}')

@bot.message_handler(content_types=['text'])
def handle_text(message):

    print(message.chat.id)
    axc = Search_name(str(message.text).lower())
    print(axc)
    global i
    i = 1
    for example in axc:
        bot.send_message(message.chat.id, f'Название: {example[0]}\nккал: {example[1]}\nБелки: {example[2]}, Жиры: {example[3]}, Углеводы: {example[4]}\nНОМЕР: {i}')
        # markup = InlineKeyboardMarkup()
        # but1 = InlineKeyboardButton(text="Добавить", switch_inline_query_current_chat=f"{i}")
        # #but2 = InlineKeyboardButton(text="Отменить", switch_inline_query_current_chat="Отменить")
        # markup.add(but1)
        # markup = types.InlineKeyboardMarkup()
        # markup.add(types.InlineKeyboardButton(text="Добавить", callback_data=f'{i}'))
        # bot.send_message(message.chat.id,
        #                  text=f'Название: {example[0]}\nккал: {example[1]}\nБелки: {example[2]}\nЖиры: {example[3]}\nУглеводы: {example[4]}\n',
        #                  reply_markup=markup)
        i+=1

    def check(message):

        if (message.text.lower() == 'да'):
            #bot.send_message(message.chat.id, "Введите номер еды, которую записать")
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            global btns
            btns = [0]*10
            for j in range(i-1):
                btns[j] = types.KeyboardButton(f'{j+1}')
                markup.add(btns[j])
            bot.send_message(message.chat.id, text="Введите номер еды, которую записать", reply_markup=markup)
            bot.register_next_step_handler(message, check_number)
        elif (message.text.lower() == 'нет'):
            bot.send_message(message.chat.id, "попробуйте другой запрос или добавьте свое блюдо")
        else:
            bot.send_message(message.chat.id, "Пожалуйста, отметье да или нет")
            bot.register_next_step_handler(message, check)

    def check_number(message):
        if (message.text.lower() == 'отменить'):
            pass
        else:
            try:
                global num
                if (int(message.text) >= 1 and int(message.text) <= i - 1):
                    num = int(message.text)
                    bot.send_message(message.chat.id, "Отличный выбор!", reply_markup=types.ReplyKeyboardRemove())
                else:
                    bot.send_message(message.chat.id, f"{num}")
                print(num)
                bot.send_message(message.chat.id, "Введите коллвичество еды (в граммах)")
                bot.register_next_step_handler(message, check_weight)
            except:
                bot.send_message(message.chat.id,
                                f'Введите номер еды цифрой от 1 до {i - 1} или напишите "Отменить"')
                bot.register_next_step_handler(message, check_number)

    def check_weight(message):
        if (message.text.lower() == 'отменить'):
            pass
        else:
            try:
                global weight
                weight = float(message.text)
                print(weight)

                bot.send_message(message.chat.id,
                                f'{axc[int(num) - 1][0]}, {axc[int(num) - 1][1]}, вес: {weight} г')
                d = {"Название": axc[int(num) - 1][0], 'ккал': float(axc[int(num) - 1][1]) * weight / 100.0,
                    'Белки (г)': float(axc[num - 1][2]) * weight / 100.0,
                    'Жиры (г)': float(axc[num - 1][3]) * weight / 100.0,
                    'Углеводы (г)': float(axc[num - 1][4]) * weight / 100.0,
                    'вес (г)': weight}
                eaten_food.append(d)
                bot.send_message(message.chat.id, 'Записал :)')
                print(eaten_food)
            except:
                bot.send_message(message.chat.id,
                                'Пожалуйста введите Вес (г) цифрами и без пробелов или напишите "Отменить"')
                bot.register_next_step_handler(message, check_weight)

    if (i != 1):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        yes_btn = types.KeyboardButton("да")
        no_btn = types.KeyboardButton("нет")
        markup.add(yes_btn, no_btn)
        bot.send_message(message.chat.id, text="Хотите что-то добавить в список сьеденноего?", reply_markup=markup)
        bot.register_next_step_handler(message, check)
    else:
        bot.send_message(message.chat.id, "Увы, по вашему запросу не было найдено ни одного блюда.")


bot.polling(none_stop=True, interval=0)
