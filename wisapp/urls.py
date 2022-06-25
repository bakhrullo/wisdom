from django.urls import path
from . import views, test

# app_name = "wisapp"


urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logout_user, name='logout'),
    path('transfer', views.transfer, name='transfer'),
    path('fine', views.fine, name='fine'),
    path('parent_fine', views.fine_parent, name='parent_fine'),
    path('login/', views.sign_in, name='login'),
    path('account_status', views.acc_stat, name='account_status'),
    path('pupil_stat', views.pupil_stat, name='pupil_stat'),
    path('pupil_login/', views.pupil_sign_in, name='pupil_sign_in'),
    path('parent_stat', views.parent_stat, name='parent_stat'),
    path('parent_login/', views.parent_sign_in, name='parent_sign_in'),
    path('transfer_parent', views.transfer_parent, name='transfer_parent'),
    path('director_login/', views.director_login, name='director_login'),
    path('director_account', views.dir_stat, name='dir_account_status'),
    path('director_trans', views.dir_trans, name='dir_trans'),
    path('director_fine', views.dir_fine, name='dir_fine'),
    path('balance_user_login', views.balance_user_sign_in, name='balance_user_sign_in'),
    path('balance_user_stat', views.balance_user_stat, name='balance_user_stat'),
    path('for_dirs', views.for_dirs, name='for_dirs_trans'),
    path('for_teachers', views.for_teaches, name='for_teachers_trans'),
    path('public_api', views.p_api, name='p_api'),
    path('balance_add', views.s_b_add, name='s_b_add'),
    path('test', views.test)
]
