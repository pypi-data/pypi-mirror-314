Erscipcard
=========
Erscipcard is a Django app to create personeli card. 
For each user,create a card and export it as pdf and docx documents.

Tip
-----------
You can edit model.py file to create your own database table , also edit template MSWord file to customize your card.

Quick start
-----------
1.Add "erscipcard" to your INSTALLED_APPS in your project setting.py file:
```
INSTALLED_APPS = [
...,
'erscipcard',
]
```

2.Include the erscipcard URLconf in your project urls.py like this:

```
path('erscipcard/', include('erscipcard.urls')),
```

3.Run ``python manage.py makemigrations``(optional) and ``python manage.py migrate``  to create the erscipcard models.

then run ``python manage.py createsuperuser`` to create personel for login erscipcard page.

4.Visit http://127.0.0.1:8000/erscipcard/ to create users and its cards.

You can download card template , edit it and uplaod your custom template , then print cards.

You can also set variables in your project settings.py to control some things like below:

```
CSRF_TRUSTED_ORIGINS = ['YourSiteAddress','https://*.127.0.0.1']
ERSCIPCARD_PICWIDTH = "5" #for width of picture in your card
ERSCIPCARD_EXCLUDE = ['reserv1','reserv2','reserv3','reserv4',] #which fields shown in your insert and edir form
ERSCIPCARD_LABELS = { 'address' : 'نشانی',}#custom labels for addition fields
```
