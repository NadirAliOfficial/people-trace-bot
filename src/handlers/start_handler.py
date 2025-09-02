# Placeholder for start handlers
from telegram import Update
from telegram.ext import ContextTypes

async def action_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass

async def choose_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass

async def city_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass

async def interrupt_current_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass

async def message_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass

async def select_lang_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass

async def choose_country(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass

async def country_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass

async def disclaimer_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass

async def start_choose_province(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass

async def start_province_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass