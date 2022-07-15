# Обрезка ссылок с помощью Битли

Проект позволяющий сокращать ссылки при помощи [bitly](https://dev.bitly.com) 

### Как установить

Для работы проекту нужен токен. Для его получения нужно зарегистрироваться на [официальном сайте](https://bitly.com/pages/pricing), 
затем в настройках получить токен и положить его в env файл.
Пример .env файла:
```
BITLY-TOKEN=ваш токен
```
Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

### Пример запуска кода
```
python main.py ваша ссылка/уже сокращенная ссылка
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).


# Bitly url shorterer

A project that allows you to shorten links using [bitly](https://dev.bitly.com) 

### How to install

The project needs a token to work. To get it, you need to register on the [official website] (https://bitly.com/pages/pricing), 
then get a token in the settings and put it in the env file.
.env file exemple:
```
BITLY-TOKEN=your token
```
Python3 should be already installed. 
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

### Code run exemple
```
python main.py your link/your shorted link
```

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
