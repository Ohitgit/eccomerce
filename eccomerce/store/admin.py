from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import *


@admin.register(Category)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(SummernoteModelAdmin):
    summernote_fields = ('productdesc','productadditonalinformation',)
    list_display = ['title', 'author', 'slug', 'price',
                    'in_stock', 'created', 'updated']
    list_filter = ['in_stock', 'is_active']
    list_editable = ['price', 'in_stock']
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(ProductImage)
admin.site.register(User)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Contact)
admin.site.register(Order)