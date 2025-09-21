from aiogram import types
from utils.storage import read_orders, write_orders

def register(dp, ADMIN_ID, bot):
    @dp.message_handler(commands=["done"], user_id=[ADMIN_ID])
    async def cmd_done(message: types.Message):
        parts = message.text.split(maxsplit=2)
        if len(parts) < 2:
            await message.reply("❌ Sai cú pháp: /done <order_id> [nội dung]")
            return

        order_id = parts[1]
        note = parts[2] if len(parts) > 2 else "Đơn hàng của bạn đã hoàn thành."

        orders = read_orders()
        new_orders = []
        found = None

        # Tìm đơn hàng và xoá
        for o in orders:
            if o["id"] == order_id:
                found = o
            else:
                new_orders.append(o)

        if not found:
            await message.reply(f"❌ Không tìm thấy đơn {order_id}")
            return

        # Ghi lại data sau khi xoá đơn
        write_orders(new_orders)

        # Gửi thông báo cho user
        await bot.send_message(found["user_id"], f"✅ Đơn {order_id} đã hoàn thành!\n📌 {note}")

        # Báo lại admin
        await message.reply(f"✔️ Đã hoàn thành và xoá đơn {order_id} khỏi hệ thống.")
