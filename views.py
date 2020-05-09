from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from calc.OCR import OCR
from calc.Wiki_Infobox import get_params
from calc.Parameters import driver, driver1
from csv import writer
import csv
import os
from django.conf import settings
from django.http import HttpResponse, Http404
from csv import reader


# Create your views here.
def home(request):
    return render(request,'home.html')

def login(request):
    username=request.POST['usr']
    password=request.POST['psd']
    if username =='admin' and password =='admin123':
	    return render(request,'First.html')
    else:
	    return render(request,'home.html')

def logout_request(request):
    logout(request)
    return render(request,'home.html')


def simple_upload(request):
    text = []
    if request.method == 'POST':
        myfiles = request.FILES.getlist('myfiles')
        cnt = len(myfiles)
        if cnt == 0:
            return render(request,'Action.html',{'cnt':cnt})
        fs = FileSystemStorage()
        for myfile in myfiles:
        	fs.save(myfile.name,myfile)
        	text.append(OCR("E:/projects/First/media/"+str(myfile)))
        return render(request, 'OCR.html',{'text': text})
    return render(request, 'OCR.html',{'text': text})


def generate_data(request):
    # return "success"
    items = request.POST.getlist('items')
    all_params = []
    for item in items:
        print(item)
        parameters = get_params(item)
        print("From wiki",parameters)

        if(parameters == None):
            parameters = driver1(item)
            print("From param",parameters)
        else:
            options = []
            i = 0
            for par in parameters:
                if(len(par) == 0):
                    options.append(i)
                i +=1
            if len(parameters) < 2:
                al_type = ""
            else:
                al_type = parameters[1]
            parameters_op = driver(item,options,al_type)
            print("from optio",parameters_op)
            j = 0
            while(j < len(parameters_op)):
                for i in options:
                    parameters[i] = parameters_op[j]
                    j+=1 

        all_params.append(parameters)
    print(all_params)
    return render(request,'Data.html',{'all_params':all_params})

def go_to_upload_page(request):
    return render(request,'Action.html')

def first_page(request):
    return render(request,'First.html')

def show_view_page(request):
    params = []
    with open('param.csv', 'r') as read_obj:
        csv_reader = reader(read_obj)
        for row in csv_reader:
            params.append(row)
    return render(request,'ViewData.html',{'params':params})

def download(request):
    print("Checking*******")
    path = "E:/projects/First/param.csv"
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404
    return render(request,'ViewData.html')
    
def view_data(request):
    # return "success"
    data = request.POST.getlist('values',"false")
    length = len(data)
    with open("param.csv", 'a', newline='') as write_obj:
        csv_writer = writer(write_obj,quoting=csv.QUOTE_ALL)
        param_list = []
        i = 0
        while (i < length):
            j = 0
            param_list = []
            while(j <= 5):
                param_list.append(data[i])
                j+=1
                i+=1
            csv_writer.writerow(param_list)

    params = []
    with open('param.csv', 'r') as read_obj:
        csv_reader = reader(read_obj)
        for row in csv_reader:
            print(row)
            params.append(row)
    return render(request,'ViewData.html',{'params':params})