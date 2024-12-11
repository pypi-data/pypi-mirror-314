from django.shortcuts import render,redirect
from django.http import FileResponse,HttpResponse
from django.conf import settings
from .models import Fileupload
from .forms import Fileform
#from django.contrib.staticfiles import finders
import random,pyqrcode,os,base64
from zipfile import ZipFile
from django.contrib.auth import authenticate, login, logout

def index(request):
    try:
        return render(request,"epfs/sharefile.html" , {'var1' : 0 })
    except:
        return redirect("/epfs")
    return redirect("/epfs")

def signin(request):
    try:
        if request.method == 'POST':
            #otp_chk=pyotp.TOTP('H4ZT2CIHQM5XO2VUSZPHWTBHMNQBDY3B')
            username=request.POST['username']
            password=request.POST['password']
            #if username=='admin':
            #    if otpcode!=otp_chk.now():
            #        return redirect ('/')
            user = authenticate(request, username=username, password=password)
            if user is not None :
                login(request , user)
                #path=os.path.join(settings.BASE_DIR)
                #path=os.path.dirname(path)
                #path=os.path.join(path,'upload')
                #os.system("rm -rf {}".format(path))
                #return HttpResponse("<h4>All Files Deleted</h4>")
                return redirect("/epfs/filelist")
            else:
                return render(request, 'epfs/sharefile.html' , {'var1' : 0 })
        return redirect("/epfs")
    except:
        return redirect("/epfs")
    return redirect("/epfs")

def signout(request):
    try:
        logout(request)
        return render(request, 'epfs/sharefile.html' , {'var1' : 0 })
    except:
        return redirect("/epfs")
    return redirect("/epfs")        

def sharefile(request):
    try:
        if request.method == 'POST':
            form = Fileform(request.POST, request.FILES)
            files = request.FILES.getlist('Name')
            if form.is_valid():
                #form.save()
                keytxt=''.join([random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for i in range(10)])
                for f in files:
                    file_instance = Fileupload(Name=f,keystring=keytxt)
                    file_instance.save()
                keystring=request.scheme + "://" + request.get_host() + '/epfs/view/' + keytxt
                qrcode=pyqrcode.create(keystring)
                qrcode.svg("qrcode.svg",scale=8)
                imgfile=base64.b64encode(open("qrcode.svg","rb").read()).decode('ascii')
                return HttpResponse("<!DOCTYPE htm><html><head><title>epfs file link</title><meta name='viewport' content='width=device-width, initial-scale=1.0' ></head><body><center><h4><a href='{}'>{}</a></h4><img src='data:image/svg+xml;base64,{}' /></center></body></html>".format(keystring,keytxt,imgfile))
        else:
            form = Fileform()
        return render(request, 'epfs/sharefile.html', {'form': form , 'var1' : 0  })
    except:
        return redirect("/epfs")
    return redirect("/epfs")

def downloadfile(request,link):
    try:
        obj=Fileupload.objects.filter(keystring=link)
        if obj.count() == 0 :
            return redirect("/epfs")
        if obj.count() == 1 :
            return FileResponse(open(obj.last().Name.path,'rb'))
        zipobj = ZipFile('download.zip', 'w')
        for i in obj:
            filepath=i.Name.path
            filename=i.Name.name
            zipobj.write(filepath,filename)
        zipobj.close()
        f=open('download.zip','rb')
        fdown=f.read()
        f.close()
        os.remove('download.zip')
        response = HttpResponse(fdown, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename={}.zip'.format(link)
        return response
    except:
        return redirect("/epfs")
    return redirect("/epfs")    

def downloadfileid(request,link):
    try:
        obj=Fileupload.objects.get(id=link)
        return FileResponse(open(obj.Name.path,'rb'))
    except:
        return redirect("/epfs")
    return redirect("/epfs")

def filelist(request):
    if not request.user.is_authenticated:
        return render (request,'epfs/sharefile.html', {'var1' : 1 } )
    try:
        filelist=Fileupload.objects.all().order_by('id')
        return render(request, 'epfs/sharefile.html',  {'filelist' : filelist , 'var1' : 2 })
    except:
        return redirect("/epfs")
    return redirect("/epfs")

def delfile(request):
    if not request.user.is_authenticated:
        return render (request,'epfs/sharefile.html', {'var1' : 1 } )
    try:
        if request.method == 'GET':
            idx = request.GET['id']
            obj=Fileupload.objects.get(id = idx)
            path=obj.Name.path
            os.system("rm -rf {}".format(path))
            Fileupload.objects.get(id = idx).delete()
        return redirect("/epfs/filelist")
    except:
        return redirect("/epfs")
    return redirect("/epfs")

def delfolder(request):
    if not request.user.is_authenticated:
        return render (request,'epfs/sharefile.html', {'var1' : 1 } )
    try:
        if request.method == 'GET':
            idx = request.GET['id']
            obj=Fileupload.objects.filter(keystring = idx)
            for i in obj:
                path=i.Name.path
                os.system("rm -rf {}".format(path))
            Fileupload.objects.filter(keystring = idx).delete()
        return redirect("/epfs/filelist")
    except:
        return redirect("/epfs")
    return redirect("/epfs")

def showpic(request,i,idx):
    if not request.user.is_authenticated:
        return render (request,'epfs/sharefile.html', {'var1' : 1 } )
    try:
        keytxt=Fileupload.objects.get(id = idx).keystring
        keystring=request.scheme + "://" + request.get_host() + '/epfs/view/' + keytxt
        if i==2:
            keystring=request.scheme + "://" + request.get_host() + '/epfs/viewid/' + str(idx)
        qrcode=pyqrcode.create(keystring)
        qrcode.svg("qrcode.svg",scale=8)
        imgfile=base64.b64encode(open("qrcode.svg","rb").read()).decode('ascii')
        return HttpResponse("<center><h4><a href='{}'>{}</a></h4><img src='data:image/svg+xml;base64,{}' /></center>".format(keystring,keytxt,imgfile))
    except:
        return redirect("/epfs")
    return redirect("/epfs")
