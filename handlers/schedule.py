from aiogram import Bot, F, types, Router, Bot, Dispatcher
from aiogram.filters import CommandStart
from keyboards.kb import start_kb, all_groups
from functions.getGroup import parse_groups
from functions.getSchedule import get_schedule
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from database.db import DB

schedule = Router()

dp = Dispatcher()


class ScheduleState(StatesGroup):
    waiting_for_group = State()


@schedule.message(CommandStart())
async def send_welcome(message: types.Message):
    username = message.from_user.first_name
    user_id = message.from_user.id

    user_group = await DB.get_user_group(user_id)

    if user_group:
        text = f"✅ <b>{username}</b>, привет!\n\nВы выбирали группу: <b>{user_group}</b>\n\n🤖 Я - чат-бот МИФИ, который поможет тебе получить расписание занятий.\n\n"
    else:
        text = f"✅ <b>{username}</b>, привет!\n\n🤖 Я - чат-бот МИФИ, который поможет тебе получить расписание занятий.\n\n"

    await message.answer(text, parse_mode="html", reply_markup=start_kb())


@schedule.callback_query(F.data == 'go_start')
async def get_msg_group(callback: types.CallbackQuery, state: FSMContext):
    text = f"Выбери группу:"
    groups = await parse_groups()
    await callback.message.answer(text, parse_mode="html", reply_markup=all_groups(groups))
    await state.set_state(ScheduleState.waiting_for_group)



@schedule.callback_query(F.data.startswith('group_btn_'))
async def process_group(callback_query: types.CallbackQuery, state: FSMContext):
    if 'group_btn' in callback_query.data:
        group_id = callback_query.data.replace('group_btn', '')
        user_id = callback_query.from_user.id
        try:
            GET_SCHEDULE = await get_schedule(group_id)
            if GET_SCHEDULE:
                await callback_query.message.answer("Ваше расписание:")
                for item in GET_SCHEDULE:
                    text = f"День недели: {item['start_time']}\n"
                    text += f"Время: {item['start_time']} - {item['end_time']}\n"
                    text += f"Предмет: {item['subject']}\n"
                    text += f"Преподаватель: {item['lecturer']}\n"
                    text += f"Аудитория: {item['auditorium']}\n\n"
                    await callback_query.message.answer(text)
                    await DB.save_user_group(user_id, group_id)
            else:
                print(user_id, group_id)
                await DB.save_user_group(user_id, group_id)
                text = f"""
🤖 Похоже у указанной вами группы сегодня нет пар.

🚀  <a href="http://www.mephi3.ru/education_new/tehnikum/year_o.pdf"><b>Недельное расписание на текущую неделю МИФИ</b></a>\n
🚀  <a href="http://www.mephi3.ru/education_new/tehnikum/year_o_next.pdf"><b>Недельное расписание на следующую неделю МИФИ</b></a>
"""
                await callback_query.message.answer(text, parse_mode='html')
        except Exception as e:
            await callback_query.message.answer("Произошла ошибка при получении расписания.")
            print(e)
            await state.clear()
    else:
        print("Callback data doesn't contain 'group_btn'")

