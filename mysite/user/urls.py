from django.conf.urls import url
from django.urls import path, include
from . import views as views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    path("user/profile", views.show_profile, name = "ShowProfile"),
    path("user/edit_user", views.editUser, name = "EditUser"),
    path("user/change_password", views.change_password, name = "ChangePassword"),
    path("user/delete_account", views.delete_account, name = "DeleteAccount"),
    path("user/time-chart/", views.time_chart, name = "time-chart"),
]