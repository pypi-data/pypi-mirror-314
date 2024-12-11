from django.shortcuts import render
from django.http import HttpResponse,FileResponse
from django.views.decorators.csrf import csrf_exempt
import os,platform

def index(request):
    return  render(request,"evtt/index.html")

@csrf_exempt
def transcribe(request):
    if request.method == 'POST':
        f=request.FILES['file']
        with open('voice.m4a', 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)
        if platform.system() == "Windows":
            os.system("vosk-transcriber.exe -l fa -i {} -o out_text.txt".format('voice.m4a'))
        else:
            os.system("vosk-transcriber -l fa -i {} -o out_text.txt".format('voice.m4a'))
        f=open('out_text.txt','r',encoding = 'utf-8')        
        return HttpResponse(f.read());
        

