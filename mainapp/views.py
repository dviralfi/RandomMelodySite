import os
from random import choice,random


from django.http import HttpResponseBadRequest
from django.http.response import Http404
from django.shortcuts import HttpResponse, redirect, render
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from mainapp.s3_methods import clean_deleted_user_files, delete_uploaded_file, upload_file, get_presigned_url_of_file
from mainapp.file_creation_methods import clean_junk_files, get_unique_file_name
from random_melody_module import random_melody_generator 

                                                
from RandomMelodySite.settings import BASE_DIR, MAINAPP_NAME, STATIC_ROOT, STATIC_URL,MIDIFILES_PATH

from .forms import RandomArgsForm, ChordsProgressionsForm


ATMOSPHERE_DICT = random_melody_generator.ATMOSPHERE_DICT
CHROMATIC_KEYS = random_melody_generator.CHROMATIC_KEYS
SCALES_DICT = random_melody_generator.SCALES_DICT


def home(request,*args,**kwargs):
    """
    Home Page view
    """
    context = {
        'random_arg_choices_form':RandomArgsForm(),
        
    }
    clean_junk_files()
    return render(request, 'home.html', context)


def about(request):
    """
    About the website view
    """
    return render(request, "about.html", {})


def register_request(request):

    if request.method == 'POST':  
        form = UserCreationForm(data=request.POST)  
        if form.is_valid():  
            
            user = form.save()  

            messages.success(request, 'Account created successfully')  
            login(request, user)

            next_page = ''
            if "next" in request.GET:
                next_page = request.GET['next'] 
            

            if next_page.startswith("/save_midi_file_for_user"):
                file_name = next_page.split("/")[2]
                return save_midi_file_for_user(request, file_name=file_name)

            return redirect('home')
        else:
            messages.error(request, form.errors)
            return redirect('register')
    else:  
        form = UserCreationForm()  
        return render(request, 'register.html', context={'form':form})  


def login_request(request,*args, **kwargs):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")

                next_page = ''
                if "next" in request.GET:
                    next_page = request.GET['next'] 

                if next_page.startswith("/save_midi_file_for_user"):
                    file_name = next_page.split("/")[2]
                    return save_midi_file_for_user(request, file_name=file_name)

                if next_page:
                    return redirect(request.GET.get('next'))
                return redirect("home")
            else:
                print(messages)
                messages.error(request,"Invalid username or password.")
        
        else:
            messages.error(request,form.errors)
            return redirect("login")

    else:    
        form = AuthenticationForm()
        return render(request, "login.html", context={"form":form})


@login_required
def logout_request(request):
    clean_junk_files()
    logout(request)
    messages.info(request, f"{request.user.username} You are now logged out .")
    return redirect('home')


@login_required
def delete_account(request):
    user_object = request.user
    clean_junk_files()
    clean_deleted_user_files(user_object.username)
    user_object.delete()
    messages.success(request, "The user {} is deleted".format(user_object.username))  
    return redirect('home')


@login_required
def delete_midi_file(request,*args,**kwargs):
    file_name = kwargs["file"]
    try:
        delete_uploaded_file(file_name)
        file = request.user.midi_files.get(file_name=file_name)
        file.delete()
        messages.success(request, "The Midi File: {} is deleted".format(file_name)) 

    except Exception as e:
        messages.error(request, e) 



            
    return get_my_files(request)


def generatemidifile(request,*args,**kwargs):
    """
    Generate New Midi file view
    """
    
    username = request.user.username

    form = RandomArgsForm()
    
    if request.method == 'POST' :
        form = RandomArgsForm(request.POST)

        if form.is_valid():
            chords_atmosphere = form.cleaned_data['chords_atmosphere']
            scale_key = form.cleaned_data['scale_key']
            scale_type = form.cleaned_data['scale_type']

            if not chords_atmosphere: chords_atmosphere = choice(list(ATMOSPHERE_DICT.keys()))
            if not scale_key: scale_key = choice(CHROMATIC_KEYS)
            if not scale_type: scale_type = choice(list(SCALES_DICT.keys()))
            
            
            temp_file_name =  "tmpfile_"+username+"_"+str(random())[2:]+"_RandomMelody.mid"

            # if the file looks :

            # user-name_Randommelody_some-number.mid -> its saved
            # tmp_user-name_56486413548641_RandomMelody.mid -> not saved, need to delete
            # tmp__45454554545454_RandomMelody.mid -> need to delete

            # File Creation : (Create file in MIDIFILES_PATH in heroku/local machine (depends if deployed))
            file_path =  random_melody_generator.main(
                file_name=temp_file_name,
                chords_atmosphere=chords_atmosphere,
                scale_key=scale_key,scale_type=scale_type,midi_file_path=MIDIFILES_PATH)

            # Uploads file to AWS S3 Bucket
            file_path = os.path.join(MIDIFILES_PATH, temp_file_name)
            response = upload_file(file_path)
            
            if response != None: 
                return HttpResponseBadRequest(response)
            
            # delete file locally after uploading
            # os.remove(file_path)

            presigned_url = get_presigned_url_of_file(temp_file_name)

            
            #presigned_url = file_path
            #print("local path of midi file: ",presigned_url)
        else:
            messages.error(request, form.errors) 
            return redirect('generatemidifile')
            
        context = {
            "file_path":presigned_url,
            "file_name":temp_file_name,
        }

        return render(request,'generatemidifile.html',context)

    elif request.method == 'GET':

        context = request.GET
        return render(request,'generatemidifile.html',context)


@login_required
def save_midi_file_for_user(request,*args,**kwargs):
    user_object = request.user
    old_file_name = kwargs["file_name"]
    old_file_path = os.path.join(MIDIFILES_PATH, old_file_name)

    if user_object.midi_files.count() == 0:
        new_file_name = user_object.username + '_RandoMMelody_1.mid'
    else:
        
        new_file_name = get_unique_file_name(user_object.midi_files.last().file_name)
        while os.path.exists(os.path.join(MIDIFILES_PATH, new_file_name)):
            new_file_name = get_unique_file_name(new_file_name)
    
     
    new_file_path = os.path.join(MIDIFILES_PATH, new_file_name)
    
    os.renames(old_file_path, new_file_path)

    
    response = delete_uploaded_file(old_file_name)
    
    if response != None: 
        return HttpResponseBadRequest(response)

        # Uploads file to AWS S3 Bucket
    response = upload_file(new_file_path)
    if response != None: 
        return HttpResponseBadRequest(response)

    os.remove(new_file_path) # delete the temp file because is already uploaded 

    # Adds the name of file to user's files in the DB:
    user_object.midi_files.create(file_name=new_file_name)

    context = {
        "file_path":get_presigned_url_of_file(new_file_name)
        }

    return render(request,'generatemidifile.html', context )
                    
    
@login_required
def get_my_files(request):
    user_object = request.user
    context = {
        'files_list' : user_object.midi_files.all()
    }
    return render(request,'my_files.html',context)


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
    form = ChordsProgressionsForm()
    if request.method == 'POST':
        form = ChordsProgressionsForm(request.POST)

        if form.is_valid():
            atmosphere = form.cleaned_data['atmosphere']
            scale_key = form.cleaned_data['scale_key']
            scale_type = form.cleaned_data['scale_type']


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


def contact(request):
    return render(request,"contact.html", {})

