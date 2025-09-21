from aiogram import types
from utils import storage

def register(dp, ADMIN_ID):
    @dp.message_handler(commands=["dsdonhang"], user_id=[ADMIN_ID])
    async def cmd_dsdonhang(message: types.Message):
        orders = storage.read_orders()

        if not orders:
            await message.reply("📭 Hiện chưa có đơn hàng nào.")
            return

        text = "📦 Danh sách đơn hàng:\n\n"
        for o in orders:
            text += (
                f"🔖 ID: `{o.get('id','N/A')}`\n"
                f"• User ID: {o['user_id']}\n"
                f"• Link: {o.get('link','N/A')}\n"
                f"• Sản phẩm: {o['product']}\n"
                f"• SL: {o['quantity']}\n"
                f"• Địa chỉ: {o['address']}\n"
                f"• SĐT: {o.get('phone','N/A')}\n"
                f"• Trạng thái: {o.get('status','pending')}\n\n"
            )

        if len(text) > 4000:
            file_path = "all_orders.txt"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(text)
            await message.reply_document(open(file_path, "rb"))
        else:
            await message.reply(text, parse_mode="Markdown")
