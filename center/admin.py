from datetime import datetime

from django.contrib import admin
from .models import Teacher, Group, Subject, Student, Membership, Payment


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    exclude = ()
    list_display = ('first_name', 'last_name', 'all_pays', 'salary', 'phone_number')
    search_fields = ('first_name', 'last_name')

    def all_pays(self, obj):
        pays = 0
        qs = Payment.objects.filter(group__owner_id=obj.id)
        for py in qs:
            if py.status == 1:
                pays += py.amount
        return pays

    def salary(self, obj):
        salary = 0
        qs = Payment.objects.filter(group__owner_id=obj.id)
        for py in qs:
            if py.status == 1:
                salary += py.amount * py.group.teacher_part
        return salary


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    exclude = ()
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    exclude = ()
    list_display = ('name', 'subject', 'owner', 'price', 'teacher_part')
    search_fields = ('name',)
    autocomplete_fields = ('subject', 'owner')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    exclude = ()
    list_display = ('full_name', 'phone_number')
    search_fields = ('full_name',)


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    exclude = ('credit',)
    list_display = ('student', 'group', 'credit_s', 'pay_update_date', 'added_date')
    autocomplete_fields = ('group', 'student')

    def credit_s(self, obj):
        qs = Payment.objects.filter(student_id=obj.student.id)
        pays = 0
        for pay in qs:
            if pay.group.id == obj.group.id:
                pays += pay.amount
        return obj.credit - pays

    def get_queryset(self, request):
        qs = super(MembershipAdmin, self).get_queryset(request)
        for obj in qs:
            if obj.credit == 123:
                obj.credit = obj.group.price * (1 - obj.discount)
                obj.save()
            elif int(obj.pay_update_date.strftime("%m")) < datetime.now().month:
                obj.credit += obj.group.price
                obj.save()
        return qs


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    exclude = ('status',)
    list_display = ('student', 'group', 'amount', 'date', 'status',)
