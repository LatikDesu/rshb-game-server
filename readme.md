# (РСХБ) Backend для браузерной игры 

Задача заключается в разработке игры для банка РСХБ, которую можно интегрировать в API на сайте банка. Цель игры - увеличить осведомленность пользователей о современных технологиях в сельском хозяйстве и вызвать у них интерес к участию в этой области.

<h2 align="center">
<p align="center">
<img src="https://img.shields.io/badge/Django-4.2.6-green">
<img src="https://img.shields.io/badge/DRF-3.14-green">
<img src="https://img.shields.io/badge/DRFspectacular-0.26-green">
<img src="https://img.shields.io/badge/gunicorn-21.2-blue">
<img src="https://img.shields.io/badge/docker-3.9-blue">
</p>
</h2>

Реализованный проект: https://rshbdigital.ru/zifrovaya-ferma


### Установка
Скопировать .env.exemple в .env, внести данные

#### Основные параметры:<br>
Раздел `Django development config` - настройки режима запуска<br>
DEVELOPMENT_MODE -> 'True' - основная база данных PostgresSQL, 'False" - SQLlite<br>
Раздел `Django Superuser` - данные для создания суперпользователя
Раздел `Django Postgres Database Config` - настройки параметров базы данных
Раздел `Postgres container config` - переменные для Postgres Container

#### Команда для развертывания:
```
docker-compose up --build
```
Суперпользователь и данные, необходимые для работы системы, устанавливаются автоматически.