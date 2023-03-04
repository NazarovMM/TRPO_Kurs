from distutils.command.upload import upload
from multiprocessing import context
from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from main.forms import CustomUserCreationForm, HistoryDB
from django.views import View
from django.views.generic import ListView
from django.contrib.auth import authenticate, login
from main.models import History
import os
import datetime
import soundfile
import torchaudio


def index(request):
    return render(request, 'main/index.html')


def faq(request):
    return render(request, 'main/faq.html')

'''class History1(View):
    def history(request):
        id=HistoryDB.get(id=request.user.id)
        print(id)
        context={id:id}
        return render(request, 'main/history.html', context)'''


def download(request):

    for file in os.scandir('D:\\Диплом\\ИУ5-83б_Назаров_М_М_Программа\\media\\'):
        if file.name.endswith(".wav"):
            os.unlink(file.path)

    if request.method == 'POST':
        try:
            ticket_attachmet_audio = request.FILES["q_attachment_audio"]
        except:
            ticket_attachmet_audio = None

        if ticket_attachmet_audio == None:
            try:
                fileObj = request.FILES['file']
            except:
                return redirect('home')

    fileObj = request.FILES['file']
    fs = FileSystemStorage()
    fs.save(fileObj.name, fileObj)
    duration = torchaudio.info(
        'D:\\Диплом\\ИУ5-83б_Назаров_М_М_Программа\\media\\'+fileObj.name)
    if request.user.id != None:
        size = fileObj.size / 1024 / 1024
        name = fileObj.name
        date = datetime.datetime.now()
        author = request.user
        form = History.create(author, name, str(
            date.strftime("%Y-%m-%d %H:%M:%S")))
        form.save()
    fileObj1 = os.path.splitext(fileObj.name)[0] + '_enhanced.wav'
    context = {
        'fileObj': fileObj1
    }
    os.system('python -m denoiser.enhance  --noisy_dir=D:\\Диплом\\ИУ5-83б_Назаров_М_М_Программа\\media\\ --out_dir=D:\\Диплом\\ИУ5-83б_Назаров_М_М_Программа\\media ')
    return render(request, 'main/download.html', context)


class registration(View):
    template_name = 'main/registration/registration.html'

    def get(self, request):
        context = {
            'form': CustomUserCreationForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            '''user = CustomUserCreationForm.is_authenticate(username=username, password=password)'''
            CustomUserCreationForm.userLogin(request, user=CustomUserCreationForm.is_authenticate(
                username=username, password=password))
            return redirect('home')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


def handle_not_faund(request, exception):
    return render(request, 'main/not-found.html', status=404)


class history(ListView):
    model = History
    template_name = 'main/history.html'
    def history(request):
        dataHistory=HistoryDB.get(id=request.user.id)
        history= {
            'id' : dataHistory.id,
            'author' : dataHistory.author,
            'name' : dataHistory.name,
            'date' : dataHistory.date
        }
        return render(request, 'main/history.html', history)
