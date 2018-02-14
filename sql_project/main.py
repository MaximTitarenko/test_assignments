# -*- coding: utf-8 -*-

#=====================================================================
# работа с базой данный ч/з SQL-запросы, согласно заданию:

#--------------------------------------------------------------------
# Программно создать базу данных SQLite3. 
# Создать 2 таблицы с одинаковой структурой 
# и заполнить их случайными данными при помощи SQL запросов. 
# Произвести сравнение 2-х таблиц и дополнить таблицу-2 данными из таблицы-1 (SQL-запрос).
#--------------------------------------------------------------------

# данные получены из списка топ-250 фильмов по отзывам пользователей imdb.com
# подробнее см скрипт get_data.py

#--------------------------------------------------------------------

# функции для пользователя:

# - create_table_from_sample(table_structure, table_name, sample)
	# создание в бд новой таблицы с именем table_name
	# и содержанием согласно table_structure и данных из sample

# - are_tables_equal(table_name_1, table_name_2)
	# сравнение таблиц table_name_1 и table_name_2 

# - update_table(table_name_2, table_name_1)
	# дополнение таблицы table_name_2 данными из таблицы table_name_1 (если возможно)

#=====================================================================

import sqlite3
from get_data import get_sample

#--------------------------------------------------------------------
# смена рабочей директории на директорию запуска скрипта:
#--------------------------------------------------------------------

import os
import sys

os.chdir(sys.path[0])

#--------------------------------------------------------------------
# константы:
#--------------------------------------------------------------------

# расположение файла базы данных
DB_LOCATION = './data/movies_db.db'

# имена и структура таблиц
TABLE_NAMES = ('Movies_Sample_1', 'Movies_Sample_2')
TABLE_STRUCTURE = 'id INTEGER, title TEXT, dir TEXT, year INTEGER, rate REAL, voters INTEGER'

# размер выборок для таблиц 
SAMPLE_LEN = 30 # <= 250

# параметр печати в консоль
PRINTOUT = True

#--------------------------------------------------------------------
# функции для выполнения задания:
#--------------------------------------------------------------------

def create_table_from_sample(table_structure, table_name, sample, db_location=DB_LOCATION, printout=PRINTOUT):
	# создание в бд новой таблицы с именем table_name
	# и содержанием согласно table_structure и данных из sample

	conn = sqlite3.connect(db_location)
	cur = conn.cursor()

	# получение из table_structure названий полей (без типа)
	table_structure_tags = ', '.join([item.strip().split()[0] for item in table_structure.split(',')])

	# удаление из бд таблицы с именем table_name и создание новой
	sql_request = '''
	DROP TABLE IF EXISTS {0};
	CREATE TABLE {0} ({1}); 
	'''.format(table_name, table_structure) 

	# заполнение таблицы:
	for item in sample:
		sql_request += '''
		INSERT INTO {0} ({1}) VALUES {2};
		'''.format(table_name, table_structure_tags, tuple(item))
	
	cur.executescript(sql_request)	

	conn.commit()
	cur.close()

	if printout:
		print('Таблица {0} (len={1}) создана ...'.format(table_name, len(sample)))

def are_tables_equal(table_name_1, table_name_2, db_location=DB_LOCATION, printout=PRINTOUT):
	# сравнение таблиц в рамках задания:
	# определяем - есть ли в table_name_1 элементы, которых нет в table_name_2

	# полагаем, что таблицы не содержат дубликатов и имеют одинаковые структуру и размер;
	# тогда, если все элементы table_name_1 содержатся также в table_name_2, 
	# table_name_1 будет совпадать с table_name_2, и функция вернет True, 
	# в противном случае - False

	conn = sqlite3.connect(db_location)
	cur = conn.cursor()

	sql_request = '''
	SELECT * FROM (
		SELECT * FROM {0}
		EXCEPT 
		SELECT * FROM {1}
	)
	'''.format(table_name_1, table_name_2)

	cur.execute(sql_request)

	result_len = len(cur.fetchall()) # количество строк table_name_1, которых нет в table_name_2

	conn.commit()
	cur.close()

	condition = (result_len == 0)

	if condition:
		if printout:
			print('Таблицы совпадают')
		return True

	else:
		if printout:
			print('Таблицы НЕ совпадают. Количество разных строк:', result_len)
		return False

def update_table(table_name_2, table_name_1, db_location=DB_LOCATION, printout=PRINTOUT):
	# дополнение table_name_2 данными из table_name_1


	if not are_tables_equal(table_name_2, table_name_1, db_location, printout):

		conn = sqlite3.connect(db_location)
		cur = conn.cursor()

		sql_request = '''
		INSERT INTO {0}
		SELECT * FROM (
			SELECT * FROM {1}
			EXCEPT 
			SELECT * FROM {0}
		 )
		'''.format(table_name_2, table_name_1)

		cur.execute(sql_request)

		cur.execute('SELECT * from {}'.format(table_name_2))
		result_len = len(cur.fetchall()) # обновленная длина table_name_2

		conn.commit()
		cur.close()

		if printout:
			print('Таблица {0} дополнена. Новое количество строк: {1}'.format(table_name_2, result_len))

	else:
		if printout:
			print('Таблицы совпадают => дополнение невозможно')

#=====================================================================
# пример:
#=====================================================================

def example_1():

	# пример:

	# 1) создаем в бд 2 таблицы одинаковой структуры и размера
	# 2) сравниваем таблицы
	# 3) дополняем 2ю таблицу данными из 1й таблицы (если это возможно)

	samples = get_sample(sample_len=SAMPLE_LEN, sample_num=len(TABLE_NAMES), printout=False)

	# 1)
	create_table_from_sample(TABLE_STRUCTURE, TABLE_NAMES[0], samples[0], printout=PRINTOUT)
	create_table_from_sample(TABLE_STRUCTURE, TABLE_NAMES[1], samples[1], printout=PRINTOUT)

	# 2), 3)
	update_table(TABLE_NAMES[1], TABLE_NAMES[0], printout=PRINTOUT)
	# update_table(TABLE_NAMES[0], TABLE_NAMES[0], printout=PRINTOUT) # случай совпадающих таблиц

def testing():
	example_1()

if __name__ == '__main__':
    testing()

#=====================================================================
