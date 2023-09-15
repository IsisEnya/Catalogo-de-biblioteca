from django.urls import path

from . import views

app_name = 'biblioteca'

urlpatterns = [
    #path('', views.all_livros, name='todos_livros'),
    path('detalhes/<slug:slug>/', views.detalhe_livro, name='detalhe_livro'),
    #path('search/<slug:genero_slug>/', views.lista_genero, name='lista_genero'),
    path('procurar/', views.procurar, name='procurar'),
    path('', views.home, name='home'),
    path('entrar/',views.entrar, name='entrar'), 
    path('postentrar/', views.postentrar), 
    path('sair/',views.logout, name='sair'),
    path('cadastro/',views.cadastro,name='cadastro'),
    path('postcadastro/',views.postcadastro,name='postcadastro'),
    
    
    #path('search/', views.pesquisar_livros, name='pesquisar'),
]

