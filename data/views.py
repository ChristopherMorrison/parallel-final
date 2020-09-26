import os

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, Http404, HttpResponse
from django.conf import settings

from .forms import RegisterForm, ProfileUpdateForm, UploadFileForm
from .models import FileUpload


# Create your views here.
@login_required
def IndexView(request):
    user_files = FileUpload.objects.filter(user=request.user)
    print(user_files)
    return render(request, 'index.html',{
        'files': user_files
    })

def RegisterView(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            return redirect('homepage')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {
        'form': form
    })


@login_required
def UpdateProfileView(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('homepage')
    else:
        form = ProfileUpdateForm()
    return render(request, 'registration/update_profile.html', {
        'form': form
    })


@login_required
def FileUploadView(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # TODO: save file and analyze
            inst = FileUpload.objects.create(
                user=request.user,
                data=request.FILES['file']
            )
            inst.save()
            return redirect('homepage')
        print(form.errors)
    else:
        form = UploadFileForm()
    return render(request, 'upload_file.html', {'form': form})


@login_required
def FileDownloadView(request, file_id=None):
    file = FileUpload.objects.filter(id=file_id).first()
    if request.user.id is not file.user.id:
        redirect('homepage')
    
    file_path = os.path.join(settings.MEDIA_ROOT, file.data.name)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response

    raise Http404