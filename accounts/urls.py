from django.contrib.auth import views as auth_views 
from django.urls import path, reverse_lazy  
from django.conf.urls.static import static

from . import views

app_name="accounts"

urlpatterns = [
    path("register/", views.RegistrationView.as_view(), name="registration"),
    path("register/done", views.registration_done, name="registration_done"),
    path( \
        "login/", \
        auth_views.LoginView.as_view(template_name="accounts/login.html"), \
        name="login" \
    ),
    path( \
        "logout/", \
        auth_views.LogoutView.as_view(template_name="accounts/logged_out.html"), \
        name="logout" \
    ),
    path( \
        "password_reset/", \
        auth_views.PasswordResetView.as_view(template_name="accounts/password_reset_form.html", \
                                             email_template_name="accounts/password_reset_email.html", \
                                             success_url=reverse_lazy('accounts:password_reset_done')), \
        name="password_reset" \
    ),
    path( \
        "password_reset/done/", \
        auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"), \
        name="password_reset_done" \
    ),
    path( \
        "reset/<uidb64>/<token>/", \
        auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html", \
                                                    success_url=reverse_lazy('accounts:password_reset_complete')), \
        name="password_reset_confirm" \
    ),
    path( \
        "reset/done/", \
        auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"), \
        name="password_reset_complete" \
    ),
]