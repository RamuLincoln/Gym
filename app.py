from decimal import Decimal
from multiprocessing import connection
# from flask import Flask, render_template, request, redirect, url_for
from flask import *
import mysql
import mysql.connector
import connect
from dateutil.relativedelta import relativedelta
from datetime import date
import re
import uuid

connection = None
dbconn = None

app = Flask(__name__)
app.secret_key = '123456'

#Database Connection
def getCursor():
    global dbconn
    global connection
    if dbconn == None:
        connection = mysql.connector.connect(user=connect.dbuser, \
                                             password=connect.dbpass, host=connect.dbhost, \
                                             database=connect.dbname, autocommit=True, buffered=True)
        dbconn = connection.cursor(dictionary=True)
        return dbconn
    else:
        return dbconn


# dbFetchAll
def dbFetchAll(query):
    cur = getCursor()
    cur.execute(query)
    data = cur.fetchall()
    rows = []
    for row in data:
        rows.append(row)

    return rows  # return on all rows


# dbFetchone
def dbFetchone(query):
    cur = getCursor()
    cur.execute(query)
    data = cur.fetchone()
    return data  # return on db row


@app.route("/")
@app.route("/Home")
def home():
    return render_template("Home.html")


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('role', None)
    session.pop('username', None)
    return redirect(url_for('login'))


# login page
@app.route("/Login", methods=['GET', 'POST'], endpoint='Login')
def login():
    msg = ''
    if request.method == 'GET':
        return render_template("login.html", msg=msg)
    else:
        data = request.form.to_dict()
        cur = getCursor()
        cur.execute(
            f"SELECT * from member WHERE CONCAT(email) LIKE '{data.get('email')}' and membershipstatus = 1")
        member = cur.fetchone()
        # member login
        if member is not None:
            cur = getCursor()
            cur.execute("select * from member where id = %s and membershipstatus = 1",
                        (member.get('id'),))
            dbmember = cur.fetchone()

            cur.execute("select * from payment where memberid = %s and type = 'membership' order by paymentdate",
                        (member.get('id'),))
            payments = cur.fetchall()

            currentDate = None
            expiredDate = None
            if len(payments) == 0:
                expiredDate = 'Unpaid'
            else:
                for payment in payments:
                    paymentDate = payment.get('paymentdate')
                    paymentamount = payment.get('paymentamount')
                    if expiredDate is None or paymentDate >= expiredDate:
                        expiredDate = paymentDate + relativedelta(months=int(paymentamount / 60))
                    else:
                        expiredDate += relativedelta(months=int(paymentamount / 60))
                    currentDate = paymentDate
                if expiredDate < expiredDate.today():
                    expiredDate = 'Expired'
            dbmember['newDate'] = expiredDate
            dbmember['paymentdate'] = currentDate
            session['memberID'] = dbmember.get('id')
            return render_template("memberhome.html", dbmember=dbmember)

            # cur = getCursor()
            # cur.execute("select * from member left join payment p on member.id = p.memberid and p.type = 'membership' \
            #                                 where id = %s and membershipstatus = 1 order by p.paymentdate desc, \
            #                                 p.paymentamount desc limit 1",
            #             (member.get('id'),))
            # dbmember = cur.fetchone()
            # amount = dbmember.get('paymentamount')
            #
            # if amount is None:
            #     newDate = 'Unpaid'
            # else:
            #     date = dbmember.get('paymentdate')
            #     paymentMonth = amount / 60
            #     newDate = date + relativedelta(months=paymentMonth)
            #     if newDate < date.today():
            #         newDate = 'Expired'
            # dbmember['newDate'] = newDate
            # session['memberID'] = dbmember.get('id')

        # trainer login
        cur.execute(
            f"SELECT * from trainer WHERE CONCAT(email) LIKE '{data.get('email')}' and status = 1")
        dbtrainer = cur.fetchone()
        if dbtrainer is not None:
            session['trainerID'] = dbtrainer.get('id')
            return render_template("trainerhome.html")
        # admin login
        elif data.get('email') == 'admin@gmail.com':
            return render_template("admin.html")

        else:
            msg = 'Incorrect username / password !'
            return render_template("login.html", msg=msg)


@app.route("/trainerhome_details", methods=['GET', 'POST'])
def getTrainerDetail():
    trainerID = session.get('trainerID')
    cur = getCursor()
    cur.execute(
        "select id, firstName, lastName, email, address, birthday, freetime from trainer where id = %s and status = 1",
        (trainerID,))
    dbtrainer = cur.fetchone()
    return render_template("trainerhome_detail.html", trainer=dbtrainer)


@app.route("/trainerhome_details/update", methods=['GET', 'POST'])
def trainerHomeUpdate():
    trainerId = request.args.get('trainerID')
    if request.method == 'GET':
        cur = getCursor()
        cur.execute(
            "select id, firstName, lastName, email, address, birthday, freetime from trainer where id = %s and status = 1",
            (trainerId,))
        dbTrainer = cur.fetchone()
        return render_template('trainerhome_update.html', trainer=dbTrainer)
    else:
        updatedata = request.form.to_dict()
        cur = getCursor()
        cur.execute("update trainer set firstName = %s, lastName = %s, email = %s, \
            address = %s, birthday = %s, freetime = %s where id = %s and status = 1", (
            updatedata.get('firstName'), updatedata.get('lastName'), updatedata.get('email'), \
            updatedata.get('address'), updatedata.get('birthday'), updatedata.get('freetime'), trainerId,))
        return redirect("/trainerhome_details?trainerID" + trainerId)


@app.route("/memberhome_details", methods=['GET', 'POST'])
def getMemberDetail():
    memberID = session.get('memberID')
    cur = getCursor()
    cur.execute("select class.id,class.classname, class.classdate,class.classday,class.classtime,trainer.firstName,\
            trainer.lastName from ((class left join trainer on class.trainerid = trainer.id) join classbooking \
                          on classbooking.classid = class.id and classbooking.memberid = %s and trainer.status = 1);",
                (memberID,))
    dbBooked = cur.fetchall()
    cur = getCursor()
    cur.execute("select * from member where id = %s and membershipstatus = 1",
                (memberID,))
    dbmember = cur.fetchone()
    cur.execute("select * from payment where memberid = %s and type = 'membership' order by paymentdate",
                (memberID,))
    payments = cur.fetchall()

    currentDate = None
    expiredDate = None
    if len(payments) == 0:
        expiredDate = 'Unpaid'
    else:
        for payment in payments:
            paymentDate = payment.get('paymentdate')
            paymentamount = payment.get('paymentamount')
            if expiredDate is None or paymentDate >= expiredDate:
                expiredDate = paymentDate + relativedelta(months=int(paymentamount / 60))
            else:
                expiredDate += relativedelta(months=int(paymentamount / 60))
            currentDate = paymentDate
        if expiredDate < expiredDate.today():
            expiredDate = 'Expired'
    dbmember['newDate'] = expiredDate
    dbmember['paymentdate'] = currentDate

    return render_template("memberhome_detail.html", member=dbmember, dbBooked=dbBooked)


@app.route("/memberhome_details/update", methods=['GET', 'POST'])
def memberHomeUpdate():
    memberId = request.args.get('memberId')
    if request.method == 'GET':
        cur = getCursor()
        cur.execute("select * from member where id = %s and membershipstatus = 1", (memberId,))
        dbMember = cur.fetchone()
        return render_template('memberhome_update.html', member=dbMember)
    else:
        updatedata = request.form.to_dict()
        cur = getCursor()
        cur.execute("update member set firstName = %s, lastName = %s, phone= %s, email = %s, \
            birthday = %s, gender = %s, address = %s, healthIssues = %s where id = %s and membershipstatus = 1", (
            updatedata.get('firstName'), updatedata.get('lastName'), updatedata.get('phone'), updatedata.get('email'), \
            updatedata.get('birthday'), updatedata.get('gender'), updatedata.get('address'), \
            updatedata.get('healthIssues'), memberId,))
        return redirect("/memberhome_details?memberId" + memberId)


@app.route("/memberhome_details/payment", methods=['GET', 'POST'])
def memberPayment():
    memberId = request.args.get('memberId')
    if request.method == 'GET':
        cur = getCursor()
        cur.execute("select * from member left join payment p on member.id = p.memberid and p.type = 'membership' \
                         where id = %s and membershipstatus = 1", (memberId,))
        dbMember = cur.fetchone()
        dbMember['paymentdate'] = date.today()
        return render_template('memberhome_payment.html', member=dbMember)
    else:
        updatedata = request.form.to_dict()
        cur = getCursor()
        cur.execute("insert into  payment (memberid,paymentdate,paymentamount,type) values \
                      (%s,%s,%s,'membership')",
                    (memberId, updatedata.get('paymentdate'), updatedata.get('paymentamount')))
        return redirect("/memberhome_details")


@app.route("/mempageClassdetails")
def classes():
    memberID = session.get('memberID')
    cur = getCursor()
    cur.execute("select class.id,class.classname, class.classdate,class.classday,class.classtime,trainer.firstName,\
        trainer.lastName from ((class left join trainer on class.trainerid = trainer.id) join classbooking \
                      on classbooking.classid = class.id and classbooking.memberid = %s and trainer.status = 1);",
                (memberID,))
    dbBooked = cur.fetchall()

    bookedClassId = []
    for item in dbBooked:
        bookedClassId.append(item.get('id'))

    cur = getCursor()
    cur.execute("select class.id,class.classname,class.classdate,class.classday,class.classtime,trainer.firstName,\
                 trainer.lastName, eNc.enrolNumber from class left join trainer on class.trainerid = trainer.id\
                 left join (select COUNT(*) as enrolNumber, classid from classbooking group by classid) as eNc on \
                 eNc.classid = class.id;")
    dbBooking = cur.fetchall()

    dbBookingDict = {}
    for bookingClass in dbBooking:
        key = bookingClass.get('classname')
        if key in dbBookingDict:
            dbBookingDict[key].append(bookingClass)
        else:
            dbBookingDict[key] = [bookingClass]

    for key in dbBookingDict.keys():
        dbBookingDict.get(key).sort(key=lambda x: (x.get("classdate"), x.get("classtime")), reverse=True)

    return render_template("mempageclassdetails.html", dbBooked=dbBooked, dbBooking=dbBooking,
                           dbBookingDict=dbBookingDict, bookedClassId=bookedClassId)


@app.route("/mempageClassdetails/book")
def bookclass():
    memberID = session.get('memberID')
    classId = request.args.get('classId')
    print(memberID, classId)
    cur = getCursor()
    cur.execute("insert into classbooking (memberid, classid) values \
                    (%s,%s)", (memberID, classId))
    return redirect("/mempageClassdetails")


@app.route("/memberhome_details/booked")
def bookedClass():
    memberID = session.get('memberID')
    cur = getCursor()
    cur.execute("select class.id,class.classname, class.classdate,class.classday,class.classtime,trainer.firstName,\
            trainer.lastName from ((class left join trainer on class.trainerid = trainer.id) join classbooking \
                          on classbooking.classid = class.id and classbooking.memberid = %s and trainer.status = 1);",
                (memberID,))
    dbBooked = cur.fetchall()

    cur.execute("select * from PTbooking left join trainer t on PTbooking.trainerid = t.id where PTbooking.memberid = %s\
                and t.status = 1;", (memberID,))
    dbPersonal = cur.fetchall()

    return render_template("memberhome_bookedclasses.html", dbBooked=dbBooked, dbPersonal=dbPersonal)


@app.route("/Admin")
def Admin():
    return render_template("Admin.html")


@app.route("/class", methods=['GET', 'POST'], endpoint='class')
def viewclasses():
    classID = session.get('classid')
    select_result = ''
    searchval = ''
    if request.method == 'POST':
        searchval = request.form['search']
        cur = getCursor()
        query = f"select class.id, class.classname, class.classdate, class.classday, class.classtime, trainer.firstName, trainer.lastName, classcount from class left join trainer on class.trainerid = trainer.id inner join (select classid, count(*) as classcount from classbooking group by classid) as popularclass on popularclass.classid = class.id WHERE CONCAT(classname, ' ', classdate) LIKE '%{searchval}%' order by popularclass.classcount desc"
        cur.execute(query)
        select_result = cur.fetchall()

    if (select_result == '' or searchval == ''):
        cur = getCursor()
        query = "select class.id, class.classname, class.classdate, class.classday, class.classtime, trainer.firstName, trainer.lastName, classcount from class left join trainer on class.trainerid = trainer.id inner join (select classid, count(*) as classcount from classbooking group by classid) as popularclass on popularclass.classid = class.id order by popularclass.classcount desc"
        cur.execute(query)
        select_result = cur.fetchall()

    return render_template("class.html", dbClass=select_result)


@app.route("/member_attendance")
def getMemberAttendance():
    return render_template("member_attendance.html")


@app.route("/membergymattendance", methods=['GET', 'POST'], endpoint='membergymattendance')
def getmemberattendance():
    # cur = getCursor()
    # cur.execute(
    #     "select member.id,member.firstName,member.lastName,gymattendance.attendancedate from member left join gymattendance on member.id = gymattendance.memberid; ")
    # dbmembergymattendance = cur.fetchall()

    select_result = ''
    searchval = ''
    if request.method == 'POST':
        searchval = request.form['search']
        cur = getCursor()
        cur.execute(f"""Select * from (select member.firstName,member.lastName,gymattendance.lastvisitdate from member left join gymattendance on member.id = gymattendance.memberid order by gymattendance.lastvisitdate) as mematt 
                        WHERE CONCAT(mematt.firstName,' ',mematt.lastName) LIKE '%{searchval}%'""")
        select_result = cur.fetchall()

    if (select_result == '' or searchval == ''):
        cur = getCursor()
        cur.execute(
            "select member.firstName,member.lastName,gymattendance.lastvisitdate from member left join gymattendance on member.id = gymattendance.memberid order by gymattendance.lastvisitdate ; ")
        select_result = cur.fetchall()

    return render_template("membergymattendance.html", dbmembergymattendance=select_result)


@app.route("/memberclassattendance", methods=['GET', 'POST'], endpoint='memberclassattendance')
def getmemberclassattendance():
    select_result = ''
    searchval = ''
    if request.method == 'POST':
        searchval = request.form['search']
        cur = getCursor()
        cur.execute(f"""Select * from (select member.firstName, member.lastName, class.classname, class.classdate, class.classtime,trainer.firstName as tf, trainer.lastName as tl,classbooking.attendancestatus from classbooking
            left join class on classbooking.classid = class.id
            left join member on classbooking.memberid = member.id
            left join trainer on class.trainerid = trainer.id order by class.classname, class.classdate) as mematt 
            WHERE CONCAT(mematt.firstName,' ',mematt.lastName,' ' ,mematt.attendancestatus) LIKE '%{searchval}%'""")
        select_result = cur.fetchall()

    if (select_result == '' or searchval == ''):
        cur = getCursor()
        cur.execute(
            "select member.firstName, member.lastName, class.classname, class.classdate, class.classtime,trainer.firstName as tf, trainer.lastName as tl,classbooking.attendancestatus from classbooking \
            left join class on classbooking.classid = class.id \
            left join member on classbooking.memberid = member.id \
            left join trainer on class.trainerid = trainer.id order by class.classname, class.classdate;")
        select_result = cur.fetchall()

    return render_template("memberclassattendance.html", dbmemberclassattendance=select_result)


@app.route("/memberptattendance", methods=['GET', 'POST'], endpoint='memberptattendance')
def getmemberptattendance():
    # cur = getCursor()
    # cur.execute(
    #     "select member.id, member.firstName, member.lastName,PTbooking.attendancestatus from member left join PTbooking on member.id = PTbooking.memberid")
    # dbmemberptattendance = cur.fetchall()
    select_result = ''
    searchval = ''
    if request.method == 'POST':
        searchval = request.form['search']
        cur = getCursor()
        cur.execute(f"""Select * from (select member.firstName, member.lastName,PTbooking.trainingname,trainer.firstName as tf,
                                        trainer.lastName as tl,PTbooking.classdate,PTbooking.classtime,PTbooking.attendancestatus from member left join PTbooking on member.id = PTbooking.memberid 
                                        left join trainer on PTbooking.trainerid = trainer.id  where location = 'Training room 2') as mematt 
                                        WHERE CONCAT(mematt.firstName,' ',mematt.lastName, ' ' ,mematt.attendancestatus) LIKE '%{searchval}%'""")
        select_result = cur.fetchall()

    if (select_result == '' or searchval == ''):
        cur = getCursor()
        cur.execute(
            "select member.firstName, member.lastName,PTbooking.trainingname,trainer.firstName as tf,trainer.lastName as tl,PTbooking.classdate,PTbooking.classtime,PTbooking.attendancestatus from member\
                 left join PTbooking on member.id = PTbooking.memberid \
                    left join trainer on PTbooking.trainerid = trainer.id  where location = 'Training room 2' order by PTbooking.trainingname, PTbooking.classdate ;")
        select_result = cur.fetchall()

    return render_template("memberptattendance.html", dbmemberptattendance=select_result)


@app.route("/Membership")
def membership():
    return render_template("membership.html")


@app.route("/trainerhome")
def Contact():
    return render_template("trainerhome.html")


@app.route("/Register", methods=['GET', 'POST'])
def memberRegister():
    if request.method == 'GET':
        return render_template("Register.html")
    else:
        updatedata = request.form.to_dict()
        cur = getCursor()
        cur.execute("insert into member (firstName, lastName, address, email, phone, birthday, gender, healthIssues,membershipstatus) values \
                (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (updatedata.get('firstName'),
                     updatedata.get('lastName'),
                     updatedata.get('address'),
                     updatedata.get('email'),
                     updatedata.get('phone'),
                     updatedata.get('birthday'),
                     updatedata.get('gender'),
                     updatedata.get('healthIssues'),
                     1,))
        memberId = cur.lastrowid
        session['memberID'] = memberId
        return redirect("/memberhome_details/payment?memberId=" + str(memberId))


@app.route("/mempageTrainerdetails", methods=['GET', 'POST'], endpoint='mempageTrainerdetails')
def trainers():
    select_result = ''
    searchval = ''
    if request.method == 'POST':
        searchval = request.form['search']
        cur = getCursor()
        cur.execute(
            f"SELECT * from trainer WHERE CONCAT(id, ' ',firstName, ' ',lastName, ' ', speciality) LIKE '%{searchval}%' and status = 1")
        select_result = cur.fetchall()

    if (select_result == '' or searchval == ''):
        cur = getCursor()
        cur.execute("select * from trainer where status = 1;")
        select_result = cur.fetchall()

    return render_template("mempageTrainerdetails.html", dbTrainer=select_result)


@app.route("/trainee")
def trainee():
    trainerID = session.get('trainerID')
    cur = getCursor()
    cur.execute(
        "select member.firstName,member.lastName, member.email, member.healthIssues,PTbooking.trainingname, PTbooking.classdate, PTbooking.classtime,PTbooking.paymentdate FROM member inner join PTbooking on member.id = PTbooking.memberid where trainerid = %s and member.membershipstatus = 1;",
        (trainerID,))
    dbTrainee = cur.fetchall()

    cur = getCursor()
    cur.execute(
        "select member.firstName,member.lastName,member.email,member.healthIssues, class.classname,class.classdate,class.classtime from member left join classbooking on member.id = classbooking.memberid left join class on class.id = classbooking.classid where trainerid = %s and member.membershipstatus = 1; ",
        (trainerID,))
    dbclassTrainee = cur.fetchall()

    return render_template("trainee.html", dbTrainee=dbTrainee, dbclassTrainee=dbclassTrainee)


@app.route("/traineeattendance")
def trainee_attendance_trainer():
    trainerID = session.get('trainerID')
    cur = getCursor()
    cur.execute(
        "select member.firstName,member.lastName, PTbooking.classdate, PTbooking.classtime, \
            PTbooking.trainingname,PTbooking.attendancestatus from member \
            join PTbooking on member.id = PTbooking.memberid where PTbooking.trainerid=%s;", (trainerID,))
    dbtraineeattendance = cur.fetchall()

    cur = getCursor()
    cur.execute(
        "select member.firstName,member.lastName,class.classname,class.classtime, class.classdate,classbooking.attendancestatus from member join class on trainerid=%s \
         join classbooking on member.id = classbooking.memberid and classbooking.classid = class.id;",(trainerID,))
    dbtraineeclassattendance = cur.fetchall()
    return render_template("traineeattendance.html", dbtraineeattendance=dbtraineeattendance,
                           dbtraineeclassattendance=dbtraineeclassattendance)


@app.route("/member_details", methods=['GET', 'POST'], endpoint='member_details')
def memberDetails():
    select_result = ''
    searchval = ''
    if request.method == 'POST':
        searchval = request.form['search']
        cur = getCursor()
        # SELECT * from member WHERE concat(id , ' ', firstName, ' ' , lastName) LIKE '%text%';
        cur.execute(
            f"SELECT * from member WHERE CONCAT(id, ' ',firstName, ' ',lastName) LIKE '%{searchval}%' and membershipstatus = 1")
        select_result = cur.fetchall()

    if (select_result == '' or searchval == ''):
        cur = getCursor()
        searchval = ''
        cur.execute("select id from member where membershipstatus = 1;")
        ids = cur.fetchall()
        select_result = []
        for id in ids:
            cur = getCursor()
            cur.execute("select * from member where id = %s and membershipstatus = 1",
                        (id.get('id'),))
            dbmember = cur.fetchone()
            cur.execute("select * from payment where memberid = %s and type = 'membership' order by paymentdate",
                        (id.get('id'),))
            payments = cur.fetchall()
            currentDate = None
            expiredDate = None
            if len(payments) == 0:
                expiredDate = 'Unpaid'
            else:
                for payment in payments:
                    paymentDate = payment.get('paymentdate')
                    paymentamount = payment.get('paymentamount')
                    if expiredDate is None or paymentDate >= expiredDate:
                        expiredDate = paymentDate + relativedelta(months=int(paymentamount / 60))
                    else:
                        expiredDate += relativedelta(months=int(paymentamount / 60))
                    currentDate = paymentDate
                if expiredDate < expiredDate.today():
                    expiredDate = 'Expired'
            dbmember['newDate'] = expiredDate
            dbmember['paymentdate'] = currentDate
            select_result.append(dbmember)

    return render_template("member_details.html", dbMember=select_result, searchval=searchval)


@app.route("/member_update", methods=['GET', 'POST'])
def memberUpdate():
    memberId = request.args.get('memberId')
    if request.method == 'GET':
        cur = getCursor()
        cur.execute("select * from member where id = %s and membershipstatus = 1", (memberId,))
        dbMember = cur.fetchone()
        return render_template('member_update.html', member=dbMember)
    else:
        updatedata = request.form.to_dict()
        cur = getCursor()
        cur.execute("update member set firstName = %s, lastName = %s, phone= %s, email = %s, \
            birthday = %s, gender = %s, address = %s, healthIssues = %s where id = %s and membershipstatus = 1", (
            updatedata.get('firstName'), updatedata.get('lastName'), updatedata.get('phone'), updatedata.get('email'),
            updatedata.get('birthday'), updatedata.get('gender'), updatedata.get('address'),
            updatedata.get('healthIssues'), memberId,))
        return redirect("/member_details")


@app.route("/member_delete", methods=['GET'])
def memberDelete():
    memberId = request.args.get('memberId')
    cur = getCursor()
    cur.execute("update member set membershipstatus = 0 where id = %s", (memberId,))
    return redirect("/member_details")


@app.route('/member_add', methods=['GET', 'POST'])
def memberAdd():
    if request.method == 'GET':
        return render_template('member_add.html')
    else:
        updatedata = request.form.to_dict()
        cur = getCursor()
        cur.execute("insert into member (firstName, lastName, address, email, phone, birthday, gender, healthIssues, membershipstatus) values \
            (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (updatedata.get('firstName'),
                     updatedata.get('lastName'),
                     updatedata.get('address'),
                     updatedata.get('email'),
                     updatedata.get('phone'),
                     updatedata.get('birthday'),
                     updatedata.get('gender'),
                     updatedata.get('healthIssues'),
                     1,))
    return redirect("/member_details")


@app.route("/trainer_details", methods=['GET', 'POST'], endpoint='trainer_details')
def trainerDetails():
    select_result = ''
    searchval = ''
    if request.method == 'POST':
        searchval = request.form['search']
        cur = getCursor()
        cur.execute(
            f"SELECT * from trainer WHERE CONCAT(id, ' ',firstName, ' ',lastName,' ', speciality) LIKE '%{searchval}%' and status = 1")
        select_result = cur.fetchall()

    if (select_result == '' or searchval == ''):
        cur = getCursor()
        cur.execute("select * from trainer where status = 1;")
        select_result = cur.fetchall()

    return render_template("trainer_details.html", dbTrainer=select_result)


@app.route("/trainer_update", methods=['GET', 'POST'])
def trainerUpdate():
    trainerId = request.args.get('trainerId')
    if request.method == 'GET':
        cur = getCursor()
        cur.execute("select * from trainer where id = %s and status = 1", (trainerId,))
        dbTrainer = cur.fetchone()
        return render_template('trainer_update.html', trainer=dbTrainer)
    else:
        updatedata = request.form.to_dict()
        cur = getCursor()
        cur.execute("update trainer set firstName = %s, lastName = %s, speciality = %s,email = %s, \
            birthday = %s, gender = %s, address = %s, freetime = %s, cost = %s where id = %s and status = 1", (
            updatedata.get('firstName'), updatedata.get('lastName'), updatedata.get('speciality'),
            updatedata.get('email'),updatedata.get('birthday'), updatedata.get('gender'), updatedata.get('address'),
            updatedata.get('freetime'), updatedata.get('cost'), trainerId,))
        cur.execute("update trainer set firstName = %s, lastName = %s, speciality = %s, email = %s, \
            address = %s, freetime = %s, cost = %s where id = %s and status = 1", (
            updatedata.get('firstName'), updatedata.get('lastName'), updatedata.get('speciality'),
            updatedata.get('email'), updatedata.get('address'),
            updatedata.get('freetime'), updatedata.get('cost'), trainerId,))

        return redirect("/trainer_details")


@app.route('/trainer_add', methods=['GET', 'POST'])
def trainerAdd():
    if request.method == 'GET':
        return render_template('trainer_add.html')
    else:
        updatedata = request.form.to_dict()
        cur = getCursor()
        cur.execute("insert into trainer (firstName, lastName, address, email, birthday, gender, speciality, freetime, cost, status) values \
            (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (updatedata.get('firstName'),
                     updatedata.get('lastName'),
                     updatedata.get('address'),
                     updatedata.get('email'),
                     updatedata.get('birthday'),
                     updatedata.get('gender'),
                     updatedata.get('speciality'),
                     updatedata.get('freetime'),
                     updatedata.get('cost'),
                     1,))
    return redirect("/trainer_details")


@app.route("/trainer_delete", methods=['GET'])
def trainerDelete():
    trainerId = request.args.get('trainerId')
    cur = getCursor()
    cur.execute("update trainer set status = 0 where id = %s", (trainerId,))
    return redirect("/trainer_details")


@app.route("/specialbooking", methods=['GET', 'POST'])
def booking():
    trainerId = request.args.get('trainerId')
    memberId = session['memberID']
    if request.method == 'GET':

        cur = getCursor()
        cur.execute("select * from trainer where id = %s and status = 1", (trainerId,))
        dbTrainer = cur.fetchone()
        cur.execute("select * from member where id = %s and membershipstatus = 1", (memberId,))
        dbmember = cur.fetchone()
        currentdate = date.today()
        return render_template('specialbooking.html', trainer=dbTrainer, dbmember=dbmember, currentdate=currentdate)

    else:
        updatedata = request.form.to_dict()
        cur = getCursor()
        # cur.execute("insert into PTbooking (memberid, trainerid, speciality, paymentdate, amount, classdate,classtime, attendancestatus) values \
        #     (%s,%s,%s,%s,%s,%s,%s,%s)", )
        cost = re.findall("\d+", updatedata.get('trainingcost'))[0]
        cur.execute("insert into PTbooking (memberid, trainerid, trainingname, paymentdate, trainingcost, classdate,classtime, location, attendancestatus) values \
              (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (
            memberId, updatedata.get('TrainerID'), updatedata.get('trainingname'),
            updatedata.get('paymentdate'), cost, updatedata.get('classdate'),
            updatedata.get('classtime'), "Training room 2", updatedata.get('AttendanceStatus')))
        return render_template("paymentspl.html")


@app.route("/ptbooking")
def ptbooking():
    cur = getCursor()
    cur.execute("select * from PTbooking;")
    select_result = cur.fetchall()

    return render_template("ptbooking.html", dbPTbooking=select_result)


@app.route("/paymentspl")
def paymentspl():
    return redirect("/mempageTrainerdetails")


@app.route("/report", methods=['GET', 'POST'])
def report():
    startdate = ''
    enddate = ''
    if request.method == 'POST':
        startdate = request.form['startdate']
        enddate = request.form['enddate']
        print(startdate)
        print(enddate)
        cur = getCursor()
        cur.execute("select member.id,member.firstName, member.lastName,PTbooking.trainingname, PTbooking.classdate, PTbooking.classtime,PTbooking.paymentdate,PTbooking.trainingcost \
        FROM member inner join PTbooking \
        on member.id = PTbooking.memberid \
        where PTbooking.paymentdate between %s and %s;", (startdate, enddate,))
        dbTrainee = cur.fetchall()

        cur = getCursor()
        cur.execute("select sum(trainingcost) as trainingcost from PTbooking where paymentdate between %s and %s;",
                    (startdate, enddate,))
        dbPTbooking = cur.fetchall()
        dbPaymentAmount = 0
        for row in dbPTbooking:
            if row['trainingcost'] == None:
                dbPaymentAmount = 0
            else:
                dbPaymentAmount = row['trainingcost']
        print('dbPaymentAmount:',dbPaymentAmount)

        cur = getCursor()
        cur.execute(
            "select memberid, member.firstName, member.lastName, paymentdate, paymentamount from payment inner join member on memberid = member.id where paymentdate between %s and %s;",
            (startdate, enddate,))
        dbpayment = cur.fetchall()

        cur = getCursor()
        cur.execute("select sum(paymentamount) as paymentamount from payment where paymentdate between %s and %s;",
                    (startdate, enddate,))
        dbpay = cur.fetchall()
        dbPayAmount = 0
        for row in dbpay:
            if row['paymentamount'] == None:
                dbPayAmount = 0
            else:
                dbPayAmount = row['paymentamount']
        print('dbPayAmount:',dbPayAmount)

        # cur = getCursor()
        # cur.execute(
        #     "select((select sum(coalesce(paymentamount,0)) from payment where paymentdate between %s and %s) + (select sum(coalesce(trainingcost,0)) from PTbooking where paymentdate between %s and %s)) as totalrevenue",
        #     (startdate, enddate, startdate, enddate,))
        dbpayments = dbPaymentAmount + dbPayAmount

        return render_template("report.html", dbTrainee=dbTrainee, dbPTbooking=dbPaymentAmount, dbpayment=dbpayment,
                               dbpay=dbPayAmount, dbpayments=dbpayments, startdate=startdate, enddate=enddate)
    cur = getCursor()
    cur.execute(
        "select member.id,member.firstName, member.lastName,PTbooking.trainingname, PTbooking.classdate, PTbooking.classtime,PTbooking.paymentdate,PTbooking.trainingcost \
         FROM member inner join PTbooking on member.id = PTbooking.memberid;")
    dbTrainee = cur.fetchall()

    cur = getCursor()
    cur.execute("select sum(trainingcost) as trainingcost from PTbooking")
    dbPTbooking = cur.fetchall()
    dbPaymentAmount = 0
    for row in dbPTbooking:
        if row['trainingcost'] == None:
            dbPaymentAmount = 0
        else:
            dbPaymentAmount = row['trainingcost']
    print('dbPaymentAmount:',dbPaymentAmount)

    cur = getCursor()
    cur.execute(
        "select memberid, member.firstName, member.lastName, paymentdate, paymentamount from payment inner join member on memberid = member.id; ")
    dbpayment = cur.fetchall()

    cur = getCursor()
    cur.execute("select sum(paymentamount) as paymentamount from payment;")
    dbpay = cur.fetchall()
    dbPayAmount = 0
    for row in dbpay:
        if row['paymentamount'] == None:
            dbPayAmount = 0
        else:
            dbPayAmount = row['paymentamount']
    print('dbPayAmount:',dbPayAmount)

    # cur = getCursor()
    # cur.execute(
    #     "select((select sum(paymentamount) from payment) + (select sum(trainingcost) from PTbooking)) as totalrevenue")
    # dbpayments = cur.fetchall()
    dbpayments = dbPaymentAmount + dbPayAmount

    return render_template("report.html", dbTrainee=dbTrainee, dbPTbooking=dbPaymentAmount, dbpayment=dbpayment,
                           dbpay=dbPayAmount, dbpayments=dbpayments)


if __name__ == "__main__":
    app.run(debug=True)
