from django.urls import path
import main.views


app_name = "main"

urlpatterns = [
    path("", main.views.MainView.as_view(), name="main"),
]


__all__ = ()
