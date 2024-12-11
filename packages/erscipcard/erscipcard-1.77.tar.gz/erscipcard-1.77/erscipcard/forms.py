from django import forms
from .models import User1
from .widget import AvatarFileUploadInput
from .widget import JalaliDateWidget
from django.conf import settings
from .models import Fileupload

class Fileform(forms.ModelForm):
    class Meta:
        model = Fileupload
        fields = ('Name', )


class User1form(forms.ModelForm):
    class Meta:
        model = User1
        #fields = "__all__"
        widgets = { "etebar": JalaliDateWidget , "pic": AvatarFileUploadInput  }
        try:
            exclude = settings.ERSCIPCARD_EXCLUDE if hasattr(settings, 'ERSCIPCARD_EXCLUDE') and settings.ERSCIPCARD_EXCLUDE else ['address','reserv1','reserv2','reserv3','reserv4',]
            labels = settings.ERSCIPCARD_LABELS if hasattr(settings, 'ERSCIPCARD_LABELS') and settings.ERSCIPCARD_LABELS else {}
        except:
            pass
        


