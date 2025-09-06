import praw
import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv
from tqdm import tqdm
import time
import logging

class RedditScraper:
    def __init__(self):
        """Initialize the Reddit scraper with configuration from .env file"""
        load_dotenv()
        
        # Setup logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        
        # Reddit API credentials
        self.client_id = os.getenv('REDDIT_CLIENT_ID')
        self.client_secret = os.getenv('REDDIT_CLIENT_SECRET')
        self.user_agent = os.getenv('REDDIT_USER_AGENT')
        
        # Scraping configuration
        self.subreddit_name = os.getenv('SUBREDDIT', 'indianstocks')
        self.max_posts = int(os.getenv('MAX_POSTS', 100))
        self.comments_per_post = int(os.getenv('COMMENTS_PER_POST', 50))
        
        # Validate credentials
        if not all([self.client_id, self.client_secret, self.user_agent]):
            raise ValueError("Reddit API credentials are missing. Please check your .env file.")
        
        # Initialize Reddit instance
        try:
            self.reddit = praw.Reddit(
                client_id=self.client_id,
                client_secret=self.client_secret,
                user_agent=self.user_agent
            )
            self.logger.info("Successfully connected to Reddit API")
        except Exception as e:
            self.logger.error(f"Failed to connect to Reddit API: {e}")
            raise
    
    def scrape_comments(self, sort_by='hot', time_filter='week'):
        """
        Scrape comments from r/indianstocks
        
        Args:
            sort_by (str): How to sort posts ('hot', 'new', 'top', 'rising')
            time_filter (str): Time filter for top posts ('hour', 'day', 'week', 'month', 'year', 'all')
        
        Returns:
            pd.DataFrame: DataFrame containing scraped comments
        """
        self.logger.info(f"Starting to scrape comments from r/{self.subreddit_name}")
        
        try:
            subreddit = self.reddit.subreddit(self.subreddit_name)
            
            # Get posts based on sorting method
            if sort_by == 'hot':
                posts = subreddit.hot(limit=self.max_posts)
            elif sort_by == 'new':
                posts = subreddit.new(limit=self.max_posts)
            elif sort_by == 'top':
                posts = subreddit.top(time_filter=time_filter, limit=self.max_posts)
            elif sort_by == 'rising':
                posts = subreddit.rising(limit=self.max_posts)
            else:
                raise ValueError(f"Invalid sort_by parameter: {sort_by}")
            
            comments_data = []
            
            for post in tqdm(posts, desc="Processing posts", unit="post"):
                try:
                    # Get post information
                    post_info = {
                        'post_id': post.id,
                        'post_title': post.title,
                        'post_score': post.score,
                        'post_url': post.url,
                        'post_created_utc': datetime.fromtimestamp(post.created_utc),
                        'post_num_comments': post.num_comments,
                        'post_author': str(post.author) if post.author else '[deleted]'
                    }
                    
                    # Get comments
                    post.comments.replace_more(limit=0)  # Remove MoreComments objects
                    comments = post.comments.list()[:self.comments_per_post]
                    
                    for comment in comments:
                        try:
                            comment_data = {
                                **post_info,
                                'comment_id': comment.id,
                                'comment_body': comment.body,
                                'comment_score': comment.score,
                                'comment_created_utc': datetime.fromtimestamp(comment.created_utc),
                                'comment_author': str(comment.author) if comment.author else '[deleted]',
                                'comment_is_submitter': comment.is_submitter,
                                'comment_permalink': f"https://reddit.com{comment.permalink}"
                            }
                            comments_data.append(comment_data)
                        except Exception as e:
                            self.logger.warning(f"Error processing comment {comment.id}: {e}")
                            continue
                    
                    # Add a small delay to be respectful to Reddit's API
                    time.sleep(0.1)
                    
                except Exception as e:
                    self.logger.warning(f"Error processing post {post.id}: {e}")
                    continue
            
            df = pd.DataFrame(comments_data)
            self.logger.info(f"Successfully scraped {len(df)} comments from {len(df['post_id'].unique()) if not df.empty else 0} posts")
            
            return df
            
        except Exception as e:
            self.logger.error(f"Error during scraping: {e}")
            raise
    
    def save_to_csv(self, df, filename=None):
        """
        Save DataFrame to CSV file
        
        Args:
            df (pd.DataFrame): DataFrame to save
            filename (str): Custom filename (optional)
        
        Returns:
            str: Path to saved file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reddit_comments_{self.subreddit_name}_{timestamp}.csv"
        
        filepath = os.path.join(os.getcwd(), filename)
        df.to_csv(filepath, index=False, encoding='utf-8')
        self.logger.info(f"Data saved to {filepath}")
        
        return filepath
    
    def get_stats(self, df):
        """
        Get statistics about the scraped data
        
        Args:
            df (pd.DataFrame): DataFrame with scraped data
        
        Returns:
            dict: Statistics about the data
        """
        if df.empty:
            return {"message": "No data to analyze"}
        
        stats = {
            "total_comments": len(df),
            "unique_posts": df['post_id'].nunique(),
            "unique_authors": df['comment_author'].nunique(),
            "date_range": {
                "earliest": df['comment_created_utc'].min(),
                "latest": df['comment_created_utc'].max()
            },
            "average_comment_score": df['comment_score'].mean(),
            "total_comment_score": df['comment_score'].sum(),
            "comments_per_post": len(df) / df['post_id'].nunique()
        }
        
        return stats

def main():
    """Main function to run the scraper"""
    try:
        scraper = RedditScraper()
        
        # Scrape comments
        print("Starting Reddit scraping...")
        df = scraper.scrape_comments(sort_by='hot', time_filter='week')
        
        if df.empty:
            print("No comments were scraped. Please check your configuration.")
            return
        
        # Save to CSV
        filepath = scraper.save_to_csv(df)
        
        # Display statistics
        stats = scraper.get_stats(df)
        print("\n" + "="*50)
        print("SCRAPING STATISTICS")
        print("="*50)
        print(f"Total comments scraped: {stats['total_comments']}")
        print(f"Unique posts: {stats['unique_posts']}")
        print(f"Unique authors: {stats['unique_authors']}")
        print(f"Average comments per post: {stats['comments_per_post']:.2f}")
        print(f"Date range: {stats['date_range']['earliest']} to {stats['date_range']['latest']}")
        print(f"Average comment score: {stats['average_comment_score']:.2f}")
        print(f"Data saved to: {filepath}")
        print("="*50)
        
        # Show sample data
        print("\nSample comments:")
        print("-" * 50)
        sample_comments = df[['comment_body', 'comment_score', 'comment_author']].head(3)
        for idx, row in sample_comments.iterrows():
            print(f"Author: {row['comment_author']}")
            print(f"Score: {row['comment_score']}")
            print(f"Comment: {row['comment_body'][:100]}...")
            print("-" * 30)
        
    except Exception as e:
        print(f"Error: {e}")
        print("Please make sure you have configured your Reddit API credentials in the .env file.")

if __name__ == "__main__":
    main()
