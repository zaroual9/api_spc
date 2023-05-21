
from django.urls import path
from . import views
from .views import SubmissionCreate

urlpatterns = [
    path('', views.getData),
    path('submissions/', SubmissionCreate.as_view()),
]
