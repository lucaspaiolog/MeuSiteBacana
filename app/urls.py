from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path ('', views.index, name="index"),
    
    path('usuarios', views.exibirUsuarios, name="exibirUsuarios"),
    
    path('add-usuario', views.addUsuario, name="addUsuario"),
    
    path('excluir-usuario/<int:pk>', views.excluirUsuario, name="excluirUsuario"),
    
    path('editar-usuario/<int:id_usuario>', views.editarUsuario, name="editarUsuario"),
    
    path('produtos/', views.listar_produtos, name='listar_produtos'),

    path('produtos/listar/', views.listar_produtos_card, name='listar_produtos_card'),

     path('produtos/adicionar/', views.adicionar_produto, name='adicionar_produto'),
    
     path('produtos/editar/<int:pk>/', views.editar_produto, name='editar_produto'),
    
    path('produtos/excluir/<int:pk>/', views.excluir_produto, name='excluir_produto'),
    
    path('login/', views.login_view, name='login'),

    path('logout/', views.logout_view, name='logout'),

    path('produtos/checkout/<int:produto_id>/', views.checkout, name='checkout'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('graficos/estoque/', views.grafico_estoque_html, name='grafico_estoque_html'),
    path('graficos/dados-estoque/', views.grafico_estoque_json, name='grafico_estoque_json'),

    path('graficos/vendas/', views.grafico_vendas_html, name='grafico_vendas_html'),
    path('graficos/dados-vendas/', views.grafico_vendas_json, name='grafico_vendas_json'),
      
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




