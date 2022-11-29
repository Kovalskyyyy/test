from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
btnMain = KeyboardButton("Главное меню")


# -------Registration Menu-------
btnRegOrg = KeyboardButton("Зарегестрироваться как организация")
btnRegFiz = KeyboardButton("Зарегестрироваться как физлицо")

RegistrationMenu = ReplyKeyboardMarkup(resize_keyboard = True).add(btnRegOrg, btnRegFiz)

# -------Main Menu-------
btnPrice = KeyboardButton("Прайс лист")
btnZakaz = KeyboardButton("Заказать")
btnOther = KeyboardButton("Другое")

mainMenu = ReplyKeyboardMarkup(resize_keyboard = True).add(btnPrice, btnZakaz, btnOther)


# -------Other Menu-------
btnInfo = KeyboardButton("Информация")

otherMenu = ReplyKeyboardMarkup(resize_keyboard = True).add(btnInfo, btnMain)


# -------Zakaz Menu-------
btnMenedjer = KeyboardButton("Заказать у менеджера")
btnSite = KeyboardButton("Заказать на сайте")

ZakazMenu = ReplyKeyboardMarkup(resize_keyboard = True).add(btnMenedjer, btnSite, btnMain)