from aiogram import types
from utils.storage import get_balance, add_balance, add_order

FEE = 13000

def register(dp, ADMIN_ID, bot, order_map):
    @dp.message_handler(commands=["order"])
    async def cmd_order(message: types.Message):
        try:
            data = message.text.replace("/order", "", 1).strip().split("|")
            link, product, quantity, address, phone = [d.strip() for d in data]
        except Exception:
            await message.reply(
                "❌ Sai cú pháp!\n"
                "Dùng:\n/order LinkSP | TênSP | SL | Địa chỉ | SĐT"
            )
            return

        user_id = message.from_user.id
        bal = get_balance(user_id)

        # kiểm tra số dư
        if bal < FEE:
            await message.reply(f"❌ Số dư không đủ ({bal} VND). Vui lòng /naptien.")
            return

        # trừ tiền
        new_bal = add_balance(user_id, -FEE)
        order_id = add_order(user_id, product, quantity, address, link=link, phone=phone)

        # trả lời khách
        await message.reply(
            f"✅ Đơn hàng **{order_id}** đã ghi nhận (trừ {FEE} VND).\n"
            f"• Link: {link}\n"
            f"• Tên SP: {product}\n"
            f"• Số lượng: {quantity}\n"
            f"• Địa chỉ: {address}\n"
            f"• SĐT: {phone}\n"
            f"💰 Số dư còn lại: {new_bal} VND",
            parse_mode="Markdown"
        )

        # 🔔 Nhắc nạp thêm nếu số dư thấp
        if new_bal < 20000:
            await message.reply(
                f"⚠️ Số dư của bạn còn thấp ({new_bal} VND).\n"
                f"👉 Dùng /naptien để nạp thêm."
            )

        # nhận diện khách
        who = f"@{message.from_user.username}" if message.from_user.username else f"{message.from_user.full_name} (ID: {user_id})"

        # gửi cho admin
        admin_msg = await bot.send_message(
            ADMIN_ID,
            f"📦 Đơn mới {order_id} từ {who}\n"
            f"• Link: {link}\n"
            f"• SP: {product} | SL: {quantity}\n"
            f"• Địa chỉ: {address}\n"
            f"• SĐT: {phone}\n"
            f"💰 Số dư: {new_bal}"
        )

        order_map[admin_msg.message_id] = user_id
