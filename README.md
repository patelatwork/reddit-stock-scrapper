# 🇮🇳 Hinglish Stock Market Sentiment Scraper

**The Ultimate Tool for Scraping Pure Hinglish Comments from r/indianstocks**

This scraper collects Hindi-written-in-English comments from Reddit's r/indianstocks subreddit to build datasets for sentiment analysis of Indian stock market discussions.

## 🎯 What You Get

- **Pure Hinglish Comments**: Hindi words written in English script
- **Sentiment Classification**: Bullish 🐂, Bearish 🐻, Neutral 😐
- **Complete Dataset**: Comments, dates, scores, and metadata
- **Ready for ML**: Clean CSV format perfect for sentiment analysis

## 🚀 Quick Start

### 1. Setup Environment
```powershell
# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Reddit API
Edit `.env` file with your Reddit credentials:
```
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here
REDDIT_USER_AGENT=hinglish_scraper_v1.0_by_yourusername
```

**Get Reddit API credentials:**
1. Go to https://www.reddit.com/prefs/apps/
2. Create new app (type: "script")
3. Copy Client ID and Secret

### 3. Run the Scraper
```powershell
python hinglish_scraper.py
```

## 📊 Output Dataset

**File**: `final_hinglish_sentiment_dataset.csv`

**Columns**:
- `comment` - The Hinglish comment text
- `sentiment` - bullish/bearish/neutral classification
- `comment_date` - When the comment was posted
- `comment_year` - Year of the comment
- `comment_score` - Reddit upvotes/downvotes
- `post_title` - Title of the original post
- `post_date` - When the post was created

## 💬 Sample Data

**Bullish Example:**
```
"Bhai 5L ak stock me dal or 7 8% return leke profit Book kro simple"
Sentiment: bullish | Date: 2025-09-05 | Score: 1
```

**Bearish Example:**
```
"7000 cror aur 3500 crore unke stocks 80 aur 50 hai. nuksan bahut hai"
Sentiment: bearish | Date: 2025-09-06 | Score: 1
```

## 🔧 How It Works

1. **Connects to Reddit API** using PRAW library
2. **Scrapes multiple post types**: Hot, New, Top posts from different time periods
3. **Filters for Hinglish**: Identifies Hindi words written in English
4. **Classifies sentiment**: Uses keyword matching and comment scores
5. **Exports clean data**: Ready-to-use CSV format

## 📁 Project Files

- `hinglish_scraper.py` - Main scraper (THIS IS THE ONE TO USE)
- `reddit_scraper.py` - Base Reddit scraper class
- `requirements.txt` - Python dependencies
- `.env` - Configuration file
- `README.md` - This file

## ⚙️ Configuration

Edit `.env` to customize:
```
SUBREDDIT=indianstocks
MAX_POSTS=100
COMMENTS_PER_POST=50
```

## 🛡️ Features

- **Rate Limiting**: Respects Reddit API limits
- **Error Handling**: Robust error recovery
- **Duplicate Removal**: Clean, unique dataset
- **Progress Tracking**: Visual progress indicators
- **Comprehensive Coverage**: Multiple scraping strategies

## 🎯 Perfect For

- **Sentiment Analysis**: Train ML models on Indian stock sentiment
- **Hinglish NLP**: Study Hindi-English code-mixing
- **Market Research**: Analyze retail investor sentiment
- **Academic Research**: Indian social media and finance

---

**Ready to scrape? Just run `python hinglish_scraper.py` and get your Hinglish dataset! 🚀**
