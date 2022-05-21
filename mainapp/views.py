import os
from random import choice
from django import forms

from django.http import request
from django.http.response import Http404
from django.shortcuts import HttpResponse, redirect, render

from random_melody_module import random_melody_generator #from the package import the module
                                                
from RandomMelodySite.settings import BASE_DIR, MAINAPP_NAME, STATIC_URL,MIDIFILES_PATH

from .forms import RandomArgsChoose,AtmosForm


ATMOSPHERE_DICT = random_melody_generator.ATMOSPHERE_DICT
CHROMATIC_KEYS = random_melody_generator.CHROMATIC_KEYS
SCALES_DICT = random_melody_generator.SCALES_DICT

def home(request):

    context = {
        'random_arg_choices_form':RandomArgsChoose()
    }
    return render(request, 'home.html', context)


def about(request):
    return render(request, "about.html", {})


def contact(request):
    return render(request,"contact.html", {})


def chords(request):

    if request.method == 'POST':
        
        chord_note = request.POST.get('Notes', None)
        chord_type = request.POST.get('Types', None)

        chromatic_keys = random_melody_generator.CHROMATIC_KEYS

        chord_notes = random_melody_generator.get_chord_notes_by_note_and_type(chord_note,chord_type)

        try:
            context = {
                "chromatic_keys":chromatic_keys,
                "chord_types":list(random_melody_generator.CHORDS_SEQUENCE_DICT.keys()),
                "chord_seqs":random_melody_generator.CHORDS_SEQUENCE_DICT.values(),

                "chord_notes":chord_notes,
                "chord_note":chord_note,
                "chord_type":chord_type.capitalize()
            }
            
            return render(request,'chords.html',context)
        except Exception:
            return HttpResponse(Http404)  

    else:
        context = {

        "chromatic_keys":random_melody_generator.CHROMATIC_KEYS,
        "chord_types":random_melody_generator.CHORDS_SEQUENCE_DICT.keys(),
        "chord_seqs":random_melody_generator.CHORDS_SEQUENCE_DICT.values(),

                  }
        return render(request, 'chords.html',context)


def convert_midi(request):
    return render(request,'convertmidi.html',{})


def generatemidifile(request):
    print('GEnerate Me Midi File!!!!!!!!!!!!!!!!')
    random_args = RandomArgsChoose()
    path = ''
    name = ''
    if request.method == 'POST' :
        random_args = RandomArgsChoose(request.POST)

        if random_args.is_valid():
            chords_atmosphere = random_args.cleaned_data['chords_atmosphere']
            scale_key = random_args.cleaned_data['scale_key']
            scale_type = random_args.cleaned_data['scale_type']


            if chords_atmosphere == "":
                print(ATMOSPHERE_DICT.keys())
                chords_atmosphere = choice(list(ATMOSPHERE_DICT.keys()))
                
            if scale_key == '':
                scale_key = choice(CHROMATIC_KEYS)
            if scale_type == '':
                scale_type = choice(list(SCALES_DICT.keys()))
            

            django_midi_files_path = MIDIFILES_PATH

            path =  random_melody_generator.main(
                midi_file_path = django_midi_files_path,chords_atmosphere=chords_atmosphere,
                scale_key=scale_key,scale_type=scale_type)
            name = path.split("/")[-1]
            path = MIDIFILES_PATH +'/'+ name
            
        context = {
            "file_path":path,
            "file_name":name,
        }


        return render(request,'generatemidifile.html',context)

    else:

        context = request.GET
        print(context)
        return render(request,'generatemidifile.html',context)


def scales(request):

    if request.method == 'POST':
        
        chromatic_keys = random_melody_generator.CHROMATIC_KEYS
        types = random_melody_generator.SCALES_DICT.keys

        scale_key = request.POST.get('Keys', None)
        scale_type = request.POST.get('Types', None)

        scale_notes = random_melody_generator.get_scale_notes(scale_key,scale_type)
        roman_letters_value_dict = random_melody_generator.ROMAN_LETTERS_VALUE_DICT
    

        chords_dict = random_melody_generator.get_chords_of_scale(scale_key,scale_type)

        chords_type_in_scales_dict = {}
        if scale_type.find("minor") > 0 or scale_type.find("minor") == 0:
            chords_types_list = random_melody_generator.MINOR_CHORDS_TYPES
        else:
            chords_types_list = random_melody_generator.MAJOR_CHORDS_TYPES

        for c, type in enumerate(chords_types_list):
            chords_type_in_scales_dict[scale_notes[c]] = type
            if len(scale_notes) == c+1:
                break

        print(chords_type_in_scales_dict)


        try:
            context = {
                "scale_key":scale_key,
                "scale_type":scale_type.capitalize(),
                "scale_notes":scale_notes,
                "chromatic_keys":chromatic_keys,
                "types":types,
                "roman_letters_value_dict":roman_letters_value_dict,
                "chords_dict":chords_dict,
                "chords_type_in_scales_dict":chords_type_in_scales_dict,
            
            }


            return render(request,'scales.html',context)


        except Exception:
            return HttpResponse(Http404)  

    else: #  request.method == 'GET'...

        chromatic_keys = random_melody_generator.CHROMATIC_KEYS
        types = random_melody_generator.SCALES_DICT.keys()

        context = {
        "chromatic_keys":chromatic_keys,
        "types":types
                  }
        return render(request, 'scales.html',context)


def chordprogs(request):
    atmos_form = AtmosForm()
    if request.method == 'POST':
        atmos_form = AtmosForm(request.POST)

        if atmos_form.is_valid():
            atmosphere = atmos_form.cleaned_data['atmosphere']
            scale_key = atmos_form.cleaned_data['scale_key']
            scale_type = atmos_form.cleaned_data['scale_type']


            if atmosphere == "":
                print(ATMOSPHERE_DICT.keys())
                atmosphere = choice(list(ATMOSPHERE_DICT.keys()))
                
            if scale_key == '':
                scale_key = choice(CHROMATIC_KEYS)
            if scale_type == '':
                scale_type = choice(list(SCALES_DICT.keys()))

            progression = ATMOSPHERE_DICT[atmosphere].split('-')
            progression = [random_melody_generator.ROMAN_LETTERS_VALUE_LIST.index(p.upper()) for p in progression]
            scale_notes = random_melody_generator.get_scale_notes(scale_key=scale_key,scale_type=scale_type)
            
            chords_dict = [random_melody_generator.get_chord_notes_by_num(scale_notes,x) for x in progression ]
            
            #chords_type_list = [random_melody_generator.CHORDS_TYPE_IN_SCALES_LIST[progression.index(t)+1] for t in progression]
            #first_notes_list = [c[0] for c in chords_dict]


            context = {
                "chords_dict":chords_dict,
                'scale_type':scale_type.capitalize(),
                'scale_key':scale_key,
                'atmosphere':atmosphere.capitalize(),

            }

        return render(request, 'chordprogs.html',context)

    else:
        


        context = {
        'atmos_form':AtmosForm()
                  }
        return render(request, 'chordprogs.html',context)
