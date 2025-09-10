from django.urls import path
import contacts.views


app_name = "contacts"

urlpatterns = [
    path("", contacts.views.LinksView.as_view(), name="contacts"),
]
