# 🛍️ Huma - Smart E-Commerce AI Assistant

**Huma** is an intelligent, 24/7 customer support and order management chatbot built using **Python** and the **Google Gemini API**. Designed specifically for online stores, it communicates seamlessly in both **English** and **Roman Urdu**, handles customer inquiries, checks live inventory, calculates bills, and automates order logging.

---

## ✨ Key Features

* **Bilingual Support:** Understands and replies naturally in both **English** and **Roman Urdu**.
* **Real-Time Inventory Check:** Reads live stock data from `inventory.json` before confirming any product availability.
* **Automated Order Processing:** Calculates the total bill, confirms customer orders, and automatically deducts purchased quantities from `inventory.json`.
* **Automatic Record Keeping:** Saves every confirmed order, customer details, and billing summary into `orders.csv`.
* **24/7 Availability:** Reduces manual workload for e-commerce store owners by handling repetitive customer queries and order placements.

---

## 🎥 Demo Video



https://github.com/user-attachments/assets/969c582d-eb14-434e-9efc-f46e672f6d32



---

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **AI Model:** Google Gemini API (`google-genai`)
* **Data Storage:** JSON (`inventory.json`) & CSV (`orders.csv`)

---

## 📂 Project Structure

```text
ai-chatbot/
├── chatbot.py           # Main chatbot application script
├── inventory.json       # Stores product names, prices, and live stock quantities
├── orders.csv           # Logs all confirmed customer orders and total bills
├── requirements.txt     # Required Python dependencies
├── .env.example         # Template for environment variables
└── README.md            # Project documentation
```

---

## 🚀 How to Run Locally

Follow these steps to set up and run the project on your machine:

### 1. Clone the Repository
```bash
git clone https://github.com
cd ai-chatbot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Your API Key
1. Create a `.env` file in the `ai-chatbot` directory.
2. Add your Google Gemini API key inside it:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

### 4. Run the Chatbot
```bash
python chatbot.py
```

---

## 💡 Example Workflow

1. **Customer:** *"Embroidered Lawn Suit available hai?"*
2. **Huma:** Checks `inventory.json` and replies with price and available stock (e.g., *5 pieces available*).
3. **Customer:** *"Mujhe 2 suits order karne hain."*
4. **Huma:** Confirms the order, calculates the total bill, updates `inventory.json` from `5` to `3`, and saves the order in `orders.csv`.

---

## 🤝 Contributing & Contact

Feel free to fork this repository, open issues, or submit pull requests to improve **Huma**. 

* **LinkedIn:** [Humaira A.](https://www.linkedin.com/in/humaira-a-282112404/)
* **GitHub:** [humairaameen07-07](https://github.com)
