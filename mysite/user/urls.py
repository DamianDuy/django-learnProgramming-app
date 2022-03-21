from django.conf.urls import url
from django.urls import path, include
from . import views as views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/$',
        views.activate, name='activate'),
    path("user/profile", views.show_profile, name = "ShowProfile"),
    path("user/edit_user", views.editUser, name = "EditUser"),
    path("user/change_password", views.change_password, name = "ChangePassword"),
    path("user/delete_account", views.delete_account, name = "DeleteAccount"),
    path("user/statistics/", views.statistics, name = "statistics"),
    path("user/my_statistics/", views.my_statistics, name = "my_statistics"),
    path("user/users_statistics/", views.users_statistics, name = "users_statistics"),
    #path("user/statistics/time-chart/", views.time_chart, name = "time-chart"),
    #path("user/statistics/correctness-chart/", views.correctness_chart, name = "correctness-chart"),
    #path("user/statistics/test_attempt-chart/", views.test_attempt_chart, name = "test_attempt-chart"),
    path("user/my_statistics/time-chart/", views.time_chart, name = "time-chart"),
    path("user/my_statistics/correctness-chart/", views.correctness_chart, name = "correctness-chart"),
    path("user/my_statistics/test_attempt-chart/", views.test_attempt_chart, name = "test_attempt-chart"),
    path("user/users_statistics/statistics_incorrect_answers-chart/", views.incorrect_answers_chart, name = "incorrect_answers_chart"),
]