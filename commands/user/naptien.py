from aiogram import types
import aiohttp

async def fetch_qr(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                return await resp.read()
            return None

def register(dp, ADMIN_ID, bot, pending_topup, BANK_ID, ACCOUNT_NO, ACCOUNT_NAME):
    @dp.message_handler(commands=["naptien"])
    async def cmd_naptien(message: types.Message):
        parts = message.text.split()
        if len(parts) != 2 or not parts[1].isdigit():
            await message.reply("❌ Sai cú pháp! /naptien SOTIEN")
            return

        amount = int(parts[1])
        uid = message.from_user.id

        # Tạo URL QR
        qr_url = (
            f"https://img.vietqr.io/image/{BANK_ID}-{ACCOUNT_NO}-compact2.png"
            f"?amount={amount}&addInfo={uid}&accountName={ACCOUNT_NAME.replace(' ', '')}"
        )

        # Lấy ảnh QR về dạng bytes
        img_bytes = await fetch_qr(qr_url)

        if img_bytes:
            await message.reply_photo(
                photo=img_bytes,
                caption=(
                    f"💳 Quét QR để nạp {amount} VND\n"
                    f"• Ngân hàng: {BANK_ID.upper()}\n"
                    f"• Số TK: {ACCOUNT_NO}\n"
                    f"• Chủ TK: {ACCOUNT_NAME}\n"
                    f"• Nội dung CK: {uid}"
                )
            )
        else:
            await message.reply(f"❌ Không tải được QR, bạn mở trực tiếp link: {qr_url}")

        # Báo admin
        who = f"@{message.from_user.username}" if message.from_user.username else f"{message.from_user.full_name} (ID: {uid})"
        admin_msg = await bot.send_message(
            ADMIN_ID,
            f"💰 Yêu cầu nạp tiền từ {who}\n"
            f"• Số tiền: {amount}\n"
            f"• Nội dung CK: {uid}\n\n👉 Reply tin này và gõ /duyet"
        )
        pending_topup[admin_msg.message_id] = (uid, amount)
