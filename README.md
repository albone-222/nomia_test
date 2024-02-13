### Тестовое задание Nomia
В данном репозитории представлен код выполнения тестового задания от Nomia.
[Ссылка на ТЗ.](https://nomia2.notion.site/Python-developer-7adf62ee6a9f4aaab28db4ac661e2139)
Реализован простой веб-сервер на базе Django, который реализует систему создания опросов. Веб интерфейс собран с помощью шаблонизатора Django. Реализована возможность создания нескольких опросов с индивидуальными вопросами под каждый опрос. Следующий вопрос зависит от ответа на текущий, вся логика создается так же в админ-панели.
Возможны несколько типов вопросов: 
 - выбор из заданных ответов
 - ввод произвольного числа
 - ввод произвольного текста
Также реализованы несколько условий проверки ответа:
 для заданных ответов
  - равно
  - не равно

 для произвольного числа
  - равно
  - не равно
  - больше чем
  - больше или равно
  - меньше чем
  - меньше или равно
  - между (задается 2 числа интервала через пробел, в котором левая граница входит в интервал, правая нет)
  - не между (обратный результат предыдущему условию)
 
 для произвольного теста
  - равно (регистронезависимый)
  - не равно (регистронезависимый)
  - больше чем (длина строки)
  - меньше чем (длина строки)
  - содержит (содержит ли ответ заданную подстроку, регистронезависимый)
  - не сожержит (обратный результат предыдущему условию)

Хранение данных реализовано с помощью БД PostgreSQL.

### Установка сервиса
Сервис реализован в виде докер-контейнеров. Для установки необходимо скачать репозиторий и перейти в папку с ним.
Перед запуском сервисов необходимо откорректировать переменные окружения. Для этого нужно переименовать файл **env example** в **.env**.
Если есть необходимость в запуске сервиса с подключением к своему серверу БД, то в файле **.env** нужно откорректировать следующие значения:
    - ***POSTGRES_USER*** - имя пользователя для доступа к Вашему экземпляру БД
    - ***POSTGRES_PASSWORD*** - пароль для доступа к Вашему экземпляру БД
    - ***POSTGRES_DB*** - имя создаваемой БД
    - ***HOST*** - IP адрес сервера БД и порт в виде IP:PORT

Если используется контейнер из данного репозитория - предыдущий шаг можно пропустить. 
Перед запуском сборки контейнера в файле **.env** нужно откорректировать следующие значения:
    - ***DJANGO_SUPERUSER_USERNAME*** - логин администратора для входа в админку Django
    - ***DJANGO_SUPERUSER_PASSWORD*** - пароль администратора для входа в админку Django

Если необходимо развернуть веб-сервер с экземпляром БД PostgreSQL, то нужно из корневой папки репозитория выполнить команду

        docker compose -f app_db.yml up -d

либо, при использовании UNIX системы короткую команду 

        make app-db

В случае разворачивания только веб-сервиса

        docker compose -f app.yml up -d

либо, при использовании UNIX системы короткую команду 

        make app

Сервис будет доступен по адресу - ***http://IP_adress:8000***. Тестовый экземпляр доступен по адресу ***http://nomia.kostiakov.pro***
