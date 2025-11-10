# 🎓 Student Assistant Bot

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Telegram Bot](https://img.shields.io/badge/Telegram%20Bot-Telebot-green)

A simple **Telegram bot** built with `pyTelegramBotAPI` that helps students **manage tasks**, **calculate GPA**, and stay organized — all through chat.

---

## 🚀 Features

### 🗂 Task Management
- `/addtask <task>` → Add a new task  
- `/viewtasks` → View your to-do list  
- `/marktask <task number>` → Mark a task as complete ✅  
- `/removetask <task number>` → Remove a task  
- `/cleartasks` → Clear all tasks  

### 🎓 GPA Calculator
- `/gpa <current_GPA> <current_credits> <course_credits> <course_mark>`  
  → Calculates updated GPA based on your new course grade  

### 💬 Info Commands
- `/start` → Welcome message & command list  
- `/about` → Learn about the bot
- 
Each user has their own separate task list (stored in memory).
