📊 Exchange Rate Scraper

A simple Python project that fetches real-time exchange rates using the ExchangeRate-API, sorts the currencies by value, and saves the results as CSV and Excel files.

This project can be used as a building block for:

Fintech dashboards

Currency converter tools

Market analysis scripts

Treasury reporting automation

✨ Features

✔ Fetch real-time exchange rates
✔ Sort currencies by rate descending
✔ Save results as .csv and .xlsx
✔ Auto-create output folder
✔ File name includes timestamp
✔ Overwrite protection (confirmation dialog)
✔ Simple GUI alerts using tkinter

🛠️ Tech Stack
Component	Tool
Language	Python 3
HTTP	requests
Data	pandas
Export	openpyxl
GUI	tkinter

📦 Installation
1️⃣ Clone the repo
git clone https://github.com/pouya-razavi21/exchange-rate-scraper.git

2️⃣ Install dependencies
pip install -r requirements.txt

▶️ Usage

Run the script:

python ./src/exchange_rate_scraper.py


Files will be saved in the exports/ folder, with a timestamped name.

🔑 API Setup

This project uses ExchangeRate-API.

Get your own API key here:
https://www.exchangerate-api.com/

Then open the script and replace:

api_key = "YOUR_API_KEY"

📂 Project Structure
exchange-rate-scraper
│── src/
│   └── exchange_rate_scraper.py
│── exports/
│── LICENSE
│── .gitignore
│── README.md
│── requirements.txt

🧪 Example Output

Example CSV:

Currency,Rate
KWD,3.259
BHD,2.652
OMR,2.600
GBP,1.249
EUR,1.082
...

🤝 Contributing

Pull Requests are welcome.
Please create a feature branch:

git checkout -b feature-name

🪪 License

This project is licensed under the MIT License.

⭐ Support

If you like this project, please give it a star ⭐ on GitHub!

🚀 About the Author

Built by Pouya Razavi, as a learning project for
Python + API + data automation.

🧭 Notes

This project can be extended with:

CLI flags

Logging

Exception handling

Currency converter UI

Docker packaging

Auto upload to Google Sheets

