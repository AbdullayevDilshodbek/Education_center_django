
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        unique_together = ('name',)


class Teacher(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    image = models.ImageField(upload_to="teacher_image")

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        unique_together = ('first_name', 'last_name')


class Group(models.Model):
    name = models.CharField(max_length=100)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    owner = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    price = models.IntegerField()
    teacher_part = models.FloatField()

    def __str__(self):
        return f'{self.name}->{self.subject}->{self.owner}'

    class Meta:
        unique_together = ('name', 'subject', 'owner')


class Student(models.Model):
    full_name = models.CharField(max_length=200)
    phone_number = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    group = models.ManyToManyField('Group', through='Membership', related_name="+",
                                   through_fields=('student', 'group'))

    def __str__(self):
        return f'{self.full_name}'

    class Meta:
        unique_together = ('full_name',)


class Membership(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    credit = models.IntegerField(default=123)
    discount = models.FloatField()
    pay_update_date = models.DateTimeField(auto_now=True)
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student}->{self.group}->{self.group.subject}'

    class Meta:
        unique_together = ('student', 'group')


class Payment(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    amount = models.IntegerField()
    date = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=1)
