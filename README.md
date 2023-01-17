### Проект Yatube — платформа для публикаций, блог.
[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=ffffff&color=043A6B)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=ffffff&color=043A6B)](https://www.djangoproject.com/)
[![HTML](https://img.shields.io/badge/-HTML-464646?style=flat&logo=Html5&logoColor=ffffff&color=043A6B)](https://html.spec.whatwg.org/multipage/)
[![CSS](https://img.shields.io/badge/-CSS_Bootstrap-464646?style=flat&logo=Css3&logoColor=ffffff&color=043A6B)]([https://html.spec.whatwg.org/multipage/](https://getbootstrap.ru/))

### Техническое задание
> Необходимо разработать социальную сеть для публикации личных дневников.
> Это будет сайт, на котором можно создать свою страницу. 
>Если на нее зайти, то можно посмотреть все записи автора.
> Пользователи смогут заходить на чужие страницы, подписываться на авторов и комментировать их записи. 
> Автор может выбрать имя и уникальный адрес для своей страницы. 
> Дизайн можно взять самый обычный, но красивый. Тексты без особой разметки. 
> Должно выглядеть нормально, поиграйте со шрифтами. Еще надо иметь возможность модерировать записи и блокировать пользователей, если начнут присылать спам. Записи можно отправить в сообщество и посмотреть там записи разных авторов. 
>Вы же программисты, сами понимаете, как лучше сделать. =)

### Unitest тестирование для проекта Yatube
#### Тестирование Models
- для класса Post — первые пятнадцать символов поста: **post.text[:15];
- для класса Group — название группы.
- verbose_name в полях совпадает с ожидаемым
- help_text в полях совпадает с ожидаемым
#### Тестирование URLs
- доступность страниц с авторизацией и без
- соответствие страниц и шаблонов
- проверка 404 страницы
- доступность страницы редактирования поста /posts/post_id/edit/ для
  анонимного пользователя, авторизованных автора и не автора поста;
- проверка используемых редиректов на всех страницах
#### Тестирование Views
- проверка отображения нового поста в фиде подписок
- новый пост появляется на главной странице
- страницы используют правильные шаблоны
- шаблоны сфомированы с правильным контекстом
- тест кэша
- авторизированный юзер может писать комменты (не авторизированный не может)
- создание новой подписки и нельзя подписаться на себя
#### Тест приложения About:
- страницы /about/author/ и /about/tech/ доступны неавторизованному пользователю;
- для отображения страниц /about/author/ и /about/tech/применяются ожидаемые view-функции и шаблоны.
#### Тестирование Forms
- валидная форма создает/изменяет пост

# Запуск
1. Скопировать репозиторий:
```
git clone https://github.com/MrGorkiy/hw05_final
```
2. Создать и активировать виртуальное окружение:
```
python -m venv <env_name>
source venv/Scripts/activate
```
3. Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
4. Выполнить миграции:
```
python manage.py migrate
```
5. В папке с файлом manage.py выполнить команду:
```
python manage.py runserver
```

Автор: [Брысин Максим (Mr. Gorkiy)](https://github.com/MrGorkiy)
