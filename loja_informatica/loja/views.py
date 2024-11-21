from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Produto, Carrinho, ItemCarrinho, Pedido

# View para listar produtos
def lista_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'loja/lista_produtos.html', {'produtos': produtos})

# View para exibir o carrinho
def exibir_carrinho(request):
    carrinho_id = request.session.get('carrinho_id')
    if carrinho_id:
        carrinho = Carrinho.objects.prefetch_related('itens__produto').get(id=carrinho_id)
    else:
        carrinho = None
    return render(request, 'loja/carrinho.html', {'carrinho': carrinho})

# View para adicionar um produto ao carrinho
def adicionar_ao_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    carrinho_id = request.session.get('carrinho_id')

    if not carrinho_id:
        carrinho = Carrinho.objects.create()
        request.session['carrinho_id'] = carrinho.id
    else:
        carrinho = Carrinho.objects.get(id=carrinho_id)

    item, created = ItemCarrinho.objects.get_or_create(carrinho=carrinho, produto=produto)
    if not created:
        item.quantidade += 1
        item.save()

    return redirect('exibir_carrinho')

# View para remover um item do carrinho
def remover_do_carrinho(request, item_id):
    carrinho_id = request.session.get('carrinho_id')
    if carrinho_id:
        item = get_object_or_404(ItemCarrinho, id=item_id, carrinho_id=carrinho_id)
        item.delete()
    return redirect('exibir_carrinho')

# View para exibir a página de checkout
def checkout(request):
    carrinho_id = request.session.get('carrinho_id')
    if not carrinho_id:
        return redirect('lista_produtos')

    carrinho = get_object_or_404(Carrinho, id=carrinho_id)
    if request.method == 'POST':
        nome_cliente = request.POST.get('nome_cliente')
        email_cliente = request.POST.get('email_cliente')
        endereco_entrega = request.POST.get('endereco_entrega')

        if nome_cliente and email_cliente and endereco_entrega:
            pedido = Pedido.objects.create(
                carrinho=carrinho,
                nome_cliente=nome_cliente,
                email_cliente=email_cliente,
                endereco_entrega=endereco_entrega,
            )
            del request.session['carrinho_id']  # Limpar carrinho após a compra
            return render(request, 'loja/compra_finalizada.html', {'pedido': pedido})

    return render(request, 'loja/checkout.html', {'carrinho': carrinho})

# View para finalizar a compra
def finalizar_compra(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.status = 'Pago'
    pedido.save()
    return render(request, 'loja/finalizar_compra.html', {'pedido': pedido})
