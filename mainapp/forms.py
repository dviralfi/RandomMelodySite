from django import forms
from RandomMelody.RandoMMelodyGenerator import ATMOSPHERE_DICT, SCALES_DICT,CHROMATIC_KEYS

HTML_SPACE = '&nbsp;'
midi_file_path_help_text = HTML_SPACE+HTML_SPACE+'Path to save the Midi file.'
chords_atmosphere_help_text = HTML_SPACE+HTML_SPACE+'Emotional Atmosphere of the chords progressions.'
melody_length_help_text = HTML_SPACE+HTML_SPACE+'Number of Beats - common lenght is 16'
bpm_help_text = HTML_SPACE+HTML_SPACE+'Beats Per Minute'

random_choise = ('','Random value')

ATMO_CHOICES = (random_choise,) + tuple( [ (x,x.capitalize(),) for x in ATMOSPHERE_DICT.keys() ] )
KEYS_CHOICES  = (random_choise,) + tuple( [ (x,x.capitalize(),) for x in CHROMATIC_KEYS] )
TYPES_CHOICES = (random_choise,) + tuple( [ (x,x.capitalize(),) for x in SCALES_DICT.keys() ] )



class RandomArgsChoose(forms.Form):

    scale_type = forms.ChoiceField(choices = TYPES_CHOICES,initial=random_choise,required=False)

    scale_key= forms.ChoiceField(choices = KEYS_CHOICES,initial=random_choise,required=False)

    chords_atmosphere = forms.ChoiceField(choices = ATMO_CHOICES, help_text=chords_atmosphere_help_text,initial=random_choise,required=False)

    melody_length = forms.IntegerField(max_value=48,help_text=melody_length_help_text,initial=16)

    bpm = forms.IntegerField(max_value=240,help_text=bpm_help_text,initial=120)


class AtmosForm(forms.Form):

    atmosphere = forms.ChoiceField(choices = ATMO_CHOICES, help_text=chords_atmosphere_help_text,initial=random_choise,required=False)

    scale_type = forms.ChoiceField(choices = TYPES_CHOICES,initial=random_choise,required=False)

    scale_key= forms.ChoiceField(choices = KEYS_CHOICES,initial=random_choise,required=False)