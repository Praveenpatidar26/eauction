from django.shortcuts import render,redirect
from django.http import HttpResponse
from myapp import models as ad_model
from django.core.files.storage import FileSystemStorage

from . import models
from myapp import models as myapp_model
# Create your views here.
# Admin ka view h ye...


def myadmin_middleware(get_response):
    def middleware(request):
        if request.path=='/myadmin/' or request.path=='/myadmin/manageusers/' or request.path=='/myadmin/manageuserstatus/' or request.path=='/myadmin/addcategory/' or request.path=='/myadmin/addsubcategory/'  or request.path=='/myadmin/changeadminpassword/' or request.path=='/myadmin/editadminprofile/':
            if request.session['snum']==None or request.session['srol']!='admin':
                response=redirect('/login/')
            else:
                response=get_response(request)
        else:
            response=get_response(request)
        return response
    return middleware

def adminhome(request):
    return render(request,'adminhome.html',{"Email_track":request.session['snum']})

def manageusers(request):
    userDetails=ad_model.Register.objects.filter(role="user")
    # print(userDetails)
    return render(request,'manageusers.html',{"userDetails" : userDetails,"Email_track":request.session['snum']})

def manageuserstatus(request):
    s=request.GET.get("s")
    regid=request.GET.get("regid")
    if s=="block":
        ad_model.Register.objects.filter(regid=regid).update(status=0)
    elif s=="verify":
        ad_model.Register.objects.filter(regid=regid).update(status=1)
    else:
        ad_model.Register.objects.filter(regid=regid).delete()
    return redirect('/myadmin/manageusers') 


def addcategory(request):
    if request.method=="GET":
        return render(request,'addcategory.html',{'msg':"","Email_track":request.session['snum']})
    else :
        cat_name=request.POST.get('category_name')
        category_name=models.Category.objects.filter(Category_name=cat_name)        #category Exixt or not check krne k liye
        if len(category_name)>0:
            return render(request,'addcategory.html',{'msg':"Category Already EXISTS","Email_track":request.session['snum']})
        else:
            cat_name=request.POST.get('category_name')
            file_name=request.FILES['file_name']
            fs=FileSystemStorage()
            cat_icon_name=fs.save(file_name.name,file_name)
            p=models.Category(Category_name=cat_name,Category_file=file_name)
            p.save()
            # print(cat_name,file_name)
            return render(request,'addcategory.html',{'msg' : "file uploaded..","Email_track":request.session['snum']})



def addsubcategory(request):
    category_list=models.Category.objects.all()                                                  # This list of object is from Category to fetch category list................
    if request.method=="GET":
        return render(request,'addsubcategory.html',{'msg':" ","category_list":category_list,"Email_track":request.session['snum']})
    else :
        cat_nam=request.POST.get('category_name')
        subcat_name=request.POST.get('subcategory_name')
        sclist=models.SubCategory.objects.filter(SubCategory_name=subcat_name)                    
        # print(sclist)
        # print(cat_nam)
        if len(sclist)>0:
            return render(request,"addsubcategory.html",{"msg":"Sub category already exists please try again.....","category_list":category_list,"Email_track":request.session['snum']})
        else:
            caticon=request.FILES["caticon"]
            fs=FileSystemStorage()
            subcaticonnm=fs.save(caticon.name,caticon)
            p=models.SubCategory(SubCategory_name=subcat_name,SubCategory_file=caticon,Category_name=cat_nam)
            p.save()
            return render(request,"addsubcategory.html",{"msg":"Sub category added successfully.....","category_list":category_list,"Email_track":request.session['snum']})
        # return render(request,'addsubcategory.html',{'msg' : "file uploaded..",'clist':"category_list"})



def change_admin_password(request):
    if request.method=="GET":
        return render(request,'change_password.html',{'Email_track':request.session['snum']})
    else:
        old_pass=request.POST.get('current_password')
        new_pass=request.POST.get('new_password')
        new_2_pass=request.POST.get('new_2_password')
        print(old_pass,new_2_pass,new_pass)
        if new_pass==new_2_pass and ad_model.Register.objects.filter(password=old_pass):
            ad_model.Register.objects.filter(password=old_pass,username=request.session['snum']).update(password=new_2_pass)
            return render(request,'change_password.html',{"success":"Password changed Successfully..",'Email_track':request.session['snum']})
        else:
            return render(request,'change_password.html',{"success":"Password do not match...",'Email_track':request.session['snum']})
    

#editing admin profile... 
def editadminprofile(request):
    Details=myapp_model.Register.objects.filter(username=request.session['snum'])
    print(Details[0].username)
    m,f,o="","",""
    if Details[0].gender=="male":
        m="checked"
    elif Details[0].gender=="female":
        f="checked"
    else:
        o="checked"
    if request.method=="GET":
        return render(request,'editadminprofile.html',{'Email_track':request.session['snum'],'Details':Details[0],"m":m,"f":f,"o":o})
    else:
        name=request.POST.get('name')
        mobile=request.POST.get('mobile')
        gender=request.POST.get('gender')
        city=request.POST.get('city')
        
        myapp_model.Register.objects.filter(username=request.session['snum']).update(name=name,mobile=mobile,city=city,gender=gender)
        return render(request,'editadminprofile.html',{'Email_track':request.session['snum'],'Details':Details[0],"m":m,"f":f,"o":o})
    
