#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import datetime
import sys
import argparse
from datetime import datetime, timedelta, date


#ВВодные данные

login = "login"
password = "password"
logs = "/var/log/" #Путь куда будет сохранена выборка пользователей на удаление 
url_add = "localhost" #url 
time_diff = timedelta(days=35) # Указываем число с которой будем высчитывать разницу. Число дней неактивности пользователя 


whitelist = ["admin", "test", "test1"] #Список пользаков по логину, которых нельзя удалять

headers = {	
			"Authorization" : "Bearer ", #api ключ
			"Accept" : "application/json",
			"Content-Type" : "application/json"
			
}

#Вводные данные заканчиваются


auth_url = f"http://{login}:{password}@{url_add}" 
url = auth_url + "/api/users/"
url_del = auth_url + "/api/admin/users/"


today = date.today()  
today_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
name_log = datetime.now()
d_t = date.today() - time_diff #высчитываем разницу 



#Аргумент для удаления
parser = argparse.ArgumentParser() 
parser.add_argument("delete", nargs='?',type=str) #Добавляем аргумент для командной строки
args = parser.parse_args()

	
	
resp = requests.get(url = url, verify=False, headers=headers) #беру данные с урла

data = resp.json()


users = [] #создаем пустой список для выборки пользователей
json_data = data
id_num = 0 
id_sum = 0


while True:
	try:
		usr = json_data[id_num]['login']
		if usr in whitelist:
			id_num+=1
		else:
			last_seen = json_data[id_num]['lastSeenAt'] #записываем строчку с датой lastSeenAt в отдельную переменную для сравнения
			if last_seen <= str(d_t):       #Если последняя дата меньше или равна заданной дате сравнения / преобразовываем d_t в str, т.к. изначально d_t в формате даты(date.time)
				print("User", json_data[id_num]['name'], "otpravlen v otdelnie spisok") #выводим на экран какие пользователи отправлены в отдельный список
				users.append(json_data[id_num]) #добавляем элемент в конец списка
				id_sum+=1

			id_num+=1
	except IndexError:
		break

if len(users):
	print('-----------------------------------')
	print('Количество пользователей на удаление:', id_sum)
else:
	print('Нет кандидатов на удаление')
	sys.exit()




if args.delete:
	with open(f"{logs}/{today_time}.json", "w") as g:
		json.dump(users, g, indent=3, ensure_ascii=False)

	with open(f"{logs}/{today_time}.json", "r") as e:
		json_del = json.load(e)
		id_num = 0
		
		while True:
			try:
				del_num = json_del[id_num]['id'] # присваиваем переменной id который необходимо удалить 
				resp_del = requests.delete(url_del + f"{del_num}", verify=False, headers=headers) # делаем запрос на удаление нужного id 
				id_num+=1
				
				
			except IndexError:
				print(f"Пользователи удалены, список удаленных пользователей помещен в {logs}, лог {today_time}")
				break
