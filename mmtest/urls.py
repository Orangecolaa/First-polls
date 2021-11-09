from django.urls import path
from . import views

# 指定该应用的命名空间,此urls只应用于此应用
app_name = 'mmtest'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
]
