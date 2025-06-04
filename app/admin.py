from django.contrib import admin
from .models import Usuario
from .models import Categoria
from .models import Produto

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("nome","email","senha")

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("nome","descricao","preco","estoque","foto","categoria")

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome",)
    
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Categoria, CategoriaAdmin)

