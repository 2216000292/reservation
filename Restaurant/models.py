from django.db import models
from django.contrib import admin
from django.utils.html import format_html
TimePriod = {"1": "9:00-11:00", "2": "11:00-13:00", "3": "15:00-17:00", "4": "17:00-19:00",
             "5": "19:00-21:00", "6": "21:00-23:00"}
class Dinning(models.Model):
    choice = (("9:00-11:00","1"),
              ("11:00-13:00","2"),
              ("15:00-17:00","3"),
              ("17:00-19:00","4"),
              ("19:00-21:00","5"),
              ("21:00-23:00","6"))
    name = models.CharField(verbose_name="customer", default="default", max_length=20)
    date = models.DateField(verbose_name="orderdate")
    title = models.CharField(verbose_name="title", default="default", max_length=20)
    state =  models.CharField(verbose_name="state", default="empty", max_length=20)
    select_time_period = models.CharField(verbose_name="select_time_period", choices=choice, default="1",max_length=20)


class TableInforamtion(models.Model):
    choice = (("9:00-11:00","1"),
              ("11:00-13:00","2"),
              ("15:00-17:00","3"),
              ("17:00-19:00","4"),
              ("19:00-21:00","5"),
              ("21:00-23:00","6"))


    number = models.IntegerField(verbose_name='number')
    date = models.DateField(verbose_name="order date")
    customer = models.CharField(verbose_name="customer", default="default", max_length=20)
    state =  models.CharField(verbose_name="state", default="empty", max_length=20)
    table_id =  models.IntegerField(verbose_name='tableId',default=0)
    select_time_period = models.CharField(verbose_name="select_time_period", choices=choice, default="1",max_length=20)
    def period_dis(self):

        return format_html(
            '<span style="color: {}">{}</span>',
            "#333",
            TimePriod[self.select_time_period],
        )

    def save(self, *args, **kwargs):

        dinner =Dinning.objects.filter(select_time_period=self.select_time_period,date =self.date).first()
        if dinner:
            if self.state == 'Free':
                dinner.state = 'Free'
                dinner.save()
        super(TableInforamtion, self).save()


@admin.register(TableInforamtion)
class TableInforamtionAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'date', 'customer', 'table_id', 'period_dis','state')
    list_per_page = 20
    search_fields = ('id', 'number', 'date', 'customer', 'table_id', 'period_dis','state')
    # list_editable = ('state',)
    fields = ('number', 'date', 'customer', 'table_id','state')


    list_filter = ("state", )

# Create your models here.
class TableOrder(models.Model):
    choice = (("9:00-11:00","1"),
              ("11:00-13:00","2"),
              ("15:00-17:00","3"),
              ("17:00-19:00","4"),
              ("19:00-21:00","5"),
              ("21:00-23:00","6"))
    name = models.CharField(verbose_name="customer", default="default", max_length=20)
    price = models.FloatField(verbose_name="shopPrice", default=0.0)
    number = models.IntegerField(verbose_name="number")
    date = models.DateField(verbose_name="order date")
    reser_date = models.DateField(verbose_name="reservation_date")
    introduce = models.CharField(verbose_name="introduce", default="default", max_length=256)
    table_ids = models.CharField(verbose_name="table_ids", default="", max_length=256)
    select_time_period = models.CharField(verbose_name="select_time_period", choices=choice, default="1",max_length=20)
    state = models.CharField(verbose_name="state", default="order", max_length=20) # in other state cancel
    class Meta:
        verbose_name = 'TableOrder'

    def __str__(self):
        return self.name + " " + str(self.reser_date) + " " + TimePriod[self.select_time_period]



class UserInfo(models.Model):
    options = (("cash", "cash"), ("credit", "credit"), ("check", "check"))
    username = models.CharField(verbose_name="username", unique=True, max_length=256)
    password = models.CharField(verbose_name="password", default="", max_length=256)
    name = models.CharField(verbose_name="Name",  max_length=256)
    mailling_address = models.CharField(verbose_name="mailling address",  max_length=256)
    billing_address = models.CharField(verbose_name="billing address",  max_length=256)
    preferred_diner = models.CharField(verbose_name="preferred diner", max_length=256)
    earned_points = models.FloatField(default=0.0)
    preferred_payment_method = models.CharField(choices=options, verbose_name="preferred_payment_method",
                                                max_length=256)

    class Meta:
        verbose_name = "UserInfo"

@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'password', 'name', 'mailling_address', 'billing_address', 'preferred_diner','earned_points','preferred_payment_method')
    list_per_page = 20
