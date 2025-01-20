from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse
from typing import List, Union
from django.db.models import QuerySet
from .models import Order, Dish
import json


def order_list(request: HttpRequest) -> HttpResponse:
    """ Отображаем список всех заказов с окном поиска """
    query: str = request.GET.get('search', '').strip()
    orders: QuerySet[Order] = Order.objects.all()

    if query:
        if query.isdigit():
            orders = orders.filter(table_number=int(query))  # Поиск по номеру стола
        else:
            orders = orders.filter(status__icontains=query)  # Поиск по статусу

    return render(request, 'orders/order_list.html', {'orders': orders})


def order_create(request: HttpRequest) -> HttpResponse:
    """ Создание нового заказа """
    dishes: QuerySet[Dish] = Dish.objects.all()

    if request.method == 'POST':
        table_number: int = int(request.POST.get('table_number')) #  Выбранный номер стола
        selected_dishes: List[str] = request.POST.getlist('dishes')  # Список выбранных блюд (ID)
        quantities: List[str]= request.POST.getlist('quantities')  # Список количеств

        # Формируем JSON-список блюд
        items: List[dict] = []
        for dish_id, quantity in zip(selected_dishes, quantities):
            dish = Dish.objects.get(id=dish_id)
            items.append({
                "name": dish.name,
                "quantity": int(quantity),
                "price": float(dish.price)
            })

        order: Order = Order(table_number=table_number, items=json.dumps(items))
        order.calculate_total_price()  # Рассчитываем общую стоимость
        order.save() # Сохраняем изменения
        return redirect('order_list')

    return render(request, 'orders/order_form.html', {'dishes': dishes})


def order_delete(request: HttpRequest, order_id: int) -> HttpResponse:
    """ Удаление заказа """
    order: Order = get_object_or_404(Order, id=order_id) # Получаем заказ по ID или 404
    order.delete()
    return redirect('order_list')


def update_order_status(request: HttpRequest, order_id: int) -> HttpResponse:
    order: Order = get_object_or_404(Order, id=order_id)  # Получаем заказ по ID или 404
    if request.method == 'POST':
        new_status: str = request.POST.get('status')  # Получаем новый статус из формы
        if new_status in ['pending', 'ready', 'paid']:  # Проверяем допустимые значения
            order.status = new_status
            order.save()  # Сохраняем изменения
            return redirect('order_list')  # Возвращаемся на страницу списка заказов
    return render(request, 'orders/update_status.html', {'order': order})


def revenue_summary(request: HttpRequest) -> HttpResponse:
    paid_orders: QuerySet[Order] = Order.objects.filter(status='paid') # Фильтруем заказы со статусом "оплачено"
    total_revenue: float = sum(order.total_price for order in paid_orders) # Считаем общую сумму выручки

    return render(request, 'orders/revenue_summary.html', {'total_revenue': total_revenue, 'paid_orders': paid_orders}) 

