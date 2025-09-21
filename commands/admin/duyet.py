from aiogram import types
from utils.storage import add_balance

def register(dp, ADMIN_ID, bot, pending_topup):
    @dp.message_handler(commands=["duyet"], user_id=[ADMIN_ID])
    async def cmd_duyet(message: types.Message):
        if message.reply_to_message:
            key = message.reply_to_message.message_id
            if key in pending_topup:
                uid, amount = pending_topup.pop(key)
                new_bal = add_balance(uid, amount)
                await bot.send_message(uid, f"✅ Nạp {amount} VND thành công!\n💰 Số dư: {new_bal}")
                await message.reply(f"✔️ Đã cộng {amount} VND cho user {uid}. Số dư mới: {new_bal}")
                return
            else:
                await message.reply("⚠️ Tin không hợp lệ hoặc đã duyệt trước đó.")
                return

        parts = message.text.split()
        if len(parts) == 3 and parts[1].isdigit() and parts[2].isdigit():
            uid = int(parts[1]); amount = int(parts[2])
            new_bal = add_balance(uid, amount)
            await bot.send_message(uid, f"✅ Nạp {amount} VND thành công!\n💰 Số dư: {new_bal}")
            await message.reply(f"✔️ Đã cộng {amount} VND cho user {uid}. Số dư mới: {new_bal}")
        else:
            await message.reply("❗ /duyet <user_id> <amount> hoặc reply tin yêu cầu nạp")
