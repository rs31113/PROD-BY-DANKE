from django.urls import path
from .views import SignupView
from django.views.generic import TemplateView

app_name = 'signup'

urlpatterns = [
    path('', SignupView.as_view(), name='signup'),
    path('success/', TemplateView.as_view(template_name='signup/success.html'), name='success'),
    path('failure/', TemplateView.as_view(template_name='signup/failure.html'), name='failure'),

]
