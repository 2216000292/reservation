import requests
from django.shortcuts import render, HttpResponse, redirect
from django.http import FileResponse, JsonResponse
import time

from .models import UserInfo, TableOrder, TableInforamtion, Dinning

# Create your views here.
# home page
Table8Num = 2
Table6Num = 2
Table4Num = 8
Table2Num = 6
count = 1

DinningName = ["Happy eating", 'Mile melo', 'Lady hill', 'Pure-zone', 'Encounter', 'Hall']
SelectName = ["cash", "credit", "check"]
TimePriod = {"1": "9:00-11:00", "2": "11:00-13:00", "3": "15:00-17:00", "4": "17:00-19:00",
             "5": "19:00-21:00", "6": "21:00-23:00"}


# Sign up for an account
def register(request):
    print(request.POST)
    username = request.POST.get("username")
    password = request.POST.get("password")
    name = request.POST.get("name")
    mailling_address = request.POST.get('mailing address')
    billing_address = request.POST.get('billing address')
    same = request.POST.get('same')
    payment = request.POST.get("payment")
    print(username, password, mailling_address, billing_address, same, payment)

    try:
        errors = []
        if not username:
            errors.append('username')
        if not password:
            errors.append('password')
        if not name:
            errors.append('name')

        if not mailling_address:
            errors.append('mailling address')
        if not same and not billing_address:
            errors.append('billing address')
        if same:
            billing_address = mailling_address
        if len(errors) == 0:
            userinfo = UserInfo()
            userinfo.username = username
            userinfo.password = str(password)
            userinfo.name = name
            userinfo.mailling_address = mailling_address
            userinfo.billing_address = billing_address
            userinfo.preferred_diner = "The hall"
            userinfo.preferred_payment_method = SelectName[int(payment) - 1]
            request.session["username"] = username
            request.session.set_expiry(60000)
            userinfo.save()
            res = {'status': 0, 'msg': 'Registered successfully'}
        else:
            res = {'status': 1, 'msg': ' ,'.join(errors) + " is empty ,please rewrite it！"}
    except errors as e:
        print(e)
        res = {'status': 1, 'msg': 'The user name repetition'}

    return JsonResponse(res)


# Log on to check
def login(request):
    username = request.POST.get("username")
    password = request.POST.get("password")

    result = UserInfo.objects.filter(username=username).first()

    if password == result.password:
        res = {'status': 0, 'msg': 'Login successfully'}
        request.session["username"] = username

        username = request.session.get('username', None)
        user = UserInfo.objects.filter(username=username).first()
        user.save()
        request.session.set_expiry(60000)
    else:
        res = {'status': 1, 'msg': 'The user name or password error'}

    return JsonResponse(res)


# logout
def logout(request):
    request.session.flush()
    return redirect("/")


def createVisitorAccount():
    name = UserInfo.objects.filter(username="visitor").first()

    if not name:
        userinfo = UserInfo()
        userinfo.username = "visitor"
        userinfo.password = "11111111"
        userinfo.name = "visitor"
        userinfo.mailling_address = "NONE"
        userinfo.billing_address = "NONE"
        userinfo.preferred_diner = "The hall"
        userinfo.save()
    else:
        userinfo = name


def generate_preferred(request):
    if request.method == "POST":
        username = request.session.get('username', None)
        print("TEST:", username)
        if username:

            datas = UserInfo.objects.filter(username=username).first()
            print("TEST:", datas)
            if datas:
                # Get the people often go to which restaurant
                orders = Dinning.objects.filter(name=datas.name).all()
                if orders:
                    dict_order = {}
                    for order in orders:
                        if dict_order.get(order.title):
                            dict_order[order.title] += 1
                        else:
                            dict_order[order.title] = 1
                    print("TEST:", dict_order)
                    # The sorting
                    sorted_name = sorted(dict_order.items(), key=lambda s: s[1], reverse=True)
                    preferred = sorted_name[0][0]
                    datas.preferred_diner = preferred
                    datas.save()
                    print('TEST：', datas)
                    return JsonResponse({'msg': preferred, 'ep': datas.earned_points})
        return JsonResponse({'msg': 'Hall', 'ep': 0})


# Commodity page
def create_free_tables(request=None):
    global count
    if request:
        timeNow = request.POST.get("date")
        time_period = request.POST.get("period")
    else:
        timeNow = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        time_period = "1"
    count = 1
    datas = TableInforamtion.objects.filter(date=str(timeNow))

    if not datas:
        for w in TimePriod.keys():
            for i in range(Table8Num):
                create_table_sql(8, timeNow, w)
            for i in range(Table6Num):
                create_table_sql(6, timeNow, w)
            for i in range(Table4Num):
                create_table_sql(4, timeNow, w)
            for i in range(Table2Num):
                create_table_sql(2, timeNow, w)
            # 生成餐厅名字
            for title in DinningName:
                create_dinner_sql(title, timeNow, w)

    if request:
        res = {'status': 0, 'msg': 'update！'}
        return JsonResponse(res)
    else:
        return None


def search_dinner(request):
    if request.method == "GET":
        datevalue = request.GET.get('datevalue')
        period = request.GET.get('period')
        print("datevalue:", datevalue)
        dinners = Dinning.objects.filter(date=str(datevalue), select_time_period=period)
        return render(request, 'dinner.html', {'dinners': dinners})


def create_table_sql(n, timeNow, select="1"):
    global count
    tablenew = TableInforamtion()
    tablenew.number = n
    tablenew.state = "Free"
    tablenew.date = timeNow
    tablenew.table_id = count
    tablenew.select_time_period = select
    tablenew.save()
    count += 1


def create_dinner_sql(title, timeNow, select):
    dinner = Dinning()
    # dinner.name = name
    dinner.title = title
    dinner.select_time_period = select
    dinner.date = timeNow
    dinner.state = 'Free'
    dinner.save()


def reservation(request):
    username = request.session.get('username', None)
    datas = UserInfo.objects.filter(username=username).first()

    create_free_tables()
    timeNow = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    tabledatas = TableInforamtion.objects.filter(date=str(timeNow))

    return render(request, 'reservation.html', {'datas': datas, 'tabledatas': tabledatas, })


def resevation_order(request):
    user = request.session.get('username', None)
    print(request.POST)
    if user == None:
        createVisitorAccount()
        user = "visitor"
    select_date = request.POST.get("select_date")
    number = request.POST.get("number of people")
    dinner_name = request.POST.get("dinner name")
    period = request.POST.get("downBox")
    credit_card =  request.POST.get("credit_card")

    if number:
        number = int(number)
        if credit_card.strip() == '':
            res = {'status': 1, 'msg': 'Reserve Failed!Please Entry your Credit Card Information！'}
            return JsonResponse(res)
        tabels = []
        tablenew = 0
        if number <= 2:
            tablenew = TableInforamtion.objects.filter(number=2, state='Free', date=select_date,
                                                       select_time_period=period).first()
            tableupper = TableInforamtion.objects.filter(number=4, state='Free', date=select_date,
                                                         select_time_period=period).all()

            if tablenew:
                tablenew.state = "Order"
            elif len(tableupper) >= 1:
                tables = [tableupper[0]]
        elif number <= 4 and number > 2:
            tablenew = TableInforamtion.objects.filter(number=4, state='Free', date=select_date,
                                                       select_time_period=period).first()
            tableupper = TableInforamtion.objects.filter(number=6, state='Free', date=select_date,
                                                         select_time_period=period).all()

            if tablenew:

                tablenew.state = "Order"
            else:
                # 如果四个座位的桌子不够 则进行拼桌
                table = TableInforamtion.objects.filter(number=2, state='Free', date=select_date,
                                                        select_time_period=period).all()
                if len(table) >= 2:
                    tabels = table[0:2]
                    for i in tabels:
                        i.status = "Order"
                elif len(tableupper) >= 1:
                    print("选择大桌")
                    tabels = [tableupper[0]]
                else:
                    tables = []

        elif number <= 6 and number > 4:
            tablenew = TableInforamtion.objects.filter(number=6, state='Free', date=select_date,
                                                       select_time_period=period).first()
            tableupper = TableInforamtion.objects.filter(number=8, state='Free', date=select_date,
                                                         select_time_period=period).all()
            if tablenew:
                tablenew.state = "Order"
            else:
                # 如果六个座位的桌子不够 则进行拼桌
                table = TableInforamtion.objects.filter(number=4, state='Free', date=select_date,
                                                        select_time_period=period).all()
                table2 = TableInforamtion.objects.filter(number=2, state='Free', date=select_date,
                                                         select_time_period=period).all()

                if len(table2) >= 1 and len(table) >= 1:
                    tabels = [table[0], table2[0]]
                elif len(table2) == 0:
                    if len(table) >= 2:
                        tabels = table[:2]
                    elif len(tableupper) >= 1:
                        print("选择大桌")
                        tabels = [tableupper[0]]
                    else:
                        tabels = []




        elif number <= 8 and number > 6:
            tablenew = TableInforamtion.objects.filter(number=8, state='Free', date=select_date,
                                                       select_time_period=period).first()
            if tablenew:
                tablenew.state = "Order"
            else:
                # 如果六个座位的桌子不够 则进行拼桌
                table = TableInforamtion.objects.filter(number=6, state='Free', date=select_date,
                                                        select_time_period=period).all()
                if len(table) >= 1:
                    tabels.append(table[0])
                    table2 = TableInforamtion.objects.filter(number=2, state='Free', date=select_date,
                                                             select_time_period=period).all()
                    if len(table2) >= 1:
                        tabels.append(table2[0])
                        for i in tabels:
                            i.status = "Order"
                    else:
                        tables = []
                else:
                    table = TableInforamtion.objects.filter(number=4, state='Free', date=select_date,
                                                            select_time_period=period).all()
                    if len(table) >= 2:
                        tabels = table[:2]
                        for i in tabels:
                            i.status = "Order"
                    else:
                        tables = []
        elif number <= 10 and number > 8:

            table = TableInforamtion.objects.filter(number=8, state='Free', date=select_date,
                                                    select_time_period=period).all()
            table2 = TableInforamtion.objects.filter(number=2, state='Free', date=select_date,
                                                     select_time_period=period).all()
            table4 = TableInforamtion.objects.filter(number=4, state='Free', date=select_date,
                                                     select_time_period=period).all()
            table6 = TableInforamtion.objects.filter(number=6, state='Free', date=select_date,
                                                     select_time_period=period).all()

            if len(table) >= 1:
                tabels.append(table[0])
                if len(table2) >= 1:
                    tabels.append(table2[0])
                    for i in tabels:
                        i.status = "Order"
            elif len(table6) >= 1:
                tabels.append(table6[0])
                if len(table4) >= 1:
                    tabels.append(table4[0])
                    for i in tabels:
                        i.status = "Order"
            else:
                tables = []
        elif number <= 12 and number > 10:

            table = TableInforamtion.objects.filter(number=8, state='Free', date=select_date,
                                                    select_time_period=period).all()
            table4 = TableInforamtion.objects.filter(number=4, state='Free', date=select_date,
                                                     select_time_period=period).all()
            table6 = TableInforamtion.objects.filter(number=6, state='Free', date=select_date,
                                                     select_time_period=period).all()

            if len(table) >= 1:
                tabels.append(table[0])
                if len(table4) >= 1:
                    tabels.append(table4[0])
                    for i in tabels:
                        i.status = "Order"
                elif len(table6) >= 2:
                    tabels = table6[:2]
                    for i in tabels:
                        i.status = "Order"
                else:
                    tables = []
        elif number <= 14 and number > 12:

            table = TableInforamtion.objects.filter(number=8, state='Free', date=select_date,
                                                    select_time_period=period).all()
            table6 = TableInforamtion.objects.filter(number=6, state='Free', date=select_date,
                                                     select_time_period=period).all()

            if len(table) >= 1:
                tabels.append(table[0])
                if len(table6) >= 1:
                    tabels.append(table6[0])
                    for i in tabels:
                        i.status = "Order"
                elif len(table) >= 2:
                    tabels = table[:2]
                    for i in tabels:
                        i.status = "Order"
                else:
                    tables = []
        elif number <= 16 and number > 14:
            table = TableInforamtion.objects.filter(number=8, state='Free', date=select_date,
                                                    select_time_period=period).all()
            if len(table) >= 2:
                tables = table[:2]
            else:
                table = []

        if tablenew and len(tabels) == 0:
            if user != 'visitor':
                username = request.session.get('username', None)
                datas = UserInfo.objects.filter(username=username).first()
                tablenew.customer = datas.name
            else:

                datas = UserInfo.objects.filter(username=user).first()
                request.session['visitor'] = request.POST.get("name")
                datas.name = request.POST.get("name")
                datas.save()
                tablenew.customer = request.POST.get("name")
            tablenew.date = select_date

            tablenew.save()

            tableorder = TableOrder()
            tableorder.date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            tableorder.reser_date = select_date
            tableorder.name = datas.name
            tableorder.number = number
            tableorder.price = 15 * number
            tableorder.table_ids = str(tablenew.table_id)
            tableorder.select_time_period = period
            tableorder.introduce = f''' Name:{datas.name} Deposit:{tableorder.price}$<br>
                                        Target date: {tableorder.reser_date} Order time: {tableorder.date}<br>
                                        Please seat in ID[{tablenew.table_id}] table in 【{dinner_name}】<br>
                                        at [{TimePriod[period]}] Looking forward to your arrival！<br>'''

            if request.POST.get("tele"):
                tableorder.introduce += f'You TELE:{request.POST.get("tele")}<br>'
            if request.POST.get("email"):
                tableorder.introduce += f'You Email:{request.POST.get("email")}<br>'
            tableorder.save()
            change_dinning_state(dinner_name, select_date, datas.name, period)

            datas.earned_points += 15 * number / 10
            datas.save()

            res = {'status': 0, 'msg': 'Reserve Successfully!'}
            return JsonResponse(res)
        elif len(tabels) >= 1:

            if user != 'visitor':
                username = request.session.get('username', None)
                datas = UserInfo.objects.filter(username=username).first()


            else:

                datas = UserInfo.objects.filter(username=user).first()
                request.session['visitor'] = request.POST.get("name")
                datas.name = request.POST.get("name")
                datas.save()

            tableids = []
            for table in tabels:
                table.state = 'Order'
                table.date = select_date
                table.customer = datas.name
                tableids.append(str(table.table_id))
                table.save()
            tableorder = TableOrder()
            tableorder.date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            tableorder.reser_date = select_date
            tableorder.name = datas.name
            tableorder.price = 15 * number
            tableorder.number = number
            tableorder.select_time_period = period
            tableorder.table_ids = " ".join(tableids)

            tableorder.introduce = f'''Name:{datas.name} Deposit:{tableorder.price}$<br>
                                       Target date: {tableorder.reser_date} Order time: {tableorder.date}<br>
                                       Please seat in ID[{tableorder.table_ids}] table in 【{dinner_name}】 <br>
                                       at [{TimePriod[period]}] We will combine these tables<br>
                                       Looking forward to your arrival！<br>'''
            if request.POST.get("tele"):
                tableorder.introduce += f'You TELE:{request.POST.get("tele")}<br>'
            if request.POST.get("email"):
                tableorder.introduce += f'You Email:{request.POST.get("email")}<br>'

            change_dinning_state(dinner_name, select_date, datas.name, period)
            tableorder.save()

            datas.earned_points += 15 * number / 10
            datas.save()

            res = {'status': 0, 'msg': 'Reserve Successfully!'}
            return JsonResponse(res)

        else:
            res = {'status': 1, 'msg': 'Reserve Failed!'}
            return JsonResponse(res)
    else:
        res = {'status': 1, 'msg': 'Reserve Failed!'}
        return JsonResponse(res)
    # else:
    #     res = {'status': 2, 'msg': 'Please Login!'}
    #     return JsonResponse(res)


def change_dinning_state(title, time, name, select):
    dinning = Dinning.objects.filter(title=title, date=time, select_time_period=select).first()
    if title != "Hall":
        dinning.name = name
        dinning.state = "Order"
        dinning.save()
    else:
        new_dinning = Dinning()
        new_dinning.name = name
        new_dinning.state = "Order"
        new_dinning.title = title
        new_dinning.date = time
        new_dinning.save()


def change(request):
    if request.method == "GET":
        datevalue = request.GET.get('datevalue')
        period = request.GET.get('period')
        print("datevalue:", datevalue)
        print("period:", period)
        tabledatas = TableInforamtion.objects.filter(date=str(datevalue), select_time_period=period)
        return render(request, 'add.html', {'tabledatas': tabledatas})


def getIntroduce(request):
    if request:
        username = request.session.get('username', None)
        datas = UserInfo.objects.filter(username=username).first()
        timeNow = request.POST.get("date")
        if datas:
            order = TableOrder.objects.filter(reser_date=str(timeNow), name=datas.name).order_by('id').last()
        else:
            username = request.session.get('visitor')
            order = TableOrder.objects.filter(reser_date=str(timeNow), name=username).order_by('id').last()
        if order:
            return JsonResponse({'msg': order.introduce})
        else:
            return JsonResponse({'msg': 'No tips'})
    else:
        return JsonResponse({'msg': 'No tips'})
