# Telegram Weather Bot (Chelyabinsk)

Бот показывает прогноз погоды (сегодня и завтра) для Челябинска. Источник — Open‑Meteo (без ключа API).

## Возможности
- Команды: `/start`, `/today [город]`, `/tomorrow [город]`, `/weather <город>`
- Эмодзи и описание погоды на русском
- Локальная таймзона `Asia/Yekaterinburg`

## Подготовка
1. Установите Python 3.10+.
2. Скопируйте `env.example` в `.env` и вставьте токен бота.
3. Установите зависимости:
```bash
pip install -r requirements.txt
```

## Запуск локально (Windows)
```bash
copy env.example .env
python -m src.bot
```

Либо используйте `run.bat`:
```bat
@echo off
if not exist .env copy env.example .env >nul
python -m src.bot
```

## Raspberry Pi 3 (Raspberry Pi OS)
```bash
sudo apt update && sudo apt install -y python3 python3-pip python3-venv
cd ~/weather_bot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp env.example .env
# Отредактируйте .env и вставьте TELEGRAM_BOT_TOKEN
python -m src.bot
```

### systemd сервис (опционально)
Создайте `/etc/systemd/system/weather-bot.service`:
```ini
[Unit]
Description=Telegram Weather Bot (Chelyabinsk)
After=network.target

[Service]
WorkingDirectory=/home/pi/weather_bot
Environment=PYTHONUNBUFFERED=1
ExecStart=/home/pi/weather_bot/.venv/bin/python -m src.bot
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now weather-bot
journalctl -u weather-bot -f
```

## Примечания
- Источник данных: `https://open-meteo.com/`
- Координаты Челябинска: 55.1644, 61.4368
- Таймзона: Asia/Yekaterinburg


