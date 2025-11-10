import telebot

token = '8229510751:AAFVPpjZKkGLG_ytVBIZBJijZJPikwcdXQo'

bot = telebot.TeleBot(token)

tasks = []

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
                                 "Let's get started!")


# Add task handler
@bot.message_handler(commands=['addtask'])
def add_task(message):
    task = message.text.replace('/addtask', '').strip()

    if task not in tasks and task != '':
        tasks.append(task)
        bot.send_message(message.chat.id,f"Task [{task}] added to your To-Do List.")
    else:
        bot.reply_to(message, "Task already exists or is empty.")        


# View tasks handler
@bot.message_handler(commands=['viewtasks'])
def view_tasks(message):
    formatted_message = ""

    if len(tasks) != 0:
        for task in tasks:
            formatted_message += f"{tasks.index(task)+1}. {task}\n"

        bot.send_message(message.chat.id, f"Your tasks are:\n{formatted_message}")
    else:
        bot.reply_to(message, "Your To-Do List is empty.")


# Mark task as complete handler
@bot.message_handler(commands=['marktask'])
def mark_task(message):
    task_no = int(message.text.replace('/marktask', '').strip())
    tasks[task_no - 1] += " ✅"
    bot.send_message(message.chat.id, f"Task {tasks[task_no - 1]} marked as complete.")
   

# Remove task handler
@bot.message_handler(commands=['removetask'])
def remove_task(message):
    task = message.text.replace('/removetask', '').strip()

    if task in tasks:
        tasks.remove(task)
        bot.send_message(message.chat.id, f"Task [{task}] removed from your To-Do List.")
    else:
        bot.reply_to(message, "Task is not in your To-Do List!")


# make the bot always run
bot.polling()


    


