
# [Рукописные конспекты](https://icq.im/text_bot)

<a href="https://icq.im/text_bot"><img src="https://github.com/ICQ-BOTS/paint_text_bot/blob/main/paint_text.png" width="100" height="100"></a>

# Оглавление 
 - [Описание](https://github.com/ICQ-BOTS/paint_text_bot#описание)
 - [Установка](https://github.com/ICQ-BOTS/paint_text_bot#установка)
 - [Скриншоты работы](https://github.com/ICQ-BOTS/paint_text_bot#скриншоты-работы)

# Описание
Это твое одеяло. Я буду напоминать тебе каждый день, как я по тебе скучаю.

# Установка

1. Установка всех зависимостей 
```bash
pip3 install -r requirements.txt
```

2. Запуск space tarantool.
```bash
tarantoolctl start paint_text.lua
```
> Файл из папки scheme нужно перекинуть в /etc/tarantool/instances.available

3. Вставляем токен в paint_text_bot.py 

4. Запуск бота!
```bash
python3 paint_text_bot.py
```

# Скриншоты работы
<img src="https://github.com/ICQ-BOTS/paint_text_bot/blob/main/img/1.png" width="400">
<img src="https://github.com/ICQ-BOTS/paint_text_bot/blob/main/img/2.png" width="400">