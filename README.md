# Reddit Stock Sentiment Analysis Scraper

**Advanced Tool for Analyzing Indian Stock Market Sentiment from r/indianstocks**

This comprehensive project scrapes Hinglish (Hindi-English) comments from Reddit's r/indianstocks community and performs sophisticated sentiment analysis with real stock price correlation.

## What You Get

- **Stock-Specific Analysis**: Target individual Nifty 50 stocks (RELIANCE, TCS, HDFC, etc.)
- **Hinglish Detection**: AI-powered identification of Hindi words in English script  
- **Dual Sentiment Analysis**: VADER + TextBlob for accurate sentiment scoring
- **Stock Price Correlation**: Yahoo Finance integration for price movement analysis
- **Time-Series Data**: Historical analysis with custom date ranges
- **Export Ready**: Clean CSV datasets for machine learning

## Quick Start

### 1. Install Dependencies
```powershell
# Clone or download this repository
# Navigate to project directory
cd webscrapper

# Install all required packages
pip install -r requirements.txt
```

### 2. Setup Reddit API Credentials

**Get Your Reddit API Keys:**
1. Visit https://www.reddit.com/prefs/apps/
2. Click "Create App" or "Create Another App"
3. Choose **"script"** as application type
4. Fill in details:
   - **Name**: `hinglish-stock-scraper`
   - **Description**: `Stock sentiment analysis tool`
   - **Redirect URI**: `http://localhost:8080`

**Configure .env File:**
Edit `.env` and replace with your credentials:
```env
REDDIT_CLIENT_ID=your_14_character_client_id
REDDIT_CLIENT_SECRET=your_27_character_secret_key  
REDDIT_USER_AGENT=hinglish_stock_scraper_v1.0_by_yourusername
```

### 3. Run Analysis

**Option A: Jupyter Notebook (Recommended)**
```powershell
# Start Jupyter
jupyter notebook

# Open stock_sentiment_analysis.ipynb
# Run all cells step by step
```

**Option B: Python Script**
```powershell
# Use the base scraper class
python reddit_scraper.py
```

## Configuration Guide

### Stock Selection
Choose from popular Nifty 50 stocks:
```python
# Edit in notebook or .env file
STOCK_TICKER = "RELIANCE.NS"  # Reliance Industries
STOCK_TICKER = "TCS.NS"       # Tata Consultancy Services  
STOCK_TICKER = "HDFCBANK.NS"  # HDFC Bank
STOCK_TICKER = "INFY.NS"      # Infosys
STOCK_TICKER = "HINDUNILVR.NS" # Hindustan Unilever
STOCK_TICKER = "ITC.NS"       # ITC Limited
```

### Time Period Settings
```python
# In notebook configuration cell:
time_period = "month"    # Last 30 days
time_period = "year"     # Last 365 days  
time_period = "all"      # All available data

# Custom date range:
start_date = "2024-01-01"
end_date = "2024-12-31"
```

### Subreddit Options
```python
# Primary target (recommended):
subreddit = "indianstocks"     # 100K+ active members

# Alternative options:
subreddit = "IndianStreetBets" # Meme-focused trading
subreddit = "investing"        # Global investing (limited Hinglish)
subreddit = "SecurityAnalysis" # Fundamental analysis
```

### Scraping Parameters
```python
# Adjust in notebook:
howmanysubmissions = 100        # Number of posts to analyze
max_comments_per_post = 50      # Comments per post limit
min_ticker_mentions = 1         # Minimum stock mentions required
analyze_comments = True         # Include comment analysis
```

## Output Files

The scraper generates timestamped CSV files:

### Sentiment Analysis Results
**File**: `{STOCK}_comment_analysis_YYYYMMDD_HHMMSS.csv`

**Columns**:
- `Title` - Reddit post title
- `Ticker` - Stock symbol (e.g., RELIANCE.NS)
- `Date` - Post creation date
- `DateTime` - Full timestamp
- `Post_ID` - Unique Reddit post identifier
- `Score` - Reddit upvotes minus downvotes
- `Num_Comments` - Total comment count
- `Author` - Post author username
- `NumberOfTickerMentions` - Stock mention frequency
- `Is_Hinglish` - Boolean Hinglish detection
- `VADER_Positive/Negative/Neutral` - VADER sentiment counts
- `TextBlob_Positive/Negative/Neutral` - TextBlob sentiment counts

### Stock Price History
**File**: `{STOCK}_stock_history_YYYYMMDD_HHMMSS.csv`

**Yahoo Finance Data**:
- `Date`, `Open`, `High`, `Low`, `Close`, `Volume`
- Perfect for correlation analysis with sentiment data

## 💬 Sample Results

**Hinglish Comment Analysis:**
```
"RIL me 2800 level pe support hai bhai, yaha se bounce expected"
→ Sentiment: BULLISH (VADER: +0.6, TextBlob: +0.4)
→ Stock: RELIANCE.NS | Date: 2025-09-15 | Mentions: 1
```

**Sentiment Summary:**
```
RELIANCE.NS Analysis Results:
   Posts: 13 | Comments: 581
   BULLISH: 43.5% | BEARISH: 13.1% | NEUTRAL: 43.4%
   Hinglish Content: 61.5%
   Overall Score: +0.282 (BULLISH)
```

## Advanced Features

### Hinglish Detection Algorithm
- **Smart Pattern Matching**: Identifies Hindi words in Roman script
- **Context Analysis**: Distinguishes from English false positives
- **Cultural Keywords**: Recognizes Indian financial terminology

### Dual Sentiment Analysis
- **VADER**: Lexicon-based, handles social media text well
- **TextBlob**: Rule-based, good for formal language
- **Combined Scoring**: Weighted average for final sentiment

### Stock Price Integration
- **Yahoo Finance API**: Real-time and historical data
- **NSE/BSE Support**: Indian stock exchanges
- **Correlation Ready**: Timestamp alignment for analysis

## Troubleshooting

### Reddit API Issues
```
Error: 401 Unauthorized
→ Check your Reddit credentials in .env
→ Ensure app type is "script" not "web app"
```

### Package Installation
```powershell
# If yfinance fails:
pip install yfinance --no-dependencies
pip install multitasking --no-dependencies

# If NLTK data missing:
python -c "import nltk; nltk.download('vader_lexicon'); nltk.download('punkt')"
```

### Rate Limiting
```
Error: 429 Too Many Requests
→ Reddit API limit reached
→ Reduce MAX_POSTS in .env
→ Wait 10-15 minutes before retry
```

## Project Structure

```
webscrapper/
├── 📓 stock_sentiment_analysis.ipynb  # Main analysis notebook
├── .env                           # Configuration file
├── requirements.txt               # Dependencies
├── README.md                      # This documentation
└── *.csv                          # Generated datasets
=======
├── ⚙️ .env                           # Configuration file
├── 📦 requirements.txt               # Dependencies
├── 📖 README.md                      # This documentation
└── 📊 *.csv                          # Generated datasets
>>>>>>> 22aa34eed0de0bf5d5233c636ed4a8ec435e76ae
```

## Research Applications

- **Sentiment-Price Correlation**: Study relationship between social sentiment and stock movements
- **Hinglish NLP Research**: Analyze code-mixing patterns in financial discussions  
- **Retail Investor Behavior**: Understand Indian retail trading sentiment
- **ML Model Training**: Build predictive models with sentiment features
- **Market Microstructure**: Analyze social media impact on price discovery

## Contributing

Want to improve the scraper?
1. Fork this repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m 'Add feature'`
4. Push branch: `git push origin feature-name`
5. Submit pull request

## License

This project is for educational and research purposes. Please respect Reddit's Terms of Service and API rate limits.

---

**Ready to analyze Indian stock sentiment? Open `stock_sentiment_analysis.ipynb` and start exploring!**
