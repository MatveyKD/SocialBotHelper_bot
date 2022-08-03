#!/usr/bin/python
# -*- coding: UTF-8 -*-

import telebot
import json
import time
import os
from dotenv import load_dotenv


load_dotenv()

bot = telebot.TeleBot(os.getenv("TOKEN"))


#-----------------------------------------HELP--Помощь----------------------------------------------#
@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, '''
    Социальный чат-бот помощник направлен на определение и помощь в коррекции психологических состояний.
<b>Результаты, полученные без участия специалиста не воспринимайте всерьёз.</b>\n
Список основных команд бота:
    /help - краткое описание бота;
    /start - полное описание бота;
    /completeTest_depressive - пройти тест на депрессию;
    /completeTest_vygoranie - пройти тест на профессиональное выгорание;
    /completeTest_optimism - пройти тест на оптимизм;
    /completeTest_PersonType - пройти тест на тип личности;
    /ShowMyResults - показать мои результаты по всем пройденным тестам (<u>последние прохождения для каждого теста</u>);
    /ResetAllResults - сбросить результаты по всем пройденным тестам <b>без возможности восстановления</b>;
    /Tips - показать советы по психологическим темам.''', parse_mode= 'html')

#-----------------------------------------HELP---Помощь--------------------------------------------#



#-----------------------------------------START--Полное описание----------------------------------------------#
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, '''Вас приветствует <b>Социальный чат-бот помощник</b>. 
Этот бот предзначен для определения психологических состояний с помощью следущих тестов:
    1. Тест на депрессию
    2. Тест на оптимизм
    3. Тест на выгорание
    4. Тест на тип личности
    
Также бот записывает результаты всех пройденных тестов. 
Благодаря этому Вы можете в любой момент посмотреть их, вписав команду <b>/ShowMyResults</b>.

Если вам вдруг понадобится сбросить все результаты, то используйте команду <b>/ResetAllResults</b>.


Чтобы просмотреть краткое описание бота, используйте команду <b>/help</b>.

Список всех команд:
    /help - краткое описание бота;
    /start - полное описание бота;
    /completeTest_depressive - пройти тест на депрессию;
    /completeTest_vygoranie - пройти тест на профессиональное выгорание;
    /completeTest_optimism - пройти тест на оптимизм;
    /completeTest_PersonType - пройти тест на тип личности;
    /ShowMyResults - показать мои результаты по всем пройденным тестам (<u>последние прохождения для каждого теста</u>);
    /ResetAllResults - сбросить результаты по всем пройденным тестам <b>без возможности восстановления</b>;
    /Tips - показать советы по психологическим темам.



<code>Бот разработан с помощью Python 3.9.0</code>''', parse_mode='html')
#-----------------------------------------START--Полное описание----------------------------------------------#







#-START------------------------------------Depressive----Тест на депрессию-----------------------------------------START-
@bot.message_handler(commands=['completeTest_depressive'])
def Depressive(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = telebot.types.KeyboardButton('Старт')
    button2 = telebot.types.KeyboardButton('Назад')
    keyboard.add(button1, button2)
    bot.send_message(message.chat.id, 'Данный тест основан на общепринятой методике диагностики депрессивных состояний разработанной Аароном Бэком в 1961 году.\nВ нём 20 вопросов. Для каждого вопроса выберите один из четырёх вариантов ответа, наиболее точно описывающий ваше состояние. Нажмите <b>Старт</b>, чтобы начать.', reply_markup=keyboard, parse_mode='html')
    bot.register_next_step_handler(message, nextChecker_Depressive)

def nextChecker_Depressive(message):
    global questionsDepressive
    if message.text == "Старт":
        readHeandle = open("depressive.json", 'r', encoding="utf-8")
        questionsDepressive = json.load(readHeandle)["questions"]
        readHeandle.close()

        resultsDepressive["results"][message.chat.id] = {"result": 0, "curr_index": 0}

        asks_Depressive(message)
    elif message.text == "Назад":
        bot.send_message(message.chat.id, "Вы вернулись в главное меню", reply_markup=telebot.types.ReplyKeyboardRemove())
    else:
        bot.send_message(message.chat.id, '''Пожалуйста, введите:
    <b>Старт</b> - чтобы начать
    <b>Назад</b> - чтобы вернуться в главное меню''', parse_mode='html')
        bot.register_next_step_handler(message, nextChecker_Depressive)

def get_keyboard_depressive(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = telebot.types.KeyboardButton(questionsDepressive[resultsDepressive["results"][message.chat.id]["curr_index"]]["answers"][0])
    button2 = telebot.types.KeyboardButton(questionsDepressive[resultsDepressive["results"][message.chat.id]["curr_index"]]["answers"][1])
    button3 = telebot.types.KeyboardButton(questionsDepressive[resultsDepressive["results"][message.chat.id]["curr_index"]]["answers"][2])
    button4 = telebot.types.KeyboardButton(questionsDepressive[resultsDepressive["results"][message.chat.id]["curr_index"]]["answers"][3])
    keyboard.add(button1)
    keyboard.add(button2)
    keyboard.add(button3)
    keyboard.add(button4)
    return keyboard

def asks_Depressive(message):
    curr_index = resultsDepressive["results"][message.chat.id]["curr_index"]
    if curr_index > 0:
        if message.text in questionsDepressive[curr_index-1]["answers"]:
            resultsDepressive["results"][message.chat.id]["result"] += questionsDepressive[curr_index-1]["answers"].index(message.text)
        else:
            bot.send_message(message.chat.id, "Пожалуйста, выберите одну из кнопок")
            bot.register_next_step_handler(message, asks_Depressive)
            return
    if curr_index < len(questionsDepressive):
        bot.send_message(message.chat.id, str(curr_index+1) + ". " + questionsDepressive[curr_index]["ask"], reply_markup=get_keyboard_depressive(message))
        curr_index += 1
        resultsDepressive["results"][message.chat.id]["curr_index"] += 1
        bot.register_next_step_handler(message, asks_Depressive)
    else:
        print(resultsDepressive)
        TestResultCalculation_Depressive(message)

def TestResultCalculation_Depressive(message):
    result = resultsDepressive['results'][message.chat.id]["result"]
    bot.send_message(message.chat.id, "Ваш результат - " + str(result) + "\n")

    if result <= 9:
        bot.send_message(message.chat.id, 'Это говорит о том, что у вас полностью отсутствуют признаки депрессии или они незначительны и временны. Ваше эмоциональное состояние не вызывает опасений.\nЕсли отметка приближена к 9, то рекомендовано больше времени посвящать отдыху, чтобы не допустить развитие депрессивного состояния.', reply_markup=telebot.types.ReplyKeyboardRemove())
    elif result <= 15:
        bot.send_message(message.chat.id, 'Это говорит о первых симптомах депрессии. Ваше состояние субдепрессивное, что не является психопатологией и не свидетельствует о нарушениях социального характера. При таких результатах пациенту рекомендуется проконсультироваться со специалистом, чтобы проконтролировать ситуацию.', reply_markup=telebot.types.ReplyKeyboardRemove())
    elif result <= 19:
        bot.send_message(message.chat.id, 'Вы находитесь в стадии умеренного депрессивного состояния. В отличие от легкой формы депрессии, в данной ситуации характерные признаки проблем с психикой проявляются гораздо чаще. Такие люди больше грустят, устают быстрее обычного, теряют интерес к социальной жизни и испытывают постоянное чувство вины. Шкала депрессии Бека создана для выявления именно этой категории людей.', reply_markup=telebot.types.ReplyKeyboardRemove())
    elif result <= 29:
        bot.send_message(message.chat.id, 'Результат говорит о наличии средней тяжести депрессии. Такие пациенты жалуются на ухудшение аппетита и потерю сна. В их организме происходят не только эмоциональные сбои, но и физические. На этой стадии перестает вырабатываться гормон счастья. Пытаясь его восполнить, люди часто прибегают к алкоголю и наркотическим средствам, что приводит к зависимости или летальному исходу. Такое состояние пациента нуждается в срочном лечении. По статистике, примерно 70% людей с подобными симптомами пытаются покончить с жизнью.', reply_markup=telebot.types.ReplyKeyboardRemove())
    elif result <= 63:
        bot.send_message(message.chat.id, 'Критические показатели свидетельствуют о признаках глубокой депрессии. У пациентов с подобными психологическими проблемами наблюдается постоянное гнетущее состояние. Они ненавидят себя и чувствуют себя бесполезными. Такие люди подвержены резкими эмоциональным переменам. Они не представляют своего будущего, легко впадают в истерику, склонны к суициду и насилию. Эта категория должна находится под постоянным наблюдением специалиста, во избежание негативных последствий.', reply_markup=telebot.types.ReplyKeyboardRemove())

    if result > 15:
        bot.send_message(message.chat.id, 'Рекомендуем обратиться к специалисту.')


    #---------Сохранение результатов--------------------------#
    file = open("results.json", 'r')
    Dict = json.load(file)
    file.close()
    Dict["Depressive"][message.chat.id] = result
    file = open("results.json", 'w')
    file.write(json.dumps(Dict))
    file.close()
    # ---------Сохранение результатов--------------------------#


#END--------------------------------------Depressive----Тест на депрессию----------------------------------------END-





#-START------------------------------------Optimism----Тест на оптимизм-----------------------------------------START-
@bot.message_handler(commands=['completeTest_optimism'])
def Optimism(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = telebot.types.KeyboardButton('Старт')
    button2 = telebot.types.KeyboardButton('Назад')
    keyboard.add(button1, button2)
    bot.send_message(message.chat.id, 'Этот психологический тест на оптимизм создан для определения уровня оптимизма и пессимзма. В нём 10 вопросов. На каждый вопрос вам будет дано 4 варианта ответа. Веберите тот, который наиболее точно описывает ваше состояние. Нажмите <b>Старт</b>, чтобы начать.', reply_markup=keyboard, parse_mode='html')
    bot.register_next_step_handler(message, nextChecker_Optimism)

def nextChecker_Optimism(message):
    global questionsOptimism
    if message.text == "Старт":
        readHeandle = open("optimism.json", 'r', encoding="utf-8")
        questionsOptimism = json.load(readHeandle)["questions"]
        readHeandle.close()

        resultsOptimism["results"][message.chat.id] = {"result": 0, "curr_index": 0}

        asks_Optimism(message)
    elif message.text == "Назад":
        bot.send_message(message.chat.id, "Вы вернулись в главное меню", reply_markup=telebot.types.ReplyKeyboardRemove())
    else:
        bot.send_message(message.chat.id, '''Пожалуйста, введите:
    <b>Старт</b> - чтобы начать
    <b>Назад</b> - чтобы вернуться в главное меню''', parse_mode='html')
        bot.register_next_step_handler(message, nextChecker_Optimism)

def get_keyboard_optimism(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = telebot.types.KeyboardButton(questionsOptimism[resultsOptimism["results"][message.chat.id]["curr_index"]]["answers"][0])
    button2 = telebot.types.KeyboardButton(questionsOptimism[resultsOptimism["results"][message.chat.id]["curr_index"]]["answers"][1])
    button3 = telebot.types.KeyboardButton(questionsOptimism[resultsOptimism["results"][message.chat.id]["curr_index"]]["answers"][2])
    button4 = telebot.types.KeyboardButton(questionsOptimism[resultsOptimism["results"][message.chat.id]["curr_index"]]["answers"][3])
    keyboard.add(button1)
    keyboard.add(button2)
    keyboard.add(button3)
    keyboard.add(button4)
    return keyboard

def asks_Optimism(message):
    curr_index = resultsOptimism["results"][message.chat.id]["curr_index"]
    if curr_index > 0:
        if message.text in questionsOptimism[curr_index-1]["answers"]:
            resultsOptimism["results"][message.chat.id]["result"] += questionsOptimism[curr_index-1]["answers"].index(message.text)
        else:
            bot.send_message(message.chat.id, "Пожалуйста, выберите одну из кнопок")
            bot.register_next_step_handler(message, asks_Optimism)
            return
    if curr_index < len(questionsOptimism):
        bot.send_message(message.chat.id, str(curr_index+1) + ". " + questionsOptimism[curr_index]["ask"], reply_markup=get_keyboard_optimism(message))
        curr_index += 1
        resultsOptimism["results"][message.chat.id]["curr_index"] += 1
        bot.register_next_step_handler(message, asks_Optimism)
    else:
        print(resultsDepressive)
        TestResultCalculation_Optimism(message)

def TestResultCalculation_Optimism(message):
    result = resultsOptimism['results'][message.chat.id]["result"]
    bot.send_message(message.chat.id, "Ваш результат - " + str(result) + "\n")

    if result <= 5:
        bot.send_message(message.chat.id, 'У вас обнаружены призрнаки выраженного пессимизма. Вы всегда ожидаете невезения, никогда не надеятесь на хорошее. Вы всегда подозреваете подвох и мало на что соглашаетесь. Из-за этого вы можете упустить шанс или потерять что-то ценное.', reply_markup=telebot.types.ReplyKeyboardRemove())
    elif result <= 10:
        bot.send_message(message.chat.id, 'Это означает, что у вас присутствуют признаки пессимизма. Вы пессимистично смотрите на мир, события, проишествия. Но это не мешает вам в нужный момент включить ум, правильно проанализировать ситуацию и принять правильное решение.', reply_markup=telebot.types.ReplyKeyboardRemove())
    elif result < 20:
        bot.send_message(message.chat.id, 'Результаты теста показывают, что вы реалист. В вашей картине мира нет четкого деления на черное и белое, во главе всегда стоит ум и холодный расчет. Вы в люой момент способны взвесить все за и против, сосчитать количество плюсов и минусов в любой ситуации и сделать правильный выбор. ', reply_markup=telebot.types.ReplyKeyboardRemove())
    elif result < 25:
        bot.send_message(message.chat.id, 'Это означает, что у вас присутствуют признаки оптимизма. Вы оптимистично смотрите на мир, события, проишествия. Но это не мешает вам в нужный момент включить мозг, правильно проанализировать ситуацию и принять правильное решение.', reply_markup=telebot.types.ReplyKeyboardRemove())
    else:
        bot.send_message(message.chat.id, 'У вас обнаружены призрнаки выраженного оптимизма. Вы всегда оптимистичны, ожидаете только хорошего, никогда не грустите. Вы очень доверчивы к людям, и многие этим пользуются.', reply_markup=telebot.types.ReplyKeyboardRemove())



    #---------Сохранение результатов--------------------------#
    file = open("results.json", 'r')
    Dict = json.load(file)
    file.close()
    Dict["Optimism"][message.chat.id] = result
    file = open("results.json", 'w')
    file.write(json.dumps(Dict))
    file.close()
    # ---------Сохранение результатов--------------------------#


#END--------------------------------------Optimism----Тест на оптимизм----------------------------------------END-







#-START------------------------------------Vygoranie----Тест на выгорание-----------------------------------------START-
@bot.message_handler(commands=['completeTest_vygoranie'])
def Vygoranie(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = telebot.types.KeyboardButton('Старт')
    button2 = telebot.types.KeyboardButton('Назад')
    keyboard.add(button1, button2)
    bot.send_message(message.chat.id, '''Тест на профессиональное выгорание предназначен для выявления выраженности проявлений выгорания по 3 шкалам:
    «Эмоциональное истощение»
    «Деперсонализация»
    «Редукция личных достижений»''', reply_markup=keyboard, parse_mode='html')
    time.sleep(2)

    bot.send_message(message.chat.id, '''После прохождения будут выданы результаты по всем 3 шкалам, а также общий результат (сумму результатов 3 шкал), который и будет тяжестью профессионального выгорания.''', reply_markup=keyboard, parse_mode='html')
    time.sleep(2)

    bot.send_message(message.chat.id, '''Для каждого вопроса выберите 1 из 7 вариантов ответа, показывающий частоту того или иного переживания.
Нажмите <b>Старт</b>, чтобы начать.''', reply_markup=keyboard, parse_mode='html')
    bot.register_next_step_handler(message, nextChecker_Vygoranie)

def nextChecker_Vygoranie(message):
    global questionsVygoranie
    if message.text == "Старт":
        readHeandle = open("vygoranie.json", 'r', encoding="utf-8")
        questionsVygoranie = json.load(readHeandle)
        readHeandle.close()

        resultsVygoranie["results"][message.chat.id] = {
            "result": {
                "EmocIst": 0,
                "Depress": 0,
                "Reduc": 0,
            },
            "curr_index": 0,
            "curr_cat": "EmocIst"
        }

        bot.send_message(message.chat.id, "Категория <b>«ЭМОЦИОНАЛЬНОЕ ИСТОЩЕНИЕ»</b>", parse_mode='html')
        asks_Vygoranie(message)
    elif message.text == "Назад":
        bot.send_message(message.chat.id, "Вы вернулись в главное меню", reply_markup=telebot.types.ReplyKeyboardRemove())
    else:
        bot.send_message(message.chat.id, '''Пожалуйста, введите:
    <b>Старт</b> - чтобы начать
    <b>Назад</b> - чтобы вернуться в главное меню''', parse_mode='html')
        bot.register_next_step_handler(message, nextChecker_Vygoranie)

def get_keyboard_vygoranie(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = telebot.types.KeyboardButton("Никогда")
    button2 = telebot.types.KeyboardButton("Очень редко")
    button3 = telebot.types.KeyboardButton("Редко")
    button4 = telebot.types.KeyboardButton("Иногда")
    button5 = telebot.types.KeyboardButton("Часто")
    button6 = telebot.types.KeyboardButton("Очень часто")
    button7 = telebot.types.KeyboardButton("Всегда")

    keyboard.add(button1, button2, button3)
    keyboard.add(button4)
    keyboard.add(button5, button6, button7)
    return keyboard

def asks_Vygoranie(message):
    curr_index = resultsVygoranie["results"][message.chat.id]["curr_index"]
    curr_cat = resultsVygoranie["results"][message.chat.id]["curr_cat"]
    list_of_questions = [
        "Никогда", "Очень редко",
        "Редко", "Иногда",
        "Часто", "Очень часто",
        "Всегда",
    ]
    if curr_index > 0:
        if message.text in list_of_questions:
            if curr_cat == "Reduc":
                list_of_questions = [
                    "Всегда", "Очень часто",
                    "Часто", "Иногда",
                    "Редко", "Очень редко",
                    "Никогда",
                ]
            resultsVygoranie["results"][message.chat.id]["result"][curr_cat] += list_of_questions.index(message.text)
        else:
            bot.send_message(message.chat.id, "Пожалуйста, выберите одну из кнопок")
            bot.register_next_step_handler(message, asks_Vygoranie)
            return
    if curr_index < len(questionsVygoranie[curr_cat]):
        bot.send_message(message.chat.id, str(curr_index+1) + ". " + questionsVygoranie[curr_cat][curr_index]["ask"], reply_markup=get_keyboard_vygoranie(message))
        curr_index += 1
        resultsVygoranie["results"][message.chat.id]["curr_index"] += 1
        bot.register_next_step_handler(message, asks_Vygoranie)
    elif curr_cat != "Reduc":
        if curr_cat == "EmocIst":
            resultsVygoranie["results"][message.chat.id]["curr_cat"] = "Depress"
            resultsVygoranie["results"][message.chat.id]["curr_index"] = 0
            bot.send_message(message.chat.id, "Категория <b>«ДЕПЕРСОНАЛИЗАЦИЯ»</b>", parse_mode='html')
        elif curr_cat == "Depress":
            resultsVygoranie["results"][message.chat.id]["curr_cat"] = "Reduc"
            resultsVygoranie["results"][message.chat.id]["curr_index"] = 0
            bot.send_message(message.chat.id, "Категория <b>«РЕДУКЦИЯ ЛИЧНЫХ ДОСТИЖЕНИЙ»</b>", parse_mode='html')
        asks_Vygoranie(message)
    else:
        print(resultsVygoranie)
        TestResultCalculation_Vygoranie(message)

def TestResultCalculation_Vygoranie(message):
    results = resultsVygoranie['results'][message.chat.id]["result"]
    result_EmocIst = results["EmocIst"]
    result_Depress = results["Depress"]
    result_Reduc = results["Reduc"]

    time.sleep(3)
    #-------EmocIst-------------
    res = ""
    res += "Категория <b>«ЭМОЦИОНАЛЬНОЕ ИСТОЩЕНИЕ»</b>\n"
    res += "Результат - " + str(result_EmocIst) + "\n"
    if result_EmocIst <= 10: res += "<b>Крайне низкое</b>"
    elif result_EmocIst <= 20: res += "<b>Низкое</b>"
    elif result_EmocIst <= 30: res += "<b>Среднее</b>"
    elif result_EmocIst <= 40: res += "<b>Высокое</b>"
    else: res += "<b>Крайне высокое</b>"
    res += " значение по шкале «Эмоциональное истощение»"
    bot.send_message(message.chat.id, res, parse_mode='html', reply_markup=telebot.types.ReplyKeyboardRemove())

    time.sleep(2)
    # -------Depress-------------
    res = ""
    res += "Категория <b>«ДЕПЕРСОНАЛИЗАЦИЯ»</b>\n"
    res += "Результат - " + str(result_Depress) + "\n"
    if result_Depress <= 5:
        res += "<b>Крайне низкое</b>"
    elif result_Depress <= 11:
        res += "<b>Низкое</b>"
    elif result_Depress <= 17:
        res += "<b>Среднее</b>"
    elif result_Depress <= 23:
        res += "<b>Высокое</b>"
    else:
        res += "<b>Крайне высокое</b>"
    res += " значение по шкале «Деперсонализация»"
    bot.send_message(message.chat.id, res, parse_mode='html', reply_markup=telebot.types.ReplyKeyboardRemove())

    time.sleep(2)
    # -------Reduc-------------
    res = ""
    res += "Категория <b>«РЕДУКЦИЯ ЛИЧНЫХ ДОСТИЖИЕНИЙ»</b>\n"
    res += "Результат - " + str(result_Reduc) + "\n"
    if result_Reduc <= 5:
        res += "<b>Крайне низкое</b>"
    elif result_Reduc <= 11:
        res += "<b>Низкое</b>"
    elif result_Reduc <= 17:
        res += "<b>Среднее</b>"
    elif result_Reduc <= 23:
        res += "<b>Высокое</b>"
    else:
        res += "<b>Крайне высокое</b>"
    res += " значение по шкале «Редукция личных достижений»"
    bot.send_message(message.chat.id, res, parse_mode='html', reply_markup=telebot.types.ReplyKeyboardRemove())

    result_shkals = [
        result_EmocIst,
        result_Depress,
        result_Reduc
    ]

    time.sleep(3)
    summ_result = result_EmocIst + result_Depress + result_Reduc
    summ_message = ""
    summ_message += "<b>Общий результат - " + str(summ_result) + "</b>\n"
    if summ_result <= 23:
        summ_message += "<b><u>Крайне низкая</u></b>"
    elif summ_result <= 49:
        summ_message += "<b><u>Низкая<u>/</b>"
    elif summ_result <= 75:
        summ_message += "<b><u>Средняя</u></b>"
    elif summ_result <= 101:
        summ_message += "<b><u>Высокая</u></b>"
    else:
        summ_message += "<b><u>Крайне высокая</u></b>"
    summ_message += " вероятность профессионального выгорания"

    bot.send_message(message.chat.id, summ_message, parse_mode='html', reply_markup=telebot.types.ReplyKeyboardRemove())



    #---------Сохранение результатов--------------------------#
    file = open("results.json", 'r')
    Dict = json.load(file)
    file.close()
    Dict["Vygoranie"][message.chat.id] = result_shkals
    file = open("results.json", 'w')
    file.write(json.dumps(Dict))
    file.close()
    # ---------Сохранение результатов--------------------------#


#END--------------------------------------Vygoranie----Тест на выгорание----------------------------------------END-






#-START------------------------------------PersonType----Тест на тип личности-----------------------------------------START-
@bot.message_handler(commands=['completeTest_PersonType'])
def PersonType(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = telebot.types.KeyboardButton('Старт')
    button2 = telebot.types.KeyboardButton('Назад')
    keyboard.add(button1, button2)
    bot.send_message(message.chat.id, '''Тест на тип личности создан для определения осноного типа личности из 4:
    1. Холерик
    2. Сангвиник
    3. Флегматик
    4. Меланхолик
В тесте 56 вопросов-утверждений, по 14 на каждый тип личности. Для каждого утверждения выберите:
<b>"ДА"</b> - если вы согласны с ним
<b>"НЕТ"</b> - если не согласны

После прохождения будут выданы результаты по всем 4 типам, Ваш основной тип - тот, по которому вы набрали больше всего баллов, а также краткая информация по этому типу личности. 
Нажмите <b>Старт</b>, чтобы начать.''', reply_markup=keyboard, parse_mode='html')
    bot.register_next_step_handler(message, nextChecker_PersonType)

def nextChecker_PersonType(message):
    global questionsPersonType
    if message.text == "Старт":
        readHeandle = open("PersonType.json", 'r', encoding="utf-8")
        questionsPersonType = json.load(readHeandle)
        readHeandle.close()

        resultsPersonType["results"][message.chat.id] = {
            "result": {
                "Holeric": 0,
                "Sangvinic": 0,
                "Flegmatic": 0,
                "Melanholic": 0
            },
            "curr_index": 0,
            "show_index": 0,
            "curr_cat": "Holeric"
        }
        asks_PersonType(message)
    elif message.text == "Назад":
        bot.send_message(message.chat.id, "Вы вернулись в главное меню", reply_markup=telebot.types.ReplyKeyboardRemove())
    else:
        bot.send_message(message.chat.id, '''Пожалуйста, введите:
    <b>Старт</b> - чтобы начать
    <b>Назад</b> - чтобы вернуться в главное меню''', parse_mode='html')
        bot.register_next_step_handler(message, nextChecker_PersonType)

def get_keyboard_person_type(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = telebot.types.KeyboardButton("Да")
    button2 = telebot.types.KeyboardButton("Нет")

    keyboard.add(button1, button2)
    return keyboard

def asks_PersonType(message):
    curr_index = resultsPersonType["results"][message.chat.id]["curr_index"]
    show_index = resultsPersonType["results"][message.chat.id]["show_index"]
    curr_cat = resultsPersonType["results"][message.chat.id]["curr_cat"]
    if curr_index > 0:
        if message.text.lower() == "да":
            resultsPersonType["results"][message.chat.id]["result"][curr_cat] += 1
        elif message.text.lower() != "нет":
            bot.send_message(message.chat.id, "Пожалуйста, выберите одну из кнопок")
            bot.register_next_step_handler(message, asks_PersonType)
            return
    if curr_index % len(questionsPersonType[curr_cat]) != 0 or curr_index == 0:
        bot.send_message(message.chat.id, str(show_index+1) + ". " + questionsPersonType[curr_cat][curr_index]["ask"], reply_markup=get_keyboard_person_type(message))
        curr_index += 1
        resultsPersonType["results"][message.chat.id]["curr_index"] += 1
        resultsPersonType["results"][message.chat.id]["show_index"] += 1
        bot.register_next_step_handler(message, asks_PersonType)
    elif curr_cat != "Melanholic":
        if curr_cat == "Holeric":
            resultsPersonType["results"][message.chat.id]["curr_cat"] = "Sangvinic"
        elif curr_cat == "Sangvinic":
            resultsPersonType["results"][message.chat.id]["curr_cat"] = "Flegmatic"
        elif curr_cat == "Flegmatic":
            resultsPersonType["results"][message.chat.id]["curr_cat"] = "Melanholic"
        resultsPersonType["results"][message.chat.id]["curr_index"] = 0
        asks_PersonType(message)
    else:
        print(resultsPersonType)
        TestResultCalculation_PersonType(message)

def TestResultCalculation_PersonType(message):
    results = resultsPersonType['results'][message.chat.id]["result"]
    result_Holeric = results["Holeric"]
    result_Sangvinic = results["Sangvinic"]
    result_Flegmatic = results["Flegmatic"]
    result_Melanholic = results["Melanholic"]


    time.sleep(3)
    #-------Holeric-------------
    res = ""
    res += "Темперамент <b>«ХОЛЕРИК»</b>\n"
    res += "Результат - " + str(result_Holeric) + "\n"
    if result_Holeric >= 10:
        res += "<b>Доминирующий</b>"
    elif result_Holeric >= 5:
        res += "<b>Умеренный</b>"
    else:
        res += "<b>Слабо выраженный</b>"
    res += " темперамент"
    bot.send_message(message.chat.id, res, parse_mode='html', reply_markup=telebot.types.ReplyKeyboardRemove())


    time.sleep(2)
    # -------Sangvinic-------------
    res = ""
    res += "Темперамент <b>«САНГВИНИК»</b>\n"
    res += "Результат - " + str(result_Sangvinic) + "\n"
    if result_Sangvinic >= 10:
        res += "<b>Доминирующий</b>"
    elif result_Sangvinic >= 5:
        res += "<b>Умеренный</b>"
    else:
        res += "<b>Слабо выраженный</b>"
    res += " темперамент"
    bot.send_message(message.chat.id, res, parse_mode='html', reply_markup=telebot.types.ReplyKeyboardRemove())


    time.sleep(2)
    # -------Flegmatic-------------
    res = ""
    res += "Темперамент <b>«ФЛЕГМАТИК»</b>\n"
    res += "Результат - " + str(result_Flegmatic) + "\n"
    if result_Flegmatic >= 10:
        res += "<b>Доминирующий</b>"
    elif result_Flegmatic >= 5:
        res += "<b>Умеренный</b>"
    else:
        res += "<b>Слабо выраженный</b>"
    res += " темперамент"
    bot.send_message(message.chat.id, res, parse_mode='html', reply_markup=telebot.types.ReplyKeyboardRemove())


    time.sleep(2)
    # ------Melanholic-------------
    res = ""
    res += "Темперамент <b>«МЕЛАНХОЛИК»</b>\n"
    res += "Результат - " + str(result_Melanholic) + "\n"
    if result_Melanholic >= 10:
        res += "<b>Доминирующий</b>"
    elif result_Melanholic >= 5:
        res += "<b>Умеренный</b>"
    else:
        res += "<b>Слабо выраженный</b>"
    res += " темперамент"
    bot.send_message(message.chat.id, res, parse_mode='html', reply_markup=telebot.types.ReplyKeyboardRemove())


    result_temp = [
        result_Holeric,
        result_Sangvinic,
        result_Flegmatic,
        result_Melanholic
    ]

    time.sleep(3)
    about_temp_mess = ""
    most_res = max(result_temp)
    index = result_temp.index(most_res)
    if index == 0:
        most_temp = "Холерик"
        about_temp_mess = "Вспыльчивость, легкая агрессивность и непостоянство — это самые заметные черты холериков. Несмотря на это, они обычно не злопамятны и довольно отходчивы. Холерики способны организовывать людей и быстро принимать сложные решения. Также имеется некоторая склонность к доминации над остальными людьми, из-за чего агрессивность холериков может оказаться неприятной. Монотонность — их злейший враг, им быстро надоедает заниматься одним и тем же делом, накопившаяся энергия требует ее немедленно «потратить»."
    elif index == 1:
        most_temp = "Сангвиник"
        about_temp_mess = "Сангвиники легки на подъем и жизнерадостны. Как и флегматики, они стараются доводить дело до конца, однако ничто не мешает им рвануть вперед, к приключениям. Сангвиникам присущи критическое мышление и самоирония, их речь обычно несколько тороплива, но отчётлива, как и жестикуляция. Люди с этим темпераментом легко приспосабливаются к любым условиям."
    elif index == 2:
        most_temp = "Флегматик"
        about_temp_mess = "Флегматики отличаются неторопливостью, старательностью и вдумчивостью. Как правило, имеют склонность к порядку, предпочитают работать в привычной обстановке и доводить дело до конца независимо от обстоятельств. Крайне спокойны. К ним присущи такие качества, как уравновешенность, надёжность, трудолюбие. Флегматика практически невозможно вывести из себя, даже в критических стрессовых ситуациях подобные люди способны сохранять самоконтроль."
    else:
        most_temp = "Меланхолик"
        about_temp_mess = "Скрытные, склонные к депрессии и приступам отчаянья, меланхолики, это обычно вялые и пессимистичные люди. Они неспособны на постоянный монотонный труд, им требуется прибегать к регулярным коротким перерывам для того чтобы, стабилизировать психологическое состояние. Им сложно проявлять активность и жизнерадостность. Но тем не менее, меланхоликам присущи доброта, сдержанность, осторожность, развитая интуиция."

    summ_message = ""
    summ_message += "<b>Наиболее выраженный темперамент - " + most_temp + "</b>\n"

    bot.send_message(message.chat.id, summ_message, parse_mode='html', reply_markup=telebot.types.ReplyKeyboardRemove())
    time.sleep(1.5)
    bot.send_message(message.chat.id, about_temp_mess, parse_mode='html')



    #---------Сохранение результатов--------------------------#
    file = open("results.json", 'r')
    Dict = json.load(file)
    file.close()
    Dict["PersonType"][message.chat.id] = result_temp
    file = open("results.json", 'w')
    file.write(json.dumps(Dict))
    file.close()
    # ---------Сохранение результатов--------------------------#


#END--------------------------------------PersonType----Тест на тип личности----------------------------------------END-










#--START--------------ShowMyResults----Показать результаты-------------------------------------START----#
@bot.message_handler(commands=['ShowMyResults'])
def ShowResults(message):
    #PARSING---------------------#
    handle = open("results.json", 'r')
    Dict = json.load(handle)
    handle.close()
    # PARSING---------------------#


    #DEPRESSIVE------------------------------start------------------------------------------#
    depressiveRes = Dict["Depressive"].get(str(message.chat.id))
    if depressiveRes:
        deprMessage = f'''<b>Тест на депрессию:</b>
    Результат - {depressiveRes}\n\n'''
        if depressiveRes <= 55:
            deprMessage += 'Это говорит о том, что у вас полностью отсутствуют признаки депрессии или они незначительны и временны. Ваше эмоциональное состояние не вызывает опасений.\nЕсли отметка приближена к 9, то рекомендовано больше времени посвящать отдыху, чтобы не допустить развитие депрессивного состояния.'
        elif depressiveRes <= 15:
            deprMessage += 'Это говорит о первых симптомах депрессии. Ваше состояние субдепрессивное, что не является психопатологией и не свидетельствует о нарушениях социального характера. При таких результатах пациенту рекомендуется проконсультироваться со специалистом, чтобы проконтролировать ситуацию.'
        elif depressiveRes <= 19:
            deprMessage += 'Вы находитесь в стадии умеренного депрессивного состояния. ' \
                           'В отличие от легкой формы депрессии, в данной ситуации характерные признаки проблем с психикой проявляются гораздо чаще. ' \
                           'Такие люди больше грустят, устают быстрее обычного, теряют интерес к социальной жизни и испытывают постоянное чувство вины. ' \
                           'Шкала депрессии Бека создана для выявления именно этой категории людей.'
        elif depressiveRes <= 29:
            deprMessage += 'Результат говорит о наличии средней тяжести депрессии. ' \
                           'Такие пациенты жалуются на ухудшение аппетита и потерю сна. ' \
                           'В их организме происходят не только эмоциональные сбои, но и физические. ' \
                           'На этой стадии перестает вырабатываться гормон счастья. Пытаясь его восполнить, ' \
                           'люди часто прибегают к алкоголю и наркотическим средствам, что приводит к зависимости или летальному исходу. ' \
                           'Такое состояние пациента нуждается в срочном лечении. ' \
                           'По статистике, примерно 70% людей с подобными симптомами пытаются покончить с жизнью.'
        elif depressiveRes <= 63:
            deprMessage += 'Критические показатели свидетельствуют о признаках глубокой депрессии. ' \
                           'У пациентов с подобными психологическими проблемами наблюдается постоянное гнетущее состояние. ' \
                           'Они ненавидят себя и чувствуют себя бесполезными. ' \
                           'Такие люди подвержены резкими эмоциональным переменам. ' \
                           'Они не представляют своего будущего, легко впадают в истерику, склонны к суициду и насилию. ' \
                           'Эта категория должна находится под постоянным наблюдением специалиста, во избежание негативных последствий.'
        bot.send_message(message.chat.id, deprMessage, parse_mode='html')
    else:
        bot.send_message(message.chat.id, "<b>Тест на депрессию:</b>\nНе пройден (пройти - /completeTest_depressive)", parse_mode='html')
    # DEPRESSIVE--------------------------------end------------------------------------------------#




    # Optimism------------------------------start------------------------------------------#
    optimismRes = Dict["Optimism"].get(str(message.chat.id))
    if optimismRes:
        optMessage = f'''<b>Тест на оптимизм:</b>
    Результат - {optimismRes}\n\n'''
        if optimismRes <= 5:
            optMessage += 'У вас обнаружены призрнаки выраженного пессимизма. Вы всегда ожидаете невезения, никогда не надеятесь на хорошее. Вы всегда подозреваете подвох и мало на что соглашаетесь. Из-за этого вы можете упустить шанс или потерять что-то ценное.'
        elif optimismRes <= 10:
            optMessage += 'Это означает, что у вас присутствуют признаки пессимизма. Вы пессимистично смотрите на мир, события, проишествия. Но это не мешает вам в нужный момент включить ум, правильно проанализировать ситуацию и принять правильное решение.'
        elif optimismRes < 20:
            optMessage += 'Результаты теста показывают, что вы реалист. В вашей картине мира нет четкого деления на черное и белое, во главе всегда стоит ум и холодный расчет. Вы в люой момент способны взвесить все за и против, сосчитать количество плюсов и минусов в любой ситуации и сделать правильный выбор.'
        elif optimismRes <= 25:
            optMessage += 'Это означает, что у вас присутствуют признаки оптимизма. Вы оптимистично смотрите на мир, события, проишествия. Но это не мешает вам в нужный момент включить мозг, правильно проанализировать ситуацию и принять правильное решение.'
        elif optimismRes <= 30:
            optMessage += 'У вас обнаружены призрнаки выраженного оптимизма. Вы всегда оптимистичны, ожидаете только хорошего, никогда не грустите. Вы очень доверчивы к людям, и многие этим пользуются.'
        bot.send_message(message.chat.id, optMessage, parse_mode='html')
    else:
        bot.send_message(message.chat.id, "<b>Тест на оптимизм:</b>\nНе пройден (пройти - /completeTest_optimism)", parse_mode='html')
    # OPTIMISM--------------------------------end------------------------------------------------#



    # Vygoranie--------------------------------start------------------------------------------------#
    results = Dict["Vygoranie"].get(str(message.chat.id))
    if results:
        result_EmocIst = results[0]
        result_Depress = results[1]
        result_Reduc = results[2]

        res = "<b>Тест на выгорание:</b>\n\n"
        # -------EmocIst-------------
        res += "Категория «ЭМОЦИОНАЛЬНОЕ ИСТОЩЕНИЕ»\n"
        res += "Результат - " + str(result_EmocIst) + "\n"
        if result_EmocIst <= 10:
            res += "<b>Крайне низкое</b>"
        elif result_EmocIst <= 20:
            res += "<b>Низкое</b>"
        elif result_EmocIst <= 30:
            res += "<b>Среднее</b>"
        elif result_EmocIst <= 40:
            res += "<b>Высокое</b>"
        else:
            res += "<b>Крайне высокое</b>"
        res += " значение по шкале «Эмоциональное истощение»"
        res += "\n\n"

        # -------Depress-------------
        res += "Категория «ДЕПЕРСОНАЛИЗАЦИЯ»\n"
        res += "Результат - " + str(result_Depress) + "\n"
        if result_Depress <= 5:
            res += "<b>Крайне низкое</b>"
        elif result_Depress <= 11:
            res += "<b>Низкое</b>"
        elif result_Depress <= 17:
            res += "<b>Среднее</b>"
        elif result_Depress <= 23:
            res += "<b>Высокое</b>"
        else:
            res += "<b>Крайне высокое</b>"
        res += " значение по шкале «Деперсонализация»"
        res += "\n\n"

        # -------Reduc-------------
        res += "Категория «РЕДУКЦИЯ ЛИЧНЫХ ДОСТИЖИЕНИЙ»\n"
        res += "Результат - " + str(result_Reduc) + "\n"
        if result_Reduc <= 5:
            res += "<b>Крайне низкое</b>"
        elif result_Reduc <= 11:
            res += "<b>Низкое</b>"
        elif result_Reduc <= 17:
            res += "<b>Среднее</b>"
        elif result_Reduc <= 23:
            res += "<b>Высокое</b>"
        else:
            res += "<b>Крайне высокое</b>"
        res += " значение по шкале «Редукция личных достижений»"
        res += "\n\n\n"


        #------------Summa-------------------
        summ_result = result_EmocIst + result_Depress + result_Reduc
        summ_message = ""
        summ_message += "<b>Общий результат - " + str(summ_result) + "</b>\n"
        if summ_result <= 23:
            summ_message += "<b><u>Крайне низкая</u></b>"
        elif summ_result <= 49:
            summ_message += "<b><u>Низкая</u></b>"
        elif summ_result <= 75:
            summ_message += "<b><u>Средняя</u></b>"
        elif summ_result <= 101:
            summ_message += "<b><u>Высокая</u></b>"
        else:
            summ_message += "<b><u>Крайне высокая</u></b>"
        summ_message += " вероятность профессионального выгорания"

        res += summ_message
        bot.send_message(message.chat.id, res, parse_mode='html', reply_markup=telebot.types.ReplyKeyboardRemove())
    else:
        bot.send_message(message.chat.id, "<b>Тест на профессиональное выгорание:</b>\nНе пройден (пройти - /completeTest_vygoranie)", parse_mode='html')
    # Vygoranie--------------------------------end------------------------------------------------#




    #PersonType----------------------------start---------------------------------------------------#
    results = Dict['PersonType'].get(str(message.chat.id))
    if results != None:
        result_Holeric = results[0]
        result_Sangvinic = results[1]
        result_Flegmatic = results[2]
        result_Melanholic = results[3]

        res = "<b>Тест на тип личности:</b>\n\n"

        # -------Holeric-------------
        res += "Темперамент <b>«ХОЛЕРИК»</b>\n"
        res += "Результат - " + str(result_Holeric) + "\n"
        if result_Holeric >= 10:
            res += "<b>Доминирующий</b>"
        elif result_Holeric >= 5:
            res += "<b>Умеренный</b>"
        else:
            res += "<b>Слабо выраженный</b>"
        res += " темперамент"


        res += "\n\n"
        # -------Sangvinic-------------
        res += "Темперамент <b>«САНГВИНИК»</b>\n"
        res += "Результат - " + str(result_Sangvinic) + "\n"
        if result_Sangvinic >= 10:
            res += "<b>Доминирующий</b>"
        elif result_Sangvinic >= 5:
            res += "<b>Умеренный</b>"
        else:
            res += "<b>Слабо выраженный</b>"
        res += " темперамент"


        res += "\n\n"
        # -------Flegmatic-------------
        res += "Темперамент <b>«ФЛЕГМАТИК»</b>\n"
        res += "Результат - " + str(result_Flegmatic) + "\n"
        if result_Flegmatic >= 10:
            res += "<b>Доминирующий</b>"
        elif result_Flegmatic >= 5:
            res += "<b>Умеренный</b>"
        else:
            res += "<b>Слабо выраженный</b>"
        res += " темперамент"


        res += "\n\n"
        # ------Melanholic-------------
        res += "Темперамент <b>«МЕЛАНХОЛИК»</b>\n"
        res += "Результат - " + str(result_Melanholic) + "\n"
        if result_Melanholic >= 10:
            res += "<b>Доминирующий</b>"
        elif result_Melanholic >= 5:
            res += "<b>Умеренный</b>"
        else:
            res += "<b>Слабо выраженный</b>"
        res += " темперамент"


        res += "\n\n\n"

        result_temp = [
            result_Holeric,
            result_Sangvinic,
            result_Flegmatic,
            result_Melanholic
        ]


        most_res = max(result_temp)
        index = result_temp.index(most_res)
        if index == 0:
            most_temp = "Холерик"
        elif index == 1:
            most_temp = "Сангвиник"
        elif index == 2:
            most_temp = "Флегматик"
        else:
            most_temp = "Меланхолик"

        res += "<b>Наиболее выраженный темперамент - <u>" + most_temp + "</u></b>"

        bot.send_message(message.chat.id, res, parse_mode='html', reply_markup=telebot.types.ReplyKeyboardRemove())
    else:
        bot.send_message(message.chat.id, "<b>Тест на тип личности:</b>\nНе пройден (пройти - /completeTest_PersonType)", parse_mode='html')
    #PersonType-------------------------------end--------------------------------------------------#
#--END--------------ShowMyResults----Показать результаты-------------------------------------END----#




#--START--------------ResetAllResults----Сбросить результаты--------------------START----#
@bot.message_handler(commands=['ResetAllResults'])
def ResetResults(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = telebot.types.KeyboardButton('Сброс')
    button2 = telebot.types.KeyboardButton('Отмена')
    keyboard.add(button1, button2)
    bot.send_message(message.chat.id, "Вы точно хотите сбросить все результаты?\nПосле сброса результаты будут утеряны\n<b><u>БЕЗ возможности восстановления</u></b>", parse_mode='html', reply_markup=keyboard)
    bot.register_next_step_handler(message, AskForReset)

def AskForReset(message):
    if message.text == "Сброс":
        Reset(message)
        bot.send_message(message.chat.id, "Результаты сброшены успешно.", reply_markup=telebot.types.ReplyKeyboardRemove())
    elif message.text == "Отмена" or message.text == "Назад":
        bot.send_message(message.chat.id, "Операция отменена.", reply_markup=telebot.types.ReplyKeyboardRemove())
    else:
        bot.send_message(message.chat.id, "Текст не распознан. Пожалуйста, введите <b>Сброс</b> для сброса, <b>Отмена</b> для отмены")
        bot.register_next_step_handler(message, AskForReset)


def Reset(message):
    file = open("results.json", 'r')
    Dict = json.load(file)
    file.close()
    Dict["Depressive"].pop(str(message.chat.id), None)
    Dict["Optimism"].pop(str(message.chat.id), None)
    Dict["Vygoranie"].pop(str(message.chat.id), None)
    Dict["PersonType"].pop(str(message.chat.id), None)
    file = open("results.json", 'w')
    file.write(json.dumps(Dict))
    file.close()

#--END--------------ResetAllResults----Сбросить результаты--------------------END----#






#--START--------------Tips----Советы--------------------START----#
@bot.message_handler(commands=['Tips'])
def Tips(message):
    global TipsTopics
    #-------parsing----------------#
    file = open("tips.json", 'r', encoding="UTF-8")
    TipsTopics = json.load(file)
    file.close()
    #-------parsing----------------#


    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    for topic in list(TipsTopics.keys()):
        keyboard.add(telebot.types.KeyboardButton(topic))
    keyboard.add(telebot.types.KeyboardButton("Назад"))

    bot.send_message(message.chat.id, "Выберите психологическую тему, которая вас интересует, и по которой вы хотите получить советы", parse_mode='html', reply_markup=keyboard)
    bot.register_next_step_handler(message, AskForTips)

def AskForTips(message):
    MessUp = message.text[0].upper() + message.text.lower()[1::]
    if MessUp in list(TipsTopics.keys()):
        UsersTopics[message.chat.id] = MessUp

        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        for topic in list(TipsTopics[MessUp].keys()):
            keyboard.add(telebot.types.KeyboardButton(topic))
        keyboard.add(telebot.types.KeyboardButton("Назад"))

        bot.send_message(message.chat.id, "Теперь введите то, что вас интересует в этой теме", parse_mode='html', reply_markup=keyboard)
        bot.register_next_step_handler(message, AskForTopic)
    elif MessUp == "Назад":
        bot.send_message(message.chat.id, "Вы вернулись в главное меню", reply_markup=telebot.types.ReplyKeyboardRemove())
    else:
        bot.send_message(message.chat.id, '''Текст не распознан. Пожалуйста, введите 1 из 4 вариантов ответа, в зависимости от того, что вас интересует:
    1. Депрессия
    2. Выгорание
    3. Оптимизм''')
        bot.register_next_step_handler(message, AskForTips)


def AskForTopic(message):
    MessUp = message.text[0].upper() + message.text.lower()[1::]
    if MessUp in TipsTopics[UsersTopics[message.chat.id]]:
        bot.send_message(message.chat.id, MessUp + ": " + TipsTopics[UsersTopics[message.chat.id]][MessUp], reply_markup=telebot.types.ReplyKeyboardRemove())
    elif MessUp == "Назад":
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        for topic in list(TipsTopics.keys()):
            keyboard.add(telebot.types.KeyboardButton(topic))
        keyboard.add(telebot.types.KeyboardButton("Назад"))

        bot.send_message(message.chat.id, "Вы вернулись к выбору темы. Выберите тему, по которой вы хотите получить психологические советы", reply_markup=keyboard)
        bot.register_next_step_handler(message, AskForTips)
    else:
        bot.send_message(message.chat.id, "Текст не распознан. Пожалуйста, выберите одну из кнопок, в зависимости от того, по чему вы хотите получить советы")
        bot.register_next_step_handler(message, AskForTopic)

#--END--------------Tips----Советы--------------------END----#


if __name__ == '__main__':
    resultsDepressive = {"results": {}}
    questionsDepressive = []

    resultsOptimism = {"results": {}}
    questionsOptimism = []

    resultsVygoranie = {"results": {}}
    questionsVygoranie = []

    resultsPersonType = {"results": {}}
    questionsPersonType = []

    TipsTopics = {}
    UsersTopics = {}

    bot.polling(none_stop=True)