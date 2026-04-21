# Vulnerable HelpDesk Application

Уязвимое веб-приложение HelpDesk для демонстрации уязвимости **PT-2025-45119** (ORM Injection в Django)

## 📋 Описание уязвимости

Уязвимость позволяет злоумышленнику через параметры поиска осуществлять ORM-инъекции, получая доступ к конфиденциальным данным, которые не должны быть доступны согласно политике контроля доступа.

**Идентификатор:** PT-2025-45119  
**Тип:** Инъекция в параметры поиска Django ORM  
**Класс CWE:** CWE-89 - SQL Injection  
**Уровень риска:** Критический (CVSS 9.4)

## 🚀 Быстрый старт

### Установка и запуск

```bash
# Клонируйте репозиторий
git clone https://github.com/Dartstrong/vulnerable-helpdesk.git
cd vulnerable-helpdesk

# Установите зависимости
pip install -r requirements.txt

# Выполните миграции
python manage.py migrate

# Создайте суперпользователя
python manage.py createsuperuser

# Запустите сервер
python manage.py runserver
