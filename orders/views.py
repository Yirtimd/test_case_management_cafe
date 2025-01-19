from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Order, Dish
import json
import datetime


def order_list(request):
    """ Список всех заказов """
    query = request.GET.get('search', '').strip()  # Удаляем лишние пробелы
    orders = Order.objects.all()  # Получаем все заказы по умолчанию

    if query:  # Если поисковый запрос существует
        if query.isdigit():  # Если запрос — число
            orders = orders.filter(Q(table_number=query))  # Фильтрация по номеру стола
        else:  # Если запрос — строка
            orders = orders.filter(Q(status__icontains=query))  # Фильтрация по статусу

    # Явно возвращаем результат через шаблон
    return render(request, 'orders/order_list.html', {'orders': orders})


def order_create(request):
    """ Создание нового заказа """
    dishes = Dish.objects.all()

    if request.method == 'POST':
        table_number = request.POST.get('table_number')
        selected_dishes = request.POST.getlist('dishes')  # Список выбранных блюд (ID)
        quantities = request.POST.getlist('quantities')  # Список количеств

        # Формируем JSON-список блюд
        items = []
        for dish_id, quantity in zip(selected_dishes, quantities):
            dish = Dish.objects.get(id=dish_id)
            items.append({
                "name": dish.name,
                "quantity": int(quantity),
                "price": float(dish.price)
            })

        order = Order(table_number=table_number, items=json.dumps(items))
        order.calculate_total_price()  # Рассчитываем общую стоимость
        order.save()
        return redirect('order_list')

    return render(request, 'orders/order_form.html', {'dishes': dishes})


def order_delete(request, order_id):
    """ Удаление заказа """
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return redirect('order_list')


def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)  # Получаем заказ по ID или 404
    if request.method == 'POST':
        new_status = request.POST.get('status')  # Получаем новый статус из формы
        if new_status in ['pending', 'ready', 'paid']:  # Проверяем допустимые значения
            order.status = new_status
            order.save()  # Сохраняем изменения
            return redirect('order_list')  # Возвращаемся на страницу списка заказов
    return render(request, 'orders/update_status.html', {'order': order})


def revenue_summary(request):
    # Фильтруем заказы со статусом "оплачено"
    paid_orders = Order.objects.filter(status='paid')
    
    # Считаем общую сумму выручки
    total_revenue = sum(order.total_price for order in paid_orders)
    
    # Передаем данные в шаблон
    return render(request, 'orders/revenue_summary.html', {'total_revenue': total_revenue, 'paid_orders': paid_orders})

