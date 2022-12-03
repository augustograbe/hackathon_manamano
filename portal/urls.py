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
    path("grupo/<str:grupo_id>/lista_categorias/<str:categoria_id>", views.categoria, name="categoria"),
    path("lista_grupos", views.lista_grupos, name="lista_grupos"),
    path("grupo/<str:grupo_id>", views.grupo, name="grupo"),
    path("grupo/<str:grupo_id>/sobre", views.sobre, name="sobre"),
    path("grupo/<str:grupo_id>/config", views.config_grupo, name="config_grupo"),
    path("salvos", views.salvos, name="salvos"),
    path("publicar", views.publicar, name="publicar"),
    path("post/<str:post_id>", views.post, name="post"), 
    # api
    #path("criar_categoria")

]
