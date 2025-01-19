from django.contrib import admin
from .models import Order, Dish

# Регистрируем модель Order в административный интерйфес для управление заказами 
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'table_number', 'total_price', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('table_number',)


# Регистрация модели Dish для формирование ассортимента блюд через административный интерфейс
@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

    