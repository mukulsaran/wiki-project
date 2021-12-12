from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.page, name="page"),
    path("search", views.search, name="search"),
    path("createNewPage",views.createNewPage,name="createNewPage"),
    path("wiki/<str:title>/edit",views.edit,name="edit"),
    path("random",views.random,name="random")
]
