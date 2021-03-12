from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage      #this is to save photos  in media file


from myadmin import models as sub_model
from myapp import models as myapp_model
from user import models as user_model

import time 

media_url=settings.MEDIA_URL               # this is to render media files



def users_middleware(get_response):
    def middleware(request):
        if request.path=="/user/" or request.path=="/user/lookproducts/" or request.path=="/user/looksubproducts/" or request.path=="/user/addproducts/":
            if request.session['snum']== None or request.session['srol']!='user':
                response=redirect('/login/')
            else:
                response=get_response(request)
        else:
            response=get_response(request)
        return response
    return middleware



# Create your views here.

def userhome(request):
    
    return render(request,'userhome.html',{"User_track":request.session['snum']})

def lookproducts(request):
    clist=sub_model.Category.objects.all()
    
    # print(clist)
    return render(request,'lookproducts.html',{'media_url':media_url,'clist':clist,"User_track":request.session['snum']})

def looksubproducts(request):
    category_list=sub_model.Category.objects.all()
    cat_nam=request.GET.get('catname')
    subcategory_list=sub_model.SubCategory.objects.filter(Category_name=cat_nam)
    return render(request,'looksubproducts.html',{"media_url":media_url,'category_list':category_list,'subcategory_list':subcategory_list,'cat_nam':cat_nam,"User_track":request.session['snum']})


#this funcation is to add products by users
def addproducts(request):
    category_list=sub_model.Category.objects.all() #this is done to use AJAX
    if request.method=="GET":
        return render(request, 'addproducts.html',{'category_list':category_list,"User_track":request.session['snum']})
    else:
        title=request.POST.get('title_name')
        category=request.POST.get('category_name')
        subcategory=request.POST.get('subcategory_name')
        baseprice=request.POST.get('base_price')
        description=request.POST.get('description_area')

        pic1=request.FILES['pic_1']
        fs=FileSystemStorage()
        file1_nm=fs.save(pic1.name,pic1)
        
        if request.POST.get('pic_2')==None:
            pic2=request.FILES['pic_2']
            fs=FileSystemStorage()
            file2_nm=fs.save(pic2.name,pic2)
        else:
            file2_nm="mylogo.jpg"
        
        if request.POST.get('pic_3')==None:
            pic3=request.FILES['pic_3']
            fs=FileSystemStorage()
            file3_nm=fs.save(pic3.name,pic3)
        else:
            file3_nm="mylogo.jpg"
        
        if request.POST.get('pic_4')==None:
            pic4=request.FILES['pic_4']
            fs=FileSystemStorage()
            file4_nm=fs.save(pic4.name,pic4)
        else:
            file4_nm="mylogo.jpg"

        User_ID=request.session['snum']
        UStatus=0
        Date=time.time()

        print(title,category,description,pic1)
        p=user_model.Products(Title=title,Category=category,SubCategory_name=subcategory,Base_price=baseprice,Description=description,Pic1=file1_nm,Pic2=file2_nm,Pic3=file3_nm,Pic4=file4_nm,User_ID=User_ID,UStatus=UStatus,Date=Date)
        p.save()
        return render(request, 'addproducts.html',{'category_list':category_list,"User_track":request.session['snum']})


def addsubcategory(request):
    catnm=request.GET.get('cat_nam')                                   #data fetched from form instantly by AJAX code
    cat=sub_model.SubCategory.objects.filter(Category_name=catnm)       # catagery name matched in table of database.
    subcat="<option>Select Sub-Category</option>"                       
    # print(cat)
    for i in cat:
        subcat+=("<option>"+ i.SubCategory_name +"</option>")
    return HttpResponse(subcat)



def changepassword(request):
    if request.method=='GET':
        return render(request,'change_pass.html',{"User_track":request.session['snum']})
    else:
        old_password=request.POST.get("current_password")
        new_password=request.POST.get("new_password")
        new_2_password=request.POST.get("new_2_password")
        print(request.session['snum'])
        if new_2_password==new_password and myapp_model.Register.objects.filter(password=old_password):
            myapp_model.Register.objects.filter(password=old_password,username=request.session['snum']).update(password=new_password)
            return render(request,'change_pass.html',{'success':"Password change Successfully","User_track":request.session['snum']})
        else:
            return render(request,'change_pass.html',{'success':"Please Enter correct Password ","User_track":request.session['snum']})

def edituserprofile(request):
    details=myapp_model.Register.objects.filter(username=request.session['snum'])
    # print(details)
    m,f,o="","",""
    if details[0].gender=="male":
        m="checked"
    elif details[0].gender=="female":
        f="checked"
    else:
        o="checked"
    # print(details[0].city)
    return render(request,'edituserprofile.html',{"User_track":request.session['snum'],"userdetails":details[0],"m":m,"f":f,"o":o})


def updateuserprofile(request):
    name_user=request.POST.get('name')
    email_user=request.POST.get('email')
    mob_user=request.POST.get('mobile')
    gender_user=request.POST.get('gender')
    city_user=request.POST.get('city')
    # print(email_user)
    myapp_model.Register.objects.filter(username=email_user).update(name=name_user,mobile=mob_user,gender=gender_user,city=city_user)

    return redirect('/user/userhome/')


#This function is to verify user's product or make payment.
def verify(request):
    PaypalURL="https://www.sandbox.paypal.com/cgi-bin/webscr"
    PaypalID="sb-d49fl4842617@business.example.com"
    product=user_model.Products.objects.filter(User_ID=request.session['snum']).all()
    # print(product[0])
    return render(request,'verifyproduct.html',{"User_track":request.session['snum'],"product":product,"media":media_url,"paypalURL":PaypalURL,"paypalID":PaypalID})


def payment(request):
    pid=request.GET.get('pid')
    price=request.GET.get('price')
    uid=request.GET.get('uid')      #user Id fetched by session management.
    dt=time.time()
    print(pid,price,uid,dt)

    p=user_model.Payment(Product_ID=int(pid),price=int(price),Uid=uid,dt=dt)  #This is to save details in payment table
    p.save()
    user_model.Products.objects.filter(Product_ID=int(pid)).update(UStatus=1,Date=dt)  #this is to update details of user's product table

    return redirect("/user/verifyproduct/")