from django.contrib import admin
from django.contrib.auth.models import Group,User
from .models import Category, Product

#DELETANDO UMA COISINHAS
admin.site.unregister(Group)
#----------------------------


class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username"]

admin.site.unregister(User)



admin.site.register(User,UserAdmin)




@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug','id']
    prepopulated_fields = {'slug': ('name',)}



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['categoria','titulo', 'autor', 'slug', 'quantidade',
                    'no_estoque', 'criado', 'updated','reserva','editora','data_publicacao','codigo_livro']
    list_filter = ['no_estoque', 'disponivel']
    list_editable = ['quantidade', 'no_estoque']
    prepopulated_fields = {'slug': ('titulo',)}
