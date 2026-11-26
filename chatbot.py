import os
import json
import csv
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load API key securely from .env file
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

INVENTORY_FILE = "inventory.json"
ORDERS_FILE = "orders.csv"

default_inventory = {
    "lawn_suit": {"name": "Embroidered Lawn Suit (3-Piece)", "price": 4500, "stock": 5},
    "cotton_kurti": {"name": "Cotton Printed Kurti", "price": 2200, "stock": 8},
    "chiffon_dupatta": {"name": "Chiffon Festive Dupatta", "price": 1800, "stock": 2},
    "mens_suit": {"name": "Men's Wash & Wear Suit", "price": 3800, "stock": 0}
}

def load_inventory():
    if not os.path.exists(INVENTORY_FILE):
        with open(INVENTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(default_inventory, f, indent=4)
    with open(INVENTORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_inventory(inv_data):
    with open(INVENTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(inv_data, f, indent=4)

def save_order(name, phone, address, item_name, qty, total_bill):
    file_exists = os.path.isfile(ORDERS_FILE)
    with open(ORDERS_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Date & Time", "Customer Name", "Phone", "Address", "Item", "Quantity", "Total Bill (PKR)"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), name, phone, address, item_name, qty, total_bill])

def get_live_stock_text():
    inv = load_inventory()
    lines = []
    for key, item in inv.items():
        status = f"{item['stock']} pieces available" if item['stock'] > 0 else "OUT OF STOCK (0 available)"
        lines.append(f"- ID: '{key}' | Name: {item['name']} | Price: Rs. {item['price']} | Stock: {status}")
    return "\n".join(lines)

def create_chat_session():
    live_stock = get_live_stock_text()
    system_instruction = f"""
    You are 'Huma', an intelligent E-Commerce Sales & Inventory Assistant for an online store in Pakistan.

    LIVE STORE INVENTORY (Real-time stock):
    {live_stock}

    Store Rules:
    - Delivery charges: Rs. 250 all over Pakistan (Free delivery on orders above Rs. 5,000).
    - Payment: Cash on Delivery (COD) only.

    Your Responsibilities:
    1. Reply politely in Roman Urdu or English (matching the customer's language).
    2. Check the LIVE STORE INVENTORY before taking an order. If an item is OUT OF STOCK or the customer asks for more quantity than available stock, politely refuse and tell them how many pieces are left.
    3. To confirm an order, collect:
       - Exact Item ID & Quantity
       - Customer Full Name
       - Phone Number
       - Full Delivery Address & City
    4. CRITICAL SYSTEM COMMAND: When the customer confirms the order with all details, add this EXACT hidden line at the very end of your message so our database updates stock automatically:
       EXECUTE_ORDER | item_id: [ID] | qty: [number] | name: [Customer Name] | phone: [Phone] | address: [Address] | total: [Total Amount]
    """
    return client.chats.create(
        model="gemini-3.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.4,
        )
    )

chat = create_chat_session()

print("🛒 Smart E-Commerce & Auto-Inventory Chatbot is LIVE!")
print("💡 Tip: 'stock' likh kar aap kisi bhi waqt live inventory check kar sakti hain. Band karne ke liye 'exit' likhein.\n")

response = chat.send_message("Customer ne chat kholi hai. Salam karein aur batayein ke aap unki shopping mein kya madad kar sakti hain?")
print(f"Huma(chatBot): {response.text}\n")

while True:
    user_input = input("Customer: ")

    if user_input.lower() in ['exit', 'quit', 'bye']:
        print("Huma(chatBot): Allah Hafiz! Hamare store par aane ka shukriya.")
        break

    if user_input.lower() == 'stock':
        print("\n📊 --- LIVE INVENTORY STATUS ---")
        print(get_live_stock_text())
        print("--------------------------------\n")
        continue

    if not user_input.strip():
        continue

    try:
        response = chat.send_message(user_input)
        bot_reply = response.text

        if "EXECUTE_ORDER" in bot_reply:
            lines = bot_reply.split("\n")
            for line in lines:
                if "EXECUTE_ORDER" in line:
                    parts = [p.strip() for p in line.split("|")]
                    data = {}
                    for p in parts[1:]:
                        if ":" in p:
                            k, v = p.split(":", 1)
                            data[k.strip()] = v.strip()

                    item_id = data.get("item_id")
                    qty = int(data.get("qty", 1))
                    cust_name = data.get("name", "Unknown")
                    phone = data.get("phone", "Unknown")
                    address = data.get("address", "Unknown")
                    total = data.get("total", "0")

                    inv = load_inventory()
                    if item_id in inv and inv[item_id]["stock"] >= qty:
                        inv[item_id]["stock"] -= qty
                        save_inventory(inv)
                        save_order(cust_name, phone, address, inv[item_id]["name"], qty, total)

                        bot_reply = bot_reply.replace(line, "").strip()
                        print(f"\nHuma (chatBot): {bot_reply}")
                        print(f"\n✅ [AUTO-SYSTEM]: Order 'orders.csv' mein save ho gaya!")
                        print(f"📉 [INVENTORY UPDATED]: '{inv[item_id]['name']}' ka naya stock ab {inv[item_id]['stock']} reh gaya hai!\n")

                        chat = create_chat_session()
                    else:
                        print("\n⚠️ [SYSTEM ERROR]: Stock kam hone ki wajah se order process nahi ho saka.\n")
        else:
            print(f"\nHuma(chatBot): {bot_reply}\n")

    except Exception as e:
        print(f"Error: {e}\n")
