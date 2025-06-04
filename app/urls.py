from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path ('', views.index, name="index"),
    
    path('usuarios', views.exibirUsuarios,
         name="exibirUsuarios"),
    
    path('add-usuario', views.addUsuario,
         name="addUsuario"),
    
    path('excluir-usuario/<int:id_usuario>', views.excluirUsuario,
         name="excluirUsuario"),
    
    path('editar-usuario/<int:id_usuario>', views.editarUsuario,
         name="editarUsuario"),
    
    path('produtos/', views.listar_produtos, name='listar_produtos'),

    path('produtos/adicionar/', views.adicionar_produto, name='adicionar_produto'),

     path('produtos/novo/', views.cadastrar_produto, name='cadastrar_produto'),
    
     path('produtos/editar/<int:pk>/', views.editar_produto, name='editar_produto'),
    
     path('produtos/excluir/<int:pk>/', views.excluir_produto, name='excluir_produto'),
    
    path ('login', views.login, name="login"),
    
    path ('dashboard', views.dashboard, name="dashboard"),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)