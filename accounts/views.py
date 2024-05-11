from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.urls.base import reverse_lazy, reverse, resolve
from django.urls.resolvers import URLPattern, URLResolver, RegexPattern, RoutePattern
from django.views.generic.base import View, TemplateView, RedirectView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView, FormMixin, ProcessFormView
from django.views.generic.list import ListView, MultipleObjectMixin, MultipleObjectTemplateResponseMixin, BaseListView
from django.views.generic.detail import DetailView, SingleObjectMixin, SingleObjectTemplateResponseMixin, BaseDetailView
from django.views.generic.dates import ArchiveIndexView, BaseDateListView, YearArchiveView, MonthArchiveView, WeekArchiveView, DayArchiveView, TodayArchiveView
# All the built-in views for user authentication as well as the forms used by those views
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm


from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, AccessMixin
from .models import NewUser

from dotenv import load_dotenv

def get_account_url():
    """This function returns the URL for the account page
    """
    return reverse_lazy('accounts/account.html')

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accounts/account.html')  # or your own view
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

# Create the LoginView class
class Login(LoginView):
    template_name = 'accounts/login.html'
    form_class = AuthenticationForm
    redirect_authenticated_user = True
    
    class Meta:
        model = NewUser
        fields = ["email", "password"]
        
    def get_success_url(self):
        return reverse_lazy('accounts/account.html')
    
    
def profile(request):
    """This just renders the profile page for the user
    """
    return render(request, 'accounts/profile.html')

class Logout(LogoutView):
    template_name = 'accounts/logout.html'
    next_page = 'login'
    
    def get_success_url(self):
        return reverse_lazy('login')
    
    
class PasswordReset(PasswordResetView):
    template_name = 'accounts/password/password_reset.html'
    form_class = PasswordResetForm
    email_template_name = 'accounts/password/password_reset_email.html'
    subject_template_name = 'accounts/password/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('password_reset_done')
    
class PasswordResetDone(PasswordResetDoneView):
    template_name = 'accounts/password/password_reset_done.html'
    
    def get_success_url(self):
        return reverse_lazy('password_reset_done')
    
class PasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'accounts/password/password_reset_confirm.html'
    form_class = SetPasswordForm
    success_url = reverse_lazy('password_reset_complete')
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('password_reset_complete')
    
class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'accounts/password/password_reset_complete.html'
    
    def get_success_url(self):
        return reverse_lazy('password_reset_complete')
    
class PasswordChange(PasswordChangeView):
    template_name = 'accounts/password/password_change.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_change_done')
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('password_change_done')
    
class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'accounts/password/password_change_done.html'
    
    def get_success_url(self):
        return reverse_lazy('password_change_done')

# Create the UserUpdateView class
class UserUpdateView(UpdateView):
    model = NewUser
    fields = ["first_name", "last_name", "email", "phone_number"]
    template_name = 'accounts/user_update.html'
    success_url = reverse_lazy('profile')
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('profile')
    
# Create the UserDeleteView class
class UserDeleteView(DeleteView):
    model = NewUser
    template_name = 'accounts/user_delete.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('login')
    