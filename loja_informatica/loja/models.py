from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, null=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True)

    def __str__(self):
        return self.nome

class Carrinho(models.Model):
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Carrinho #{self.id}'

    def total(self):
        return sum(item.subtotal() for item in self.itens.all())

    def total_itens(self):
        return self.itens.count()

class ItemCarrinho(models.Model):
    carrinho = models.ForeignKey(Carrinho, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantidade} x {self.produto.nome}'

    def subtotal(self):
        return self.produto.preco * self.quantidade

class Pedido(models.Model):
    carrinho = models.OneToOneField(Carrinho, on_delete=models.CASCADE)
    nome_cliente = models.CharField(max_length=255)
    email_cliente = models.EmailField()
    endereco_entrega = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=50,
        choices=[
            ('Pendente', 'Pendente'),
            ('Pago', 'Pago'),
            ('Enviado', 'Enviado'),
            ('Concluído', 'Concluído'),
        ],
        default='Pendente'
    )

    def __str__(self):
        return f'Pedido #{self.id} - {self.status}'
