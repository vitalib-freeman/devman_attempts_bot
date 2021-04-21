# Devman attempts telegram bot

This is an application that notifies you about checked devman attempts.

## Installation
```bash
git clone git@github.com:vitalib-freeman/devman_attempts_bot.git
cd devman_attempts_bot
python -m .venv venv
source venv/bin/activate
python -m pip install -r requirements.txt 
```

Add credentials to .env file
```
echo 'DEVMAN_API_TOKEN=your_value' >> .env
echo 'TELEGRAM_BOT_TOKEN=your_value' >> .env
echo 'TELEGRAM_CHAT_ID=your_value' >> .env
```


```bash
python main.py
```

## License
[MIT](https://choosealicense.com/licenses/mit/)