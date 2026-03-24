import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests

# ========== КЛЮЧИ ==========
TOKEN = "7471651648:AAGQaorukNs7LvYSXMCS28rd9Mw26YccuHM"
DEEPSEEK_KEY = "sk-2fbd82195e0c4ede97eef4b4338e9715"

# ========== НАСТРОЙКА ==========
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def ask_deepseek(question):
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "Ты — koisskAI, дружелюбный и умный помощник. Отвечай кратко, по делу, с лёгким характером."},
            {"role": "user", "content": question}
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    try:
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            return f"Ошибка API: {response.status_code}"
            
    except Exception as e:
        return f"Ошибка: {e}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "koisskAI приветствует тебя.\n\n"
        "Задавай вопрос — я отвечу."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    await update.message.reply_text(f"🤔 {query}")
    
    answer = ask_deepseek(query)
    await update.message.reply_text(answer)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("koisskAI запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
