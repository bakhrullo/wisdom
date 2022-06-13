from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from . import forms, models


def index(request):
    return render(request, 'wisapp/index.html')


def director_login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("/director_account")
        else:
            return redirect("/director_login")
    else:
        form = AuthenticationForm()
        return render(request, "wisapp/director_login.html", {"form": form})


class TeacherCreate(CreateView):
    model = models.Teacher
    fields = ['name', 'lastName', 'grade_t', 'acc']
    template_name = 'wisapp/teacher_form.html'
    success_url = '/'


def transfer(request):
    print(request.POST)
    user_name = request.user
    content = models.Teacher.objects.get(user=user_name)
    transfer_history = models.TransferHistory.objects.filter(teacher_name=content.id)
    curr_points = models.PointTrans.objects.filter(teacher=content.id)
    list_grade = []
    for i in content.grade_t.all():
        list_grade.append(i)
    pupil = models.Pupil.objects.filter(grade_p__in=list_grade)
    # transfer_history = models.TransferHistory.objects.filter(transfer_grade__in=list_grade)
    if request.method == 'POST':
        form = forms.TransferForm(request.POST)
        form_history = forms.TransferHistoryForm(request.POST)
        if form.is_valid() and form_history.is_valid():
            form.save()
            curr_trans = models.Transfers.objects.get(teacher_name=content.id)
            trans_pupil = []
            for i in curr_trans.pupil.all():
                trans_pupil.append(i.id)
            print(trans_pupil)
            curr_pupil = models.Pupil.objects.filter(id__in=trans_pupil)
            for f in curr_pupil:
                cpoint, created = models.PointTrans.objects.get_or_create(
                    teacher=content,
                    pupil=f,
                    defaults={'teacher': content,
                              'pupil': f,
                              'point': 0,
                              'point_sum': 0}
                )

            point_sum = 0
            for i in curr_pupil:
                point_sum += curr_trans.point
            if point_sum > content.acc:
                curr_trans.delete()
                error = 'wispont на вашем счету не достаточно'
                return render(request, "wisapp/transfer.html", {"content": content, 'pupil': pupil, 'error': error})

            content.acc -= point_sum
            content.save()
            form_history.save()
            for i in curr_pupil:
                i.acc += curr_trans.point
                i.save()
            curr_point = models.PointTrans.objects.filter(pupil__in=trans_pupil)
            for i in curr_point:
                i.point += curr_trans.point
                i.point_sum += curr_trans.point
                i.save()
            success = 'wispont переведены успешно'
            curr_trans.delete()
            return render(request, "wisapp/transfer.html", {"content": content, 'pupil': pupil, 'success': success,
                                                            "curr_point": curr_points})
        return render(request, "wisapp/transfer.html", {"content": content, 'pupil': pupil, 'error': form.errors,
                                                        'curr_point': curr_points})
    return render(request, "wisapp/transfer.html", {"content": content, 'pupil': pupil, "trans": transfer_history,
                                                    'curr_point': curr_points})


def transfer_parent(request):
    print(request.POST)
    user_name = request.user
    content = models.Parent.objects.get(user=user_name)
    curr_points = models.PointTransParents.objects.filter(teacher=content.id)
    if request.method == 'POST':
        form = forms.ParentTransferForm(request.POST)
        form_history = forms.ParentTransferHistoryForm(request.POST)
        if form.is_valid() and form_history.is_valid():
            form.save()
            curr_trans = models.ParentTransfer.objects.get(parent_name=content.id)
            trans_pupil = []
            for i in curr_trans.pupil.all():
                trans_pupil.append(i.id)
            print(trans_pupil)
            curr_pupil = models.Pupil.objects.filter(id__in=trans_pupil)
            for f in curr_pupil:
                cpoint, created = models.PointTransParents.objects.get_or_create(
                    teacher=content,
                    pupil=f,
                    defaults={'teacher': content,
                              'pupil': f,
                              'point': 0,
                              'point_sum': 0}
                )

            point_sum = 0
            for i in curr_pupil:
                point_sum += curr_trans.point
            if point_sum > content.acc:
                curr_trans.delete()
                error = 'wispont на вашем счету не достаточно'
                return render(request, "wisapp/parent_transfer.html", {"content": content, 'error': error, "curr_point":
                    curr_points})
            content.acc -= point_sum
            content.save()
            form_history.save()
            curr_point = models.PointTransParents.objects.filter(pupil__in=trans_pupil)
            for i in curr_point:
                i.point += curr_trans.point
                i.point_sum += curr_trans.point
                i.save()
            for i in curr_pupil:
                i.acc += curr_trans.point
                i.save()
            success = 'wispont переведены успешно'
            curr_trans.delete()
            return render(request, "wisapp/transfer_parent.html", {"content": content, 'success': success, "curr_point":
                curr_points})
        return render(request, "wisapp/transfer_parent.html", {"content": content, 'error': form.errors, "curr_point":
            curr_points})
    return render(request, "wisapp/transfer_parent.html", {"content": content, "curr_point": curr_points})


def sign_in(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # if request.htmx:
            #     return render(request, 'wisapp/profile.html')
            return redirect("/account_status")
        else:
            return redirect("/login")
    else:
        form = AuthenticationForm()
        return render(request, "wisapp/sign_in.html", {"form": form})


def pupil_sign_in(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("/pupil_stat")
        else:
            return redirect("/pupil_login")
    else:
        form = AuthenticationForm()
        return render(request, "wisapp/pupil_sign_in.html", {"form": form})


def parent_sign_in(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("/parent_stat")
        else:
            return redirect("/parent_login")
    else:
        form = AuthenticationForm()
        return render(request, "wisapp/parent_sign_in.html", {"form": form})


def acc_stat(request):
    print(request.user)
    curr_user = models.Teacher.objects.get(user=request.user)
    return render(request, "wisapp/profile.html", {"curr_user": curr_user})


def pupil_stat(request):
    curr_pupil = models.Pupil.objects.get(user=request.user)
    return render(request, "wisapp/pupil_profile.html", {"curr_pupil": curr_pupil})


def parent_stat(request):
    curr_parent = models.Parent.objects.get(user=request.user)
    return render(request, "wisapp/parent_profile.html", {"curr_parent": curr_parent})


def dir_stat(request):
    curr_d = models.DorZ.objects.get(user=request.user)
    pupil = models.Pupil.objects.all()
    teachers = models.Teacher.objects.all()
    return render(request, "wisapp/dir_profile.html", {"curr_d": curr_d, "pupil": pupil, "teacher": teachers})


def fine(request):
    print(request.POST)
    user_name = request.user
    content = models.Teacher.objects.get(user=user_name)
    fine_history = models.FineHistory.objects.filter(teacher_name=content.id)
    curr_points = models.PointTrans.objects.filter(teacher=content.id)
    list_grade = []
    for i in content.grade_t.all():
        list_grade.append(i)
    pupil = models.Pupil.objects.filter(grade_p__in=list_grade)
    if request.method == 'POST':
        form = forms.FineForm(request.POST)
        form_history = forms.FineHistoryForm(request.POST)
        if form.is_valid() and form_history.is_valid():
            form.save()
            curr_fine = models.Fine.objects.get(teacher_name=content.id)
            curr_pupil = models.Pupil.objects.get(id=curr_fine.pupil.id)
            try:
                curr_stat = models.PointTrans.objects.get(pupil=curr_pupil, teacher=content.id)
            except:
                curr_fine.delete()
                error = 'wispont который вы перевели не достаточно'
                return render(request, "wisapp/transfer.html", {"content": content, 'pupil': pupil, 'error': error,
                                                                'curr_point': curr_points})
            if curr_fine.point > curr_stat.point:
                curr_fine.delete()
                error = 'wispont который вы перевели не достаточно'
                return render(request, "wisapp/transfer.html", {"content": content, 'pupil': pupil, 'error': error,
                                                                'curr_point': curr_points})
            curr_pupil.acc -= curr_fine.point
            curr_stat.point -= curr_fine.point
            curr_stat.save()
            curr_pupil.save()
            curr_fine.delete()
            form_history.save()
            success = 'wispont сняты успешно'
            return render(request, "wisapp/transfer.html", {"content": content, 'pupil': pupil, 'error': success,
                                                            'curr_point': curr_points})
        return render(request, "wisapp/transfer.html", {"content": content, 'pupil': pupil, 'error': form.errors,
                                                        'curr_point': curr_points})
    return render(request, "wisapp/fine.html", {"content": content, 'pupil': pupil, "trans": fine_history,
                                                'curr_point': curr_points})


def fine_parent(request):
    print(request.POST)
    user_name = request.user
    content = models.Parent.objects.get(user=user_name)
    fine_history = models.FineParentHistory.objects.filter(parent_name=content.id)
    curr_points = models.PointTransParents.objects.filter(teacher=content.id)
    if request.method == 'POST':
        form = forms.FineParentForm(request.POST)
        form_history = forms.FineParentHistoryForm(request.POST)
        if form.is_valid() and form_history.is_valid():
            form.save()
            curr_fine = models.FineParent.objects.get(parent_name=content.id)
            curr_pupil = models.Pupil.objects.get(id=curr_fine.pupil.id)
            try:
                curr_stat = models.PointTransParents.objects.get(pupil=curr_pupil, teacher=content.id)
            except:
                curr_fine.delete()
                error = 'wispont который вы перевели не достаточно'
                return render(request, "wisapp/fine_parent.html", {"content": content, 'error': error,
                                                                   'curr_point': curr_points})
            if curr_fine.point > curr_stat.point:
                curr_fine.delete()
                error = 'wispont который вы перевели не достаточно'
                return render(request, "wisapp/fine_parent.html", {"content": content, 'error': error,
                                                                   'curr_point': curr_points})
            curr_pupil.acc -= curr_fine.point
            curr_stat.point -= curr_fine.point
            content.acc += curr_fine.point
            content.save()
            curr_stat.save()
            curr_pupil.save()
            form_history.save()
            curr_fine.delete()
            success = 'wispont сняты успешно'
            return render(request, "wisapp/fine_parent.html", {"content": content, 'error': success,
                                                               'curr_point': curr_points})
        return render(request, "wisapp/fine_parent.html", {"content": content, 'error': form.errors,
                                                           'curr_point': curr_points})
    return render(request, "wisapp/fine_parent.html", {"content": content, "trans": fine_history,
                                                       'curr_point': curr_points})


def dir_fine(request):
    pupil = models.Pupil.objects.all()
    content = models.DorZ.objects.get(user=request.user)
    grades = models.Grade.objects.all()
    s_b = models.SchoolBalance.objects.get()
    if request.method == 'POST':
        form = forms.DorZFineForm(request.POST)
        form_history = forms.DorZTFineHistoryForm(request.POST)
        if form.is_valid() and form_history.is_valid():
            form.save()
            curr_trans = models.FineDorZ.objects.get(dorz_name=content.id)
            curr_pupil = models.Pupil.objects.get(id=curr_trans.pupil.id)
            if curr_trans.point > curr_pupil.acc:
                curr_trans.delete()
                error = 'wispoint на счету данного ученика не достаточно'
                return render(request, "wisapp/d_fine.html", {"content": content, 'error': error,
                                                              "pupil": pupil, 'grade': grades})
            curr_pupil.acc -= curr_trans.point
            s_b.balance += curr_trans.point
            s_b.save()
            curr_pupil.save()
            form_history.save()
            success = 'wispont сняты успешно'
            curr_trans.delete()
            return render(request, "wisapp/d_fine.html", {"content": content, 'success': success,
                                                          "pupil": pupil, 'grade': grades})
        return render(request, "wisapp/d_fine.html", {"content": content, 'error': form.errors,
                                                      "pupil": pupil, 'grade': grades})
    return render(request, "wisapp/d_fine.html", {"content": content, "pupil": pupil, 'grade': grades})


def dir_trans(request):
    pupil = models.Pupil.objects.all()
    content = models.DorZ.objects.get(user=request.user)
    grades = models.Grade.objects.all()
    if request.method == 'POST':
        form = forms.DorZTransferForm(request.POST)
        form_history = forms.DorZTransferHistoryForm(request.POST)
        if form.is_valid() and form_history.is_valid():
            form.save()
            curr_trans = models.DorZTransfer.objects.get(dorz_name=content.id)
            trans_pupil = []
            for i in curr_trans.pupil.all():
                trans_pupil.append(i.id)
            print(trans_pupil)
            curr_pupil = models.Pupil.objects.filter(id__in=trans_pupil)
            point_sum = 0
            for i in curr_pupil:
                point_sum += curr_trans.point
            if point_sum > content.acc:
                curr_trans.delete()
                error = 'wispont на вашем счету не достаточно'
                return render(request, "wisapp/d_transfer.html", {"content": content, 'error': error, "pupil": pupil,
                                                                  'grade': grades})
            content.acc -= point_sum
            content.save()
            form_history.save()
            for i in curr_pupil:
                i.acc += curr_trans.point
                i.save()
            success = 'wispont переведены успешно'
            curr_trans.delete()
            return render(request, "wisapp/d_transfer.html", {"content": content, 'success': success,
                                                              "pupil": pupil, 'grade': grades})
        return render(request, "wisapp/d_transfer.html", {"content": content, 'error': form.errors,
                                                          "pupil": pupil, 'grade': grades})
    return render(request, "wisapp/d_transfer.html", {"content": content, "pupil": pupil, 'grade': grades})


def balance_user_sign_in(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("/balance_user_stat")
        else:
            return redirect("/balance_user_sign_in")
    else:
        form = AuthenticationForm()
        return render(request, "wisapp/balance_user_sign_in.html", {"form": form})


def balance_user_stat(request):
    content = models.SchoolBalanceUser.objects.get(user=request.user)
    balance = models.SchoolBalance.objects.get()
    return render(request, "wisapp/balance_user_stat.html", {'content': content, 'school': balance})


def for_dirs(request):
    content = models.SchoolBalanceUser(user=request.user)
    dorz = models.DorZ.objects.all()
    s_b = models.SchoolBalance.objects.all()
    # if request.method == 'POST':
    #     form = forms.SuperUTransDForm(request.POST)
    #     form_history = forms.SuperUTransDHForm(request.POST)
    #     if form.is_valid() and form_history.is_valid():
    #         form.save()
    #         curr_trans = models.SuperUTransD.objects.get(dorz_name=content.id)
    #         trans_pupil = []
    #         for i in curr_trans.pupil.all():
    #             trans_pupil.append(i.id)
    #         print(trans_pupil)
    #         curr_pupil = models.Pupil.objects.filter(id__in=trans_pupil)
    #         point_sum = 0
    #         for i in curr_pupil:
    #             point_sum += curr_trans.point
    #         if point_sum > content.acc:
    #             curr_trans.delete()
    #             error = 'wispont на вашем счету не достаточно'
    #             return render(request, "wisapp/d_transfer.html", {"content": content, 'error': error, "pupil": pupil,
    #                                                               'grade': grades})
    #         content.acc -= point_sum
    #         content.save()
    #         form_history.save()
    #         for i in curr_pupil:
    #             i.acc += curr_trans.point
    #             i.save()
    #         success = 'wispont переведены успешно'
    #         curr_trans.delete()
    #         return render(request, "wisapp/d_transfer.html", {"content": content, 'success': success,
    #                                                           "pupil": pupil, 'grade': grades})
    #     return render(request, "wisapp/d_transfer.html", {"content": content, 'error': form.errors,
    #                                                       "pupil": pupil, 'grade': grades})
    #     return render(request, "wisapp/d_transfer.html", {"content": content, "pupil": pupil, 'grade': grades})
    #

def for_teaches(request):
    pass