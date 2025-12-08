# 📊 Exchange Rate Scraper

A Python script to fetch **real-time currency exchange rates** from the ExchangeRate-API, sort currencies by value, and export the result as **CSV** and **Excel**.

This project is ideal for:
- Financial dashboards
- Currency converter tools
- Market research automation
- Treasury reporting
- Data analysis learning exercises

---

## ✨ Features

✔ Fetch latest exchange rates (USD base)  
✔ Save results to `.csv` and `.xlsx`  
✔ Auto-create output folder  
✔ Timestamped filenames  
✔ Overwrite protection dialog  
✔ GUI notifications (tkinter)  
✔ Logging for debugging  
✔ Environment variable API key  

---

## 🛠 Tech Stack

| Component | Tool |
|----------|------|
| Language | Python 3 |
| HTTP     | requests |
| Data     | pandas |
| Export   | openpyxl |
| GUI      | tkinter |
| Logging  | logging |
| Env Vars | python-dotenv |

---

## 📦 Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/pouya-razavi21/exchange-rate-scraper.git
cd exchange-rate-scraper
2️⃣ Create virtual environment (recommended)
bash
Copy code
python -m venv venv
source venv/bin/activate     # Linux/Mac
venv\Scripts\activate        # Windows
3️⃣ Install dependencies
bash
Copy code
pip install -r requirements.txt
🔑 API Setup
This project requires an API key from:
➡ https://www.exchangerate-api.com/

Create a .env file in the project root:

env
Copy code
API_KEY=your_api_key_here
Or copy the example:

bash
Copy code
cp .env.example .env
▶️ Usage
Run the script:

bash
Copy code
python ./src/exchange_rate_scraper.py
Files will be created under:

java
Copy code
exports/
Example filename:

Copy code
exchange_rates_2025-12-08_14-30-02.xlsx
📂 Project Structure
arduino
Copy code
exchange-rate-scraper/
│── src/
│   └── exchange_rate_scraper.py
│── exports/            # auto-created output
│── .env.example
│── requirements.txt
│── README.md
│── LICENSE
│── .gitignore
🧪 Sample Output
Example rows sorted by rate:

python-repl
Copy code
Currency  Rate
KWD       3.2590
BHD       2.6520
OMR       2.6000
GBP       1.2490
EUR       1.0820
...
🧭 Notes & Limitations
Base currency is fixed to USD

API has call limits (free tier)

Requires internet access

No CLI flags yet

Future improvements:

CLI options (--base, --save-type)

UI application

Convert to Docker

Auto-upload to Google Sheets

🤝 Contributing
Pull Requests are welcome.

Create a feature branch:

bash
Copy code
git checkout -b feature-name
🪪 License
This project is licensed under the MIT License.

⭐ Support
If you like this project, give it a star ⭐ on GitHub.

👨‍💻 Author
Built by Pouya Razavi as a learning project for:
Python + API + Data Automation

