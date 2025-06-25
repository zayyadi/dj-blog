from django import views
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
# from django.core.mail import send_mail
# from django.template.loader import render_to_string
# from django.utils.http import urlsafe_base64_encode
# from django.utils.encoding import force_bytes
# from django.utils.encoding import force_str
# from django.utils.http import urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from .forms import UserUpdateForm, ProfileUpdateForm
# from core.settings import DEFAULT_FROM_EMAIL

from social_django.models import UserSocialAuth

from users.forms import SignUpForm
from users.models import CustomUser

from blog.models import Article # Assuming your Article model is in the 'blog' app

@login_required
def profile(request):
    # Get all articles authored by the current user
    user_articles = Article.objects.filter(author=request.user).order_by('-publish')

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('users:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'articles': user_articles,
    }
    
    return render(request, 'users/profile.html', context)


@method_decorator(ratelimit(key='ip', rate='5/h', method='POST', block=True), name='dispatch')
class RegisterView(views.View):
    def get(self, request):
        return render(request, "registration/register.html", {"form": SignUpForm()})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect(reverse("users:login"))

        return render(request, "register.html", {"form": form})


@method_decorator(ratelimit(key='ip', rate='5/m', method='POST', block=True), name='dispatch')
class MyLoginView(LoginView):
    def get_success_url(self):
        redirect_url = self.request.GET.get("next")
        if redirect_url:
            return redirect_url

        return reverse("blog:articles")


def social_login(request):
    return render(request, "registration/socials.html")


@login_required
def settings(request):
    user = request.user

    try:
        github_login = user.social_auth.get(provider="github")
    except UserSocialAuth.DoesNotExist:
        github_login = None

    try:
        twitter_login = user.social_auth.get(provider="twitter")
    except UserSocialAuth.DoesNotExist:
        twitter_login = None

    try:
        facebook_login = user.social_auth.get(provider="facebook")
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    can_disconnect = user.social_auth.count() > 1 or user.has_usable_password()

    return render(
        request,
        "registration/settings.html",
        {
            "github_login": github_login,
            "twitter_login": twitter_login,
            "facebook_login": facebook_login,
            "can_disconnect": can_disconnect,
        },
    )


@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == "POST":
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Your password was successfully updated!")
            return redirect("password")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = PasswordForm(request.user)
    return render(request, "users/password.html", {"form": form})


def validate_username(request):
    """Check username availability"""
    username = request.GET.get("email", None)
    response = {"is_taken": CustomUser.objects.filter(email__iexact=username).exists()}
    return JsonResponse(response)


class CustomPasswordResetView(PasswordResetView):
    email_template_name = "registration/password_reset_email.html"
    # subject_template_name = "registration/password_reset_subject.txt" # Optional: if you want a separate subject template
    success_url = reverse_lazy("users:password_reset_done")
    template_name = "registration/password_reset_form.html" # Explicitly set if not default

    def form_valid(self, form):
        # The form_valid method in Django's PasswordResetView handles saving the form,
        # generating the token, and sending the email.
        # We override it to add a success message and potentially customize context for the email.
        opts = {
            "use_https": self.request.is_secure(),
            "token_generator": self.token_generator,
            "from_email": self.from_email,
            "email_template_name": self.email_template_name,
            "subject_template_name": self.subject_template_name,
            "request": self.request,
            "html_email_template_name": self.html_email_template_name,
            "extra_email_context": {
                **(self.extra_email_context or {}),
                "current_site": get_current_site(self.request), # Pass current site for domain
            },
        }
        form.save(**opts) # This now sends the email
        messages.success(self.request, "Password reset email sent successfully. Please check your inbox.")
        return super().form_valid(form) # This will redirect to success_url


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy("users:password_reset_complete")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Password successfully reset.")
        return response


def custom_password_reset_done(request):
    # Your custom password reset done view logic
    return render(request, "registration/password_reset_done.html")


def custom_password_reset_complete(request):
    # Your custom password reset complete view logic
    return render(request, "registration/password_reset_complete.html")


def logout_view(request):
    logout(request)
    return render(request, "registration/logout.html")
