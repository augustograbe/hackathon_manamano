from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("perfil/<str:user_name>", views.perfil, name="perfil"),
    path("editar_perfil/<str:user_name>", views.editar_perfil, name="editar_perfil"),
    path("grupo/<str:grupo_id>/lista_categorias", views.lista_categorias, name="lista_categorias"),
    # api

]
