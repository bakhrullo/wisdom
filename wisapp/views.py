from django.contrib.auth import login, logout
# from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.shortcuts import render, redirect
from . import forms, models
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, 'wisapp/index.html')


def logout_user(request):
    logout(request)
    return redirect('index')


def director_login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("/director_account")
        else:
            err = "Iltimos, ma'lumotlaringizni qayta tekshirib kiriting"
            return render(request, "wisapp/sign_in.html", {'mess': err})
    else:
        return render(request, "wisapp/sign_in.html")


def pupil_sign_in(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("/pupil_stat")
        else:
            err = "Iltimos, ma'lumotlaringizni qayta tekshirib kiriting"
            return render(request, "wisapp/sign_in.html", {'mess': err})
    else:
        return render(request, "wisapp/sign_in.html")


def sign_in(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            print(request)
            login(request, user)
            return redirect("/account_status")
        else:
            err = "Iltimos, ma'lumotlaringizni qayta tekshirib kiriting"
            return render(request, "wisapp/sign_in.html", {'mess': err})
    else:
        return render(request, "wisapp/sign_in.html")


def parent_sign_in(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("/parent_stat")
        else:
            err = "Iltimos, ma'lumotlaringizni qayta tekshirib kiriting"
            return render(request, "wisapp/sign_in.html", {'mess': err})
    else:
        return render(request, "wisapp/sign_in.html")


def balance_user_sign_in(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("/balance_user_stat")
        else:
            err = "Iltimos, ma'lumotlaringizni qayta tekshirib kiriting"
            return render(request, "wisapp/sign_in.html", {'mess': err})
    else:
        return render(request, "wisapp/sign_in.html")


@login_required
def acc_stat(request):
    curr_user = models.Teacher.objects.get(user=request.user)
    return render(request, "wisapp/profile.html", {"curr_user": curr_user})


@login_required
def pupil_stat(request):
    curr_pupil = models.Pupil.objects.get(user=request.user)
    return render(request, "wisapp/pupil_profile.html", {"curr_user": curr_pupil})


@login_required
def parent_stat(request):
    curr_parent = models.Parent.objects.get(user=request.user)
    return render(request, "wisapp/parent_profile.html", {"curr_user": curr_parent})


@login_required
def dir_stat(request):
    curr_d = models.DorZ.objects.get(user=request.user)
    return render(request, "wisapp/dir_profile.html", {"curr_user": curr_d})


@login_required
def balance_user_stat(request):
    curr_bu = models.SchoolBalanceUser.objects.get(user=request.user)
    balance = models.SchoolBalance.objects.get()
    return render(request, "wisapp/balance_user_stat.html", {'curr_user': curr_bu, 'school': balance})


@login_required
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


@login_required
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


@login_required
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


@login_required
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


@login_required
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


@login_required
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


@login_required
def for_dirs(request):
    content = models.SchoolBalanceUser.objects.get(user=request.user)
    dorz = models.DorZ.objects.all()
    s_b = models.SchoolBalance.objects.get()
    if request.method == 'POST':
        form = forms.SuperUTransDForm(request.POST)
        form_history = forms.SuperUTransDHForm(request.POST)
        if form.is_valid() and form_history.is_valid():
            form.save()
            curr_trans = models.SuperUTransD.objects.get(dorz=content.id)
            trans_dorz = []
            for i in curr_trans.dorz.all():
                trans_dorz.append(i.id)
            print(trans_dorz)
            curr_dorz = models.DorZ.objects.filter(id__in=trans_dorz)
            point_sum = 0
            for i in curr_dorz:
                point_sum += curr_trans.point
            if point_sum > s_b.balance:
                curr_trans.delete()
                error = 'wispont на счету не достаточно'
                return render(request, "wisapp/super_u_d.html", {"content": content, 'error': error, "dorz": dorz})
            s_b.balance -= point_sum
            s_b.save()
            content.save()
            form_history.save()
            for i in curr_dorz:
                i.acc += curr_trans.point
                i.save()
            success = 'wispont переведены успешно'
            curr_trans.delete()
            return render(request, "wisapp/super_u_d.html", {"content": content, 'success': success, 'dorz': dorz,
                                                             's_b': s_b})
        return render(request, "wisapp/super_u_d.html", {"content": content, 'error': form.errors, 'dorz': dorz,
                                                         's_b': s_b})
    return render(request, "wisapp/super_u_d.html", {"content": content, 'dorz': dorz, 's_b': s_b})


@login_required
def for_teaches(request):
    content = models.SchoolBalanceUser.objects.get(user=request.user)
    teacher = models.Teacher.objects.all()
    s_b = models.SchoolBalance.objects.get()
    if request.method == 'POST':
        form = forms.SuperUTransTForm(request.POST)
        form_history = forms.SuperUTransTHForm(request.POST)
        if form.is_valid() and form_history.is_valid():
            form.save()
            curr_trans = models.SuperUTransT.objects.get(teacher=content.id)
            trans_teacher = []
            for i in curr_trans.teacher.all():
                trans_teacher.append(i.id)
            print(trans_teacher)
            curr_teacher = models.Teacher.objects.filter(id__in=trans_teacher)
            point_sum = 0
            for i in curr_teacher:
                point_sum += curr_trans.point
            if point_sum > s_b.balance:
                curr_trans.delete()
                error = 'wispont на счету не достаточно'
                return render(request, "wisapp/super_u_t.html",
                              {"content": content, 'error': error, "teacher": teacher})
            s_b.balance -= point_sum
            s_b.save()
            content.save()
            form_history.save()
            for i in curr_teacher:
                i.acc += curr_trans.point
                i.save()
            success = 'wispont переведены успешно'
            curr_trans.delete()
            return render(request, "wisapp/super_u_t.html", {"content": content, 'success': success, 'teacher': teacher,
                                                             's_b': s_b})
        return render(request, "wisapp/super_u_t.html", {"content": content, 'error': form.errors, 'teacher': teacher,
                                                         's_b': s_b})
    return render(request, "wisapp/super_u_t.html", {"content": content, 'teacher': teacher, 's_b': s_b})


def s_b_add(request):
    content = models.SchoolBalanceUser.objects.get(user=request.user)
    s_b = models.SchoolBalance.objects.get()
    form_temp = forms.BalanceAddForm
    if request.method == 'POST':
        form = forms.BalanceAddForm(request.POST)

        if form.is_valid():

            form.save()
            point = request.POST.get('point')
            s_b.balance += int(point)
            s_b.save()
            return render(request, 'wisapp/balance_add.html', {'curr_user': content})
    return render(request, 'wisapp/balance_add.html', {'curr_user': content})


@csrf_exempt
def p_api(request):
    if request.method == 'GET':
        # print(request.GET)
        data = {'ok': 0}
        get = request.GET
        if get['username'] and get['password'] and get['roll']:
            form = AuthenticationForm(data=get)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                if get['roll'] == 'direktor':
                    context = models.DorZ.objects.get(user=request.user)
                    grades_for_d = models.Grade.objects.all()
                    data = {'ok': 1, "roll": get['roll'],
                            "user": {
                                'username': str(context.user),
                                'name': context.name,
                                'last_name': context.lastName,
                                'balance': context.acc,
                                'grades': [{'grade_name': i.gradeName,
                                            'grade_id': i.id} for i in grades_for_d]
                            }
                            }
                    if get.get('r_type') == 'transfers':
                        # trans = models.TransferHistory.objects.filter(dorz_name=context.id)
                        trans = models.TransferHistory.objects.order_by("-id")[0:50]

                        data = {'ok': 1, "roll": get['roll'],
                                "user": {
                                    "id": context.id,
                                    'username': str(context.user),
                                    'name': context.name,
                                    'last_name': context.lastName,
                                    'balance': context.acc,
                                },
                                "transfer_history": [{'teacher_name': i.teacher_name.name,
                                                      'point': i.point,
                                                      'date': i.data,
                                                      'pupils': [{'pupil_name': f'{d.name} {d.lastName}',
                                                                  'pupil_balance': d.acc} for d in i.pupil.all()],
                                                      } for i in trans]

                                }

                    elif get.get('r_type') == 'teachers':
                        teachers = models.Teacher.objects.all()
                        data = {'ok': 1, "roll": get['roll'],
                                "user": {
                                    'username': str(context.user),
                                    'name': context.name,
                                    'last_name': context.lastName,
                                    'balance': context.acc,
                                    'teachers': [{'name': i.name,
                                                  'lastName': i.lastName,
                                                  'acc': i.acc,
                                                  'grade_t': [d.gradeName for d in i.grade_t.all()],
                                                  } for i in teachers]
                                }
                                }
                    elif get.get('r_type') == 'pupils':
                        pupils = models.Pupil.objects.filter(grade_p=get.get('grade_id'))
                        data = {'ok': 1, "roll": get['roll'],
                                "user": {
                                    'username': str(context.user),
                                    'name': context.name,
                                    'last_name': context.lastName,
                                    'balance': context.acc,
                                    'pupils': [{'pupil_id': i.id,
                                                'name': i.name,
                                                'lastName': i.lastName,
                                                'acc': i.acc,
                                                'grade_p': i.grade_p.gradeName,
                                                } for i in pupils]
                                }
                                }

                elif get['roll'] == 'parent':
                    context = models.Parent.objects.get(user=request.user)
                    childs = [{"id": i.id,
                               "name": i.name,
                               "last_name": i.lastName,
                               "grade": i.grade_p.gradeName,
                               "balance": i.acc
                               } for i in context.child.all()]

                    data = {'ok': 1, "roll": get['roll'],
                            "user": {
                                "id": context.id,
                                'username': str(context.user),
                                'name': context.name,
                                'last_name': context.lastName,
                                'childs': childs,
                                'balance': context.acc
                            }
                            }
                    if get.get('r_type') == 'transfers':
                        pupils = list(set([int(n) for n in get['pupils'].split(",") if len(n.strip()) > 0]))
                        transfer_point = int(get['transfer_point'])
                        data = {'ok': 1, "roll": get['roll'],
                                "transfer": {
                                    "parent_id": context.id,
                                    'parent_balance': context.acc,
                                    'transfer_list': []
                                }
                                }
                        if transfer_point > 0:
                            pupils_db = models.Pupil.objects.filter(id__in=pupils)
                            # grade_db = models.Grade.objects.get(id=pupils_db[0].grade_p.id)
                            trans_list = []
                            trans_pupil = []
                            for pupil in pupils_db:
                                if context.acc < transfer_point:
                                    break
                                trans_doc, sec_doc = models.PointTransParents.objects.get_or_create(
                                    teacher=context,
                                    pupil=pupil,
                                    defaults={'teacher': context,
                                              'pupil': pupil,
                                              'point': 0,
                                              'point_sum': 0}
                                )
                                pupil.acc += transfer_point
                                trans_doc = trans_doc if trans_doc else sec_doc
                                trans_doc.point += transfer_point
                                trans_doc.point_sum += transfer_point
                                trans_doc.save()
                                context.acc -= transfer_point
                                context.save()
                                pupil.save()
                                trans_pupil.append(pupil)

                                trans_list.append({'pupil_id': pupil.id,
                                                   'point': trans_doc.point,
                                                   'point_sum': trans_doc.point_sum,
                                                   'pupil_balance': pupil.acc,
                                                   })

                            transfer_history = models.ParentTransferHistory.objects.create(parent_name=context,
                                                                                           point=transfer_point)
                            for i in trans_pupil:
                                transfer_history.pupil.add(i)

                            data['transfer']['parent_balance'] = context.acc
                            data['transfer']['transfer_list'] = trans_list

                        elif transfer_point < 0:
                            transfer_point = abs(transfer_point)
                            pupils_db = models.Pupil.objects.filter(id__in=pupils)
                            # grade_db = models.Grade.objects.get(id=pupils_db[0].grade_p.id)
                            trans_list = []
                            for pupil in pupils_db:
                                trans_doc = models.PointTransParents.objects.filter(teacher=context, pupil=pupil)
                                if trans_doc.count() != 1 or trans_doc[0].point < transfer_point:
                                    continue
                                trans_doc = trans_doc[0]
                                pupil.acc -= transfer_point
                                trans_doc.point -= transfer_point
                                trans_doc.save()
                                context.acc += transfer_point
                                pupil.save()
                                context.save()
                                models.FineParentHistory.objects.create(parent_name=context,
                                                                        pupil=pupil,
                                                                        point=transfer_point)
                                trans_list.append({'pupil_id': pupil.id,
                                                   'point': trans_doc.point,
                                                   'point_sum': trans_doc.point_sum,
                                                   'pupil_balance': pupil.acc,
                                                   })
                                data['transfer']['parent_balance'] = context.acc
                                data['transfer']['transfer_list'] = trans_list

                elif get['roll'] == 'teacher':
                    context = models.Teacher.objects.get(user=request.user)
                    if get['r_type'] == 'tech_account':
                        grades = []
                        for g in context.grade_t.all():
                            pupils_list = [{"id": p.id,
                                            "name": p.name,
                                            "last_name": p.lastName,
                                            "balance": p.acc,
                                            "exchange": [k.point for k in models.PointTrans.objects.filter(pupil=p.id,
                                                                                teacher=context.id)]
                                            } for p in models.Pupil.objects.filter(grade_p=g.id)]
                            grades.append({"id": g.id, "name": g.gradeName, "pupils_list": pupils_list})

                        data = {'ok': 1, "roll": get['roll'],
                                "user": {
                                    "id": context.id,
                                    'username': str(context.user),
                                    'name': context.name,
                                    'last_name': context.lastName,
                                    'balance': context.acc,
                                    'grades': grades
                                }
                                }
                    elif get['r_type'] == 'transfer':
                        pupils = list(set([int(n) for n in get['pupils'].split(",") if len(n.strip()) > 0]))
                        print(pupils)
                        transfer_point = int(get['transfer_point'])
                        data = {'ok': 1, "roll": get['roll'],
                                "transfer": {
                                    "teacher_id": context.id,
                                    'parent_balance': context.acc,
                                    'transfer_list': []
                                }
                                }
                        if transfer_point > 0:
                            pupils_db = models.Pupil.objects.filter(id__in=pupils)
                            grade_db = models.Grade.objects.get(id=pupils_db[0].grade_p.id)
                            trans_list = []
                            trans_pupil = []
                            for pupil in pupils_db:
                                if context.acc < transfer_point:
                                    break
                                trans_doc, sec_doc = models.PointTrans.objects.get_or_create(
                                    teacher=context,
                                    pupil=pupil,
                                    defaults={'teacher': context,
                                              'pupil': pupil,
                                              'point': 0,
                                              'point_sum': 0}
                                )
                                pupil.acc += transfer_point
                                trans_doc = trans_doc if trans_doc else sec_doc
                                trans_doc.point += transfer_point
                                trans_doc.point_sum += transfer_point
                                trans_doc.save()
                                context.acc -= transfer_point
                                context.save()
                                pupil.save()
                                trans_pupil.append(pupil)

                                trans_list.append({'pupil_id': pupil.id,
                                                   'point': trans_doc.point,
                                                   'point_sum': trans_doc.point_sum,
                                                   'pupil_balance': pupil.acc,
                                                   })

                            transfer_history = models.TransferHistory.objects.create(teacher_name=context,
                                                                                     transfer_grade=grade_db,
                                                                                     point=transfer_point)
                            for i in trans_pupil:
                                transfer_history.pupil.add(i)

                            data['transfer']['teacher_balance'] = context.acc
                            data['transfer']['transfer_list'] = trans_list

                        elif transfer_point < 0:
                            transfer_point = abs(transfer_point)
                            pupils_db = models.Pupil.objects.filter(id__in=pupils)
                            grade_db = models.Grade.objects.get(id=pupils_db[0].grade_p.id)
                            trans_list = []
                            for pupil in pupils_db:
                                trans_doc = models.PointTrans.objects.filter(teacher=context, pupil=pupil)
                                if trans_doc.count() != 1 or trans_doc[0].point < transfer_point:
                                    continue
                                trans_doc = trans_doc[0]
                                pupil.acc -= transfer_point
                                trans_doc.point -= transfer_point
                                trans_doc.save()
                                context.acc += transfer_point
                                pupil.save()
                                context.save()
                                models.FineHistory.objects.create(teacher_name=context,
                                                                  transfer_grade=grade_db,
                                                                  pupil=pupil,
                                                                  point=transfer_point)
                                trans_list.append({'pupil_id': pupil.id,
                                                   'point': trans_doc.point,
                                                   'point_sum': trans_doc.point_sum,
                                                   'pupil_balance': pupil.acc,
                                                   })
                                data['transfer']['teacher_balance'] = context.acc
                                data['transfer']['transfer_list'] = trans_list
                elif get['roll'] == 'pupil':
                    context = models.Pupil.objects.get(user=request.user)
                    data = {'ok': 1, "roll": get['roll'],
                            "user": {
                                'id': context.id,
                                'username': str(context.user),
                                'name': context.name,
                                'last_name': context.lastName,
                                'balance': context.acc,
                                'grade': context.grade_p.gradeName,
                                'grade_id': context.grade_p.id
                            }
                            }
        return JsonResponse(data)
