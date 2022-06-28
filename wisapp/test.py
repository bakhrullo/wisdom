# # import openpyxl
# # from django.contrib.auth.models import User
# #
# # from peewee import *
# #
# # conn = SqliteDatabase('db.sqlite3')
# # cursor = conn.cursor()
# #
# #
# # book = openpyxl.load_workbook('Книга1.xlsx')
# # worksheet = book.active
# # user = []
# # passw = []
# # for i in range(1, worksheet.max_row):
# #     for col in worksheet.iter_cols(1, worksheet.max_column):
# #         if len(str(col[i].value)) == 5:
# #             passw.append(col[i].value)
# #         else:
# #             user.append(col[i].value)
# #
# # for i in range(1, len(user)+1):
# #     User.create(username=passw[i], password=user[i])
# # conn.close()
#
# #
# # import sqlite3
# #
# # conn = sqlite3.connect('mydatabase.db')
# # cur = conn.cursor()
# # users = {}
# # curs = conn.cursor()
# # curs.execute('''
# # Create table if not exists USER(NAME varchar(100), PASSWORD varchar(100))
# # ''')
# # NAME = 'june'
# # PASSWORD = 'salafan21'
# # conn.executemany('INSERT INTO USER(NAME,PASSWORD) VALUES (? ,?);', [(NAME, PASSWORD)])
# # conn.commit()
#
#
# import openpyxl
# import models
# book = openpyxl.load_workbook('PUPS.xlsx')
# worksheet = book.active
#
# p_code = []
# p_name = []
# p_lastname = []
# p_class = []
# p_user = []
#
# печатаем список листов
# sheets = book.sheetnames
# for sheet in sheets:
#     print(sheet)
#
# получаем активный лист
# sheet = book.active
#
# for cell in sheet['A']:
#     p_code.append(cell.value)
#
# for cell in sheet['B']:
#     p_name.append(cell.value)
#
# for cell in sheet['C']:
#     p_lastname.append(cell.value)
#
# for cell in sheet['F']:
#     p_class.append(cell.value)
#
# for cell in sheet['G']:
#     p_user.append(cell.value)
#
# print(p_code)
# print(p_user)
# print(p_name)
# print(p_class)
# print(len(p_lastname))
#
# for i in range(1, len(p_lastname)+1):
#     models.Pupil.objects.create(pupil_copde=p_code[i], user=p_user[i], name=p_name[i], lastName=p_lastname[i],
#                                grade_p=p_class[i], acc=0)
#