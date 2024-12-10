import os
import json
from telegram import Update
from telegram.ext import ContextTypes

from src.memory import Memory
from src.assistant import Assistant
from src.logger import logger

class Handlers:
    def __init__(self):
        self.botname = os.environ.get("TELEGRAM_BOT_NAME", "")
        self.memory_instance = Memory()
        self.assistant_instance = Assistant()

    def intro_message(self):
        return f"""Hi! I am a bot assistant.
When added to a group, I only respond to messages that start with my user name @{self.botname} or a /command.
Available commands are as follows:
    * /help to display this message again
        """

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        logger.info("\n\nStart command received from Chat ID %s", str(update.effective_chat.id))
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=self.intro_message(),
        )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        logger.info("\n\nHelp command received from Chat ID %s", str(update.effective_chat.id))
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=self.intro_message(),
        )

    async def reset_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        logger.info("\n\nReset command received from Chat ID %s", str(update.effective_chat.id))
        chat_id = str(update.effective_chat.id)
        self.memory_instance.reset_conversation(chat_id)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="The conversation has been reset.",
        )

    async def history_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        logger.info("\n\nHistory command received from Chat ID %s", str(update.effective_chat.id))
        chat_id = str(update.effective_chat.id)
        chat_history = self.memory_instance.get_chat_history(chat_id)
        chat_history_text = json.dumps(chat_history, indent=4)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=chat_history_text,
        )

    async def any_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            logger.info("\n\nChat message received from Chat ID %s", str(update.effective_chat.id))
            chat_id = str(update.effective_chat.id)
            sender_id = str(update.effective_user.id)
            input = update.message.text
            # Check if the message starts with the bot name (if in a group)
            if int(chat_id) < 0 and not input.startswith("@" + self.botname):
                return
            input = input.replace("@" + self.botname, "").strip()
            # Get chat history
            chat_history = self.memory_instance.get_chat_history(chat_id)
            logger.info("Chat history: %s", chat_history)
            # Log user message
            self.memory_instance.log_message(
                chat_id=chat_id,
                sender_id=sender_id,
                sender_type="user",
                message=input,
                history=chat_history,
            )
            logger.info("Input: %s", input)
            assistant_response = await self.assistant_instance.run_assistant(
                chat_id=chat_id,
                message=input,
                history=chat_history,
            )
            # Log assistant response
            chat_history.append(
                {
                    "role": "user",
                    "content": input,
                }
            )
            if assistant_response != "Error, the conversation has been reset.":
                self.memory_instance.log_message(
                    chat_id=chat_id,
                    sender_id=sender_id,
                    sender_type="assistant",
                    message=assistant_response,
                    history=chat_history,
                )
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=assistant_response,
            )
        except Exception as e:
            logger.error("Error in any_message", e)
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="The bot encountered an error, please try again.",
            )
            logger.info("Resetting thread.")
            self.memory_instance.reset_conversation(chat_id)
