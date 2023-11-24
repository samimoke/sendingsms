from django.urls import path
from . import views
from . views import CustomPasswordResetView
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import (
    
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

urlpatterns = [
    path('',views.index,name='index'),
    path('home',views.home,name='home'),
    path('registration',views.register,name='register'),
    path('connect',views.connect,name='connect'),
    path('send',views.send,name='send'),
    path('checkout',views.checkout,name='checkout'),
    path('chapapayment', views.chapa_webhook, name='chapa'),
    path('login/', views.logins,name='login'),
    path('logout/',views.logout_request,name='logout'),
    path('contact/',views.Contacts,name="contact"),
    path('profile',views.profile,name='profile'),
    path('choice',views.choice,name='choice'),
    path('change',views.admin_view,name='change'),
    # path('send-activation-email/', views.send_activation_email, name='send_activation_email'),

    # path('send-message/', views.send_message, name='send_message'),
    # path('chart/', views.chart_view, name='message_chart'),
    path('messsage-chart/', views.chart_view, name='message_chart'),
   
    path('activate/<slug:uidb64>/<slug:token>)/', views.activate_account, name='activate'),

    path('password-reset/', PasswordResetView.as_view(template_name='registration/password_reset.html'),name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),name='password_reset_confirm'),
   
    path('password-reset-complete/', CustomPasswordResetView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset'),
    # path('settings/', views.SettingsView.as_view(), name='settings'),
    path('settings/password/', views.password, name='password'), 
    path('go',views.go,name="go"),
    path('fm',views.fm,name="fm"),
    

]



urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)