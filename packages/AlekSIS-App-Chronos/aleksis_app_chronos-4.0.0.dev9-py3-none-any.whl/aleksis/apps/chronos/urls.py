from django.urls import path

from . import views

urlpatterns = [
    path(
        "substitutions/print/",
        views.substitutions_print,
        name="substitutions_print",
    ),
    path(
        "substitutions/print/<str:day>/",
        views.substitutions_print,
        name="substitutions_print",
    ),
]
