import os
from RandomMelodySite.settings import MIDIFILES_PATH
from mainapp.s3_methods import delete_uploaded_file

def get_unique_file_name(last_file_name):
        
    file_name = last_file_name.split('.')[0]
    next_number = int(file_name.split("_")[2])+1
    changed_name = file_name.split("_")
    changed_name[-1] = str(next_number)
    new_file_name = "_".join(changed_name)+'.mid'
    return new_file_name


def clean_junk_files(user):
    saved_midi_files = [file.file_name for file in user.midi_files.all()]

    for file_name in os.listdir(MIDIFILES_PATH):
        # if the file exists on the local machine
        full_path_file = os.path.join(MIDIFILES_PATH, file_name)
        # delets all saved midi files on local machine because its saved on s3 
        os.remove(full_path_file)

        if file_name not in saved_midi_files:
            if os.path.splitext(file_name)[1].startswith('.mid'):
                # deletes the file from the s3 bucket
                delete_uploaded_file(file_name)

    
