from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from imac_main.scripts.fbauth import fbsignup, fblogin, fblogout
from imac_main.scripts.database import fbloginread, getuserapproval_list, fbapprove_user, fbapprove_booking, getallseats, fbbookingreq, fbcancel_booking, get_unapproved_booking_requests, get_booked_seats, get_booking_history, gethistory, fbreject_booking
from imac_main.scripts import timetest
from datetime import datetime, timedelta
from django.core.cache import cache

# Create your views here.

lab_no = 1

def index(request):
    uid = request.session.get('localid')
    User = request.session.get(uid)
    if User != None:
        if User['acc_type'] == 'Admin':
            return HttpResponseRedirect('/adminportal')
        else:
            return HttpResponseRedirect('/portal_pending')
    else:
        return render(request, 'index.html')

def signup(request):
    return render(request, 'signup.html')

def signupPost(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        if "@srmist.edu.in" not in email:
            return HttpResponse("Invalid email address. Please use your SRM email address.")
        else:
            empid = request.POST.get('empid')
            dept = request.POST.get('dept')
            password = request.POST.get('password')
            fbsignup(name, email, empid, dept, password)
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')
        
def logout(request):
    fblogout()
    request.session.clear()
    return HttpResponseRedirect('/')

def login(request):
    cache.clear()
    print(request.session.keys())
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        uid = fblogin(email, password)

        if uid != None:
            localid = uid[0]['localId']
            user_data = {
                'uid': uid[0]['localId'],
                'name' : uid[1],
                'dept' : uid[2],
                'empid' : uid[3],
                'acc_type' : uid[4],
                'email' : uid[0]['email']
            }
            request.session['localid'] = user_data['uid']
            request.session[localid] = user_data
            User = request.session.get(localid)
            print(request.session.keys())
            if User['acc_type'] == 'Admin':
                return HttpResponseRedirect('/adminportal')
            else:
                return HttpResponseRedirect('/portal_pending')
        else:
            return HttpResponse('Invalid credentials')

def adminportal(request):
    uid = request.session.get('localid')
    User = request.session.get(uid)
    if User != None:
        uid = request.session.get('localid')
        User = request.session.get(uid)
        userapproval_list = getuserapproval_list()
        print(userapproval_list)
        bookingapproval_list = get_unapproved_booking_requests()
        context={'userapproval_list': userapproval_list, "bookingapproval_list": bookingapproval_list, 'name': User['name']}
        return render(request, 'adminportal.html', context)
    else:
        return HttpResponseRedirect('/')

def approve_user(request):
    user_uid = request.session.get('localid')
    User = request.session.get(user_uid)
    if User != None:
        uid = request.POST.get('uid')
        fbapprove_user(uid)
        return HttpResponseRedirect('/adminportal')
    else:
        return HttpResponseRedirect('/')

def approve_booking(request):
    uid = request.session.get('localid')
    User = request.session.get(uid)
    if User != None:
        uid = request.POST.get('uid')
        fbapprove_booking(uid)
        return HttpResponseRedirect('/adminportal')
    else:
        return HttpResponseRedirect('/')

def portal(request):
    uid = request.session.get('localid')
    User = request.session.get(uid)
    if User != None:
        lab_no = 1
        seats = getallseats(lab_no)
        now = datetime.now()
        date = (now + timedelta(days=2)).strftime("%Y-%m-%d") 
        time_from = now.strftime("%H:%M")
        time_till = (now + timedelta(hours=2)).strftime("%H:%M")
        try:
            booked_seats = get_booked_seats(lab_no, date, time_from, time_till).keys()
            booked_seats = [int(x) for x in list(booked_seats)]
        except:
            booked_seats = []
        row1 = seats["row 1"]
        row2 = seats["row 2"]
        row3 = seats["row 3"]
        row4 = seats["row 4"]
        row5 = seats["row 5"]
        row6 = seats["row 6"]
        row7 = seats["row 7"]
        
        context = {
            'lab_no': lab_no,
            'booked_seats': booked_seats,
            'rows': {
                'row1': row1[1:],
                'row2': row2[1:],
                'row3': row3[1:],
                'row4': row4[1:],
                'row5': row5[1:],
                'row6': row6[1:],
                'row7': row7[1:],
            },
            'acc_type': User['acc_type'],
            'date': date,
            'time_from': time_from,
            'time_till': time_till,
        }
        return render(request, 'facultyportal.html', context)
    else:
        return HttpResponseRedirect('/')

def loadlab(request):
    uid = request.session.get('localid')
    User = request.session.get(uid)
    if User != None:
        lab_no = request.POST.get('lab-no')[0]
        date = request.POST.get('date')
        time_from = request.POST.get('time_from')
        time_till = request.POST.get('time_till')
        try:
            booked_seats = get_booked_seats(lab_no, date, time_from, time_till).keys()
            booked_seats = [int(x) for x in list(booked_seats)]
        except:
            booked_seats = []
        if lab_no < '3':
            seats = getallseats(lab_no)
            row1 = seats["row 1"]
            row2 = seats["row 2"]
            row3 = seats["row 3"]
            row4 = seats["row 4"]
            row5 = seats["row 5"]
            row6 = seats["row 6"]
            row7 = seats["row 7"]
            
            context = {
                'lab_no': lab_no,
                'booked_seats': booked_seats,
                'rows': {
                    'row1': row1[1:],
                    'row2': row2[1:],
                    'row3': row3[1:],
                    'row4': row4[1:],
                    'row5': row5[1:],
                    'row6': row6[1:],
                    'row7': row7[1:],
                },
                'acc_type': User['acc_type'],
                'date': date,
                'time_from': time_from,
                'time_till': time_till,
            }
        else:
            seats = getallseats(lab_no)
            row1 = seats["row 1"]
            row2 = seats["row 2"]
            row3 = seats["row 3"]
            row4 = seats["row 4"]
            row5 = seats["row 5"]
            row6 = seats["row 6"]
            row7 = seats["row 7"]
            row8 = seats["row 8"]
            
            context = {
                'lab_no': lab_no,
                'booked_seats': booked_seats,
                'rows': {
                    'row1': row1[1:],
                    'row2': row2[1:],
                    'row3': row3[1:],
                    'row4': row4[1:],
                    'row5': row5[1:],
                    'row6': row6[1:],
                    'row7': row7[1:],
                    'row8': row8[1:],
                },
                'acc_type': User['acc_type'],
                'date': date,
                'time_from': time_from,
                'time_till': time_till,
            }
        return render(request, 'facultyportal.html', context)
    else:
        return HttpResponseRedirect('/')


def portal_pending(request):
    uid = request.session.get('localid')
    User = request.session.get(uid)
    if User != None:
        approved = fbloginread(User['uid'])
        approved = approved["approved"]
        if approved:
            return HttpResponseRedirect('portal')
        else:
            return render(request, 'portal-nopermission.html')
    else:
        return HttpResponseRedirect('/')
        
def submitreq(request):
    uid = request.session.get('localid')
    User = request.session.get(uid)
    if User != None:
        if request.method == 'POST':
            sysid = request.POST.get('sys-no')
            lab_no = request.POST.get('lab-no')[0]
            date = request.POST.get('date')
            time_from = request.POST.get('time_from')
            time_till = request.POST.get('time_till')
            reason = request.POST.get('reason')
            uid = User['uid']
            name = User['name']
            email = User['email']
            empid = User['empid']
            dept = User['dept']
            acc_type = User['acc_type']
            fbbookingreq(uid, name, email, empid, dept, acc_type, lab_no, sysid, date, time_from, time_till, reason)
        return HttpResponseRedirect('/portal')
    else:
        return HttpResponseRedirect('/')
    

def bookinghistory(request):
    uid = request.session.get('localid')
    User = request.session.get(uid)
    if User != None:
        uid = request.session.get('localid')
        User = request.session.get(uid)
        history = get_booking_history(User['uid'], User['acc_type'])
        context={

            'booking_history': history,
            'acc_type': User['acc_type'],
            'name': User['name']
            
            }
        return render(request, 'portalbookinghistory.html', context)
    else:
        return HttpResponseRedirect('/')

def cancelbooking(request):
    uid = request.session.get('localid')
    User = request.session.get(uid)
    if User != None:
        uid = request.session.get('localid')
        User = request.session.get(uid)
        uid = User['uid']
        labno = request.POST.get('lab_no')
        seatno = request.POST.get('seatno')
        date = request.POST.get('date')
        time_from = request.POST.get('time_from')
        time_till = request.POST.get('time_till')
        fbcancel_booking(uid, labno, seatno, date, time_from, time_till)
        return HttpResponseRedirect('/bookinghistory')
    else:
        return HttpResponseRedirect('/')

def reject_booking(request):
    uid = request.session.get('localid')
    User = request.session.get(uid)
    if User != None:
        uid = request.POST.get('uid')
        fbreject_booking(uid)
        return HttpResponseRedirect('/adminportal')
    else:
        return HttpResponseRedirect('/')

def get_report(request):
    uid = request.session.get('localid')
    User = request.session.get(uid)
    if User['acc_type'] == 'Admin':
        now = datetime.now()
        date_from = request.POST.get('date_from')
        date_till = request.POST.get('date_till')
        history = gethistory(date_from, date_till)
        context={

        'booking_history': history,
        'acc_type': User['acc_type'],
        'name': User['name']
        
        }
        return render(request, 'report.html', context)
    else:
        return HttpResponseRedirect('/')