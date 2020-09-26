from django.urls import path
from . import views


app_name = 'main'  # here for namespacing of urls.

urlpatterns = [
    path('', views.IndexView, name="homepage"),
    path('accounts/register/', views.RegisterView, name="register"),
    path('accounts/update/', views.UpdateProfileView, name="update_profile"),
    path('files/upload/', views.FileUploadView, name="file_upload"),
    path('files/download/<file_id>', views.FileDownloadView, name="file_download"),
]