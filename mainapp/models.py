
from django.db import models
from django.contrib.auth.models import User
from mainapp.s3_methods import get_presigned_url_of_file
from mainapp.views import delete_midi_file


class MidiFile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=False,related_name="midi_files")
    file_name = models.CharField(max_length=300)
    creation_date = models.DateTimeField(auto_now_add=True)

    def get_presigned_url(self):
        return get_presigned_url_of_file(self.file_name)

    def __str__(self):
        return self.file_name
    class Meta:
        ordering = ["file_name"]

    


