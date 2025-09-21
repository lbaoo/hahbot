import os, json, random, string
import uuid


DATA_DIR = "data"
BALANCE_FILE = os.path.join(DATA_DIR, "balances.json")
ORDERS_FILE = os.path.join(DATA_DIR, "orders.json")

def generate_id():
    """Tạo ID ngắn gọn, duy nhất cho đơn hàng"""
    return uuid.uuid4().hex[:8]  # ví dụ: a1b2c3d4

def ensure_dirs():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def read_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            try: return json.load(f)
            except: return {}
    return {}

def write_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ===== BALANCE =====
def get_balance(user_id: int) -> int:
    data = read_json(BALANCE_FILE)
    return int(data.get(str(user_id), 0))

def set_balance(user_id: int, new_balance: int) -> int:
    data = read_json(BALANCE_FILE)
    data[str(user_id)] = int(new_balance)
    write_json(BALANCE_FILE, data)
    return int(data[str(user_id)])

def add_balance(user_id: int, amount: int) -> int:
    return set_balance(user_id, get_balance(user_id) + int(amount))

# ===== ORDERS =====
def read_orders():
    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, "r", encoding="utf-8") as f:
            try: return json.load(f)
            except: return []
    return []

def write_orders(data):
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def add_order(user_id, product, quantity, address):
    orders = read_orders()
    orders.append({
        "user_id": user_id,
        "product": product,
        "quantity": quantity,
        "address": address
    })
    write_orders(orders)
def generate_order_id(length=6):
    return "ORD-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=length))

def add_order(user_id, product, quantity, address, link=None, phone=None):
    orders = read_orders()
    order_id = generate_id()
    orders.append({
        "id": order_id,
        "user_id": user_id,
        "link": link,
        "product": product,
        "quantity": quantity,
        "address": address,
        "phone": phone,
        "status": "pending"
    })
    write_orders(orders)
    return order_id

LOW_BALANCE_THRESHOLD = 20000  # ngưỡng cảnh báo

def check_low_balance(user_id, dp, bot):
    bal = get_balance(user_id)
    if bal < LOW_BALANCE_THRESHOLD:
        return bal
    return None
