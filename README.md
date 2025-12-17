```markdown
# Flask приложение: Колонизация Марса

## Описание проекта
Веб-приложение на Flask для подготовки к миссии колонизации Марса. Приложение включает различные страницы с информацией об экипаже, профессиях, размещении и позволяет записываться добровольцами.

## Установка и запуск

### 1. Установка зависимостей
```bash
pip install flask flask-wtf email-validator bootstrap-flask
```

### 2. Запуск приложения
```bash
python app.py
```

Приложение будет доступно по адресу: [http://127.0.0.1:8080](http://127.0.0.1:8080)

## Основные страницы приложения

### 1. Главная страница
- **URL:** `/`, `/index`
- **Заголовок:** "Добро пожаловать!"
- **Описание:** Содержит список ссылок на все страницы приложения
<img width="1083" height="688" alt="image" src="https://github.com/user-attachments/assets/2b7a9d0c-5e3b-4138-a443-f0e899651fb5" />

### 2. Список профессий
- **URL:** `/list_prof/<list>`
- **Заголовок:** "Список профессий"
- **Параметры:**
  - `list=ol` - нумерованный список
  - `list=ul` - маркированный список
- **Описание:** Отображает список профессий для работы на Марсе
<img width="721" height="427" alt="image" src="https://github.com/user-attachments/assets/c31218a8-1144-45a8-b5b6-c9c557ab87c4" />
<img width="976" height="633" alt="image" src="https://github.com/user-attachments/assets/486e32d5-ff4f-4bfd-be0b-a7c31ec8bb79" />

### 3. Размещение по каютам
- **URL:** `/distribution`
- **Заголовок:** "Размещение"
- **Описание:** Показывает размещение членов экипажа по каютам
<img width="1322" height="552" alt="image" src="https://github.com/user-attachments/assets/c830c9fa-1435-43dd-91cf-16fd7c2c9fbe" />

### 4. Информация о члене экипажа
- **URLы:**
  - `/member/<int:number>` - конкретный член экипажа по номеру
  - `/member/random` - случайный член экипажа
- **Заголовок:** "Член экипажа"
- **Отображает:**
  - ФИО
  - Фотографию
  - Список специальностей
<img width="787" height="600" alt="image" src="https://github.com/user-attachments/assets/ab9c8b25-fbfe-4260-b884-0e99eb5218c5" />

### 5. Оформление каюты
- **URL:** `/room/<sex>/<int:age>`
- **Заголовок:** "Оформление каюты"
- **Параметры:**
  - `sex`: `male` или `female`
  - `age`: возраст в годах
- **Описание:** Показывает цвет стен и эмблему для каюты в зависимости от пола и возраста
<img width="1328" height="405" alt="image" src="https://github.com/user-attachments/assets/7b8e4a34-b60e-4ea2-a8f2-4787059b39c4" />
<img width="1311" height="410" alt="image" src="https://github.com/user-attachments/assets/7267ba00-db95-4acd-a44d-b2010142d924" />

### 6. Запись добровольцем
- **URL:** `/astronaut_selection`
- **Заголовок:** "Запись добровольцем"
- **Форма содержит поля:**
  - Фамилия
  - Имя
  - Email
  - Образование
  - Основная профессия (выбор из списка)
  - Пол
  - Мотивация
  - Готовность остаться на Марсе
  - Фотография
- **Особенности:** Отправляет данные на email с прикрепленным файлом
<img width="1330" height="240" alt="image" src="https://github.com/user-attachments/assets/48d80c8b-7f9a-42e2-973b-59e06baa5ffd" />
<img width="445" height="473" alt="image" src="https://github.com/user-attachments/assets/cfc790cc-ab3d-44e2-8be3-78f39aa1314a" />

### 7. Галерея
- **URL:** `/galery`
- **Заголовок:** "Галерея"
- **Описание:** Галерея марсианских ландшафтов с использованием Bootstrap Carousel
- **Функции:**
  - Просмотр изображений
  - Загрузка новых изображений
<img width="1419" height="731" alt="image" src="https://github.com/user-attachments/assets/3a8a1e96-758a-476f-a5af-0086f65b7b72" />
