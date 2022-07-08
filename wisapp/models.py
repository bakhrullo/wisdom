from django.db import models
from django.conf import settings


class Grade(models.Model):
    gradeName = models.CharField(max_length=100, verbose_name="Класс", unique=True)
    data = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    def __str__(self):
        return self.gradeName

    class Meta:
        verbose_name = "Классы"
        verbose_name_plural = "Классы"


class Seller(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="Имя")
    lastName = models.CharField(max_length=100, verbose_name="Фамилия")
    data = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    class Meta:
        verbose_name = "Продавцы"
        verbose_name_plural = "Продавцы"

    def __str__(self):
        return self.name


class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="Имя")
    lastName = models.CharField(max_length=100, verbose_name="Фамилия")
    grade_t = models.ManyToManyField(Grade, verbose_name="Закрепленные классы")
    acc = models.IntegerField(null=True, blank=True, verbose_name="Баланс")
    data = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    def __str__(self):
        return self.name + ' ' + self.lastName

    def grades(self):
        return "\n".join([g.gradeName for g in self.grade_t.all()])

    class Meta:
        verbose_name = "Учителя"
        verbose_name_plural = "Учителя"


class Pupil(models.Model):
    pupil_code = models.PositiveIntegerField(verbose_name='Код ученика', null=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lastName = models.CharField(max_length=100, verbose_name="Фамилия")
    name = models.CharField(max_length=100, verbose_name="Имя")
    grade_p = models.ForeignKey(Grade, on_delete=models.PROTECT, verbose_name="Класс")
    acc = models.IntegerField(null=True, blank=True, verbose_name="Баланс")
    data = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    def __str__(self):
        return self.name + ' ' + self.lastName

    class Meta:
        verbose_name = "Ученики"
        verbose_name_plural = "Ученики"


class Parent(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="Имя")
    lastName = models.CharField(max_length=100, verbose_name="Фамилия")
    child = models.ManyToManyField(Pupil, verbose_name="Ученик")
    acc = models.IntegerField(null=True, blank=True, verbose_name="Баланс")
    data = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    def __str__(self):
        return self.name + ' ' + self.lastName

    def childes(self):
        return "\n".join([g.name for g in self.child.all()])

    class Meta:
        verbose_name = "Родители"
        verbose_name_plural = "Родители"


class DorZ(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="Имя")
    lastName = models.CharField(max_length=100, verbose_name="Фамилия")
    acc = models.PositiveIntegerField(default=0, verbose_name="Баланс")
    data = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    def __str__(self):
        return self.name + ' ' + self.lastName

    class Meta:
        verbose_name = "Директоры"
        verbose_name_plural = "Директоры"


class Transfers(models.Model):
    teacher_name = models.ForeignKey(Teacher, on_delete=models.PROTECT)
    transfer_grade = models.ForeignKey(Grade, on_delete=models.PROTECT, null=True)
    pupil = models.ManyToManyField(Pupil, verbose_name='Выберете ученика')
    point = models.PositiveIntegerField()

    def t_g(self):
        return "\n".join([g.name for g in self.pupil.all()])


class TransferHistory(models.Model):
    teacher_name = models.ForeignKey(Teacher, on_delete=models.PROTECT, verbose_name='Уччитель')
    transfer_grade = models.ForeignKey(Grade, on_delete=models.PROTECT, null=True, verbose_name='Класс')
    pupil = models.ManyToManyField(Pupil, verbose_name='Выберете ученика')
    point = models.PositiveIntegerField()
    data = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    def t_g(self):
        return "\n".join([g.name for g in self.pupil.all()])

    class Meta:
        verbose_name = "История переводов учителей"
        verbose_name_plural = "История переводов учителей"


class ParentTransfer(models.Model):
    parent_name = models.ForeignKey(Parent, on_delete=models.PROTECT)
    pupil = models.ManyToManyField(Pupil, verbose_name='Выберете ученика')
    point = models.PositiveIntegerField()

    def t_g(self):
        return "\n".join([g.name for g in self.pupil.all()])


class ParentTransferHistory(models.Model):
    parent_name = models.ForeignKey(Parent, on_delete=models.PROTECT, verbose_name='Родитель')
    pupil = models.ManyToManyField(Pupil, verbose_name='Выберете ученика')
    point = models.PositiveIntegerField()
    data = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    def t_g(self):
        return "\n".join([g.name for g in self.pupil.all()])

    class Meta:
        verbose_name = "История переводов родителей"
        verbose_name_plural = "История переводов родителей"


class PointTrans(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT)
    pupil = models.ForeignKey(Pupil, on_delete=models.PROTECT)
    point = models.IntegerField(default=0)
    point_sum = models.PositiveIntegerField(default=0)
    data = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    class Meta:
        verbose_name = "Переводы учителей"
        verbose_name_plural = "Переводы учителей"


class Fine(models.Model):
    teacher_name = models.ForeignKey(Teacher, on_delete=models.PROTECT)
    transfer_grade = models.ForeignKey(Grade, on_delete=models.PROTECT, null=True)
    pupil = models.ManyToManyField(Pupil)
    fine_descr = models.CharField(max_length=250, null=True)
    point = models.PositiveIntegerField()


class FineHistory(models.Model):
    teacher_name = models.ForeignKey(Teacher, on_delete=models.PROTECT, verbose_name='Имя учителя')
    transfer_grade = models.ForeignKey(Grade, on_delete=models.PROTECT, null=True, verbose_name='Класс')
    pupil = models.ManyToManyField(Pupil, verbose_name='Выберете ученика')
    point = models.PositiveIntegerField()
    fine_descr = models.CharField(max_length=250, null=True, verbose_name='Описание штрафа')
    data = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    def f_p(self):
        return "\n".join([g.name for g in self.pupil.all()])

    class Meta:
        verbose_name = "История штрафов учителей"
        verbose_name_plural = "История штрафов учителей"


class PointTransParents(models.Model):
    teacher = models.ForeignKey(Parent, on_delete=models.PROTECT, verbose_name='Учитель')
    pupil = models.ForeignKey(Pupil, on_delete=models.PROTECT, verbose_name='Ученик')
    point = models.IntegerField(default=0)
    point_sum = models.PositiveIntegerField(default=0)
    data = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    class Meta:
        verbose_name = "Переводы родителей"
        verbose_name_plural = "Переводы родителей"


class FineParent(models.Model):
    parent_name = models.ForeignKey(Parent, on_delete=models.PROTECT)
    pupil = models.ManyToManyField(Pupil, verbose_name='Выберете ученика')
    fine_descr = models.CharField(max_length=250, null=True, verbose_name='Описание штрафа')
    point = models.PositiveIntegerField()


class FineParentHistory(models.Model):
    parent_name = models.ForeignKey(Parent, on_delete=models.PROTECT, verbose_name='Родители')
    pupil = models.ManyToManyField(Pupil, verbose_name='Выберете ученика')
    fine_descr = models.CharField(max_length=250, null=True, verbose_name='Описание штрафа')
    point = models.PositiveIntegerField()
    data = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    def f_p(self):
        return "\n".join([g.name for g in self.pupil.all()])

    class Meta:
        verbose_name = "История штрафов родителей"
        verbose_name_plural = "История штрафов родителей"


class SchoolBalance(models.Model):
    balance = models.PositiveBigIntegerField(verbose_name='Баланс')

    class Meta:
        verbose_name = "Баланс школы"
        verbose_name_plural = "Баланс школы"


class DorZTransfer(models.Model):
    dorz_name = models.ForeignKey(DorZ, on_delete=models.PROTECT)
    pupil = models.ManyToManyField(Pupil)
    point = models.PositiveIntegerField()

    def pupil_show(self):
        return "\n".join([g.name for g in self.pupil.all()])


class DorZTransferHistory(models.Model):
    dorz_name = models.ForeignKey(DorZ, on_delete=models.PROTECT, verbose_name='Директор')
    pupil = models.ManyToManyField(Pupil, verbose_name='Ученик')
    point = models.PositiveIntegerField()
    data = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    def pupil_show(self):
        return "\n".join([g.name for g in self.pupil.all()])

    class Meta:
        verbose_name = "История переводов завучы и директоры"
        verbose_name_plural = "История переводов завучы и директоры"


class FineDorZ(models.Model):
    dorz_name = models.ForeignKey(DorZ, on_delete=models.PROTECT)
    pupil = models.ManyToManyField(Pupil)
    fine_descr = models.CharField(max_length=250, null=True)
    point = models.PositiveIntegerField()


class FineDorZHistory(models.Model):
    dorz_name = models.ForeignKey(DorZ, on_delete=models.PROTECT, verbose_name='Директор')
    pupil = models.ManyToManyField(Pupil, verbose_name='Ученик')
    fine_descr = models.CharField(max_length=250, null=True, verbose_name='Описание штрафа')
    point = models.PositiveIntegerField()
    data = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    def f_p(self):
        return "\n".join([g.name for g in self.pupil.all()])

    class Meta:
        verbose_name = "История штрафов завучы и директоры"
        verbose_name_plural = "История штрафов завучы и директоры"


class SchoolBalanceUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='Имя')
    lastName = models.CharField(max_length=100, verbose_name='Фамилия')
    date = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    class Meta:
        verbose_name = "Пользователь обшего баланса"
        verbose_name_plural = "Пользователь обшего баланса"

    def __str__(self):
        return self.name


class SuperUTransT(models.Model):
    user = models.ForeignKey(SchoolBalanceUser, on_delete=models.PROTECT)
    teacher = models.ManyToManyField(Teacher)
    point = models.PositiveIntegerField()


class SuperUTransTH(models.Model):
    user = models.ForeignKey(SchoolBalanceUser, on_delete=models.PROTECT)
    teacher = models.ManyToManyField(Teacher, verbose_name="Учитель")
    point = models.PositiveIntegerField()
    data = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    class Meta:
        verbose_name = "ПОБ история учителей"
        verbose_name_plural = "ПОБ история учителей"


class SuperUTransD(models.Model):
    user = models.ForeignKey(SchoolBalanceUser, on_delete=models.PROTECT)
    dorz = models.ManyToManyField(DorZ)
    point = models.PositiveIntegerField()


class SuperUTransDH(models.Model):
    user = models.ForeignKey(SchoolBalanceUser, on_delete=models.PROTECT)
    dorz = models.ManyToManyField(DorZ, verbose_name="Директор")
    point = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    class Meta:
        verbose_name = "ПОБ история д или з"
        verbose_name_plural = "ПОБ история д или з"


class SuperUTransP(models.Model):
    user = models.ForeignKey(SchoolBalanceUser, on_delete=models.PROTECT)
    parent = models.ManyToManyField(Parent)
    point = models.PositiveIntegerField()


class SuperUTransPH(models.Model):
    user = models.ForeignKey(SchoolBalanceUser, on_delete=models.PROTECT)
    parent = models.ManyToManyField(Parent, verbose_name="Родители")
    point = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    class Meta:
        verbose_name = "ПОБ история родителм"
        verbose_name_plural = "ПОБ история родители"


class SchoolBalanceAdd(models.Model):
    user = models.ForeignKey(SchoolBalanceUser, on_delete=models.PROTECT)
    point = models.PositiveBigIntegerField()
    date = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    class Meta:
        verbose_name = "Пополнение школьного баланса"
        verbose_name_plural = "Пополнение школьного баланса"


class Sell(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.PROTECT, verbose_name="Продавец")
    pupil = models.ForeignKey(Pupil, on_delete=models.PROTECT, verbose_name="Ученик")
    good_name = models.CharField(max_length=100, verbose_name="Товар")
    point = models.PositiveIntegerField()
    datetime = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    class Meta:
        verbose_name = "История продаж"
        verbose_name_plural = "История продаж"

