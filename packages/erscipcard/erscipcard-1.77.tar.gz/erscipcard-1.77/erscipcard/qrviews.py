from django.shortcuts import render,redirect
import pyqrcode
from django.http import HttpResponse,FileResponse
import re,base64


def qr(request):
    try:
        pic=request.GET['text']
        qr_code = pyqrcode.create(pic)#request.headers['HTTP_REFERER'])
        qr_code.svg('a.svg', scale=6)
        img=open('a.svg', "r")
        #image_data = base64.b64encode(img.read()).decode('utf-8')
        imgdata = "{}".format(img.read())
        return HttpResponse (imgdata)
    except:
        return HttpResponse ('Error!!!')
        
def qrtext(request,text):
    try:
        qr_code = pyqrcode.create(text)#request.headers['HTTP_REFERER'])
        qr_code.svg('a.svg', scale=6)
        img=open('a.svg', "r")
        #image_data = base64.b64encode(img.read()).decode('utf-8')
        imgdata = "{}".format(img.read())
        return HttpResponse (imgdata)
    except:
        return HttpResponse ('Error!!!')
        
