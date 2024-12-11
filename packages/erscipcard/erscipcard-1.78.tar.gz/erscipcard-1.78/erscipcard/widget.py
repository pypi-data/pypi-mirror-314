from django import forms
from django.utils.html import html_safe
import os,base64

class AvatarFileUploadInput(forms.ClearableFileInput):    
    template_name = "AvatarFileUploadInput.html"
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        if value:
            img=open(value.path, "rb")
            value.name = os.path.basename(value.name)
            image_data = base64.b64encode(img.read()).decode('utf-8')
            imgdata = "data:image/png;base64,{}".format(image_data)
            context["widget"]["imgdata"] = imgdata
        return context

class JalaliDateWidget(forms.TextInput):
    '''
    @property
    def media(self):
        js = ('persianDatepicker.js',)
        css = {'all' : ('persianDatepicker-default.css',) }
        return forms.Media(js=js, css=css)
    '''
    class Media:
        js = ('bt/js/persianDatepicker.js',)
        css = {  'all' : ('bt/css/persianDatepicker-default.css',) }

    def __init__(self, attrs=None):
        final_attrs = {'class': 'parsDate'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(JalaliDateWidget, self).__init__(attrs=final_attrs)


