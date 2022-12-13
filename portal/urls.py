from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("perfil/<str:user_name>", views.perfil, name="perfil"),
    path("editar_perfil", views.editar_perfil, name="editar_perfil"),
    path("lista_categorias/<str:grupo_id>", views.lista_categorias, name="lista_categorias"),
    path("categoria/<str:grupo_id>/<str:categoria_id>", views.categoria, name="categoria"),
    path("lista_grupos", views.lista_grupos, name="lista_grupos"),
    path("criar_grupo", views.criar_grupo, name="criar_grupo"),
    path("criar_categoria/<str:grupo_id>", views.criar_categoria, name="criar_categoria"),
    path("grupo/<str:grupo_id>", views.grupo, name="grupo"),
    path("sobre/<str:grupo_id>", views.sobre, name="sobre"),
    path("configg/<str:grupo_id>", views.config_grupo, name="configg"),
    path("salvos", views.salvos, name="salvos"),
    path("publicar", views.publicar, name="publicar"),
    path("post/<str:post_id>", views.post, name="post"),
    path("escolher_grupo/<str:post_id>", views.escolher_grupo, name="escolher_grupo"),
    path("pesquisar/<str:grupo_id>", views.pesquisar, name="pesquisar"),
    path("postsAutor/<str:autor_id>", views.postsAutor, name="postsAutor"),


]
