
from api import get_token, get_form
from func import get_task_list_red, get_task_list_green, save_to_excel


login = "info@speedtrans.ee"
key = "0VoKqTuRUFNT8LLXTpC6agAtocLnoIt8ok3LEevZ9SK9FVcNidg0cX283B1ejuJjD1GQTSqc4m7rC2nwpjPlfh7-uhMXDZYw"
task_id = 150832702
form_nr = 1125654  # HC Finances GREEN


# 1. Получаем токен
token = get_token(login, key)

# 2. Получаем регистр формы (form_register.json)
form_content = get_form(form_nr, token)

# 3. парсим контент из регистра входящих счетов HC Finances RED
# task_list = get_task_list_red(form_content)

# парсим контент из регистра исходящих счетов HC Finances GREEN
# task_list = get_task_list_green(form_content)

# 4. отображаем данные или сохраняем в excel
# save_to_excel(task_list, "HC Finances GREEN", False)

# 5 Скрипт пробегается по задачам, находит  вложения, фильтрует по валюте и скачивает в директории
# необходимо указать валюту EUR, USD, RSD
# main(token, form_nr, task_list, 'EUR')

