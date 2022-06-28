# import sqlite3
# import datetime
#
# now = datetime.datetime.now()
#
# conn = sqlite3.connect('mydatabase')
# cur = conn.cursor()
# users = {}
# curs = conn.cursor()
# curs.execute('''
# Create table if not exists auth_user(username varchar(100), password varchar(100))
# ''')
# NAME = 'june'
# PASSWORD = 'salafan21'
# conn.executemany('INSERT INTO auth_user(username,password,is_superuser,last_name,email,is_staff,is_active,date_joined, first_name) VALUES (? ,? ,? ,? ,? ,? ,? ,? ,?);', [(NAME, PASSWORD, 0, 'fuu', "wadw", 0, 1, now.isoformat(), 'dwd')])
# conn.commit()

#
# from django.contrib.auth.models import User
# user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
#
# # At this point, user is a User object that has already been saved
# # to the database. You can continue to change its attributes
# # if you want to change other fields.
# user.last_name = 'Lennon'
# user.save()