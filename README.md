Функционал


Добавлять заказы: вводить номер стола, выбирать блюда и автоматически рассчитывать общую стоимость.
Удалять заказы: удалять заказы через интерфейс.<br/>
Искать заказы: поиск по номеру стола или статусу через строку поиска.
Обновлять статус заказа: менять статус заказа (в ожидании, готово, оплачено).
Просматривать список заказов: отображение всех заказов с детальной информацией.
Расчет выручки за смену: отдельная страница для просмотра общей выручки по заказам со статусом оплачено.
Используемые технологии
Backend: Python 3.8+, Django 2.2.
Frontend: HTML, Bootstrap 5 для стилизации.
База данных: SQLite.


Установка и запуск проекта
1. Клонируйте репозиторий
<pre> 
git clone https://github.com/Yirtimd/test_case_management_cafe.git
cd test_case_management_cafe
</pre>



3. Установите виртуальное окружение и зависимости
<pre>
python -m venv venv
source venv/bin/activate  # Для macOS/Linux
venv\Scripts\activate     # Для Windows
pip install -r requirements.txt
</pre>

4. Выполните миграции базы данных
<pre>
python manage.py makemigrations
python manage.py migrate
</pre>

6. Запустите сервер разработки
<pre>
python manage.py runserver
</pre>


