from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
            types.BotCommand("help", "Вывести справку"),
            types.BotCommand("description", "Описание бота"),
            types.BotCommand("registration", "Предложить вакансию"),
            types.BotCommand("channel", "Я бот для регистрации заявок в "),

        ]
    )
