from django.contrib import admin
from django.contrib.auth.models import User

from .models import *



class DAdmin(admin.ModelAdmin):
    list_display = ['name', 'lastName', 'acc']
    list_filter = ['name', 'lastName', 'data']


class ParentAdmin(admin.ModelAdmin):
    list_display = ['name', 'lastName', 'childes', 'acc', 'data']
    list_filter = ['name', 'lastName', 'data']


class PupilAdmin(admin.ModelAdmin):
    list_display = ['name', 'lastName', 'grade_p', 'acc', 'data']
    list_filter = ['name', 'lastName', 'data']


class TeachAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'lastName', 'grades', 'acc', 'data']
    list_filter = ['name', 'lastName', 'data']


class GradeAdmin(admin.ModelAdmin):
    list_display = ['id', 'gradeName', 'data']
    list_filter = ['gradeName', 'data']


class TransHistoryAdmin(admin.ModelAdmin):
    list_display = ['teacher_name', 'transfer_grade', 't_g', 'point', 'data']
    list_filter = ['teacher_name', 'transfer_grade', 'point', 'data']


class ParentTransferHistoryAdmin(admin.ModelAdmin):
    list_display = ['parent_name', 't_g', 'point', 'data']
    list_filter = ['parent_name', 'point', 'data']


class PointTransferAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'pupil', 'point', 'point_sum', 'data']
    list_filter = ['teacher', 'pupil', 'point', 'point_sum', 'data']


class FineHistoryAdmin(admin.ModelAdmin):
    list_display = ['teacher_name', 'transfer_grade', 'pupil', 'point', 'data']
    list_filter = ['teacher_name', 'transfer_grade', 'pupil', 'point', 'data']


class PointTransParentsAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'pupil', 'point', 'point_sum', 'data']
    list_filter = ['teacher', 'pupil', 'point', 'point_sum', 'data']


class ParentFineHistoryAdmin(admin.ModelAdmin):
    list_display = ['parent_name', 'pupil', 'point', 'data']
    list_filter = ['parent_name', 'pupil', 'point', 'data']


class SchoolBalanceAdmin(admin.ModelAdmin):
    list_display = ['balance']


class DorZTransferHistoryAdmin(admin.ModelAdmin):
    list_display = ['dorz_name', 'pupil_show', 'point', 'data']
    list_filter = ['dorz_name', 'point', 'data']


class DorZFineHistoryAdmin(admin.ModelAdmin):
    list_display = ['dorz_name', 'pupil', 'point', 'data']
    list_filter = ['dorz_name', 'pupil', 'point', 'data']


class SchoolBalanceUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'lastName']


admin.site.register(SchoolBalanceAdd)
admin.site.register(SchoolBalanceUser, SchoolBalanceUserAdmin)
admin.site.register(FineDorZHistory, DorZFineHistoryAdmin)
admin.site.register(DorZTransferHistory, DorZTransferHistoryAdmin)
admin.site.register(SchoolBalance, SchoolBalanceAdmin)
admin.site.register(FineParentHistory, ParentFineHistoryAdmin)
admin.site.register(PointTransParents, PointTransParentsAdmin)
admin.site.register(FineHistory, FineHistoryAdmin)
admin.site.register(PointTrans, PointTransferAdmin)
admin.site.register(ParentTransferHistory, ParentTransferHistoryAdmin)
admin.site.register(TransferHistory, TransHistoryAdmin)
admin.site.register(DorZ, DAdmin)
admin.site.register(Parent, ParentAdmin)
# admin.site.register(Pupil, PupilAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(Teacher, TeachAdmin)

#
# class ListAdminMixin(object):
#     def __init__(self, model, admin_site):
#         self.list_display = '__all__'
#         super(ListAdminMixin, self).__init__(model, admin_site)
#
#
# models = apps.get_models()
# for model in models:
#     admin_class = type('AdminClass', (ListAdminMixin, admin.ModelAdmin), {})
#     try:
#         admin.site.register(model, admin_class)
#     except admin.sites.AlreadyRegistered:
#         pass