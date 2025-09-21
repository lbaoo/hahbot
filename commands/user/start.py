from aiogram import types

HELP_TEXT = (
    "📖 Danh sách lệnh:\n\n"
    "👤 Người dùng:\n"
    "• /order     → Đặt đơn hàng\n"
    "• /naptien   → Nạp tiền \n"
    "• /sodu      → Kiểm tra số dư\n"
    "• /donhang   → Xem đơn hàng của bạn\n"
    "• /help      → Xem danh sách lệnh\n"
)

def register(dp):
    @dp.message_handler(commands=["start"])
    async def cmd_start(message: types.Message):
        await message.reply("Chào bạn 👋\n\n" + HELP_TEXT)

    @dp.message_handler(commands=["help"])
    async def cmd_help(message: types.Message):
        await message.reply(HELP_TEXT)
