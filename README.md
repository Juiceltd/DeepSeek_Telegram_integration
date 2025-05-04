# 🤖 DeepSeek Telegram Integration

This project connects the [DeepSeek LLM](https://deepseek.com/) with Telegram, allowing users to interact with the language model via a Telegram bot interface. It also generates HTML pages based on user queries and saves them to a specified directory on your server.

---

## 🚀 Features

- Integration with the DeepSeek API
- Telegram bot with user interaction
- HTML content generation
- Dockerized for easy deployment
- Environment-variable-based configuration

---

## 📦 Project Structure


```text
DeepSeek_Telegram_integration/
├── info/                  # List of registered users (JSON), System instruction for the LLM
├── pages/                 # Generated HTML files
├── .env
├── API_deepseek.py        # DeepSeek API wrapper
├── HTML_generate.py       # HTML content generation logic
├── main.py                # Telegram bot entry point
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```


---

## ⚙️ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Juiceltd/DeepSeek_Telegram_integration.git
cd DeepSeek_Telegram_integration
```
### 2. Create a .env file

Copy the example and fill in your actual values:
```bash
cp .env.example .env
```

Edit .env:
```env
telegram_token="YOUR TELEGRAM BOT TOKEN"
deepseek_api_key="YOUR DEEPSEEK API KEY"
admin="YOUR TELEGRAM USER ID"
url="YOUR PUBLICLY ACCESSIBLE URL"
OPEN_CLOUD_PATH=/var/www/yourdomain.com
```
⚠️ Make sure the OPEN_CLOUD_PATH directory exists and is writable by Docker.

### 3. Run with Docker Compose

```bash
docker-compose up --build
```

The bot should now be running and responding to Telegram messages.

## 📄 Environment Variables Reference

| Variable          | Description                                 |
|-------------------|---------------------------------------------|
| `telegram_token`  | Your Telegram bot token                     |
| `deepseek_api_key`| API key for DeepSeek                        |
| `admin`           | Your Telegram user ID (for admin access)    |
| `url`             | The public URL to access generated HTML     |
| `OPEN_CLOUD_PATH` | Absolute path to store generated HTML       |


## 📌 TODO

* Store context in a database