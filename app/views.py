from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Usuario, Produto, Venda
from .forms import formUsuario, formLogin, ProdutoForm, VendaForm
import requests
from .decorators import precisa_login
import json
from django.http import JsonResponse
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate


# -------------------
# USUÁRIOS
# -------------------

def index(request):
    # Página inicial
    return render(request, "index.html")

def exibirUsuarios(request):
    # Lista todos os usuários (tela de listagem de usuários)
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios.html', {'ListUsuarios': usuarios})


def addUsuario(request):
    # Formulário para criar um novo usuário
    formUser = formUsuario(request.POST or None)
    if request.method == 'POST':
        if formUser.is_valid():
            formUser.save()
            return redirect("exibirUsuarios")
    return render(request, "add-usuario.html", {'form': formUser})


def editarUsuario(request, id_usuario):
    # Editar usuário existente
    usuario = get_object_or_404(Usuario, id=pk)
    formUser = formUsuario(request.POST or None, instance=usuario)
    if request.method == 'POST':
        if formUser.is_valid():
            formUser.save()
            return redirect("exibirUsuarios")
    return render(request, "editar-usuario.html", {'form': formUser, 'usuario': usuario})


def excluirUsuario(request, pk):
    # Confirmar exclusão e excluir
    usuario = get_object_or_404(Usuario, id=pk)
    if request.method == 'POST':
        usuario.delete()
        return redirect("exibirUsuarios")
    return render(request, "confirmar_exclusao_usuario.html", {'usuario': usuario})


def login_view(request):

    if request.method == 'POST':
        form = formLogin(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            senha = form.cleaned_data['senha']
            
            try:
                # Aqui você busca o usuário no seu modelo
                usuario = Usuario.objects.get(email=email, senha=senha)

                # Grava o e-mail (e, se quiser, o ID) na sessão
                request.session['usuario_email'] = usuario.email
                request.session['usuario_id'] = usuario.id

                # Redireciona para a página inicial (ou dashboard)
                return redirect('index')
            except Usuario.DoesNotExist:
                return render(request, 'login.html', {
                    'form': form,
                    'erro': 'Credenciais inválidas'
                })
    else:
        form = formLogin()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    request.session.flush()
    return redirect('index') 



# -------------------
# PRODUTOS
# -------------------

def listar_produtos(request):
    # 1. Pegue todos os produtos, ordenados por algum critério (aqui usamos o id).
    todos_os_produtos = Produto.objects.all().order_by('id')
    
    # 2. Defina “Mais Vendidos” como os primeiros N produtos. Por exemplo, N = 1:
    produtos_destaque = todos_os_produtos[:1]
    #    Se quiser destacar os 3 primeiros, use:
    #    produtos_destaque = todos_os_produtos[:3]
    
    # 3. Defina a “Galeria Internacional” como todos os produtos restantes:
    produtos_galeria = todos_os_produtos[1:]
    #    Se você destacar 3, seria:
    #    produtos_galeria = todos_os_produtos[3:]
    
    return render(request, 'produtos.html', {
        'produtos_destaque': produtos_destaque,
        'produtos_galeria': produtos_galeria
    })

@precisa_login
def listar_produtos_card(request):
    produtos = Produto.objects.all()
    return render(request, 'produtos_card.html', {'produtos': produtos})
    
def adicionar_produto(request):
    # Formulário para criar novo produto
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listar_produtos')
    else:
        form = ProdutoForm()
    return render(request, 'produtos/form.html', {'form': form})


def editar_produto(request, pk):
    # Formulário para editar produto existente
    produto = get_object_or_404(Produto, id=pk)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('listar_produtos')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'produtos/editar-produto.html', {'form': form, 'produto': produto})


def excluir_produto(request, pk):
    # Confirmar e excluir produto
    produto = get_object_or_404(Produto, id=pk)
    if request.method == 'POST':
        produto.delete()
        return redirect('listar_produtos')
    return render(request, 'produtos/confirmar_exclusao.html', {'produto': produto})



# -------------------
# CHECKOUT e VENDAS
# -------------------



@precisa_login
def checkout(request, produto_id):
    

    # Busca o produto que está sendo comprado
    produto = get_object_or_404(Produto, pk=produto_id)
    # Busca o usuário logado (pega o id da sessão)
    usuario = get_object_or_404(Usuario, pk=request.session['usuario_id'])

    if request.method == 'POST':
        form = VendaForm(request.POST)
        if form.is_valid():
            venda = form.save(commit=False)
            venda.cliente = usuario
            venda.produto = produto
            venda.preco_venda = produto.preco
            venda.save()
            messages.success(request, 'Compra realizada com sucesso!')
            return redirect('dashboard')
    else:
        form = VendaForm()

    return render(request, 'checkout.html', {
        'produto': produto,
        'usuario': usuario,
        'form': form
    
    })

@precisa_login
def dashboard(request):
    usuario = Usuario.objects.get(pk=request.session['usuario_id'])
    context = {
        'usuario_email': usuario.email
    }
    return render(request, 'dashboard.html', context)


@precisa_login
def grafico_estoque_html(request):
    return render(request, 'grafico_estoque.html')

    return render(request, 'grafico_estoque.html', context)

@precisa_login
def grafico_estoque_json(request):
    # 1) Pegue todos os produtos do banco de dados
    produtos = Produto.objects.all()

    labels = [produto.nome for produto in produtos]
    valores = [produto.estoque for produto in produtos]

    # 2) Retorne um JsonResponse (ele já serializa tudo automaticamente)
    return JsonResponse({
        'labels': labels,
        'valores': valores,
    })


@precisa_login
def grafico_vendas_html(request):
    """
    Renderiza o HTML com o <canvas id="vendasChart">.
    """
    return render(request, 'grafico_vendas.html')

@precisa_login
def grafico_vendas_json(request):
    # Agregue vendas por data (assumindo que Venda.data_compra é um DateTimeField).
    qs = Venda.objects.all().annotate(data=TruncDate('data_compra')) \
               .values('data') \
               .annotate(total=Sum('preco_venda')) \
               .order_by('data')
    
    labels = [ item['data'].strftime('%Y-%m-%d') for item in qs ]
    valores = [ float(item['total']) for item in qs ]

    return JsonResponse({
        'labels': labels,
        'valores': valores,
    })    