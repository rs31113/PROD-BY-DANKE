from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import redirect
import signup.forms
import signup.models


class SignupView(FormView):
    template_name = "signup/signup.html"
    form_class = signup.forms.SignupForm
    success_url = reverse_lazy("signup:success")
    failure_url = reverse_lazy("signup:failure")

    def post(self, request, *args, **kwargs):
        email = (request.POST.get("email") or "").strip().lower()
        if email and signup.models.Subscriber.objects.filter(email__iexact=email).exists():
            return redirect(self.failure_url)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.email = (obj.email or "").strip().lower()
        obj.save()
        return super().form_valid(form)


__all__ = ()
