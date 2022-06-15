import telebot
import calc
import sqlite3
from telebot import types
import datetime
from datetime import timedelta
import math

bot = telebot.TeleBot('5510516119:AAFv8yr225_zo-Q9d8ao5QhBggFM7E9c44U')

con = sqlite3.connect("food.db", check_same_thread=False)
con2 = sqlite3.connect("users.db", check_same_thread=False)
con3 = sqlite3.connect("eaten.db", check_same_thread=False)

cur = con.cursor()
cur2 = con2.cursor()
cur3 = con3.cursor()

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
        sql = f"SELECT * FROM food WHERE name LIKE '%{x}%'"
    cur.execute(sql)
    con.commit()
    return (cur.fetchmany(10))

def Add_user(list):
    cur2.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?)", list)
    con2.commit()

def Add_food(list):
    cur.execute("INSERT INTO food VALUES(?, ?, ?, ?, ?)", list)
    con.commit()

def Add_eaten(list):
    cur3.execute("INSERT INTO eaten VALUES(?, ?, ?, ?)", list)
    con3.commit()

def Print_One(var):
    name = var[0]
    weight = var[1]
    output = f"SELECT * FROM food WHERE name LIKE '{name}'"
    cur.execute(output)
    line = cur.fetchone()
    return line

def Auto_clear_eaten(now):
    today = now.day
    previous_date = now - timedelta(days=1)
    yesterday = previous_date.day
    cur3.execute(f"DELETE FROM eaten WHERE date NOT IN ({yesterday}, {today}) ")


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
                markup.add(btn1, btn2, btn3)
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
                list_db = [message.chat.id, gender, age, weight, height, kf, mode]

                cur2.execute("SELECT * FROM users WHERE id = '%d' " % message.chat.id)
                test = cur2.fetchone()
                if test == None:
                    Add_user(list_db)
                else:
                    cur2.execute('''UPDATE users SET sex = ?, age = ?, weight = ?, height = ?, activity = ?, goal = ? 
                    WHERE id = ?''', [gender, age, weight, height, kf, mode, message.chat.id])
                con2.commit()

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
    cur2 = con2.cursor()
    user_id = message.chat.id

    cur2.execute("SELECT * FROM users WHERE id = '%i' " % user_id)
    parametrs = cur2.fetchone()
    if parametrs != None:
        gender = parametrs[1]
        age = parametrs[2]
        weight = parametrs[3]
        height = parametrs[4]
        activity = parametrs[5]
        mode = parametrs[6]
        bot.send_message(message.chat.id, f'{calc.Day_kcal(gender, age, weight, height, mode)}')
        bot.send_message(message.chat.id,"Чтобы изменить свои параметры, используйте функцию \"/add_norm_kcal\"")

    else:
        bot.send_message(message.chat.id, "Параметры не заполнены")
        bot.register_next_step_handler(message, norm_kcal)

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
                food_db = (name_self, ccal_self * weight_self / 100.0, prot_self * weight_self / 100.0, fats_self * weight_self / 100.0, cbh_self * weight_self / 100.0)
                Add_food(food_db)

                now = datetime.datetime.now()
                eaten_db = (message.chat.id, name_self, weight_self, now.day)
                Add_eaten(eaten_db)
            except:
                bot.send_message(message.chat.id,
                                 'Пожалуйста введите Вес (г) цифрами и без пробелов или напишите "Отменить"')
                bot.register_next_step_handler(message, input_weight)

    bot.register_next_step_handler(message, input_name)

@bot.message_handler(commands=['count_food'])
def count_food(message):
    ccal = 0
    prot = 0
    fat = 0
    cb = 0
    bot.send_message(message.chat.id, 'ща скажу')

    now = datetime.datetime.now()
    Auto_clear_eaten(now)
    day = now.day
    id = message.chat.id

    cur3.execute(f"SELECT * FROM eaten WHERE id = {id}")
    res = cur3.fetchall()
    yesterday = []
    today = []
    for x in res:
        if (math.fabs(day - x[3])) > 0: yesterday.append([x[1], x[2]])
        else: today.append([x[1], x[2]])
    if yesterday: bot.send_message(message.chat.id, "Вчера вы съели: ")
    else: bot.send_message(message.chat.id, "Вчера вы ничего не съели")
    for var in yesterday:
        d = Print_One(var)
        ccal += d[1]
        prot += d[2]
        fat += d[3]
        cb += d[4]
        bot.send_message(message.chat.id,
                         f'Название: {d[0]}\nKкал: {d[1]}\nБелки: {d[2]}\nЖиры: {d[3]}\nУглеводы: {d[4]}\nВес: {var[1]} (г)')

    if today: bot.send_message(message.chat.id, "Сегодня вы съели: ")
    else: bot.send_message(message.chat.id, "Сегодня вы ничего не съели")
    for var in today:
        d = Print_One(var)
        ccal += d[1]
        prot += d[2]
        fat += d[3]
        cb += d[4]
        d = Print_One(var)
        bot.send_message(message.chat.id,
                         f'Название: {d[0]}\nKкал: {d[1]}\nБелки: {d[2]}\nЖиры: {d[3]}\nУглеводы: {d[4]}\nВес: {var[1]} (г)')
    if ccal + cb + fat + prot != 0:
        bot.send_message(message.chat.id,
                    f'итого: ккал: {ccal}\nБелки (г): {prot}\nЖиры (г): {fat}\n Углеводы (г): {cb}')

    bot.send_message(message.chat.id, "Если вы хотите очистить весь список, введите команду: /clear_eaten ")

@bot.message_handler(commands=['clear_eaten'])
def clear_eaten(meaasage):
    cur3.execute(f"DELETE FROM eaten WHERE id = {meaasage.chat.id}")
    con3.commit()
    bot.send_message(meaasage.chat.id, "Изменения внесены успешно")


@bot.message_handler(content_types=['text'])
def handle_text(message):

    print(message.chat.id)
    axc = Search_name(str(message.text).lower())
    print(axc)
    global i
    i = 1
    for example in axc:
        bot.send_message(message.chat.id, f'Название: {example[0]}\nккал: {example[1]}\nБелки: {example[2]}, Жиры: {example[3]}, Углеводы: {example[4]}\nНОМЕР: {i}')
        i+=1

    def check(message):

        if (message.text.lower() == 'да'):
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

                now = datetime.datetime.now()
                eaten_db = (message.chat.id, axc[int(num) - 1][0], weight, now.day)
                Add_eaten(eaten_db)
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
