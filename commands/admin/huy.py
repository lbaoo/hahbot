from aiogram import types
from utils import storage

FEE = 13000  # phí bị trừ khi đặt đơn

def register(dp, ADMIN_ID, bot):
    @dp.message_handler(commands=["huy"], user_id=[ADMIN_ID])
    async def cmd_huy(message: types.Message):
        parts = message.text.split()
        if len(parts) < 2:
            await message.reply("❌ Dùng cú pháp: /huy <id>")
            return

        order_id = parts[1]
        orders = storage.read_orders()
        target = None

        for o in orders:
            if str(o.get("id")) == order_id:
                target = o
                break

        if not target:
            await message.reply(f"⚠️ Không tìm thấy đơn hàng với ID `{order_id}`", parse_mode="Markdown")
            return

        # Hoàn trả tiền
        uid = int(target["user_id"])
        new_balance = storage.add_balance(uid, FEE)

        # Xoá đơn
        new_orders = [o for o in orders if str(o.get("id")) != order_id]
        storage.write_orders(new_orders)

        # Thông báo cho khách
        try:
            await bot.send_message(
                uid,
                f"❌ Đơn hàng của bạn với ID `{order_id}` đã bị huỷ.\n"
                f"💰 Số tiền {FEE} VND đã được hoàn lại.\n"
                f"👉 Số dư hiện tại: {new_balance} VND",
                parse_mode="Markdown"
            )
        except:
            pass

        # Thông báo cho admin
        await message.reply(
            f"✔️ Đã huỷ đơn `{order_id}` và hoàn {FEE} VND cho user {uid}. "
            f"Số dư mới: {new_balance} VND",
            parse_mode="Markdown"
        )
