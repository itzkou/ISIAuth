from django.contrib.auth import login
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
        if request.user.is_club:
            return HttpResponse('hi club')
        else:
            return HttpResponse('hi dean')
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

class RequestListView(ListView):
    model = Request
    template_name = 'request_list.html'
    context_object_name = 'requests'

class RequestCreateView(CreateView):
    model = Request
    template_name = 'request_create.html'
    fields = ('owner',
              'date',
              'hour',
              'needs',
              'domain',
              'title',
              'description')

class RequestDetailView(DetailView):
    model = Request
    template_name = 'request_detail.html'
    context_object_name = 'request'

class RequestUpdateView(UpdateView):
    model = Request
    template_name = 'request_update.html'

class RequestDeleteView(DeleteView):
    model = Request
    template_name = 'request_delete.html.html'