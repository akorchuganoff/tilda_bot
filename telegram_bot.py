import asyncio
import logging

from aiogram import Bot, Dispatcher, executor, types

from additions import get_active_leads, remove_lead_by_id
# from browser_checker import main

TOKEN = '5284345962:AAGH3edR7JxyPDSsv7dSkvhQCek1Xs-QOdk'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

chat_ids = set()


@dp.message_handler(commands=['start', 'help'], commands_prefix='/')
async def send_welcome(message: types.Message):
    chat_ids.add(message.from_user.id)
    text_of_message = 'Приветствую. Я высылаю заявки\n'
    text_of_message += 'Используйте команду "/help" - чтобы увидеть подсказку\n'
    text_of_message += 'Используйте команду "/leads" - чтобы получить список активных заявок\n'
    text_of_message += 'Используйте коменду "/ok <Номер заявки>" - чтобы отметить заявку обработанной'

    await bot.send_message(message.from_user.id, text_of_message)


@dp.message_handler(commands=['leads'], commands_prefix='/')
async def return_active_leads(message: types.Message):
    leads = get_active_leads()

    await message.reply('Сейчас я вышлю вам активные заявки')

    if len(leads) == 0:
        await bot.send_message(message.from_user.id, 'У вас нет необработанных заявок')

    for lead in leads:
        print(lead)
        text_of_message = ''
        text_of_message += f'Заявка от {lead[0]} - {lead[2]}\n'
        text_of_message += f'Номер телефона: {lead[4]}\n'
        text_of_message += f'Имя: {lead[5]}\n'
        data = lead[6].replace("|", "\n")
        text_of_message += f'Данные заявки:\n{data}'
        await bot.send_message(message.from_user.id, text_of_message)


@dp.message_handler(commands=['ok'], commands_prefix='/')
async def remove_lead(message: types.Message):
    try:
        number = int(message.text.split(' ')[1])
    except Exception:
        await bot.send_message(message.from_user.id,
                               'Введите команду корректно. Номер должен быть'
                               ' целым числом и написан через пробел после команды')
        return False
    leads = get_active_leads()
    lead = leads[number - 1]
    lead_id = lead[1]
    done = remove_lead_by_id(lead_id)
    if done:
        text_of_message = f'Данная заявка была переведена в обработанные:\n\n'
        text_of_message += f'Заявка от {lead[0]} - {lead[2]}\n'
        text_of_message += f'Номер телефона: {lead[4]}\n'
        text_of_message += f'Имя: {lead[5]}\n'
        await bot.send_message(message.from_user.id, text_of_message)
    else:
        await bot.send_message(message.from_user.id, 'На сервере возникла ошибка. Ваш запрос не был исполнен')


async def periodic(sleep_for):
    while True:
        await asyncio.sleep(sleep_for)

        for chat_id in chat_ids:
            await bot.send_message(chat_id, 'Активные заявки')

        leads = get_active_leads()

        if len(leads) == 0:
            for chat_id in chat_ids:
                await bot.send_message(chat_id, 'У вас нет необработанных заявок')
        else:
            for lead in leads:
                text_of_message = ''
                text_of_message += f'Заявка от {lead[0]} - {lead[2]}\n'
                text_of_message += f'Номер телефона: {lead[4]}\n'
                text_of_message += f'Имя: {lead[5]}\n'
                data = lead[6].replace("|", "\n")
                text_of_message += f'Данные заявки:\n{data}'
                for chat_id in chat_ids:
                    await bot.send_message(chat_id, text_of_message, disable_notification=True)

# async def check_browser(sleep_for):
#     while True:
#         await asyncio.sleep(sleep_for)
#         await main()



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(periodic(60*60*12))
    # loop.create_task(check_browser())
    executor.start_polling(dp, skip_updates=True)
