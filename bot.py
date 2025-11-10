import os
import sys
import telebot

# Load the Telegram bot token from environment variables
token = os.getenv("TELEGRAM_TOKEN")
if not token:
    print("ERROR: TELEGRAM_TOKEN environment variable not set. Export it and restart.")
    sys.exit(1)

bot = telebot.TeleBot(token)

# In-memory storage for user tasks
user_tasks = {}

def get_tasks(chat_id):
    if chat_id not in user_tasks:
        user_tasks[chat_id] = []
    return user_tasks[chat_id]

# Decorator to pass tasks to handlers
def with_tasks(func):
    def wrapper(message):
        chat_id = message.chat.id
        tasks = get_tasks(chat_id)
        return func(message, chat_id, tasks)
    return wrapper

## Handlers and bot logic
# @ -> annotation for decorator

# Welcome message handler
@bot.message_handler(commands=['start'])
def welcome_message(message):
    bot.send_message(message.chat.id, "Hi there! I'm your Student Assistant Bot.\n"
                                 "Here's what I can do:\n\n"
                                 "- /addtask <task> - Add a task to your To Do list\n"
                                 "- /viewtasks - Display your To Do list\n"
                                 "- /marktask <task number> - Mark a task as complete\n"
                                 "- /removetask <task number> - Remove a task from your To Do list\n"
                                 "- /cleartasks - Clear all tasks from your To Do list\n"
                                 "- /gpa <current_GPA> <current_credits> <course_credits> <course_mark> - Calculate your GPA\n\n"
                                 "- /about - Learn more about this bot\n"
                                 "How can I assist you today?")


# Add task handler
@bot.message_handler(commands=['addtask'])
@with_tasks
def add_task(message, chat_id, tasks):
    task = message.text.replace('/addtask', '', 1).strip()
    if task == '':
        bot.reply_to(message, "Task cannot be empty.")
    elif task in tasks:
        bot.reply_to(message, "Task already exists.")
    else:
        tasks.append(task)
        bot.send_message(chat_id, f"Task [{task}] added to your To-Do List.")


# View tasks handler
@bot.message_handler(commands=['viewtasks'])
@with_tasks
def view_tasks(message, chat_id, tasks):
    if tasks:
        formatted = "\n".join(f"{i+1}. {t}" for i, t in enumerate(tasks))
        bot.send_message(chat_id, f"Your tasks are:\n{formatted}")
    else:
        bot.reply_to(message, "Your To-Do List is empty.")


# Mark task as complete handler
@bot.message_handler(commands=['marktask'])
@with_tasks
def mark_task(message, chat_id, tasks):
    try:
        task_no = int(message.text.replace('/marktask', '', 1).strip())
        if task_no < 1 or task_no > len(tasks):
            bot.reply_to(message, "Invalid task number.")
            return
        if not tasks[task_no - 1].endswith(" ✅"):
            tasks[task_no - 1] += " ✅"
        bot.send_message(chat_id, f"Task {tasks[task_no - 1]} marked as complete.")
    except ValueError:
        bot.reply_to(message, "Please provide a valid number: /marktask <task number>")


# Remove task handler
@bot.message_handler(commands=['removetask'])
@with_tasks
def remove_task(message, chat_id, tasks):
    try:
        task_no = int(message.text.replace('/removetask', '', 1).strip())
        if task_no < 1 or task_no > len(tasks):
            bot.reply_to(message, "Invalid task number.")
            return
        removed = tasks.pop(task_no - 1)
        bot.send_message(chat_id, f"Task [{removed}] removed from your To-Do List.")
    except ValueError:
        bot.reply_to(message, "Please provide a valid number: /removetask <task number>")


# Clear tasks handler
@bot.message_handler(commands=['cleartasks'])
@with_tasks
def clear_tasks(message, chat_id, tasks):
    tasks.clear()
    bot.send_message(chat_id, "All tasks cleared from your To-Do List.")


# GPA calculation handler
# /gpa <current_GPA> <current_credits> <course_credits> <course_mark>
@bot.message_handler(commands=['gpa'])
def calculate_gpa(message):
    try:
        params = message.text.replace('/gpa', '', 1).strip().split()
        current_gpa = float(params[0])
        current_credits = float(params[1])
        course_credits = float(params[2])
        course_mark = float(params[3])

        new_points = course_credits * (course_mark / 20)
        total_points = (current_gpa * current_credits) + new_points
        total_credits = current_credits + course_credits
        new_gpa = total_points / total_credits

        bot.send_message(message.chat.id, f"Your new GPA is: {new_gpa:.2f}")
    except (IndexError, ValueError):
        bot.reply_to(
            message,
            "Please provide valid parameters: /gpa <current_GPA> <current_credits> <course_credits> <course_mark>"
        )

# About bot handler
@bot.message_handler(commands=['about'])
def about_bot(message):
    bot.send_message(message.chat.id, "I'm a Student Assistant Bot designed to help you manage your tasks and calculate your GPA. "
                                 "Feel free to use the commands to organize your studies!")


# make the bot always run
bot.polling()


    


