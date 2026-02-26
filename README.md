## 📰 Telegram News Category Predictor Bot
A Telegram bot that scrapes Armenian news articles, processes them using Natural Language Processing (NLP), and predicts their category using a Random Forest machine learning model.

The system integrates web scraping, text preprocessing, model inference, and Telegram bot communication into a complete end-to-end pipeline.

### 🚀 Features
- Automated news scraping using `requests` and `BeautifulSoup`
- NLP preprocessing (text cleaning, TF-IDF vectorization)
- Category prediction using `RandomForestClassifier`
- Hyperparameter tuning with `GridSearchCV`
- Model pipeline built with `scikit-learn`
- Telegram bot integration via `python-telegram-bot`
- Model persistence using `joblib`

### 🛠 Tech Stack
- Python 3.10+
- python-telegram-bot
- beautifulsoup4
- requests
- scikit-learn
- joblib
- pandas
- numpy

### 📂 Project Structure
```
news-classification-telegram-bot/
│
├── src/
│   ├── scraper.py        # News scraping script
│   ├── bot.py            # Telegram bot logic
│
├── data/
│   └── news.csv          # Scraped dataset
│
├── model/
│   └── nlp_model.pkl     # Trained ML model
│
├── notebooks/
│   └── training.ipynb    # Model training notebook
│
├── .env                  # Environment variables
├── requirements.txt
└── README.md
```

## ⚙️ Installation
**Clone the Repository:**
```
git clone https://github.com/harutyun0avanesyan/news-classification-telegram-bot.git
cd news-classification-telegram-bot
```

**Create Virtual Environment:**
```
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```

**Install Dependencies:**
```
pip install -r requirements.txt
```

## 🔄 Data & Model Generation Workflow
### 1️⃣ Data Collection
Run the scraper to collect Armenian news titles:
```
python3 src/scraper.py
```
The script will generate:
```
data/news.csv
```
> ⚠️ Note: The complete scraping process may take 3+ hours.

### 2️⃣ Model Training
Open and execute `notebooks/training.ipynb` to:
- Perform NLP preprocessing
- Apply TF-IDF vectorization
- Train the Random Forest classifier
- Perform hyperparameter tuning with GridSearchCV
- Save the trained model to:
```
model/nlp_model.pkl
```

## 🔑 Telegram Bot Setup
1. Open Telegram
2. Search for @BotFather
3. Create a new bot
4. Copy the generated API token
Add your token to the `.env` file:
```
BOT_TOKEN=your_token_here
```

## ▶️ Run the Bot
```
python3 src/bot.py
```
Send a news article link or plain text to the bot.
It will respond with the predicted category.
> ⚠️ Note: The model is trained on Armenian-language news articles.

### ℹ️ Model Details
- Algorithm: RandomForestClassifier
- Text Representation: TF-IDF
- Validation: Train/Test Split
- Optimization: GridSearchCV
- Pipeline: scikit-learn Pipeline

## ✍️ Usage Example
1. Open Telegram and start your bot.
2. Send this message:
`
'Սպորտային մարմնամարզության Հայաստանի հավաքականի անդամ Արթուր Ավետիսյանը ոսկե մեդալ է նվաճել'
`
3. Bot response:
`
📰 Predicted Category: Sport
`
