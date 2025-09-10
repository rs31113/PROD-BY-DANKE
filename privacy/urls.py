from django.urls import path
import privacy.views


app_name = "privacy"

urlpatterns = [
    path("", privacy.views.PrivacyView.as_view(), name="privacy"),
]
