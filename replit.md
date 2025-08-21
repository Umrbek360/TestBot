# Overview

This is a Telegram bot-based testing system built in Python that allows users to take multiple-choice tests across different subjects. The bot provides an interactive interface with inline keyboards for navigation and test-taking. Users can view their test history and account information, while the system manages questions, subjects, and user data through JSON file storage.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Bot Framework
- **Framework**: Python Telegram Bot (python-telegram-bot library)
- **Architecture Pattern**: Handler-based event-driven system using telegram.ext
- **Communication**: Webhook/polling-based message processing with callback query handlers

## Data Storage
- **Storage Method**: File-based JSON storage for simplicity and portability
- **User Data**: Stored in `users.json` with registration timestamps and test history
- **Question Data**: Stored in `questions.json` with subjects and question banks
- **Session Management**: In-memory storage for active test sessions using dictionaries

## Core Components

### UserManager Class
- Handles user registration, data persistence, and profile management
- Manages user test history and statistics
- Provides JSON file I/O operations with error handling

### TestManager Class  
- Manages question loading and test session lifecycle
- Handles subject categorization and question retrieval
- Maintains active test sessions in memory for real-time testing

### Bot Handlers Module
- Implements command and callback query handlers
- Provides inline keyboard navigation for user interactions
- Manages the conversation flow between menu states

## Message Flow Architecture
1. **Command Processing**: `/start` command initializes user and shows main menu
2. **Callback Routing**: Pattern-based callback query handlers route user interactions
3. **State Management**: Active test sessions tracked in memory with user progress
4. **Response Generation**: Dynamic inline keyboard generation based on context

## Localization
- **Language**: Uzbek language interface with Cyrillic script
- **Content**: All user-facing text and subject names localized

# External Dependencies

## Required Python Packages
- **python-telegram-bot**: Core Telegram Bot API wrapper for message handling and inline keyboards
- **Standard Library**: json, os, logging, datetime, typing for core functionality

## Telegram Bot API
- **Bot Token**: Required environment variable `TELEGRAM_BOT_TOKEN`
- **Update Types**: Handles both message and callback_query updates
- **Features Used**: Inline keyboards, callback queries, command handling

## File System Dependencies
- **questions.json**: Question bank storage with fallback to default content
- **users.json**: User data persistence with automatic file creation
- **Environment Variables**: Bot token configuration through environment variables

## Runtime Environment
- **Python 3.7+**: Required for async/await syntax and typing annotations
- **File Permissions**: Read/write access needed for JSON data files
- **Logging**: Standard Python logging for debugging and monitoring