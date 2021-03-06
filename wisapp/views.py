from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.shortcuts import render, redirect
from . import forms, models
from django.views.decorators.csrf import csrf_exempt
from itertools import chain
import re


def index(request):
    return render(request, 'wisapp/index.html')


def logout_user(request):
    logout(request)
    return redirect('index')


def sell_login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('sell_stat')
        else:
            err = "Iltimos, ma'lumotlaringizni qayta tekshirib kiriting"
            return render(request, "wisapp/sign_in.html", {'mess': err})
    else:
        return render(request, "wisapp/sign_in.html")


def director_login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("/director_trans")
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
            return redirect("/transfer")
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
            return redirect("/transfer_parent")
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
def sell_stat(request):
    curr_user = models.Seller.objects.get(user=request.user)
    mess = ''
    if request.method == "POST":
        code = request.POST['pupil_code']
        point = int(request.POST['point'])
        pupil = models.Pupil.objects.get(pupil_code=code)
        s_b = models.SchoolBalance.objects.get()
        if pupil.acc < point:
            mess = "O'quvchinig hisobida yetrli ball mavjud emas"
        else:
            pupil.acc -= point
            s_b.balance += point
            pupil.save()
            s_b.save()
            models.Sell.objects.create(seller=curr_user, pupil=pupil, good_name=request.POST['good'], point=point)
            mess = "Ballar yechib olindi"
    return render(request, "wisapp/seller_profile.html", {"curr_user": curr_user, 'mess': mess})


@login_required
def acc_stat(request):
    try:
        curr_user = models.Teacher.objects.get(user=request.user)
    except:
        logout(request)
        err = "Iltimos, ma'lumotlaringizni qayta tekshirib kiriting"
        return redirect('login')
    return render(request, "wisapp/profile.html", {"curr_user": curr_user})


@login_required
def pupil_stat(request):
    try:
        curr_pupil = models.Pupil.objects.get(user=request.user)
    except:
        logout(request)
        err = "Iltimos, ma'lumotlaringizni qayta tekshirib kiriting"
        return redirect('pupil_sign_in')
    return render(request, "wisapp/pupil_profile.html", {"curr_user": curr_pupil})


@login_required
def parent_stat(request):
    try:
        curr_parent = models.Parent.objects.get(user=request.user)
    except:
        logout(request)
        err = "Iltimos, ma'lumotlaringizni qayta tekshirib kiriting"
        return redirect('parent_sign_in')
    children = []
    for i in curr_parent.child.all():
        children.append(i.id)
    tech_transfer = models.TransferHistory.objects.filter(pupil__in=children).order_by('-data')[:5]
    tech_fines = models.FineHistory.objects.filter(pupil__in=children).order_by('-data')[:5]
    dir_transfer = models.DorZTransferHistory.objects.filter(pupil__in=children).order_by('-data')[:5]
    dir_fines = models.FineDorZHistory.objects.filter(pupil__in=children).order_by('-data')[:5]
    trans = list(chain(tech_transfer, dir_transfer))
    fines = list(chain(tech_fines, dir_fines))
    return render(request, "wisapp/parent_profile.html", {"curr_user": curr_parent, "fine": fines, "trans": trans})


@login_required
def dir_stat(request):
    try:
        curr_d = models.DorZ.objects.get(user=request.user)
    except:
        logout(request)
        err = "Iltimos, ma'lumotlaringizni qayta tekshirib kiriting"
        return redirect('director_login')
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
    curr_points = models.PointTrans.objects.filter(teacher=content.id)
    list_grade = []
    for i in content.grade_t.all():
        list_grade.append(i)
    pupil = models.Pupil.objects.filter(grade_p__in=list_grade)

    def get_history():
        children = pupil
        tech_transfer = models.TransferHistory.objects.filter(teacher_name=content).order_by('-data')[:5]
        tech_fines = models.FineHistory.objects.filter(teacher_name=content).order_by('-data')[:5]
        par_trans = models.ParentTransferHistory.objects.filter(pupil__in=children).order_by('-data')[:5]
        par_fine = models.FineParentHistory.objects.filter(pupil__in=children).order_by('-data')[:5]
        dir_transfer = models.DorZTransferHistory.objects.filter(pupil__in=children).order_by('-data')[:5]
        dir_fines = models.FineDorZHistory.objects.filter(pupil__in=children).order_by('-data')[:5]
        trans = list(chain(tech_transfer, dir_transfer, par_trans))
        fines = list(chain(tech_fines, dir_fines, par_fine))
        return [trans, fines]

    if request.method == 'POST':
        err = "O'quvchini tanlang"
        if request.POST['trans'] == 'transfer':
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
                    error = 'Hisobingizda wispont yetarli emas'
                    return render(request, "wisapp/transfer.html", {"content": content, 'pupil': pupil, 'error': error,
                                                                    "curr_point": curr_points, "fine": get_history()[1],
                                                                    "trans": get_history()[0]})
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
                success = 'Otkazma muvaffaqiyatli yakunlandi'
                curr_trans.delete()
                return render(request, "wisapp/transfer.html", {"content": content, 'pupil': pupil, 'success': success,
                                                                "curr_point": curr_points, "fine": get_history()[1],
                                                                "trans": get_history()[0]})
            return render(request, 'wisapp/transfer.html', {"content": content, 'pupil': pupil, "curr_point":
                curr_points, 'error': err, "fine": get_history()[1],
                                                            "trans": get_history()[0]})
        elif request.POST['trans'] == 'fine':
            form = forms.FineForm(request.POST)
            form_history = forms.FineHistoryForm(request.POST)
            if form.is_valid() and form_history.is_valid():
                form.save()
                curr_fine = models.Fine.objects.get(teacher_name=content.id)
                fine_list = []
                for i in curr_fine.pupil.all():
                    fine_list.append(i.id)
                curr_pupil = models.Pupil.objects.filter(id__in=fine_list)
                curr_stat = []
                for i in curr_pupil:
                    try:
                        curr_stat.append(models.PointTrans.objects.get(pupil=i, teacher=content.id))
                    except:
                        curr_fine.delete()
                        error = 'Lmitdan katta summa kiritildi'
                        return render(request, "wisapp/transfer.html",
                                      {"content": content, 'pupil': pupil, 'error': error,
                                       'curr_point': curr_points, "fine": get_history()[1],
                                       "trans": get_history()[0]})
                for i in curr_stat:
                    if curr_fine.point > i.point:
                        curr_fine.delete()
                        error = 'Lmitdan katta summa kiritildi'
                        return render(request, "wisapp/transfer.html",
                                      {"content": content, 'pupil': pupil, 'error': error,
                                       'curr_point': curr_points, "fine": get_history()[1],
                                       "trans": get_history()[0]})
                for i in curr_pupil:
                    i.acc -= curr_fine.point
                    i.save()
                for i in curr_stat:
                    i.point -= curr_fine.point
                    content.acc += curr_fine.point
                    i.save()
                content.save()
                curr_fine.delete()
                form_history.save()
                success = 'Wispont yechib olindi'
                return render(request, "wisapp/transfer.html", {"content": content, 'pupil': pupil, 'success': success,
                                                                'curr_point': curr_points, "fine": get_history()[1],
                                                                "trans": get_history()[0]})
            txt = str(form.errors)
            clean_txt = re.sub(r"<[^>]+>", "", txt, flags=re.S)
            print(clean_txt)
            if clean_txt == 'fine_descr???????????????????????? ????????.':
                err = 'Jarima uchun izoh yozing!'
            return render(request, "wisapp/transfer.html", {"content": content, 'pupil': pupil,
                                                            'curr_point': curr_points, 'error': err,
                                                            "fine": get_history()[1],
                                                            "trans": get_history()[0]})
    return render(request, "wisapp/transfer.html",
                  {"content": content, 'pupil': pupil, 'curr_point': curr_points, "fine": get_history()[1],
                   "trans": get_history()[0]})


@login_required
def transfer_parent(request):
    print(request.POST)
    try:
        content = models.Parent.objects.get(user=request.user)
    except:
        logout(request)
        return redirect('parent_sign_in')
    curr_points = models.PointTransParents.objects.filter(teacher=content.id)

    def get_history():
        children = []
        for i in content.child.all():
            children.append(i.id)
        tech_transfer = models.TransferHistory.objects.filter(pupil__in=children).order_by('-data')[:5]
        tech_fines = models.FineHistory.objects.filter(pupil__in=children).order_by('-data')[:5]
        par_trans = models.ParentTransferHistory.objects.filter(parent_name=content).order_by('-data')[:5]
        par_fine = models.FineParentHistory.objects.filter(parent_name=content).order_by('-data')[:5]
        dir_transfer = models.DorZTransferHistory.objects.filter(pupil__in=children).order_by('-data')[:5]
        dir_fines = models.FineDorZHistory.objects.filter(pupil__in=children).order_by('-data')[:5]
        trans = list(chain(tech_transfer, dir_transfer, par_trans))
        fines = list(chain(tech_fines, dir_fines, par_fine))

        return [trans, fines]

    if request.method == 'POST':
        err = "O'quvchini tanlang"
        if request.POST['trans'] == 'transfer':
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
                    error = 'Hisobingizda wispont yetarli emas'
                    return render(request, "wisapp/transfer_parent.html", {"content": content, 'error': error,
                                                                           "curr_point": curr_points,
                                                                           "curr_user": content,
                                                                           "fine": get_history()[1],
                                                                           "trans": get_history()[0]})
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
                success = 'Otkazma muvaffaqiyatli yakunlandi'
                curr_trans.delete()
                return render(request, "wisapp/transfer_parent.html", {"content": content, 'success': success,
                                                                       "curr_point": curr_points, "curr_user": content,
                                                                       "fine": get_history()[1],
                                                                       "trans": get_history()[0]})
            return render(request, "wisapp/transfer_parent.html", {"content": content, 'error': err,
                                                                   "curr_point": curr_points, "curr_user": content,
                                                                   "fine": get_history()[1], "trans": get_history()[0]})
        elif request.POST['trans'] == 'fine':
            form = forms.FineParentForm(request.POST)
            form_history = forms.FineParentHistoryForm(request.POST)
            if form.is_valid() and form_history.is_valid():
                form.save()
                curr_fine = models.FineParent.objects.get(parent_name=content.id)
                fine_list = []
                for i in curr_fine.pupil.all():
                    fine_list.append(i.id)
                curr_pupil = models.Pupil.objects.filter(id__in=fine_list)
                curr_stat = []
                for i in curr_pupil:
                    try:
                        curr_stat.append(models.PointTransParents.objects.get(pupil=i, teacher=content.id))
                    except:
                        curr_fine.delete()
                        error = 'Limtdan katta summa kiritildi'
                        return render(request, "wisapp/transfer_parent.html", {"content": content, 'error': error,
                                                                               'curr_point': curr_points,
                                                                               "curr_user": content,
                                                                               "fine": get_history()[1],
                                                                               "trans": get_history()[0]
                                                                               })
                for i in curr_stat:
                    if curr_fine.point > i.point:
                        curr_fine.delete()
                        error = 'Limitdan katta summa kiritildi'
                        return render(request, "wisapp/transfer_parent.html", {"content": content, 'error': error,
                                                                               'curr_point': curr_points,
                                                                               "curr_user": content,
                                                                               "fine": get_history()[1],
                                                                               "trans": get_history()[0]})
                for i in curr_pupil:
                    i.acc -= curr_fine.point
                    i.save()
                for i in curr_stat:
                    i.point -= curr_fine.point
                    content.acc += curr_fine.point
                    i.save()
                content.save()
                form_history.save()
                curr_fine.delete()
                success = 'Wispoint yechib olindi'
                return render(request, "wisapp/transfer_parent.html", {"content": content, 'success': success,
                                                                       'curr_point': curr_points, "curr_user": content,
                                                                       "fine": get_history()[1],
                                                                       "trans": get_history()[0]})

            txt = str(form.errors)
            clean_txt = re.sub(r"<[^>]+>", "", txt, flags=re.S)
            print(clean_txt)
            if clean_txt == 'fine_descr???????????????????????? ????????.':
                err = 'Jarima uchun izoh yozing!'

            return render(request, "wisapp/transfer_parent.html", {"content": content, 'error': err,
                                                                   'curr_point': curr_points, "curr_user": content,
                                                                   "fine": get_history()[1], "trans": get_history()[0]})
    return render(request, "wisapp/transfer_parent.html", {"content": content, "curr_point": curr_points,
                                                           "curr_user": content, "fine": get_history()[1],
                                                           "trans": get_history()[0]})


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
                error = 'Hisobingizda wispoint yetarli emas'
                return render(request, "wisapp/fine_parent.html", {"content": content, 'error': error,
                                                                   'curr_point': curr_points})
            if curr_fine.point > curr_stat.point:
                curr_fine.delete()
                error = 'Hisobingizda wispoint yetarli emas'
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
            success = 'wispont ?????????? ??????????????'
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
                error = 'wispoint ???? ?????????? ?????????????? ?????????????? ???? ????????????????????'
                return render(request, "wisapp/d_fine.html", {"content": content, 'error': error,
                                                              "pupil": pupil, 'grade': grades})
            curr_pupil.acc -= curr_trans.point
            s_b.balance += curr_trans.point
            s_b.save()
            curr_pupil.save()
            form_history.save()
            success = 'wispont ?????????? ??????????????'
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
    s_b = models.SchoolBalance.objects.get()
    teaches = models.Teacher.objects.all()
    pars = models.Parent.objects.all()

    def get_history():
        children = pupil
        tech_transfer = models.TransferHistory.objects.filter(teacher_name__in=teaches).order_by('-data')[:5]
        tech_fines = models.FineHistory.objects.filter(teacher_name__in=teaches).order_by('-data')[:5]
        par_trans = models.ParentTransferHistory.objects.filter(parent_name__in=pars).order_by('-data')[:5]
        par_fine = models.FineParentHistory.objects.filter(parent_name__in=pars).order_by('-data')[:5]
        dir_transfer = models.DorZTransferHistory.objects.filter(dorz_name=content).order_by('-data')[:5]
        dir_fines = models.FineDorZHistory.objects.filter(dorz_name=content).order_by('-data')[:5]
        trans = list(chain(tech_transfer, dir_transfer, par_trans))
        fines = list(chain(tech_fines, dir_fines, par_fine))
        return [trans, fines]

    if request.method == 'POST':
        err = "O'quvchini tanlang"
        if request.POST['trans'] == 'transfer':
            form = forms.DorZTransferForm(request.POST)
            form_history = forms.DorZTransferHistoryForm(request.POST)
            if form.is_valid() and form_history.is_valid():
                form.save()
                curr_fine = models.DorZTransfer.objects.get(dorz_name=content.id)
                trans_pupil = []
                for i in curr_fine.pupil.all():
                    trans_pupil.append(i.id)
                print(trans_pupil)
                curr_pupil = models.Pupil.objects.filter(id__in=trans_pupil)
                point_sum = 0
                for i in curr_pupil:
                    point_sum += curr_fine.point
                if point_sum > content.acc:
                    curr_fine.delete()
                    error = 'Hisobingizda wispoint yetarli emas'
                    return render(request, "wisapp/d_transfer.html",
                                  {"content": content, 'error': error, "pupil": pupil,
                                   'grade': grades, "fine": get_history()[1],
                                   "trans": get_history()[0]})
                content.acc -= point_sum
                content.save()
                form_history.save()
                for i in curr_pupil:
                    i.acc += curr_fine.point
                    i.save()
                success = 'Otkazma muvaffaqiyatli yakunlandi'
                curr_fine.delete()
                return render(request, "wisapp/d_transfer.html", {"content": content, 'success': success,
                                                                  "pupil": pupil, 'grade': grades,
                                                                  "fine": get_history()[1],
                                                                  "trans": get_history()[0]})
            return render(request, "wisapp/d_transfer.html", {"content": content, 'error': err,
                                                              "pupil": pupil, 'grade': grades, "fine": get_history()[1],
                                                              "trans": get_history()[0]})
        elif request.POST['trans'] == 'fine':
            form = forms.DorZFineForm(request.POST)
            form_history = forms.DorZTFineHistoryForm(request.POST)
            if form.is_valid() and form_history.is_valid():
                form.save()
                curr_fine = models.FineDorZ.objects.get(dorz_name=content.id)
                fine_list = []
                for i in curr_fine.pupil.all():
                    fine_list.append(i.id)
                curr_pupil = models.Pupil.objects.filter(id__in=fine_list)
                for i in curr_pupil:
                    if curr_fine.point > i.acc:
                        curr_fine.delete()
                        error = "O'quvchinig balansidan katta summa kiritildi"
                        return render(request, "wisapp/d_transfer.html", {"content": content, 'error': error,
                                                                          "pupil": pupil, 'grade': grades,
                                                                          "fine": get_history()[1],
                                                                          "trans": get_history()[0]})
                for i in curr_pupil:
                    i.acc -= curr_fine.point
                    s_b.balance += curr_fine.point
                    i.save()
                s_b.save()
                form_history.save()
                success = 'Wispoint yechib olindi'
                curr_fine.delete()
                return render(request, "wisapp/d_transfer.html", {"content": content, 'success': success,
                                                                  "pupil": pupil, 'grade': grades,
                                                                  "fine": get_history()[1],
                                                                  "trans": get_history()[0]})
            txt = str(form.errors)
            clean_txt = re.sub(r"<[^>]+>", "", txt, flags=re.S)
            print(clean_txt)
            if clean_txt == 'fine_descr???????????????????????? ????????.':
                err = 'Jarima uchun izoh yozing!'
            return render(request, "wisapp/d_transfer.html", {"content": content, 'error': err,
                                                              "pupil": pupil, 'grade': grades, "fine": get_history()[1],
                                                              "trans": get_history()[0]})
    return render(request, "wisapp/d_transfer.html",
                  {"content": content, "pupil": pupil, 'grade': grades, "fine": get_history()[1],
                   "trans": get_history()[0]})


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
            curr_trans = models.SuperUTransD.objects.get(user=content)
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
                error = 'wispont ???? ?????????? ???? ????????????????????'
                return render(request, "wisapp/super_u_d.html", {"content": content, 'error': error, "dorz": dorz})
            s_b.balance -= point_sum
            s_b.save()
            content.save()
            form_history.save()
            for i in curr_dorz:
                i.acc += curr_trans.point
                i.save()
            success = 'Otkazma muvaffaqiyatli yakunlandi'
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
            curr_trans = models.SuperUTransT.objects.get(user=content)
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
                error = 'wispont ???? ?????????? ???? ????????????????????'
                return render(request, "wisapp/super_u_t.html",
                              {"content": content, 'error': error, "teacher": teacher})
            s_b.balance -= point_sum
            s_b.save()
            content.save()
            form_history.save()
            for i in curr_teacher:
                i.acc += curr_trans.point
                i.save()
            success = 'Otkazma muvaffaqiyatli yakunlandi'
            curr_trans.delete()
            return render(request, "wisapp/super_u_t.html", {"content": content, 'success': success, 'teacher': teacher,
                                                             's_b': s_b})
        return render(request, "wisapp/super_u_t.html", {"content": content, 'error': form.errors, 'teacher': teacher,
                                                         's_b': s_b})
    return render(request, "wisapp/super_u_t.html", {"content": content, 'teacher': teacher, 's_b': s_b})


@login_required
def for_pars(request):
    content = models.SchoolBalanceUser.objects.get(user=request.user)
    parent = models.Parent.objects.all()
    s_b = models.SchoolBalance.objects.get()
    if request.method == 'POST':
        form = forms.SuperUTransPForm(request.POST)
        form_history = forms.SuperUTransPHForm(request.POST)
        if form.is_valid() and form_history.is_valid():
            form.save()
            curr_trans = models.SuperUTransP.objects.get(user=content)
            trans_parent = []
            for i in curr_trans.parent.all():
                trans_parent.append(i.id)
            print(trans_parent)
            curr_parent = models.Parent.objects.filter(id__in=trans_parent)
            point_sum = 0
            for i in curr_parent:
                point_sum += curr_trans.point
            if point_sum > s_b.balance:
                curr_trans.delete()
                error = 'wispont ???? ?????????? ???? ????????????????????'
                return render(request, "wisapp/super_u_p.html",
                              {"content": content, 'error': error, "parent": parent})
            s_b.balance -= point_sum
            s_b.save()
            content.save()
            form_history.save()
            for i in curr_parent:
                i.acc += curr_trans.point
                i.save()
            success = 'Otkazma muvaffaqiyatli yakunlandi'
            curr_trans.delete()
            return render(request, "wisapp/super_u_p.html", {"content": content, 'success': success, 'parent': parent,
                                                             's_b': s_b})
        return render(request, "wisapp/super_u_p.html", {"content": content, 'error': form.errors, 'parent': parent,
                                                         's_b': s_b})
    return render(request, "wisapp/super_u_p.html", {"content": content, 'parent': parent, 's_b': s_b})


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
            return redirect('balance_user_stat')
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
                        trans = models.TransferHistory.objects.order_by("-data")[0:50]
                        fine = models.FineHistory.objects.order_by("-data")[0:50]

                        data = {'ok': 1, "roll": get['roll'],
                                "user": {
                                    "id": context.id,
                                    'username': str(context.user),
                                    'name': context.name,
                                    'last_name': context.lastName,
                                    'balance': context.acc,
                                },
                                "transfer_history": [{'user_name': i.teacher_name.name,
                                                      'point': i.point,
                                                      'date': i.data,
                                                      'roll': 'teacher',
                                                      'pupils': [{'pupil_name': f'{d.name} {d.lastName}',
                                                                  'pupil_balance': d.acc} for d in i.pupil.all()],
                                                      } for i in trans],
                                "fine_history": [{'user_name': i.teacher_name.name,
                                                  'point': i.point,
                                                  'transfer_coment': i.fine_descr,
                                                  'date': i.data,
                                                  'roll': 'teacher',
                                                  'pupils': [{'pupil_name': f'{d.name} {d.lastName}',
                                                              'pupil_balance': d.acc} for d in i.pupil.all()],
                                                  } for i in fine],

                                }

                        trans = models.DorZTransferHistory.objects.order_by("-data")[0:50]
                        fine = models.FineDorZHistory.objects.order_by("-data")[0:50]

                        data['transfer_history'] += [{'user_name': i.dorz_name.name,
                                                      'point': i.point,
                                                      'date': i.data,
                                                      'roll': 'direktor',
                                                      'pupils': [{'pupil_name': f'{d.name} {d.lastName}',
                                                                  'pupil_balance': d.acc} for d in i.pupil.all()],
                                                      } for i in trans]

                        data['fine_history'] += [{'user_name': i.dorz_name.name,
                                                  'point': i.point,
                                                  'date': i.data,
                                                  'transfer_coment': i.fine_descr,
                                                  'roll': 'direktor',
                                                  'pupils': [{'pupil_name': f'{d.name} {d.lastName}',
                                                              'pupil_balance': d.acc} for d in i.pupil.all()],
                                                  } for i in fine]

                        trans = models.ParentTransferHistory.objects.order_by("-data")[0:50]
                        fine = models.FineParentHistory.objects.order_by("-data")[0:50]

                        data['transfer_history'] += [{'user_name': i.parent_name.name,
                                                      'point': i.point,
                                                      'date': i.data,
                                                      'roll': 'parent',
                                                      'pupils': [{'pupil_name': f'{d.name} {d.lastName}',
                                                                  'pupil_balance': d.acc} for d in i.pupil.all()],
                                                      } for i in trans]

                        data['fine_history'] += [{'user_name': i.parent_name.name,
                                                  'point': i.point,
                                                  'date': i.data,
                                                  'transfer_coment': i.fine_descr,
                                                  'roll': 'parent',
                                                  'pupils': [{'pupil_name': f'{d.name} {d.lastName}',
                                                              'pupil_balance': d.acc} for d in i.pupil.all()],
                                                  } for i in fine]

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
                    childs = []
                    for i in context.child.all():
                        trans = [{'user_name': tf.teacher_name.name,
                                  'point': tf.point,
                                  'roll': 'teacher',
                                  'data': tf.data} for tf in
                                 models.TransferHistory.objects.filter(pupil=i).order_by("-data")[:50]]
                        trans_fine = [{'user_name': tf.teacher_name.name,
                                       'point': tf.point,
                                       'roll': 'teacher',
                                       'descr': tf.fine_descr,
                                       'data': tf.data} for tf in
                                      models.FineHistory.objects.filter(pupil=i).order_by("-data")[:50]]
                        for pt in models.ParentTransferHistory.objects.filter(parent_name=context, pupil=i).order_by(
                                "-data")[:50]:
                            trans.append({'user_name': pt.parent_name.name,
                                          'point': pt.point,
                                          'roll': 'parent',
                                          'data': pt.data})
                        for pf in models.FineParentHistory.objects.filter(parent_name=context, pupil=i).order_by(
                                "-data")[:50]:
                            trans_fine.append({'user_name': pf.parent_name.name,
                                               'point': pf.point,
                                               'roll': 'parent',
                                               'descr': pf.fine_descr,
                                               'data': pf.data})
                        for dt in models.DorZTransferHistory.objects.filter(pupil=i).order_by("-data")[:50]:
                            trans.append({'user_name': dt.dorz_name.name,
                                          'point': dt.point,
                                          'roll': 'direktor',
                                          'data': dt.data})
                        for df in models.FineDorZHistory.objects.filter(pupil=i).order_by("-data")[:50]:
                            trans_fine.append({'user_name': df.dorz_name.name,
                                               'point': df.point,
                                               'roll': 'direktor',
                                               'descr': df.fine_descr,
                                               'data': df.data})

                        childs.append({"id": i.id,
                                       "name": i.name,
                                       "last_name": i.lastName,
                                       "grade": i.grade_p.gradeName,
                                       "balance": i.acc,
                                       "trans": trans,
                                       "fine": trans_fine
                                       })

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
                                fines_his = models.FineParentHistory.objects.create(parent_name=context,
                                                                                    point=transfer_point)
                                fines_his.pupil.add(pupil)
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
                                            # "trans": [[{'user_name': m.parent_name.name,
                                            #             'point': m.point,
                                            #             'roll': 'parent',
                                            #             'data': m.data
                                            #             } for m in
                                            #            models.ParentTransferHistory.objects.filter(pupil=p).order_by(
                                            #                '-data')[:50]],
                                            #           [{'user_name': m.dorz_name.name,
                                            #             'point': m.point,
                                            #             'roll': 'direktor',
                                            #             'data': m.data
                                            #             } for m in
                                            #            models.DorZTransferHistory.objects.filter(pupil=p).order_by(
                                            #                '-data')[:50]],
                                            #
                                            #           [{'user_name': m.teacher_name.name,
                                            #             'point': m.point,
                                            #             'roll': 'teacher',
                                            #             'data': m.data
                                            #             } for m in
                                            #            models.TransferHistory.objects.filter(pupil=p).order_by('-data')[
                                            #            :50]],
                                            #           ],
                                            # "trans_fine": [[{'user_name': m.parent_name.name,
                                            #                  'point': m.point,
                                            #                  'roll': 'parent',
                                            #                  'descr': m.fine_descr,
                                            #                  'data': m.data
                                            #                  } for m in
                                            #                 models.FineParentHistory.objects.filter(pupil=p).order_by(
                                            #                     '-data')[:50]],
                                            #                [{'user_name': m.dorz_name.name,
                                            #                  'point': m.point,
                                            #                  'roll': 'direktor',
                                            #                  'descr': m.fine_descr,
                                            #                  'data': m.data
                                            #                  } for m in
                                            #                 models.FineDorZHistory.objects.filter(pupil=p).order_by(
                                            #                     '-data')[:50]],
                                            #                [{'user_name': m.teacher_name.name,
                                            #                  'point': m.point,
                                            #                  'roll': 'teacher',
                                            #                  'descr': m.fine_descr,
                                            #                  'data': m.data
                                            #                  } for m in
                                            #                 models.FineHistory.objects.filter(pupil=p).order_by(
                                            #                     '-data')[:50]
                                            #                 ]],
                                            "exchange": [k.point for k in models.PointTrans.objects.filter(pupil=p.id,
                                                                                                           teacher=
                                                                                                           context.id)]
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
                    elif get['r_type'] == 'history':
                        history_tech_trans = models.TransferHistory.objects.filter(pupil=get['pupil_id']).order_by(
                            '-data')[:50]
                        history_par_trans = models.ParentTransferHistory.objects.filter(pupil=get['pupil_id']).order_by(
                            '-data')[:50]
                        history_dorz_trans = models.DorZTransferHistory.objects.filter(pupil=get['pupil_id']).order_by(
                            '-data')[:50]
                        history_tech_fine = models.FineHistory.objects.filter(pupil=get['pupil_id']).order_by(
                            '-data')[:50]
                        history_par_fine = models.FineParentHistory.objects.filter(pupil=get['pupil_id']).order_by(
                            '-data')[:50]
                        history_dorz_fine = models.FineDorZHistory.objects.filter(pupil=get['pupil_id']).order_by(
                            '-data')[:50]

                        data = []

                        for h in list(
                                chain(history_tech_trans, history_par_trans, history_dorz_trans, history_tech_fine,
                                      history_par_fine, history_dorz_fine)):
                            if hasattr(h, 'parent_name'):
                                name = h.parent_name.name
                                roll = 'parent'
                            elif hasattr(h, 'teacher_name'):
                                name = h.teacher_name.name
                                roll = 'teacher'
                            else:
                                name = h.dorz_name.name
                                roll = 'direktor'

                            if hasattr(h, 'fine_descr'):
                                data.append({'user_name': name,
                                             'point': h.point,
                                             'roll': roll,
                                             'data': h.data,
                                             'fine_coment': h.fine_descr
                                             })
                            else:
                                data.append({'user_name': name,
                                             'point': h.point,
                                             'roll': roll,
                                             'data': h.data
                                             })

                    elif get['r_type'] == 'transfer':
                        pupils = list(set([int(n) for n in get['pupils'].split(",") if len(n.strip()) > 0]))
                        print(pupils)
                        transfer_point = int(get['transfer_point'])
                        transfer_coment = get['transfer_coment']
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
                                fine_his = models.FineHistory.objects.create(teacher_name=context,
                                                                  transfer_grade=grade_db,
                                                                  fine_descr=transfer_coment,
                                                                  point=transfer_point)
                                fine_his.pupil.add(pupil)
                                trans_list.append({'pupil_id': pupil.id,
                                                   'point': trans_doc.point,
                                                   'point_sum': trans_doc.point_sum,
                                                   'pupil_balance': pupil.acc,
                                                   })
                                data['transfer']['teacher_balance'] = context.acc
                                data['transfer']['transfer_list'] = trans_list
                                # data['transfer']['descr'] = transfer_coment
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
        return JsonResponse(data, safe=False)


def web_app(request):
    return render(request, 'wisapp/webapp/index.html')


def bot(request):
    print(request)

# import openpyxl
# def test(request):
#     book = openpyxl.load_workbook('wisapp/PUPS.xlsx')
#     worksheet = book.active
#
#     p_code = []
#     p_name = []
#     p_lastname = []
#     p_class = []
#     p_user = []
#
#     # ???????????????? ???????????? ????????????
#     sheets = book.sheetnames
#     for sheet in sheets:
#         print(sheet)
#
#     # ???????????????? ???????????????? ????????
#     sheet = book.active
#
#     for cell in sheet['A']:
#         p_code.append(cell.value)
#
#     for cell in sheet['B']:
#         p_name.append(cell.value)
#
#     for cell in sheet['C']:
#         p_lastname.append(cell.value)
#
#     for cell in sheet['F']:
#         p_class.append(cell.value)
#
#     for cell in sheet['G']:
#         p_user.append(cell.value)
#
#     print(p_code)
#     print(p_user)
#     print(p_name)
#     print(p_class)
#     print(len(p_lastname))
#
#     for i in range(1, len(p_lastname) + 1):
#         us = User.objects.get(username=p_code[i])
#         grade = models.Grade.objects.get(id=p_class[i])
#         models.Pupil.objects.create(pupil_code=p_code[i], user=us, name=p_name[i], lastName=p_lastname[i],
#                                     grade_p=grade, acc=0)

# book = openpyxl.load_workbook('wisapp/??????????1.xlsx')
# worksheet = book.active
# user = []
# passw = []
# for i in range(1, worksheet.max_row):
#     for col in worksheet.iter_cols(1, worksheet.max_column):
#         if len(str(col[i].value)) == 5:
#             user.append(col[i].value)
#         else:
#             passw.append(col[i].value)
# for i in range(0, len(user)):
#     User.objects.create_user(user[i], f'{user[i]}@test.com', passw[i]).save()
# return HttpResponse(f'{user}paaaaaaaaaas{passw}')
