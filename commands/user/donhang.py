from aiogram import types
from utils import storage

def register(dp):
    @dp.message_handler(commands=["donhang"])
    async def cmd_donhang(message: types.Message):
        user_id = message.from_user.id
        orders = storage.read_orders()

        my_orders = [o for o in orders if str(o.get("user_id")) == str(user_id)]

        if not my_orders:
            await message.reply("📭 Bạn chưa có đơn hàng nào.")
            return

        text = "🧾 Danh sách đơn hàng của bạn:\n\n"
        for order in my_orders:
            text += (
                f"🔖 ID: `{order.get('id', 'N/A')}`\n"
                f"• Link: {order.get('link', 'N/A')}\n"
                f"• Sản phẩm: {order['product']}\n"
                f"• SL: {order['quantity']}\n"
                f"• Địa chỉ: {order['address']}\n"
                f"• SĐT: {order.get('phone', 'N/A')}\n"
                f"• Trạng thái: {order.get('status','pending')}\n\n"
            )

        await message.reply(text, parse_mode="Markdown")

        # 🔔 Nhắc nạp nếu số dư thấp
        low = storage.get_balance(user_id)
        if low < 20000:
            await message.reply(
                f"⚠️ Số dư của bạn còn thấp ({low} VND).\n"
                f"👉 Dùng /naptien để nạp thêm."
            )
