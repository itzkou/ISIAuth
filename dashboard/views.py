from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, redirect
# Create your views here.
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, DeleteView, ListView

from dashboard.forms import ClubSignUpForm, DeanSignUpForm
from dashboard.models import User, Request


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def home(request):
    if request.user.is_authenticated:
        if request.user.is_dean:
            return render(request, 'request_change_list.html')
        else:
            return render(request, 'request_list.html')
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


# TODO  student decorator , dean decorator
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
        )


class RequestDeanView(LoginRequiredMixin, ListView):
    model = Request
    template_name = 'request_change_list.html'
    context_object_name = 'club_requests'
    login_url = 'login'


class RequestCreateView(LoginRequiredMixin, CreateView):
    model = Request
    template_name = 'request_create.html'
    fields = ('owner',
              'date',
              'hour',
              'needs',
              'domain',
              'title',
              'description')
    login_url = 'login'


class RequestDetailView(LoginRequiredMixin, DetailView):
    model = Request
    template_name = 'request_detail.html'
    context_object_name = 'request'
    login_url = 'login'


class RequestUpdateView(LoginRequiredMixin, UpdateView):
    model = Request
    template_name = 'request_update.html'
    login_url = 'login'


class RequestDeleteView(LoginRequiredMixin, DeleteView):
    model = Request
    template_name = 'request_delete.html.html'
    login_url = 'login'
