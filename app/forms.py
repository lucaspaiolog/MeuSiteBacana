from django import forms
from app.models import Usuario
from .models import Produto

class formUsuario(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = (
            'nome', 'email', 'senha', 'cep', 'logradouro', 'bairro',
            'localidade', 'uf', 'numero_residencia'
        )

        widgets = {
            'nome': forms.TextInput(attrs={'type': 'text'}),
            'email': forms.TextInput(attrs={'type': 'email'}),
            'senha': forms.TextInput(attrs={'type': 'password'}),
            'cep': forms.TextInput(attrs={'onblur': 'buscarCEP(this.value)'}),
        }

        
class formLogin(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('email', 'senha')
        
        widgets = {
            'email' : forms.TextInput(attrs={'type':'email'}),
            'senha' : forms.TextInput(attrs={'type':'password'}),
        }

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'preco', 'estoque', 'foto']
        widgets = {
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            }
    foto = forms.ImageField(widget=forms.FileInput(attrs={'accept': 'image/*'}))



from .models import Venda

class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = ['numero_cartao', 'validade', 'cvv']
