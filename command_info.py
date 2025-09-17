import sqlite3 # БД
import config # ПУТЬ К БД ОТ ТУДА БЕРУ

db = sqlite3.connect(config.sqlite_base) # подключение БД
cursor = db.cursor() # курсор 

def stats(id: int) -> str: 
    i = cursor.execute(f'SELECT * FROM users_bot WHERE id = ?', (id,)).fetchall()[0]
    date = cursor.execute(f'SELECT * FROM date_users WHERE id = ?', (id,)).fetchall()[0]
    text = f"""<b>Общая информация</b>
ID: {id}
Время первого появления: {date[1]} по МСК
Время последнего решенного задания: {date[2]} по МСК

<b>Русский язык</b>
Общие значения: верных {i[3]} из {i[2]} | {int(round(i[3] / i[2], 2) * 100) if i[2] != 0  else 0}%
4 Задание: верных {i[5]} из {i[4]} | {int(round(i[5] / i[4], 2) * 100) if i[4] != 0  else 0}%
5 Задание: верных {i[7]} из {i[6]} | {int(round(i[7] / i[6], 2) * 100) if i[6] != 0  else 0}%
6 Задание: верных {i[9]} из {i[8]} | {int(round(i[9] / i[8], 2) * 100) if i[8] != 0  else 0}%
7 Задание: верных {i[11]} из {i[10]} | {int(round(i[11] / i[10], 2) * 100) if i[10] != 0  else 0}%
8 Задание: {i[13]}/{i[14]}/{i[15]} из {i[12]} | {f'{int(round(i[13] / i[12], 2) * 100)}% {int(round(i[14] / i[12], 2) * 100)}% {int(round(i[15] / i[12], 2) * 100)}%' if i[12] != 0  else '0% 0% 0%'}  
13 Задание: верных {i[17]} из {i[16]} | {int(round(i[17] / i[16], 2) * 100) if i[16] != 0  else 0}%
14 Задание: верных {i[19]} из {i[18]} | {int(round(i[19] / i[18], 2) * 100) if i[18] != 0  else 0}%
15 Задание: верных {i[21]} из {i[20]} | {int(round(i[21] / i[20], 2) * 100) if i[20] != 0  else 0}%
16 Задание: верных {i[23]} из {i[22]} | {int(round(i[23] / i[22], 2) * 100) if i[22] != 0  else 0}%
17 Задание: верных {i[25]} из {i[24]} | {int(round(i[25] / i[24], 2) * 100) if i[24] != 0  else 0}%
18 Задание: верных {i[27]} из {i[26]} | {int(round(i[27] / i[26], 2) * 100) if i[26] != 0  else 0}%
19 Задание: верных {i[29]} из {i[28]} | {int(round(i[29] / i[28], 2) * 100) if i[28] != 0  else 0}%
20 Задание: верных {i[31]} из {i[30]} | {int(round(i[31] / i[30], 2) * 100) if i[30] != 0  else 0}%
"""
    return text