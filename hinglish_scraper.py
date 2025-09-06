"""
FINAL HINGLISH STOCK SENTIMENT SCRAPER
======================================
Scrapes pure Hinglish comments (Hindi written in English) from r/indianstocks
for sentiment analysis. Creates clean dataset with comments, sentiment, and dates.

Author: Reddit Scraper v1.0
Purpose: Indian Stock Market Sentiment Analysis Dataset
"""

from reddit_scraper import RedditScraper
import pandas as pd
import re
from datetime import datetime
import time

class FinalHinglishScraper(RedditScraper):
    def __init__(self):
        super().__init__()
        
    def is_pure_hinglish(self, text):
        """
        Enhanced Hinglish detection - more comprehensive
        """
        text_lower = text.lower().strip()
        
        # Remove URLs, mentions, and Reddit formatting first
        text_clean = re.sub(r'http\S+|www\S+|https\S+|u/\S+|r/\S+', '', text_lower)
        text_clean = re.sub(r'[^\w\s]', ' ', text_clean)
        text_clean = re.sub(r'\s+', ' ', text_clean).strip()
        
        # Skip very short comments
        if len(text_clean) < 15:
            return False
            
        words = text_clean.split()
        
        # Expanded Hindi words written in English
        hinglish_words = {
            # Basic Hindi words
            'hai', 'hain', 'tha', 'thi', 'the', 'hoga', 'hogi', 'hoge', 'hu', 'hun', 'ho',
            'kar', 'kara', 'kare', 'kari', 'karna', 'karne', 'karni', 'karta', 'karti', 'karte', 'karo',
            'kya', 'kyun', 'kyu', 'kaise', 'kaisa', 'kaisi', 'kahan', 'kab', 'kitna', 'kitni', 'kitne',
            'yeh', 'yah', 'ye', 'wo', 'woh', 'jo', 'jab', 'jahan', 'jinhe', 'jinko', 'jiska', 'jiski',
            'main', 'mein', 'me', 'tu', 'tum', 'aap', 'hum', 'humein', 'tumhe', 'tumko', 'apko', 'usko',
            'nahi', 'nahin', 'na', 'mat', 'mana', 'bilkul', 'zaroor', 'shayad', 'pakka', 'sure',
            'abhi', 'ab', 'phir', 'fir', 'pehle', 'baad', 'aage', 'peeche', 'upar', 'neeche', 'andar',
            'aur', 'ya', 'lekin', 'par', 'magar', 'kyunki', 'isliye', 'agar', 'warna', 'toh', 'to',
            
            # Financial/Stock terms in Hindi
            'paisa', 'paise', 'rupya', 'rupaye', 'crore', 'lakh', 'hazaar', 'hazar', 'thousand',
            'kharidna', 'khareed', 'khareedna', 'bechna', 'bech', 'bechna', 'nivesh', 'investment',
            'lagana', 'lagaya', 'laga', 'lagao', 'munafa', 'fayda', 'nuksan', 'loss', 'profit',
            'ghatna', 'ghat', 'badhna', 'badh', 'badha', 'gira', 'gaya', 'jana', 'jaana',
            'market', 'share', 'stock', 'company', 'kaam', 'business', 'vyavasaya',
            
            # Common expressions
            'bhai', 'bhaiyo', 'yaar', 'dost', 'ji', 'sahab', 'sir', 'madam', 'uncle', 'aunty',
            'accha', 'achha', 'acha', 'bura', 'badiya', 'mast', 'sahi', 'galat', 'theek', 'thik',
            'dekho', 'dekh', 'dekhna', 'suno', 'sun', 'sunna', 'samjho', 'samajh', 'samjhna',
            'pata', 'malum', 'chahiye', 'chaahiye', 'hona', 'jana', 'aana', 'lena', 'dena',
            
            # Time expressions
            'aaj', 'kal', 'parso', 'mahina', 'month', 'saal', 'year', 'din', 'day', 'raat', 'night',
            'subah', 'morning', 'shaam', 'evening', 'time', 'waqt', 'samay',
            
            # Emotions/Reactions
            'khushi', 'gam', 'dar', 'darr', 'bharosa', 'umeed', 'hope', 'pareshani', 'tension',
            'mazaa', 'maja', 'maza', 'bore', 'excited', 'nervous', 'confident', 'happy', 'sad',
            
            # Question words
            'kaun', 'kon', 'kaha', 'kahan', 'kab', 'kaise', 'kyun', 'kyu', 'kitna', 'kitni',
            
            # Common verbs
            'jaana', 'aana', 'khelna', 'khana', 'peena', 'sona', 'uthna', 'baithna', 'khada',
            'chalana', 'rukna', 'milna', 'baat', 'bolna', 'kehna', 'sunana', 'dikhana',
            
            # Intensifiers
            'bahut', 'bohot', 'kaafi', 'zyada', 'jyada', 'kam', 'thoda', 'pura', 'poora', 'sara',
            
            # Connecting words
            'matlab', 'means', 'matlab', 'yaani', 'ki', 'ke', 'ko', 'se', 'mein', 'me', 'pe', 'par'
        }
        
        # Count Hindi vs English words
        hindi_count = 0
        total_words = 0
        
        for word in words:
            if len(word) >= 2 and word.isalpha():
                total_words += 1
                if word in hinglish_words:
                    hindi_count += 1
        
        if total_words < 3:
            return False
        
        # At least 30% should be Hindi words for pure Hinglish
        hindi_ratio = hindi_count / total_words if total_words > 0 else 0
        
        # Also check for common Hinglish patterns
        hinglish_patterns = [
            r'\b(kar|kare|karo|karna|karne)\b',
            r'\b(hai|hain|hoga|hogi|hoge)\b',
            r'\b(nahi|nahin|bilkul|zaroor)\b',
            r'\b(abhi|phir|pehle|baad)\b',
            r'\b(bhai|yaar|dost|ji)\b'
        ]
        
        pattern_matches = sum(1 for pattern in hinglish_patterns 
                            if re.search(pattern, text_clean))
        
        return hindi_ratio >= 0.25 or pattern_matches >= 2
    
    def scrape_pure_hinglish_data(self):
        """
        Main method to scrape pure Hinglish data with comprehensive coverage
        """
        print("🇮🇳 SCRAPING PURE HINGLISH STOCK MARKET DATA")
        print("=" * 55)
        
        all_comments = []
        
        try:
            subreddit = self.reddit.subreddit(self.subreddit_name)
            
            # Comprehensive scraping strategies for maximum data collection
            strategies = [
                ('hot', None, 250, "🔥 Hot Posts"),
                ('new', None, 200, "🆕 Recent Posts"), 
                ('top', 'week', 100, "📈 Top This Week"),
                ('top', 'month', 150, "📅 Top This Month"),
                ('top', 'year', 200, "🏆 Top This Year"),
                ('top', 'all', 100, "👑 Top All Time")
            ]
            
            for sort_type, time_filter, limit, description in strategies:
                print(f"\n{description}...")
                
                try:
                    if sort_type == 'hot':
                        posts = list(subreddit.hot(limit=limit))
                    elif sort_type == 'new':
                        posts = list(subreddit.new(limit=limit))
                    elif sort_type == 'top':
                        posts = list(subreddit.top(time_filter=time_filter, limit=limit))
                    
                    hinglish_found = 0
                    
                    for post in posts:
                        try:
                            post_date = datetime.fromtimestamp(post.created_utc)
                            
                            post_info = {
                                'post_id': post.id,
                                'post_title': post.title,
                                'post_date': post_date.strftime('%Y-%m-%d'),
                                'post_year': post_date.year,
                                'post_score': post.score
                            }
                            
                            # Get comments
                            post.comments.replace_more(limit=0)
                            comments = post.comments.list()[:40]
                            
                            for comment in comments:
                                try:
                                    comment_date = datetime.fromtimestamp(comment.created_utc)
                                    comment_text = comment.body
                                    
                                    # Skip deleted/removed comments
                                    if comment_text in ['[deleted]', '[removed]', 'deleted', 'removed']:
                                        continue
                                    
                                    # Check if it's pure Hinglish
                                    if self.is_pure_hinglish(comment_text):
                                        sentiment = self.classify_hinglish_sentiment(comment_text, comment.score)
                                        
                                        comment_data = {
                                            **post_info,
                                            'comment': comment_text,
                                            'comment_date': comment_date.strftime('%Y-%m-%d'),
                                            'comment_year': comment_date.year,
                                            'comment_score': comment.score,
                                            'comment_author': str(comment.author) if comment.author else '[deleted]',
                                            'sentiment': sentiment
                                        }
                                        all_comments.append(comment_data)
                                        hinglish_found += 1
                                
                                except Exception as e:
                                    continue
                        
                        except Exception as e:
                            continue
                    
                    print(f"   ✅ Found {hinglish_found} Hinglish comments")
                    
                    # Add small delay to be respectful to Reddit API
                    time.sleep(1)
                
                except Exception as e:
                    print(f"   ❌ Error in {description}: {e}")
                    continue
            
            df = pd.DataFrame(all_comments)
            
            if not df.empty:
                # Remove duplicates
                df = df.drop_duplicates(subset=['comment'])
                print(f"\n📊 Total unique Hinglish comments: {len(df)}")
                
                # Show year distribution
                if 'comment_year' in df.columns:
                    year_counts = df['comment_year'].value_counts().sort_index()
                    print("\n📅 Distribution by year:")
                    for year, count in year_counts.items():
                        print(f"   {year}: {count} comments")
            
            return df
            
        except Exception as e:
            self.logger.error(f"Error during scraping: {e}")
            return pd.DataFrame()
    
    def classify_hinglish_sentiment(self, comment_text, comment_score):
        """
        Classify Hinglish comments for stock sentiment
        """
        comment_lower = comment_text.lower()
        
        # Enhanced Hinglish sentiment indicators
        bullish_indicators = [
            'achha', 'accha', 'acha', 'badiya', 'mast', 'sahi', 'theek', 'munafa', 'fayda',
            'badhega', 'badha', 'upar', 'strong', 'bharosa', 'khareed', 'kharidna', 'buy',
            'lagana', 'invest', 'hold', 'good', 'profit', 'gain', 'target', 'bullish'
        ]
        
        bearish_indicators = [
            'bura', 'galat', 'kharab', 'ghatega', 'gira', 'neeche', 'nuksan', 'loss',
            'bech', 'bechna', 'sell', 'girna', 'weak', 'bearish', 'bad', 'avoid'
        ]
        
        bullish_count = sum(1 for word in bullish_indicators if word in comment_lower)
        bearish_count = sum(1 for word in bearish_indicators if word in comment_lower)
        
        # Score influence
        if comment_score > 5:
            bullish_count += 1
        elif comment_score < -2:
            bearish_count += 1
        
        if bullish_count > bearish_count:
            return 'bullish'
        elif bearish_count > bullish_count:
            return 'bearish'
        else:
            return 'neutral'

def main():
    """
    Main function to scrape enhanced Hinglish data
    """
    try:
        scraper = FinalHinglishScraper()
        
        # Scrape Hinglish data
        df = scraper.scrape_pure_hinglish_data()
        
        if df.empty:
            print("❌ No Hinglish data found.")
            return
        
        # Save the data
        output_file = "final_hinglish_sentiment_dataset.csv"
        
        # Select final columns for clean dataset
        final_columns = ['comment', 'sentiment', 'comment_date', 'comment_year', 'comment_score', 'post_title', 'post_date']
        df_final = df[final_columns].copy()
        
        df_final.to_csv(output_file, index=False)
        
        # Show comprehensive statistics
        print("\n" + "🎯" * 25)
        print("🇮🇳 FINAL HINGLISH SENTIMENT DATASET READY 🇮🇳")
        print("🎯" * 25)
        print(f"📁 File: {output_file}")
        print(f"📊 Total comments: {len(df_final)}")
        
        # Sentiment distribution
        sentiment_counts = df_final['sentiment'].value_counts()
        print(f"\n💭 Sentiment Distribution:")
        for sentiment, count in sentiment_counts.items():
            percentage = (count / len(df_final)) * 100
            emoji = "🐂" if sentiment == "bullish" else "🐻" if sentiment == "bearish" else "😐"
            print(f"   {emoji} {sentiment.capitalize()}: {count} ({percentage:.1f}%)")
        
        # Year distribution
        year_counts = df_final['comment_year'].value_counts().sort_index()
        print(f"\n📅 Year Distribution:")
        for year, count in year_counts.items():
            percentage = (count / len(df_final)) * 100
            print(f"   📆 {year}: {count} ({percentage:.1f}%)")
        
        # Show sample Hinglish comments
        print(f"\n💬 Sample Pure Hinglish Comments:")
        print("─" * 50)
        
        for sentiment in ['bullish', 'bearish', 'neutral']:
            if sentiment in df_final['sentiment'].values:
                samples = df_final[df_final['sentiment'] == sentiment].head(2)
                emoji = "🐂" if sentiment == "bullish" else "🐻" if sentiment == "bearish" else "😐"
                print(f"\n{emoji} {sentiment.upper()} Examples:")
                for _, sample in samples.iterrows():
                    print(f"   📝 \"{sample['comment'][:70]}...\"")
                    print(f"   📅 {sample['comment_date']} | 👍 {sample['comment_score']}")
        
        print(f"\n🎉 SUCCESS! Your Hinglish dataset is ready for sentiment analysis!")
        print(f"📁 Dataset saved as: {output_file}")
        print(f"📊 Columns: {list(df_final.columns)}")
        print(f"🇮🇳 Perfect for Indian stock market sentiment analysis!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
