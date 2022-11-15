from django.urls import path, re_path

from articles import views

urlpatterns = [
    re_path(r"articles/$", views.article, name="project"),
    re_path(r"rank/$", views.rank, name="project-detail"),
]
