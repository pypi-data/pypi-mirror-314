from django.urls import path
from django.contrib import admin

from tinyturret import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main_turret_view, name='tinyturret-main'),
    path('exceptions/<str:group_key>/', views.exception_views, name='tinyturret-exception'),
]
