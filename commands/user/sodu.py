from aiogram import types
from utils.storage import get_balance

def register(dp):
    @dp.message_handler(commands=["sodu"])
    async def cmd_sodu(message: types.Message):
        bal = get_balance(message.from_user.id)
        await message.reply(f"💰 Số dư của bạn: {bal} VND")

        # 🔔 Nhắc nạp nếu số dư thấp
        if bal < 20000:
            await message.reply(
                f"⚠️ Số dư của bạn còn thấp ({bal} VND).\n"
                f"👉 Dùng /naptien để nạp thêm."
            )
