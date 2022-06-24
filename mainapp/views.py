import os
from random import choice
from telnetlib import STATUS
from django.http import HttpResponseBadRequest

from django.http.response import Http404
from django.shortcuts import HttpResponse, redirect, render


from mainapp.s3_methods import upload_file, get_presigned_url_of_file
from random_melody_module import random_melody_generator 
                                                
from RandomMelodySite.settings import BASE_DIR, MAINAPP_NAME, STATIC_ROOT, STATIC_URL,MIDIFILES_PATH

from .forms import RandomArgsForm, ChordsProgressionsForm


ATMOSPHERE_DICT = random_melody_generator.ATMOSPHERE_DICT
CHROMATIC_KEYS = random_melody_generator.CHROMATIC_KEYS
SCALES_DICT = random_melody_generator.SCALES_DICT

def home(request):
    """
    Home Page view
    """
    context = {
        'random_arg_choices_form':RandomArgsForm()
    }
    return render(request, 'home.html', context)


def about(request):
    """
    About the website view
    """
    return render(request, "about.html", {})


def contact(request):
    return render(request,"contact.html", {})


def chords(request):
    """
    Get Chords of specific music scale view
    """

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
    """
    Convert Midi file to MP3 view
    """

    context = {}

    if request.method == "POST":
        file_path = os.path.abspath(request.FILES['midifile'].name)
        print("CONVERT_MIDI:absolute path midi file: ",file_path)

        context = {
            "file_path":file_path
        }

    return render(request,'convertmidi.html',context)


def generatemidifile(request):
    """
    Generate New Midi file view
    """

    random_args = RandomArgsForm()
    
    if request.method == 'POST' :
        random_args = RandomArgsForm(request.POST)

        if random_args.is_valid():
            chords_atmosphere = random_args.cleaned_data['chords_atmosphere']
            scale_key = random_args.cleaned_data['scale_key']
            scale_type = random_args.cleaned_data['scale_type']

            if not chords_atmosphere: chords_atmosphere = choice(list(ATMOSPHERE_DICT.keys()))
            if not scale_key: scale_key = choice(CHROMATIC_KEYS)
            if not scale_type: scale_type = choice(list(SCALES_DICT.keys()))
                

            # File Creation :

            new_file_path, midi_file =  random_melody_generator.main(
                
                chords_atmosphere=chords_atmosphere,
                scale_key=scale_key,scale_type=scale_type,midi_file_path=MIDIFILES_PATH)

            name = new_file_path.split("/")[-1]

            # Create file in MIDIFILES_PATH in heroku/local machine (depends if deployed)
            with open(new_file_path,'wb') as output_file:
                midi_file.writeFile(output_file)

            # Uploads file to AWS S3 Bucket
            response = upload_file(new_file_path)
            
            if response != None: return HttpResponseBadRequest(response)

            presigned_url = get_presigned_url_of_file(name)
            

        context = {
            "file_path":presigned_url,
        }

        return render(request,'generatemidifile.html',context)

    elif request.method == 'GET':

        context = request.GET
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

    elif request.method == 'GET':

        chromatic_keys = random_melody_generator.CHROMATIC_KEYS
        types = random_melody_generator.SCALES_DICT.keys()

        context = {
        "chromatic_keys":chromatic_keys,
        "types":types
                  }
        return render(request, 'scales.html',context)


def chordprogs(request):
    atmos_form = ChordsProgressionsForm()
    if request.method == 'POST':
        atmos_form = ChordsProgressionsForm(request.POST)

        if atmos_form.is_valid():
            atmosphere = atmos_form.cleaned_data['atmosphere']
            scale_key = atmos_form.cleaned_data['scale_key']
            scale_type = atmos_form.cleaned_data['scale_type']


            if atmosphere == "":
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
        'atmos_form':ChordsProgressionsForm()
                  }
        return render(request, 'chordprogs.html',context)
