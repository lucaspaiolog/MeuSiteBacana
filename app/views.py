from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from app.models import Usuario
from app.forms import formUsuario, formLogin
from .models import Produto
from .forms import ProdutoForm
import requests

def index(request):
    return render(request, "index.html")

def exibirUsuarios(request):
    sessao = verificar_sessao(request)
    if sessao: return sessao

    usuarios = Usuario.objects.all()
    return render(request, 'usuarios.html', {'ListUsuarios': usuarios})

def addUsuario(request):
    formUser = formUsuario(request.POST or None)
    
    if request.POST:
        if formUser.is_valid():
            formUser.save()
            return redirect("exibirUsuarios")
    
    return render(request, "add-usuario.html", {'form':formUser})

def excluirUsuario(request, id_usuario):
    usuario = Usuario.objects.get(id=id_usuario)
    usuario.delete()
    return redirect("exibirUsuarios")

def editarUsuario(request, id_usuario):
    usuario = Usuario.objects.get(id=id_usuario)
    
    formUser = formUsuario(request.POST or None, instance=usuario)
    
    if request.POST:
        if formUser.is_valid():
            formUser.save()
            return redirect("exibirUsuarios")
    return render(request, "editar-usuario.html", {'form':formUser})


def listar_produtos(request):
    sessao = verificar_sessao(request)
    if sessao: return sessao
    produtosapi = requests.get("https://fakestoreapi.com/products").json()

    # produtos = Produto.objects.all()
    return render(request, 'produtos/listar.html', {'produtos': produtosapi})

def cadastrar_produto(request):
     sessao = verificar_sessao(request)
     if sessao: return sessao

     if request.method == 'POST':
         form = ProdutoForm(request.POST, request.FILES)
         if form.is_valid():
             form.save()
             return redirect('listar_produtos')
     else:
         form = ProdutoForm()

     return render(request, 'produtos/form.html', {'form': form, 'titulo': 'Cadastrar Produto'})


 def editar_produto(request, pk):
     produto = get_object_or_404(Produto, pk=pk)
     if request.method == 'POST':
         form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
             form.save()
             return redirect('listar_produtos')
     else:
        form = ProdutoForm(instance=produto)
     return render(request, 'produtos/form.html', {'form': form, 'titulo': 'Editar Produto'})

 def excluir_produto(request, pk):
     produto = get_object_or_404(Produto, pk=pk)
     if request.method == 'POST':
         produto.delete()
         return redirect('listar_produtos')
    return render(request, 'produtos/confirmar_exclusao.html', {'produto': produto})

def login(request):
    frmLogin = formLogin(request.POST or None)
    if request.POST:
        if frmLogin.is_valid():
            _email = frmLogin.cleaned_data.get('email')
            _senha = frmLogin.cleaned_data.get('senha')
            try:
                userLogin = Usuario.objects.get(email = _email, senha = _senha)
                if userLogin is not None:
                    request.session.set_expiry(timedelta(seconds=60))
                    request.session['email'] = _email
                    
                    return redirect("dashboard")
            except Usuario.DoesNotExist:
                return render(request, "login.html")
    return render(request, "login.html", {'form': frmLogin})

def dashboard(request):
    sessao = verificar_sessao(request)
    if sessao: return sessao

    _email = request.session.get("email")
    return render(request, "dashboard.html", {"email": _email})

def verificar_sessao(request):
    if not request.session.get('email'):
        return redirect('index')
    return None