from django.urls import path,include
from . import views
from django.conf.urls.i18n import i18n_patterns
from .models import User1

'''

---This is for activate djangoRestFramework---

from rest_framework import routers, serializers, viewsets


class User1Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User1
        fields = ['name', 'personeli', 'etebar', 'pic', 'number']


class User1ViewSet(viewsets.ModelViewSet):
    queryset = User1.objects.all()
    serializer_class = User1Serializer


router = routers.DefaultRouter()
router.register(r'personel', User1ViewSet)

---and add this line to below urlpatterns---

path('api', include(router.urls)),

'''

urlpatterns = [
        path('', views.index),
        path('signup/', views.signup),
	path('changepass/', views.changepass),
	path('printcard/', views.printcard),
	path('printcard2/', views.printcard2),
	path('userlist/', views.userlist),
	path('edituser/', views.edituser),
	path('deluser/', views.deluser),
	path('signin/', views.signin),
	path('logout/', views.logout_form),
	path('uploadtpl/', views.uploadtpl),
	path('printalluser/', views.printalluser),
        path('showpic/<int:picid>/', views.showpic , name = 'showpic'),
        path('setpicwidth/<int:picwidth>/', views.setpicwidth ),
        path('qr/<str:idx>/', views.shqr ),
]

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()

