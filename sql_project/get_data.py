# -*- coding: utf-8 -*-

#=====================================================================
# получение данных для main-скрипта

# данные получены из списка топ-250 фильмов по отзывам пользователей imdb.com

#--------------------------------------------------------------------
# функции для пользователя:

# - get_top250()
    # возвращает top250 - список списков вида:
    # ['1', 'Побег_из_Шоушенка', 'Frank_Darabont', '1994', '9.2', '1860788']
    # (позиция/ID, название, режиссер, год, рейтинг, количество голосов)

# - get_sample(sample_len, sample_num)
#     возвращает случайные выборки из списка top250
#     длиной = sample_len и в количестве = sample_num
#=====================================================================

import re
import random
import requests

#--------------------------------------------------------------------
# смена рабочей директории на директорию запуска скрипта:
#--------------------------------------------------------------------

import os
import sys

os.chdir(sys.path[0])

#--------------------------------------------------------------------
# константы:
#--------------------------------------------------------------------

# топ-250 фильмов по отзывам пользователей imdb.com
URL = 'http://www.imdb.com/chart/top'

# текстовый файл со списком топ-250 фильмов
# (на случай, если по какой-то причине загрузка URL не удастся)
TXT = './data/offline_top250.txt'

#=====================================================================
# вспомогательные функции:
#=====================================================================

#--------------------------------------------------
# 1. функции конвертации данных:
#--------------------------------------------------

def convert_elem_to_type(elem, type_base, type_reserve=None):
    # конвертация элемента elem в тип type_base (если это возможно)
    # type_reserve - запасной тип конвертации 

    try:
        return type_base(elem)

    except:
        if not type_reserve is None:
            return convert_elem_to_type(elem, type_reserve)
        else:
            return elem

def convert_list_to_type(my_list, type_base, type_reserve=None):
    # конвертация всех внутренних элементов списка списков в тип type_base 
    # type_reserve - запасной тип конвертации 

    return [[convert_elem_to_type(elem, type_base, type_reserve) for elem in line] for line in my_list]

#--------------------------------------------------
# 2. функции обработки непосредственно top250:
#--------------------------------------------------

def check_top250(top250):
    # проверка списка top250, исходя из assumptions:
    # - длина списка = 250
    # - длина каждого элемента списка = 6
    
    top250_error = ValueError('Ошибка! Список топ-250 имеет некорректную структуру!')

    if len(top250) != 250:
        raise top250_error

    for line in top250:
        if len(line) != 6:
            raise top250_error

def get_top250_from_html(html):
    # получение top250 из html ч/з регулярные выражения
    # а также запись данных из top250 в файл TXT
    
    #--------------------------------------------------
    # получение данных по паттернам:
    #--------------------------------------------------

    re_pattern_1 = 'td class="titleColumn"[\s\S]+?(\d+).[\s\S]+?title="([\s\S]+?) \(dir.\)'
    re_pattern_2 = '[\s\S]+?>([\s\S]+?)</a>[\s\S]+?span class="secondaryInfo">\(([\s\S]+?)\)<'
    re_pattern_3 = '[\s\S]+?strong title="([\s\S]+?) based on ([\s\S]+?) user'

    top250_raw = re.findall(re_pattern_1 + re_pattern_2 + re_pattern_3, html)

    #--------------------------------------------------
    # обработка top250_raw:
    #--------------------------------------------------

    top250 = [[item.replace(" ", "_").replace(",", "") for item in line] for line in top250_raw]

    for line in top250:
        line[1], line[2] = line[2], line[1] # смена местами режиссера и названия фильма

    #--------------------------------------------------
    # запись строкового top250 в файл:
    #--------------------------------------------------
  
    with open(TXT, 'w', encoding='utf-8') as f:
        top250_lines = [" ".join(line) for line in top250]
        f.write('\n'.join(top250_lines))
    f.close()

    #--------------------------------------------------
    # окончательный вид top250, проверка и возврат:
    #--------------------------------------------------

    top250 = convert_list_to_type(top250, int, type_reserve=float)
    check_top250(top250)

    return top250

def get_top250_from_txt():
    # получение top250 из TXT 
    # (ч/з обратное преобразование относительно записи в файл в get_top250_from_html)

    #--------------------------------------------------
    # получение строкового top250 из файла:
    #--------------------------------------------------

    with open(TXT, encoding='utf-8') as f:
        txt_data = f.read()
        top250 = [line.split() for line in txt_data.split('\n')]
    f.close()

    #--------------------------------------------------
    # окончательный вид top250, проверка и возврат:
    #--------------------------------------------------

    top250 = convert_list_to_type(top250, int, type_reserve=float)
    check_top250(top250)

    return top250

#=====================================================================
# функции для пользователя:
#=====================================================================

def get_top250(printout=False):
    # получение списка списков top250 - согласно описанию в шапке скрипта

    try:
        req = requests.get(URL)
        req.raise_for_status()
        
        html = req.text

        top250 = get_top250_from_html(html)
        
        if printout: 
            print("Данные успешно загружены из Сети!\n")

    except:
        top250 = get_top250_from_txt()
        
        if printout:
            print("При загрузке из Сети произошла ошибка, данные загружены из файла!\n")

    return top250

def get_sample(sample_len=10, sample_num=2, printout=False):
    # получение случайных выборок из top250 - согласно описанию в шапке скрипта

    samples = []

    top250 = get_top250(printout)
    top250_copy = top250[:]

    for idx in range(sample_num):
        
        random.shuffle(top250_copy) 
        samples.append(top250_copy[:sample_len])

        if printout:
            print('Sample {0} (len={1}):\n'.format(idx+1, len(samples[idx])))
        
            for item in samples[idx]:
                print(item)

            print()

    return samples

#=====================================================================
# тестирование:
#=====================================================================

def testing():
    # samples = get_sample()
    # samples = get_sample(printout=True)

    samples = get_sample(sample_len=3, sample_num=5, printout=True)
    
    print()
    print(len(samples))
    print(samples[-1])

if __name__ == '__main__':
    testing()

#=====================================================================