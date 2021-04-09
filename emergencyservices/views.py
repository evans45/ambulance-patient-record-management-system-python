from django.shortcuts import render, redirect
from django.contrib import messages
import mysql.connector
from django.db import connection
from django.db import models
import time
import string
import secrets
import random
from importlib import import_module
from django.contrib.auth.models import User, auth
from django.contrib.auth import logout
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.cache import cache_control
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from io import BytesIO
from django.views.generic import View
import base64
import pdfkit
from django.http import JsonResponse
#@cache_control(no_cache=True, must_revalidate=True)


#Create your views here.
def home(request):
    return render(request,'home.html')

def hosanapage(request):
    return render(request,'hosanalysis.html')

def analysis(request):
    return render(request,'analysis.html')

def passchange(request):
    return render(request, 'changepassword.html')

def hoshome(request):
    return render(request,'hospitalhome.html')

def patrepo(request):
    return render(request, 'patientreport.html')

def parahom(request):
    return render(request,'paramedichome.html')

def adminlogin(request):
    if request.method == 'POST':
        return redirect('/head')
    else:
        return render(request,'adminlogin.html')
    return render(request,'head.html')

def login(request):
    if request.method == 'POST':
        hos = request.POST.get('user')
        name = request.POST.get('name')
        password = request.POST.get('userpassword')#user data from login
        
        #confirming which type of user is logging in 
        if hos == 'worker':
        #parsing user login data to sql server to confirm if password matches that of an existing user
            with connection.cursor() as cursor: 
                sql = "select loginID, password from medic where (loginID, password) = (%s, %s)"#sql query to confirm that data is in the user table
                val = (name, password)
                cursor.execute(sql, val)
                x = cursor.fetchall()
            
                

                if x:    
        
                    
                    request.session["name"] = name #creating a session for the logged in user
        
                    print(name)
                    print('sql query for worker works')
                    
                    if "name" in request.session:
                
                        print('session for user made')
                        return redirect('/paramedichome')
                    else:

                        print('session failed')
                        return render(request, 'login.html')

                else:
                    print('query failure') 
                    return render(request, 'login.html')
        elif hos == 'hospital':
            with connection.cursor() as cursor: 
                sql = "select loginID, password from hospital where (loginID, password) = (%s, %s)"#sql query to confirm that data is in the user table
                val = (name, password)
                cursor.execute(sql, val)
                y = cursor.fetchall()

                if y:    #executes if username exists in the db
                    request.session["name"] = name
                    print(name+'sql query for hos works')
                    return redirect('/hospitalhome')
                else:
                    print('query failure') 
                    return render(request, 'login.html')
        else:
            print('no selection') 
            return render(request, 'login.html')
                   
    else:
        return render(request, 'login.html')
    
   

def passgen():

            #function for generating a random 12 value password for the users
            digits = string.digits
            characters = string.punctuation

            x = list(string.digits + string.ascii_letters + string.punctuation)
            random.shuffle(x)
            y = ''.join((secrets.choice(x)for i in range(2)))
            y += ''.join((secrets.choice(digits) for i in range(2)))
            y += ''.join((secrets.choice(characters) for i in range(2)))
            ylist = list(y)
            random.shuffle(ylist)
            z = ''.join(ylist)
            return z    


def head(request):         
    if request.method == 'POST': 
        hworker = request.POST.get('hworker')
        fname = request.POST.get('namer')
        lname = request.POST.get('lname1')
        login = request.POST.get('loginidr')
        password = '12345'
        phone = request.POST.get('phoner')
        email = request.POST.get('emailr')
        institute = request.POST.get('instituter')
        if fname and institute and password:

            with connection.cursor() as cursor:
                sql = "INSERT INTO medic(hworker, loginID, Fname, Lname, password, institue, email, phone_number) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                val = (hworker, login, fname, lname, password, institute, email, phone)
                cursor.execute(sql, val)
            print('user added')
            return render(request, 'head.html')
        else:

            print('incomlete')
            return render(request, 'head.html')


    else:
        return render(request, 'head.html')
    return render(request, 'head.html')

def logoutr(request):
    #del request.session['name']
    logout(request)
    return redirect('/')

def search(request):
    if request.method == 'POST':
        user = request.POST['user']
        if user:
            with connection.cursor() as cursor:
                sql = """SELECT Fname, Lname, loginID, institue, email, phone_number FROM medic WHERE loginID = (%s)"""
                val = (user)
                cursor.execute(sql,(val,))
                b =  cursor.fetchall()
                
               
            for row in b:

                fname = row[0]
                lname = row[1]
                loginid = row[2]
                institution = row[3]
                email = row[4]
                phone = row[5] 
                return render(request, 'head.html',{"fname":fname, "lname":lname, "loginid":loginid, "institution":institution, "email":email, "phone":phone})
                
        else:
            print('no data entered')
            return render(request, 'head.html')
    else:

        return render(request, 'head.html')
    return render(request, 'head.html')


def delete(request):
    if request.method == 'POST':
        login = request.POST.get('loginup')
    
        if login:
            with connection.cursor() as cursor:
                sql = """Delete FROM medic WHERE loginID = (%s)"""
                val = (login)
                cursor.execute(sql,(val,))
                print(login)
                print('user deleted')
            return render(request, 'head.html')
                
        else:
            print('no data entered')
            return redirect('/head')
            
    else:
        return render(request, 'head.html')

def update(request):
    if request.method == 'POST':
        
        fname = request.POST.get('firstname')
        lname = request.POST.get('lastname')
        login = request.POST.get('loginup')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        institute = request.POST.get('institution')
        
        if login:
            print(login)
            with connection.cursor() as cursor:
                sql = """ UPDATE medic SET Fname= %s , Lname = %s, loginID = %s, institue = %s, email = %s, phone_number = %s WHERE loginID=(%s)"""
                val = (fname, lname, login, institute, email, phone, login)
                cursor.execute(sql,(val))
                print('user updated')
                
                return render(request, 'head.html')
                
        
    else:
        return render(request, 'head.html')
    return render(request, 'head.html')

def chat(request):
    if request.method == 'POST':
        b = request.session['name']
        if b:
            with connection.cursor() as cursor:
                sql = """SELECT age, sex, injury_area, injury_description, required_procedure, extra_information, sender, reciever FROM patient_details WHERE reciever = (%s)"""
                val = (b)
                cursor.execute(sql,(val,))
               
                x = 0

                while True:

                    x +=1
                    print(x)

                    d = cursor.fetchone()
                   
                    if d:
                        age = d[0]
                        sex = d[1]
                        injury_area = d[2]
                        injury_description = d[3]
                        required_procedure = d[4]
                        extra_information = d[5]                    

                    else:
                       break
                return render(request,'patientreport.html', {'age':age, 'sex':sex, 'injury_area':injury_area, 'injury_description':injury_description, 'required_procedure':required_procedure, 'extra_information':extra_information })
                
            
        else:
            print('ooops')

    else:
        return render(request, 'patientreport.html')
    return render(request, 'patientreport.html')





def render_to_pdf(template_src, context_dict={}):
    #code for rendering page to pdf 
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()

    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)

    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def topdf(request):
    if request.method == 'POST':
        b = request.session['name']
        if b:
            with connection.cursor() as cursor:
                sql = """SELECT age, sex, injury_area, injury_description, required_procedure, extra_information, sender, reciever FROM patient_details WHERE reciever = (%s)"""
                val = (b)
                cursor.execute(sql,(val,))
               
                x = 0

                while True:

                    x +=1
                    print(x)

                    d = cursor.fetchone()
                   
                    if d:
                        age = d[0]
                        sex = d[1]
                        injury_area = d[2]
                        injury_description = d[3]
                        required_procedure = d[4]
                        extra_information = d[5]                    

                    else:
                       break
    

        template = get_template('invoice.html')
        context = {
            "patient_age": age,
            "patient_sex": sex,
            "injury_area":  injury_area,
            "description_of_injury":    injury_description,
            "procedure_required":   required_procedure,
            "extra_information":    extra_information,
        }

        html = template.render(context)
        pdf = render_to_pdf('invoice.html', context)
        
        return pdf
    else:
        return render(request, 'patientreport.html')


def patdetails(request):
    
    if request.method == 'POST':
        age = request.POST.get('age'),
        reciever = request.POST.get('reciever'),
        sex = request.POST.get('sex'),
        location = request.POST.get('pickup'),
        cause = request.POST.get('cause'),
        area = request.POST.get('area'),
        injury = request.POST.get('injury'),
        procedure = request.POST.get('procedure'),
        info = request.POST.get('info'),
        sender =  request.session['name']

        if age and sex and area and injury and procedure and info:
            with connection.cursor() as cursor:
                sql = "INSERT INTO patient_details (age, sex, injury_area, injury_description, required_procedure, extra_information, sender, reciever, location, cause) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val = (age, sex, area, injury, procedure, info, sender, reciever, location, cause)
                cursor.execute(sql,val)
            print('data entered')
        
    else:
        print(sender + "please enter patient details")
        
        return render(request,'paramedichome.html')
    
    return render(request,'paramedichome.html')

def addhos(request):
    if request.method == 'POST': 
        hcode = request.POST.get('hcode')
        name = request.POST.get('hname')
        login = request.POST.get('hlogin')
        password = '12345'
        phone = request.POST.get('hphone')
        email = request.POST.get('hemail')
        
        if name and login:

            with connection.cursor() as cursor:
                sql = "INSERT INTO hospital (hcode, name, loginID,  password, email, phone_number) VALUES (%s, %s, %s, %s, %s, %s)"
                val = (hcode, name,  login, password,  email, phone)
                cursor.execute(sql, val)
            print('hospital added')
            return render(request, 'head.html')
        else:

            print('incomplete')
            return render(request, 'head.html')
    return render(request, 'head.html')


def changepass(request):
    if request.method == 'POST':

        user = request.session['name']
        password = request.POST['password2']

        with connection.cursor() as cursor:
            sql = """SELECT loginID FROM medic WHERE  loginID = (%s)"""
            val = (user)
            cursor.execute(sql, (val,))
            b = cursor.fetchall()
            
            if b:
                with connection.cursor() as cursor:
                    sql ="UPDATE  medic SET password= %s  WHERE  loginID = (%s)"
                    val = (password, user)
                    cursor.execute(sql, (val))
                    print("medic password change successful")
                return redirect('/login')
            elif not b:
                with connection.cursor() as cursor:
                    sql = """SELECT loginID FROM hospital WHERE loginID = (%s)"""
                    val = (user)
                    x = cursor.fetchall()
                    if x:
                        with connection.cursor() as cursor:
                            sql ="UPDATE  hospital SET password= %s  WHERE  loginID = (%s)"
                            val = (password,user)
                            cursor.execute(sql, (val))
                            print("hospital password change successful")
                        return redirect('/login')
                    else:
                        print('user does not exist')
                

    else:
        return render(request, "changepassword.html")


def getcause(request):

    with connection.cursor() as cursor:
        sql = "SELECT COUNT(cause)  FROM patient_details where cause = 'accident'"
        cursor.execute(sql)
        a = cursor.fetchone()


    with connection.cursor() as cursor:
        sql = "SELECT COUNT(cause)  FROM patient_details where cause = 'unidentified'"
        cursor.execute(sql)
        n = cursor.fetchone()

    with connection.cursor() as cursor:
        sql = "SELECT COUNT(cause)  FROM patient_details where cause = 'act of nature'"
        cursor.execute(sql)
        u = cursor.fetchone()

    with connection.cursor() as cursor:
        sql = "SELECT COUNT(cause)  FROM patient_details where cause = 'attack'"
        cursor.execute(sql)
        s = cursor.fetchone()

    with connection.cursor() as cursor:
        sql = "SELECT COUNT(cause)  FROM patient_details where cause = 'Pre-existing conditions'"
        cursor.execute(sql)
        p = cursor.fetchone()
    
    with connection.cursor() as cursor:
        sql = "SELECT COUNT(location)  FROM patient_details where location= 'parklands'"
        cursor.execute(sql)
        parklands = cursor.fetchone()


    with connection.cursor() as cursor:
        sql = "SELECT COUNT(location)  FROM patient_details where location = 'westlands'"
        cursor.execute(sql)
        westlands = cursor.fetchone()

    with connection.cursor() as cursor:
        sql = "SELECT COUNT(location)  FROM patient_details where location = 'springvalley'"
        cursor.execute(sql)
        spring = cursor.fetchone()

    with connection.cursor() as cursor:
        sql = "SELECT COUNT(location)  FROM patient_details where location = 'riverside drive'"
        cursor.execute(sql)
        riverside = cursor.fetchone()

    with connection.cursor() as cursor:
        sql = "SELECT COUNT(location)  FROM patient_details where location = 'Kileleshwa'"
        cursor.execute(sql)
        kile = cursor.fetchone()
    
    with connection.cursor() as cursor:
        sql = "SELECT COUNT(location)  FROM patient_details where location = 'Kilimani'"
        cursor.execute(sql)
        kilimani = cursor.fetchone()

    with connection.cursor() as cursor:
        sql = "SELECT COUNT(location)  FROM patient_details where location = 'Loresho'"
        cursor.execute(sql)
        loresho = cursor.fetchone()

    with connection.cursor() as cursor:
        sql = "SELECT COUNT(location)  FROM patient_details where location = 'Muthaiga'"
        cursor.execute(sql)
        muthaiga = cursor.fetchone()

    with connection.cursor() as cursor:
        sql = "SELECT COUNT(location)  FROM patient_details where location = 'Mathare Valley'"
        cursor.execute(sql)
        mathare = cursor.fetchone()
    
    with connection.cursor() as cursor:
        sql = "SELECT COUNT(location)  FROM patient_details where location = 'Mathare North'"
        cursor.execute(sql)
        mathareN = cursor.fetchone()

    with connection.cursor() as cursor:
        sql = "SELECT COUNT(location)  FROM patient_details where location = 'Lower Huruma'"
        cursor.execute(sql)
        huruma = cursor.fetchone()

    with connection.cursor() as cursor:
        sql = "SELECT COUNT(location)  FROM patient_details where location = 'Kariobangi'"
        cursor.execute(sql)
        kariobangi = cursor.fetchone()

    with connection.cursor() as cursor:
        sql = "SELECT COUNT(location)  FROM patient_details where location = 'Shauri Moyo'"
        cursor.execute(sql)
        shauri = cursor.fetchone()
        
    with connection.cursor() as cursor:
        sql = "SELECT COUNT(location)  FROM patient_details where location = 'Jericho'"
        cursor.execute(sql)
        jericho = cursor.fetchone()

    with connection.cursor() as cursor:
        sql = "SELECT COUNT(location)  FROM patient_details where location = 'Makadara'"
        cursor.execute(sql)
        makadara = cursor.fetchone()

    with connection.cursor() as cursor:
        sql = "SELECT COUNT(location)  FROM patient_details where location = 'Doonholm Neighbourhood (Block 82)'"
        cursor.execute(sql)
        doni = cursor.fetchone()
        
    with connection.cursor() as cursor:
        sql = "SELECT COUNT(location)  FROM patient_details where location = 'Uhuru (1-3)'"
        cursor.execute(sql)
        uhuru = cursor.fetchone()

    with connection.cursor() as cursor:
        sql = "SELECT COUNT(location)  FROM patient_details where location = 'Buru Buru (1-6) (Blocks 72-79)'"
        cursor.execute(sql)
        buru = cursor.fetchone()

    with connection.cursor() as cursor:
        sql = "SELECT COUNT(location)  FROM patient_details where location = 'Umoja (1-2)'"
        cursor.execute(sql)
        umoja = cursor.fetchone()

    with connection.cursor() as cursor:
        sql = "SELECT COUNT(injury_area)  FROM patient_details where injury_area = 'stomach'"
        cursor.execute(sql)
        stomachdb = cursor.fetchone()

    with connection.cursor() as cursor:
        sql = "SELECT COUNT(injury_area)  FROM patient_details where injury_area = 'back'"
        cursor.execute(sql)
        backdb = cursor.fetchone()
    
    with connection.cursor() as cursor:
        sql = "SELECT COUNT(injury_area)  FROM patient_details where injury_area = 'chest'"
        cursor.execute(sql)
        chestdb = cursor.fetchone()

    with connection.cursor() as cursor:
        sql = "SELECT COUNT(injury_area)  FROM patient_details where injury_area = 'hand'"
        cursor.execute(sql)
        handdb = cursor.fetchone()

    with connection.cursor() as cursor:
        sql = "SELECT COUNT(injury_area)  FROM patient_details where injury_area = 'face'"
        cursor.execute(sql)
        facedb = cursor.fetchone()

    with connection.cursor() as cursor:
        sql = "SELECT COUNT(injury_area)  FROM patient_details where injury_area = 'leg'"
        cursor.execute(sql)
        legdb = cursor.fetchone()

    with connection.cursor() as cursor:
        sql = "SELECT COUNT(age)  FROM patient_details where age between 0 and 9"
        cursor.execute(sql)
        agegroup1 = cursor.fetchone()

    with connection.cursor() as cursor:
        sql = "SELECT COUNT(age)  FROM patient_details where age between 10 and 19"
        cursor.execute(sql)
        agegroup2 = cursor.fetchone()

    with connection.cursor() as cursor:
        sql = "SELECT COUNT(age)  FROM patient_details where age between 20 and 29"
        cursor.execute(sql)
        agegroup3 = cursor.fetchone()

    with connection.cursor() as cursor:
        sql = "SELECT COUNT(age)  FROM patient_details where age between 30 and 39"
        cursor.execute(sql)
        agegroup4 = cursor.fetchone()

    with connection.cursor() as cursor:
        sql = "SELECT COUNT(age)  FROM patient_details where age between 40 and 49"
        cursor.execute(sql)
        agegroup5 = cursor.fetchone()

    with connection.cursor() as cursor:
        sql = "SELECT COUNT(age)  FROM patient_details where age between 50 and 59"
        cursor.execute(sql)
        agegroup6 = cursor.fetchone()

    with connection.cursor() as cursor:
        sql = "SELECT COUNT(age)  FROM patient_details where age between 60 and 69"
        cursor.execute(sql)
        agegroup7 = cursor.fetchone()

    with connection.cursor() as cursor:
        sql = "SELECT COUNT(age)  FROM patient_details where age between 70 and 79"
        cursor.execute(sql)
        agegroup8 = cursor.fetchone()

    with connection.cursor() as cursor:
        sql = "SELECT COUNT(age)  FROM patient_details where age between 80 and 89"
        cursor.execute(sql)
        agegroup9 = cursor.fetchone()

    with connection.cursor() as cursor:
        sql = "SELECT COUNT(age)  FROM patient_details where age between 90 and 99"
        cursor.execute(sql)
        agegroup10 = cursor.fetchone()



        
    x = a[0]
    y = n[0]
    z = u[0]
    b = s[0]
    c = p[0]


    stomach = stomachdb[0]
    chest = chestdb[0]
    hand = handdb[0]
    face = facedb[0]
    leg = legdb[0]
    back = backdb[0]

    age1 = agegroup1[0]
    age2 = agegroup2[0]
    age3 = agegroup3[0]
    age4 = agegroup4[0]
    age5 = agegroup5[0]
    age6 = agegroup6[0]
    age7 = agegroup7[0]
    age8 = agegroup8[0]
    age9 = agegroup9[0]
    age10 = agegroup10[0]
    

    parklands = parklands[0]
    westlands = westlands[0]
    spring = spring[0]
    riverside = riverside[0]
    kile = kile[0]
    kilimani = kilimani[0]
    loresho = loresho[0]
    muthaiga = muthaiga[0]
    mathare = mathare[0]
    mathareN = mathareN[0]
    huruma = huruma[0]
    kariobangi = kariobangi[0]
    shauri = shauri[0]
    jericho = jericho[0]
    makadara = makadara[0]
    doni = doni[0]
    uhuru = uhuru[0]
    buru = buru[0]
    umoja = umoja[0]


    print(agegroup1[0])
    return render(request, 'analysis.html', {"x": x, "y": y, "z":z, "b":b, "c":c, "parklands":parklands, "westlands":westlands, "spring":spring, "riverside":riverside, "kile":kile, "kilimani":kilimani, "loresho":loresho, "muthaiga":muthaiga, "mathare":mathare, "huruma":huruma, "kariobangi":kariobangi, "shauri":shauri, "jericho":jericho, "makadara":makadara, "doni":doni, "uhuru":uhuru, "buru":buru, "umoja":umoja, "face":face, "stomach":stomach, "chest":chest, "hand":hand,  "leg":leg, "back":back, "age1":age1, "age2":age2, "age3":age3, "age4":age4, "age5":age5, "age6":age6, "age7":age7, "age8":age8, "age9":age9, "age10":age10  })
    #return JsonResponse(context)

def hosanalytics(request):
    b = request.session['name']
    with connection.cursor() as cursor:
        c = 'accident'
        sql = "SELECT COUNT(cause)  FROM patient_details where (cause,reciever) = (%s, %s)"
        val = (c,b)
        cursor.execute(sql,val)
        a = cursor.fetchone()


    with connection.cursor() as cursor:
        sql = "SELECT COUNT(cause)  FROM patient_details where (cause,reciever) = (%s, %s)"
        cu = 'unidentified'
        val = (cu,b)
        cursor.execute(sql,val)
        n = cursor.fetchone()

    with connection.cursor() as cursor:
        sql = "SELECT COUNT(cause)  FROM patient_details where (cause,reciever) = (%s, %s)"
        ca = 'act of nature'
        val = (ca,b)
        cursor.execute(sql,val)
        u = cursor.fetchone()

    with connection.cursor() as cursor:
        sql = "SELECT COUNT(cause)  FROM patient_details where (cause,reciever) = (%s, %s)"
        cat = 'attack'
        val = (cat,b)
        cursor.execute(sql,val)
        s = cursor.fetchone()

    with connection.cursor() as cursor:
        sql = "SELECT COUNT(cause)  FROM patient_details where (cause,reciever) = (%s, %s)"
        cp = 'Pre-existing conditions'
        val = (cp,b)
        cursor.execute(sql,val)
        p = cursor.fetchone()

    with connection.cursor() as cursor:
        sql = "SELECT COUNT(injury_area)  FROM patient_details where  (injury_area,reciever) = (%s, %s)"
        s = 'stomach'
        val =(s,b)
        cursor.execute(sql,val)                                 
        stomachdb = cursor.fetchone()

    with connection.cursor() as cursor:
        sql = "SELECT COUNT(injury_area)  FROM patient_details where  (injury_area,reciever) = (%s, %s)"
        back = 'back'
        val =(back,b)
        cursor.execute(sql,val)
        backdb = cursor.fetchone()
    
    with connection.cursor() as cursor:
        sql = "SELECT COUNT(injury_area)  FROM patient_details where  (injury_area,reciever) = (%s, %s)"
        c ='chest'
        val =(c,b)
        cursor.execute(sql,val)
        chestdb = cursor.fetchone()

    with connection.cursor() as cursor:
        sql = "SELECT COUNT(injury_area)  FROM patient_details where  (injury_area,reciever) = (%s, %s)"
        h = 'hand'
        val = (h,b)
        cursor.execute(sql,val)
        handdb = cursor.fetchone()

    with connection.cursor() as cursor:
        sql = "SELECT COUNT(injury_area)  FROM patient_details where  (injury_area,reciever) = (%s, %s)"
        f = 'face'
        val = (f,b)
        cursor.execute(sql,val)
        facedb = cursor.fetchone()

    with connection.cursor() as cursor:
        sql = "SELECT COUNT(injury_area)  FROM patient_details where  (injury_area,reciever) = (%s, %s)"
        l = 'leg'
        val = (l,b)
        cursor.execute(sql,val)
        legdb = cursor.fetchone()

    with connection.cursor() as cursor:
        sql = "SELECT COUNT(age)  FROM patient_details where reciever= (%s) and age between 0 and 9 "
        val = (b)
        cursor.execute(sql,(val,))
        agegroup1 = cursor.fetchone()

    with connection.cursor() as cursor:
        sql = "SELECT COUNT(age)  FROM patient_details where reciever= (%s) and age between 10 and 19"
        val = (b)
        cursor.execute(sql,(val,))
        agegroup2 = cursor.fetchone()

    with connection.cursor() as cursor:
        sql = "SELECT COUNT(age)  FROM patient_details where reciever= (%s) and age between 20 and 29"
        val = (b)
        cursor.execute(sql,(val,))
        agegroup3 = cursor.fetchone()

    with connection.cursor() as cursor:
        sql = "SELECT COUNT(age)  FROM patient_details where reciever= (%s) and  age between 30 and 39"
        val = (b)
        cursor.execute(sql,(val,))
        agegroup4 = cursor.fetchone()

    with connection.cursor() as cursor:
        sql = "SELECT COUNT(age)  FROM patient_details where reciever= (%s) and age between 40 and 49"
        val = (b)
        cursor.execute(sql,(val,))
        agegroup5 = cursor.fetchone()

    with connection.cursor() as cursor:
        sql = "SELECT COUNT(age)  FROM patient_details where reciever= (%s) and age between 50 and 59"
        val = (b)
        cursor.execute(sql,(val,))
        agegroup6 = cursor.fetchone()

    with connection.cursor() as cursor:
        sql = "SELECT COUNT(age)  FROM patient_details where reciever= (%s) and age between 60 and 69"
        val = (b)
        cursor.execute(sql,(val,))
        agegroup7 = cursor.fetchone()

    with connection.cursor() as cursor:
        sql = "SELECT COUNT(age)  FROM patient_details where reciever= (%s) and age between 70 and 79"
        val = (b)
        cursor.execute(sql,(val,))
        agegroup8 = cursor.fetchone()

    with connection.cursor() as cursor:
        sql = "SELECT COUNT(age)  FROM patient_details where reciever= (%s) and age between 80 and 89"
        val = (b)
        cursor.execute(sql,(val,))
        agegroup9 = cursor.fetchone()

    with connection.cursor() as cursor:
        sql = "SELECT COUNT(age)  FROM patient_details where reciever= (%s) and age between 90 and 99"
        val = (b)
        cursor.execute(sql,(val,))
        agegroup10 = cursor.fetchone()



        
    x = a[0]
    y = n[0]
    z = u[0]
    b = s[0]
    c = p[0]


    stomach = stomachdb[0]
    chest = chestdb[0]
    hand = handdb[0]
    face = facedb[0]
    leg = legdb[0]
    back = backdb[0]

    age1 = agegroup1[0]
    age2 = agegroup2[0]
    age3 = agegroup3[0]
    age4 = agegroup4[0]
    age5 = agegroup5[0]
    age6 = agegroup6[0]
    age7 = agegroup7[0]
    age8 = agegroup8[0]
    age9 = agegroup9[0]
    age10 = agegroup10[0]
    

    
    print(age2)
    return render(request, 'hosanalysis.html', {"x": x, "y": y, "z":z, "b":b, "c":c,  "face":face, "stomach":stomach, "chest":chest, "hand":hand,  "leg":leg, "back":back, "age1":age1, "age2":age2, "age3":age3, "age4":age4, "age5":age5, "age6":age6, "age7":age7, "age8":age8, "age9":age9, "age10":age10  })
    
    

#google maps api key -AIzaSyBR3gLjUeax_zqvIl275LT7tDVwseAPjIs

