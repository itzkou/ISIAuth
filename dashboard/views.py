from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, request
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, DeleteView, ListView

from dashboard.forms import ClubSignUpForm, DeanSignUpForm
from dashboard.models import User, Request


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def home(request):
    if request.user.is_authenticated:
        if request.user.is_dean:
            return redirect('requests_change')
        else:
            return redirect('request_list')
    return render(request, 'home.html')


class ClubSignUpView(CreateView):
    model = User
    form_class = ClubSignUpForm
    template_name = 'registration/signup_form.html'

    # You will probably be overriding this method most often to add things to display in your templates.
    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'club'
        return super().get_context_data(**kwargs)

    ''' This method is called when correct data is entered into the form and the form has been successfully validated without any errors. You can handle post-success logic here like send a notification email to the user, redirect to a thank you page etc.'''

    def form_valid(self, form):
        user = form.save()  # saving the user that submitted the form
        login(self.request, user)  # login into the user account
        return redirect('home')  # redirecting to home URL (home ->HomeView)


class DeanSignUpView(CreateView):
    model = User
    form_class = DeanSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'staff'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class RequestListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Request
    template_name = 'request_list.html'
    context_object_name = 'requests'
    login_url = 'login'

    def test_func(self):
        if self.request.user.is_club:
            return True
        else:
            return False

    def get_queryset(self):  # we use  query to filter or design the result of a view
        return Request.objects.filter(
            owner=self.request.user
        ).order_by('date')  # order by request(django) date


class RequestDeanView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Request
    template_name = 'requests_change.html'
    context_object_name = 'club_requests'
    login_url = 'login'

    def test_func(self):
        if self.request.user.is_dean:
            return True
        else:
            return False


class RequestCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Request
    template_name = 'request_create.html'
    fields = (
        'date',
        'hour',
        'needs',
        'domain',
        'title',
        'description')
    login_url = 'login'

    def test_func(self):
        if self.request.user.is_club:
            return True
        else:
            return False

    def form_valid(self,
                   form):  # This method is called when valid form data has been POSTed , u can add modifications by overriding it
        form.instance.owner = self.request.user
        return super().form_valid(form)


class RequestDetailView(LoginRequiredMixin, DetailView):
    model = Request
    template_name = 'request_detail.html'
    context_object_name = 'request'
    login_url = 'login'


class RequestUpdateView(LoginRequiredMixin, UpdateView):
    model = Request
    template_name = 'request_update.html'
    login_url = 'login'
    fields = ('date', 'hour', 'needs', 'domain', 'title', 'description')


class RequestDeleteView(LoginRequiredMixin, DeleteView):
    model = Request
    template_name = 'request_delete.html'
    login_url = 'login'
    success_url = reverse_lazy('request_list')


class RequestDeleteDView(LoginRequiredMixin, DeleteView):
    model = Request
    template_name = 'dean_delete.html'
    login_url = 'login'
    success_url = reverse_lazy('requests_change')


# TODO solve out the specific field issue
class RequestUpdateDView(LoginRequiredMixin, UpdateView):
    model = Request
    template_name = 'dean_update.html'
    login_url = 'login'
    fields = ('status',)


