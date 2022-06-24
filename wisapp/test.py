# import openpyxl
# from django.contrib.auth.models import User
#
# from peewee import *
#
# conn = SqliteDatabase('db.sqlite3')
# cursor = conn.cursor()
#
#
# book = openpyxl.load_workbook('Книга1.xlsx')
# worksheet = book.active
# user = []
# passw = []
# for i in range(1, worksheet.max_row):
#     for col in worksheet.iter_cols(1, worksheet.max_column):
#         if len(str(col[i].value)) == 5:
#             passw.append(col[i].value)
#         else:
#             user.append(col[i].value)
#
# for i in range(1, len(user)+1):
#     User.create(username=passw[i], password=user[i])
# conn.close()