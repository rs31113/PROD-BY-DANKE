from django.urls import path
import terms.views


app_name = "terms"

urlpatterns = [
    path("", terms.views.TermsView.as_view(), name="terms"),
]
