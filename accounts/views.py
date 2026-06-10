from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CUCreationForm

class SignUpView(CreateView):
    form_class = CUCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

