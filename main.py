import logging, os
from aiogram import Bot, Dispatcher, executor
from utils import storage
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat

async def set_commands(bot, ADMIN_ID):
    # Menu cho user
    user_cmds = [
        BotCommand(command="start", description="Bắt đầu"),
        BotCommand(command="help", description="Hướng dẫn"),
        BotCommand(command="order", description="Đặt đơn hàng"),
        BotCommand(command="donhang", description="Xem đơn hàng"),
        BotCommand(command="sodu", description="Xem số dư"),
        BotCommand(command="naptien", description="Nạp tiền qua QR"),
    ]
    await bot.set_my_commands(user_cmds, scope=BotCommandScopeDefault())

    # Menu cho admin
    admin_cmds = user_cmds + [
        BotCommand(command="dsdonhang", description="Xem tất cả đơn"),
        BotCommand(command="duyet", description="Duyệt nạp tiền"),
        BotCommand(command="done", description="Hoàn thành đơn"),
        BotCommand(command="huy", description="Huỷ đơn hàng"),
    ]
    await bot.set_my_commands(admin_cmds, scope=BotCommandScopeChat(chat_id=ADMIN_ID))


API_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID  = int(os.getenv("ADMIN_ID")) if os.getenv("ADMIN_ID") else None
BANK_ID   = os.getenv("BANK_ID") or "mbbank"
ACCOUNT_NO = os.getenv("ACCOUNT_NO") or "1234567890"
ACCOUNT_NAME = os.getenv("ACCOUNT_NAME") or "Unknown"

if not API_TOKEN or not ADMIN_ID:
    raise RuntimeError("Thiếu BOT_TOKEN hoặc ADMIN_ID")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp  = Dispatcher(bot)

order_map = {}
pending_topup = {}

# ===== IMPORT COMMANDS =====
from commands.user import start, order, donhang, sodu, naptien
from commands.admin import dsdonhang, duyet, done, huy

# ===== REGISTER =====
huy.register(dp, ADMIN_ID, bot)
start.register(dp)
order.register(dp, ADMIN_ID, bot, order_map)
donhang.register(dp)
sodu.register(dp)
naptien.register(dp, ADMIN_ID, bot, pending_topup, BANK_ID, ACCOUNT_NO, ACCOUNT_NAME)

dsdonhang.register(dp, ADMIN_ID)
duyet.register(dp, ADMIN_ID, bot, pending_topup)
done.register(dp, ADMIN_ID, bot)

if __name__ == "__main__":
    storage.ensure_dirs()

    async def on_startup(dp):
        await set_commands(bot, ADMIN_ID)

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

