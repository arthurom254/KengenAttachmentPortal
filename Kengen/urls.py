from django.urls import path
from . import views, student, supervisor, administrator, install
from django.contrib.auth import views as auth_views
urlpatterns = [
    #####################Install##################@############
    path('install', install.new_group, name="install"),
    path('new', administrator.newProfile, name="new Profile"),
    ##############################################
    path('login', views.login, name="login page"),
    path('logout', views.logout, name="logout"),
    ################Supervisor#########################
    path('supervisor', supervisor.index, name="supervisor"),
    ########## Student Urls##########
    path('', student.student_dashboard, name="studentDashboard"),
    path('edit/<str:id>', student.editLogs, name="StudetLogsEdit"),
    path('view/<str:id>', student.viewLogs, name="StudetLogsView"),
    path('savelogs/<str:id>', student.saveLogs, name="SaveLogs"),
    path('pdf', student.pdfLogs, name="pdfLogs"),
    path('activation', student.departmentActivation, name="Activation"),
    path('updateprofile', student.updateprofile, name='updateprofile'),
    ################ Admin##############
    path('adm', administrator.dashboard, name="dashboard"),
    path('add',administrator.addnewuser , name="AddUser" ),
    path('addnew',administrator.addNew , name="New" ),
    ################PasswordReset#####################
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]