from django.urls import path
from loja import views

app_name = 'loja'

urlpatterns = [
    path('', views.lista_produtos, name='lista_produtos'),  # Página inicial com lista de produtos
    path('carrinho/', views.carrinho, name='carrinho'),  # Página do carrinho de compras
    path('adicionar/<int:produto_id>/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),  # Adicionar ao carrinho
    path('remover/<int:item_id>/', views.remover_do_carrinho, name='remover_do_carrinho'),  # Remover do carrinho
    path('checkout/', views.checkout, name='checkout'),  # Página de checkout
    path('finalizar_compra/<int:pedido_id>/', views.finalizar_compra, name='finalizar_compra'),  # Finalizar compra
]
