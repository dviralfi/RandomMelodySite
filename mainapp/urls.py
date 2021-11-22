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
    
    
]