from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list, name='order_list'), # Общий список заказа
    path('create/', views.order_create, name='order_create'), # Создание заказа
    path('delete/<int:order_id>/', views.order_delete, name='order_delete'), # Удаление заказа
    path('orders/<int:order_id>/update/', views.update_order_status, name='update_order_status'),  # Изменение статуса
    path('revenue/', views.revenue_summary, name='revenue_summary'), # Расчет выручки за смену
]
