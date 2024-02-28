## Цель

Создание телеграм бота, который по краткому описанию выдает полноценный текст сказки.


## Описание данных:

На данный момент имеется датасет (находится на [гугл-диске](https://drive.google.com/file/d/1bugCZX1KHeX5ch86qM3Ovp5K4pQmpqTo/view?usp=sharing)), спаршенный с [сайта](https://nukadeti.ru/skazki), и содержащий 1448 сказки. Данные содержат такую информацию, как название и автора сказки, текст, краткое описание, теги. В дальнейшем возможно дополнение и расширение датасета, добавление дополнительных описаний и тегов.


## План работы

* Создание телеграм бота на aiogram и подключение к нему микросервисной архитектуры (fastapi + celery) для управления задачами в списке и для асинхронной обработки запросов; оформление Docker контейнера.
* Подключение “модели заглушки” (Gigachat API) к сервису для генерации ответов в телеграм боте.
* Выбор архитектуры LLM модели и метода Fine tuning, дообучение модели на собственных данных.
* Интеграция модели в сервис.
* Маштабирование приложения.


------------

 Автор работы: Сидорова Анастасия (github: [twilyfm](https://github.com/twilyfm), telegram: @twilyfm)

 Научный руководитель: Хажгериев Мурат (github: greedisneutral)
