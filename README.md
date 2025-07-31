> [!NOTE]
> This code was written many years ago for fun and can be not very good optimised (or written).
> 
> However, it is still can serve as PoC

# ✂️ Inline Rock-Paper-Scissors

Inline "Rock-Paper-Scissors" game for Telegram bot using inline buttons. Play directly in any chat.

## 🚀 Installation & Run

1. Install dependencies:
   ```bash
   pip install pyTelegramBotAPI
   ```

2. Clone the repository:
   ```bash
   git clone https://github.com/tizhproger/inline_rps.git
   cd inline_rps
   ```

3. Set your bot token in `inline_rps.py`:
   ```python
   API_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
   ```

4. Run the bot:
   ```bash
   python inline_rps.py
   ```

## 🧠 Usage

- In any Telegram chat, type `@YourBotUsername` in message field, select the "`Rock, paper, scissors`"
- First player makes a move, second responds
- Bot displays the result and winner
