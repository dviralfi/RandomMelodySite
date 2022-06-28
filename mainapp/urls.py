from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('scales',views.scales,name="scales"),
    path('chords',views.chords,name="chords"),
    path('convertmidi',views.convert_midi,name="convertmidi"),
    path('generatemidifile',views.generatemidifile,name="generatemidifile"),
    path('chordprogs',views.chordprogs,name="chordprogs"),
    path('register',views.register_request,name="register"),
    path('login',views.login_request,name="login"),
    path('logout',views.logout_request,name="logout"),
    path('save_midi_file_for_user/<str:file_name>',views.save_midi_file_for_user,name='save_midi_file_for_user'),
    
    path('my_files',views.get_my_files,name="my_files"),
    path('delete_account',views.delete_account,name="delete_account"),
    path('delete_midi_file/<str:file>',views.delete_midi_file,name="delete_midi_file"),
    
]