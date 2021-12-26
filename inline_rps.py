import telebot
import random
import threading
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
API_TOKEN = 'token'
bot = telebot.TeleBot(API_TOKEN)
games = {}
r_waiting_delay = 20
cleaning_delay = 20
r_start_delay = 40

def change_rps(msg_id,):
    try:
        games[msg_id][1].cancel()
        del games[msg_id]
        bot.edit_message_text(inline_message_id=msg_id, text='Сессия завершена, слишком много ждунов...', reply_markup=None)
    except Exception as e:
        print('*****')
        print("Warning!", e.__class__, "occurred.", 'Function: del_roulette')
        print('Details: ' + str(e))


def renew_rps(frst_plr, scnd_plr, frstp_name, scndp_name, frst_sign, scnd_sign, agreed=False):
    view_keyboard = InlineKeyboardMarkup().row(
    InlineKeyboardButton('✊', callback_data='rps_✊_' + frst_plr + '_' + scnd_plr + '_' + frstp_name + '_' + scndp_name + '_' + frst_sign + '_' + scnd_sign),
    InlineKeyboardButton('✋', callback_data='rps_✋_' + frst_plr + '_' + scnd_plr + '_' + frstp_name + '_' + scndp_name + '_' + frst_sign + '_' + scnd_sign),
    InlineKeyboardButton('✌️', callback_data='rps_✌️_' + frst_plr + '_' + scnd_plr + '_' + frstp_name + '_' + scndp_name + '_' + frst_sign + '_' + scnd_sign))

    if agreed:
        view_keyboard.row(InlineKeyboardButton('Выйти', callback_data='rps_leave_' + frst_plr + '_' + scnd_plr + '_' + frstp_name + '_' + scndp_name + '_' + frst_sign + '_' + scnd_sign))

    return view_keyboard


def check_win(call, info):
    if info[6] != '*' and info[7] != '*':
        initiator = "[" + info[4] + "](tg://user?id=" + str(info[2]) + ")"
        opponent = "[" + info[5] + "](tg://user?id=" + str(info[3]) + ")"

        if (info[6] == '✊' and info[7] == '✌️') or (info[6] == '✌️' and info[7] == '✋') or (info[6] == '✋' and info[7] == '✊'):
            msg_text = f'*Камень, ножницы, бумага*\n{initiator} {info[6]} vs {opponent} {info[7]}'
            msg_text += f'\n🏆 {initiator} победил!'
            bot.edit_message_text(inline_message_id=call.inline_message_id, text=msg_text + '',
                parse_mode='Markdown', reply_markup=None)
            games[call.inline_message_id][1].cancel()
            bot.answer_callback_query(call.id, 'Ты победил!')
        else:
            msg_text = f'*Камень, ножницы, бумага*\n{initiator} {info[6]} vs {opponent} {info[7]}'
            msg_text += f'\n🏆 {opponent} победил!'
            bot.edit_message_text(inline_message_id=call.inline_message_id, text=msg_text + '',
                parse_mode='Markdown', reply_markup=None)
            games[call.inline_message_id][1].cancel()
            bot.answer_callback_query(call.id, 'Ты победил!')
            
    bot.answer_callback_query(call.id, 'Ход сделан')
    games[call.inline_message_id][1].cancel()
    games[call.inline_message_id][1] = threading.Timer(cleaning_delay,
            change_rps, args=(call.inline_message_id,))
    games[call.inline_message_id][1].start()


@bot.inline_handler(lambda query: True)
def rps_game(inline_query):
    try:
        invite = InlineKeyboardMarkup().row(InlineKeyboardButton("Play",
            callback_data=f"rps_join_{inline_query.from_user.id}_0_{inline_query.from_user.first_name}_-_*_*"))

        initiator = "[" + inline_query.from_user.first_name + "](tg://user?id=" + str(inline_query.from_user.id) + ")"
        msg_text = f'*Камень, ножницы, бумага*\n⌛{initiator} ожидает оппонента...'

        rps = InlineQueryResultArticle('rock_paper_scissors', 'Rock, paper, scissors', InputTextMessageContent(msg_text, parse_mode='Markdown'), reply_markup=invite,
            description='Rock, paper, scissors by Zeus428',
            thumb_url='https://i.ibb.co/VLmWnqx/rps.jpg')

        bot.answer_inline_query(inline_query.id, [rps], is_personal=True, cache_time=10)
    except Exception as e:
        print('*****')
        print("Warning!", e.__class__, "occurred.", 'Function: rps_game')
        print('Details: ' + str(e))


@bot.callback_query_handler(func=lambda call: call.data.startswith("rps_"))
def rps_setup(call):
    try:
        players_inf = call.data.split('_')
        if players_inf[2] != '0' and players_inf[3] != '0' and players_inf[5] != '-':
            initiator = "[" + players_inf[4] + \
                "](tg://user?id=" + str(players_inf[2]) + ")"
            opponent = "[" + players_inf[5] + \
                "](tg://user?id=" + str(players_inf[3]) + ")"
        else:
            initiator = "[" + players_inf[4] + \
                "](tg://user?id=" + str(players_inf[2]) + ")"
            opponent = "[" + call.from_user.first_name + \
                "](tg://user?id=" + str(call.from_user.id) + ")"

        if 'join' in call.data[4:]:
            if players_inf[2] != str(call.from_user.id):
                msg_text = f'*Камень, ножницы, бумага*\n{initiator} vs {opponent}'
                bot.edit_message_text(inline_message_id=call.inline_message_id, text=msg_text,
                    parse_mode='Markdown', reply_markup=renew_rps(players_inf[2], str(call.from_user.id), players_inf[4], str(call.from_user.first_name), '*', '*', True))
                bot.answer_callback_query(call.id, 'Добро пожаловать в игру!')
                if call.inline_message_id in games:
                    games[call.inline_message_id][1].cancel()
                games[call.inline_message_id] = [0, threading.Timer(r_start_delay, change_rps, args=(call.inline_message_id,))]
                games[call.inline_message_id][1].start()
            else:
                bot.answer_callback_query(call.id, 'Нельзя играть самому с собой!')
                
        elif 'leave' in call.data[4:] and players_inf[5] != '-':
            if (str(call.from_user.id) == players_inf[2]) or (str(call.from_user.id) == players_inf[3]):
                join_button = ''
                if str(call.from_user.id) == players_inf[3]:
                    msg_text = f'*Камень, ножницы, бумага*\nИгра перезапущена\n⌛️{initiator} ожидает нового оппонента\n{opponent} ливнул...'
                    join_button = InlineKeyboardMarkup().row(InlineKeyboardButton("Play",
                        callback_data=f"rps_join_{players_inf[2]}_0_{players_inf[4]}_-_*_*"))
                    games[call.inline_message_id][1].cancel()
                    games[call.inline_message_id][1] = threading.Timer(r_waiting_delay,
                            change_rps, args=(call.inline_message_id,))
                    games[call.inline_message_id][1].start()

                else:
                    msg_text = f'*Камень, ножницы, бумага*\nИгра перезапущена\n⌛️{opponent} ожидает нового оппонента\n{initiator} ливнул...'
                    join_button = InlineKeyboardMarkup().row(InlineKeyboardButton("Play",
                        callback_data=f"rps_join_{players_inf[3]}_0_{players_inf[5]}_-_*_*"))
                    games[call.inline_message_id][1].cancel()
                    games[call.inline_message_id][1] = threading.Timer(r_waiting_delay,
                            change_rps, args=(call.inline_message_id,))
                    games[call.inline_message_id][1].start()
                
                bot.edit_message_text(inline_message_id=call.inline_message_id, text=msg_text, parse_mode='Markdown', reply_markup=join_button)
                bot.answer_callback_query(call.id, 'Быбы, ссыкло...')
            else:
                bot.answer_callback_query(call.id, 'Это не твоя игра, свали...')

        elif players_inf[5] != '-':
            button_data = call.data.split('_')
            if players_inf[2] == str(call.from_user.id) and players_inf[6] == '*': 
                msg_text = f'*Камень, ножницы, бумага*\n{initiator} vs {opponent}\n'
                msg_text += "[" + players_inf[4] + "](tg://user?id=" + str(players_inf[2]) + ") сделал ход...\n"
                msg_text += "Очередь [" + players_inf[5] + "](tg://user?id=" + str(players_inf[3]) + ")"
                bot.edit_message_text(inline_message_id=call.inline_message_id, text=msg_text,
                    parse_mode='Markdown', reply_markup=renew_rps(str(players_inf[2]), str(players_inf[3]), players_inf[4], players_inf[5], button_data[1], players_inf[7]))
                players_inf[6] = button_data[1]
                check_win(call, players_inf)

            elif players_inf[3] == str(call.from_user.id) and players_inf[7] == '*':
                msg_text = f'*Камень, ножницы, бумага*\n{initiator} vs {opponent}\n'
                msg_text += "[" + players_inf[5] + "](tg://user?id=" + str(players_inf[3]) + ") сделал ход...\n"
                msg_text += "Очередь [" + players_inf[4] + "](tg://user?id=" + str(players_inf[2]) + ")"
                bot.edit_message_text(inline_message_id=call.inline_message_id, text=msg_text,
                    parse_mode='Markdown', reply_markup=renew_rps(str(players_inf[2]), str(players_inf[3]), players_inf[4], players_inf[5], players_inf[6], button_data[1]))
                players_inf[7] = button_data[1]
                check_win(call, players_inf)
            else:
                bot.answer_callback_query(call.id, 'Ты уже сделал ход, жди!')
        else:
            bot.answer_callback_query(call.id, 'Ждем оппонента!')
    except Exception as e:
        print('*****')
        print("Warning!", e.__class__, "occurred.", 'Function: roulette_setup')
        print('Details: ' + str(e))

bot.infinity_polling()