from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from main.views import registration, history

urlpatterns = [
    path('', views.index, name='home'),
    path('FAQ', views.faq, name='faq'),
    path('download', views.download, name='download'),
    path('registration', registration.as_view(), name='registration'),
    path('login', views.login, name='login'),
    path('history', history.as_view(), name='history'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404="main.views.handle_not_faund"
