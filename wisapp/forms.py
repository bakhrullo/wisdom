from django import forms
from . import models


class TransferForm(forms.ModelForm):
    class Meta:
        model = models.Transfers
        fields = ['teacher_name', 'transfer_grade', 'pupil', 'point']


class TransferHistoryForm(forms.ModelForm):
    class Meta:
        model = models.TransferHistory
        fields = ['teacher_name', 'transfer_grade', 'pupil', 'point']


class ParentTransferForm(forms.ModelForm):
    class Meta:
        model = models.ParentTransfer
        fields = ['parent_name', 'pupil', 'point']


class ParentTransferHistoryForm(forms.ModelForm):
    class Meta:
        model = models.ParentTransferHistory
        fields = ['parent_name', 'pupil', 'point']


class FineForm(forms.ModelForm):
    class Meta:
        model = models.Fine
        fields = ['teacher_name', 'transfer_grade', 'pupil', 'point']


class FineHistoryForm(forms.ModelForm):
    class Meta:
        model = models.FineHistory
        fields = ['teacher_name', 'transfer_grade', 'pupil', 'point']


class FineParentForm(forms.ModelForm):
    class Meta:
        model = models.FineParent
        fields = ['parent_name', 'pupil', 'point']


class FineParentHistoryForm(forms.ModelForm):
    class Meta:
        model = models.FineParentHistory
        fields = ['parent_name', 'pupil', 'point']


class DorZTransferForm(forms.ModelForm):
    class Meta:
        model = models.DorZTransfer
        fields = '__all__'


class DorZTransferHistoryForm(forms.ModelForm):
    class Meta:
        model = models.DorZTransferHistory
        fields = '__all__'


class DorZFineForm(forms.ModelForm):
    class Meta:
        model = models.FineDorZ
        fields = '__all__'


class DorZTFineHistoryForm(forms.ModelForm):
    class Meta:
        model = models.FineDorZHistory
        fields = '__all__'


class SuperUTransDForm(forms.ModelForm):
    class Meta:
        model = models.SuperUTransD
        fields = '__all__'


class SuperUTransDHForm(forms.ModelForm):
    class Meta:
        model = models.SuperUTransDH
        fields = '__all__'


class SuperUTransTForm(forms.ModelForm):
    class Meta:
        model = models.SuperUTransT
        fields = '__all__'


class SuperUTransTHForm(forms.ModelForm):
    class Meta:
        model = models.SuperUTransTH
        fields = '__all__'


class SuperUTransPForm(forms.ModelForm):
    class Meta:
        model = models.SuperUTransP
        fields = '__all__'


class SuperUTransPHForm(forms.ModelForm):
    class Meta:
        model = models.SuperUTransPH
        fields = '__all__'


class BalanceAddForm(forms.ModelForm):
    class Meta:
        model = models.SchoolBalanceAdd
        fields = '__all__'
