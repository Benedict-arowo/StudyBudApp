from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutPage, name='logout'),

    path('room/<str:id>', views.room, name='room'),
    path('create-room/', views.createRoom, name='create-room'),
    path('delete-room/<str:id>', views.deleteRoom, name='delete-room'),
    path('edit-room/<str:id>', views.editRoom, name='edit-room'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
