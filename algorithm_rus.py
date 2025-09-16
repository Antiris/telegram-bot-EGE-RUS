import sqlite3
import config
import random
import bot_text

db = sqlite3.connect(config.sqlite_base)
cursor = db.cursor()


def rus_4(id: int) -> str:
    r = cursor.execute('SELECT yes_tip FROM rus_4').fetchall()
    yes_tip = [r[i][0] for i in range(len(r))]
    lower_t = [r[i][0].replace('Ё', 'е').lower() for i in range(len(r))]
    r = cursor.execute('SELECT no_tip FROM rus_4').fetchall()
    no_tip = [r[i][0] for i in range(len(r))]
    c = random.randint(2, 4)
    sd = [1, 2, 3]
    while len(set(sd)) != 5:
        sd = []
        s = random.sample(yes_tip, c)
        l = random.sample(no_tip, 5 - c)
        for i in s: sd.append(i.replace('Ё', 'е').lower())
        for i in l: sd.append(i.replace('Ё', 'е').lower())
    k = []
    d = ''
    k.extend(s)
    k.extend(l)
    random.shuffle(k)
    for i in s: d += f'{k.index(i) +  1}'
    m = [i.replace('Ё', 'е').lower() for i in k]
    sp = ''
    for i in m: sp += yes_tip[lower_t.index(i.lower())] + '\n'

    cursor.execute(f'UPDATE otvet_users SET reserve = "{sp}" WHERE id = {id}')
    cursor.execute(f'UPDATE otvet_users SET key = {"".join(sorted(d))} WHERE id = {id}')
    db.commit()

    text = f"""4 Задание ЕГЭ русский язык | Источник: Генератор
    
Укажите варианты ответов, в которых ВЕРНО выделена буква, обозначающая ударный гласный звук. Запишите номера ответов.

1) {k[0]}
2) {k[1]}
3) {k[2]}
4) {k[3]}
5) {k[4]}"""

    return text

def rus_5(id: int) -> str:
    r = cursor.execute('SELECT * FROM rus_5').fetchall()
    yes_tip = [r[i] for i in range(len(r)) if r[i][1] == 1]
    r = cursor.execute('SELECT * FROM rus_5').fetchall()
    no_tip = [r[i][0] for i in range(len(r)) if r[i][1] == 0]
    s = random.sample(yes_tip, 1)
    key = s[0][2]
    l = random.sample(no_tip, 4)
    k = []
    k.append(s[0][0])
    k.extend(l)
    random.shuffle(k)
    q = 'В одном из приведённых ниже предложений НЕВЕРНО употреблено выделенное слово. Исправьте лексическую ошибку, подобрав к выделенному слову пароним. Запишите подобранное слово.'
    cursor.execute(f'UPDATE otvet_users SET key = "{key}" WHERE id = {id}')
    db.commit()
    text = f"""5 Задание ЕГЭ русский язык | Источник: Генератор
    
{q}

{k[0]}

{k[1]}

{k[2]}

{k[3]}

{k[4]}"""
    
    return text

def rus_6(id: int) -> str:
    r = cursor.execute('SELECT * FROM rus_6').fetchall()
    i = random.randint(0, len(r) - 1)
    if r[i][1] == 1:
        q = 'Отредактируйте предложение: исправьте лексическую ошибку, исключив лишнее слово. Выпишите это слово.'
    else:
        q = 'Отредактируйте предложение: исправьте лексическую ошибку, заменив неверно употреблённое слово. Запишите подобранное слово, соблюдая нормы современного русского литературного языка.'
    cursor.execute(f'UPDATE otvet_users SET key = "{r[i][2]}" WHERE id = {id}')
    cursor.execute(f'UPDATE otvet_users SET reserve = "{r[i][3]}" WHERE id = {id}')
    db.commit()
    text = f"""6 Задание ЕГЭ русский язык | Источник: {r[i][4]}

{q}

{r[i][0]}"""
    return text

# Допилить алгоритм!
def rus_7(id: int) -> str:
    r = cursor.execute('SELECT * FROM rus_7').fetchall()
    yes_tip = [r[i] for i in range(len(r)) if r[i][1] == 1]
    r = cursor.execute('SELECT * FROM rus_7').fetchall()
    no_tip = [r[i][0] for i in range(len(r)) if r[i][1] == 0]
    s = random.sample(yes_tip, 1)
    key = s[0][2]
    l = random.sample(no_tip, 4)
    q = 0
    kt = key.split(' [или] ')
    while len(l) != q:
        d = 0
        while len(kt) != d:
            if kt[d].upper() in l[q]:
                l = random.sample(no_tip, 4)
                q = 0
                d = 0
            else:
                d += 1
        q += 1           
    k = []
    k.append(s[0][0])
    k.extend(l)
    random.shuffle(k)
    q = 'В одном из выделенных ниже слов допущена ошибка в образовании формы слова. Исправьте ошибку и запишите слово правильно.'
    cursor.execute(f'UPDATE otvet_users SET key = "{key}" WHERE id = {id}')
    db.commit()
    text = f"""7 Задание ЕГЭ русский язык | Источник: Генератор
    
{q}

{k[0]}

{k[1]}

{k[2]}

{k[3]}

{k[4]}"""
    return text

def rus_8(id: int) -> str:
    slow = bot_text.slow
    r = cursor.execute('SELECT * FROM rus_8').fetchall()
    no_tip = [r[i] for i in range(len(r)) if r[i][1] == 0]
    yes_tip1 = [r[i] for i in range(len(r)) if r[i][1] == 1]
    yes_tip2 = [r[i] for i in range(len(r)) if r[i][1] == 2]
    yes_tip3 = [r[i] for i in range(len(r)) if r[i][1] == 3]
    yes_tip4 = [r[i] for i in range(len(r)) if r[i][1] == 4]
    yes_tip5 = [r[i] for i in range(len(r)) if r[i][1] == 5]
    yes_tip6 = [r[i] for i in range(len(r)) if r[i][1] == 6]
    yes_tip7 = [r[i] for i in range(len(r)) if r[i][1] == 7]
    yes_tip8 = [r[i] for i in range(len(r)) if r[i][1] == 8]
    spn = random.sample(no_tip, 4)
    k = random.sample(range(1, 9), 5)
    yes_tip = []
    for j in k: yes_tip += [(random.choice(eval(f'yes_tip{j}')))]
    sp = []
    sp.extend(spn)
    sp.extend(yes_tip)
    random.shuffle(sp)
    spb = [i[1] for i in sp]
    s = ''
    for i in k: s += f'{spb.index(i) + 1}'
    q = 'Установите соответствие между грамматическими ошибками и предложениями, в которых они допущены: к каждой позиции первого столбца подберите соответствующую позицию из второго столбца.'
    text = f"""8 Задание ЕГЭ русский язык | Источник: Генератор

{q}

A) {slow[k[0]]}
Б) {slow[k[1]]}
В) {slow[k[2]]}
Г) {slow[k[3]]}
Д) {slow[k[4]]}

1) {sp[0][0]}
2) {sp[1][0]}
3) {sp[2][0]}
4) {sp[3][0]}
5) {sp[4][0]}
6) {sp[5][0]}
7) {sp[6][0]}
8) {sp[7][0]}
9) {sp[8][0]}
"""
    cursor.execute(f'UPDATE otvet_users SET key = "{s}" WHERE id = {id}')
    db.commit()
    return text

# -------------- РУС 15
def rus_15(id: int) -> str:
    r = cursor.execute('SELECT * FROM rus_15').fetchall()
    i = random.randint(0, len(r) - 1)
    q = 'Укажите все цифры, на месте которых пишется ' + 'Н' * r[i][1] + '.'
    cursor.execute(f'UPDATE otvet_users SET key = "{r[i][2]}" WHERE id = {id}')
    text = f'15 Задание ЕГЭ русский язык | Источник: {r[i][3]}\n\n{q}\n\n{r[i][0]}'
    db.commit()
    return text