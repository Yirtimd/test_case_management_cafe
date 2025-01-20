from typing import List, Dict
from django.db import models
import json

# Создание моодели Orders 

class Order(models.Model):
    STATUS_CHOICE: List[tuple] = [
        ('pending', 'В ожидание'),
        ('ready', 'Готово'),
        ('paid', 'Оплачено')
    ]

    table_number: int = models.IntegerField(verbose_name='Номер стола')
    items: str = models.TextField(verbose_name='Список блюд с ценами')
    total_price: float = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Общая стоимость')
    status: str = models.CharField(max_length=10, choices=STATUS_CHOICE, default='pending', verbose_name='Статус')
    created_at: str = models.DateTimeField(auto_now_add=True, verbose_name='Время создания заказа')
    updated_at: str = models.DateTimeField(auto_now=True, verbose_name='Время обновление заказа')


    def get_items(self) -> List[dict]:
        """Десериализация items."""
        try:
            return json.loads(self.items)  # Преобразование JSON-строки в Python-объект
        except json.JSONDecodeError:
            return []  # Если данные некорректны, вернуть пустой список


    def calculate_total_price(self) -> None:
        """ Рассчет общей стоимости заказа"""
        items: List[dict] = self.get_items()  # Получить десериализованный список блюд
        self.total_price = sum(item['price'] * item['quantity'] for item in items)
        self.save()

    
    def __str__(self) -> str:
        return f"Заказ #{self.id} для стола {self.table_number}"
    
class Dish(models.Model):
    name: str = models.CharField(max_length=100, verbose_name='Название блюда')
    price: float = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')


    def __str__(self) -> str:
        return f"{self.name} - {self.price} руб."

    
    