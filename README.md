<img src="https://github.com/ICQ-BOTS/paint_text_bot/blob/main/paint_text.png" width="100" height="100">


# Рукописные конспекты

[Рукописные конспекты](https://icq.im/text_bot)

Старт:
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
