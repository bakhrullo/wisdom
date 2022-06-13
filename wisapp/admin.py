from django.contrib import admin
from .models import *


class DAdmin(admin.ModelAdmin):
    list_display = ['name', 'lastName', 'acc']
    list_filter = ['name', 'lastName']


class ParentAdmin(admin.ModelAdmin):
    list_display = ['name', 'lastName', 'childes', 'acc']
    list_filter = ['name', 'lastName']


class PupilAdmin(admin.ModelAdmin):
    list_display = ['name', 'lastName', 'grade_p', 'acc']
    list_filter = ['name', 'lastName']


class TeachAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'lastName', 'grades', 'acc']
    list_filter = ['name', 'lastName']


class GradeAdmin(admin.ModelAdmin):
    list_display = ['gradeName']


class TransAdmin(admin.ModelAdmin):
    list_display = ['teacher_name', 'transfer_grade', 't_g', 'point']


class TransHistoryAdmin(admin.ModelAdmin):
    list_display = ['teacher_name', 'transfer_grade', 't_g', 'point']


class ParentTransferAdmin(admin.ModelAdmin):
    list_display = ['parent_name', 't_g', 'point']


class ParentTransferHistoryAdmin(admin.ModelAdmin):
    list_display = ['parent_name', 't_g', 'point']


class PointTransferAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'pupil', 'point', 'point_sum']


class FineAdmin(admin.ModelAdmin):
    list_display = ['teacher_name', 'transfer_grade', 'pupil', 'point']


class FineHistoryAdmin(admin.ModelAdmin):
    list_display = ['teacher_name', 'transfer_grade', 'pupil', 'point']


class PointTransParentsAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'pupil', 'point', 'point_sum']


class ParentFineAdmin(admin.ModelAdmin):
    list_display = ['parent_name', 'pupil', 'point']


class ParentFineHistoryAdmin(admin.ModelAdmin):
    list_display = ['parent_name', 'pupil', 'point']


class SchoolBalanceAdmin(admin.ModelAdmin):
    list_display = ['balance']


class DorZTransferAdmin(admin.ModelAdmin):
    list_display = ['dorz_name', 'pupil_show', 'point']


class DorZTransferHistoryAdmin(admin.ModelAdmin):
    list_display = ['dorz_name', 'pupil_show', 'point']


class DorZFineAdmin(admin.ModelAdmin):
    list_display = ['dorz_name', 'pupil', 'point']


class DorZFineHistoryAdmin(admin.ModelAdmin):
    list_display = ['dorz_name', 'pupil', 'point']


class SchoolBalanceUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'lastName']


admin.site.register(SchoolBalanceUser, SchoolBalanceUserAdmin)
admin.site.register(FineDorZ, DorZFineAdmin)
admin.site.register(FineDorZHistory, DorZFineHistoryAdmin)
admin.site.register(DorZTransfer, DorZTransferAdmin)
admin.site.register(DorZTransferHistory, DorZTransferHistoryAdmin)
admin.site.register(SchoolBalance, SchoolBalanceAdmin)
admin.site.register(FineParentHistory, ParentFineHistoryAdmin)
admin.site.register(FineParent, ParentFineAdmin)
admin.site.register(PointTransParents, PointTransParentsAdmin)
admin.site.register(Fine, FineAdmin)
admin.site.register(FineHistory, FineHistoryAdmin)
admin.site.register(PointTrans, PointTransferAdmin)
admin.site.register(ParentTransfer, ParentTransferAdmin)
admin.site.register(ParentTransferHistory, ParentTransferHistoryAdmin)
admin.site.register(Transfers, TransAdmin)
admin.site.register(TransferHistory, TransHistoryAdmin)
admin.site.register(DorZ, DAdmin)
admin.site.register(Parent, ParentAdmin)
admin.site.register(Pupil, PupilAdmin)
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