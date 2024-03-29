from web3 import Web3
import requests
from bs4 import BeautifulSoup
import gensim 
### tweeting to langwallet, respond to dynamically imaging, tweets in any app, scrapes likes and bookmarks, 
# window.ai 
#libraries like gpt index, llama index, (within a thread, having multiple processes, )
#google bison for free

class UserDataCollector:

    word2vec_model = gensim.models.KeyedVectors.load_word2vec_format('path_to_word2vec_model.bin', binary=True)
    
    def __init__(self, user_state):
        self.user_state = user_state
        self.provider = Web3(Web3.HTTPProvider('need to figure out link'))

    def collect_user_data(self, wallet_address):
        user_metadata = {}

        # Collect user's trades data
        trades_data = self.collect_trades_data(wallet_address)
        user_metadata['trades'] = trades_data

        # Collect user's interests data
        interests_data = self.collect_interests_data(wallet_address)
        user_metadata['interests'] = interests_data

        # Collect other relevant metadata based on user's state
        state_metadata = self.collect_state_metadata(self.user_state)
        user_metadata['state'] = state_metadata

        return user_metadata
    
    @classmethod
    def collect_trades_data(wallet_address) -> list:
        # Implement the logic to collect trades data based on wallet address
        # Can also query a database of stored user data
        trades_data = []
        transactions = self.provider.eth.get_transaction_reciept(wallet_address)
        for tx in transactions:
            # Extract relevant trade data from the transaction
            trade_data = {
                "tx_hash": tx['transactionHash'].hex(),
                "from": tx['from'],
                "to": tx['to'],
                "value": self.provider.fromWei(tx['value'], 'ether'),
              
            }
            trades_data.append(trade_data)
            
        return trades_data

    def collect_interests_data(self, user_name):
        interests_data = {}

        # Format the user name for the search query
        formatted_user_name = user_name.lower().replace(" ", "+")

        # Perform a search query on twitter (plan to add others later)
        search_url = f"https://twitter.com/search?q={formatted_user_name}"
        response = requests.get(search_url)
        if response.status_code == 200:
            # Parse the HTML content of the search results
            soup = BeautifulSoup(response.content, "html.parser")

            # Extract relevant information from the search results
            interests_data['tweets'] = self.extract_tweets(soup)
            interests_data['followers'] = self.extract_followers_count(soup)
            #can add more fields once it works

        return interests_data

    def extract_tweets(self, soup):
        tweets = []
        
        tweet_divs = soup.find_all("div", {"data-testid": "tweet"})

        # Iterate through tweet div element
        for div in tweet_divs:
            tweet_data = {}

            # Extract the text content 
            tweet_text_element = div.find("div", {"class": "tweet-text"})
            if tweet_text_element is not None:
                tweet_text = tweet_text_element.get_text().strip()
                tweet_data["text"] = tweet_text

                # Store the text as embeddings
                tweet_text_embeddings = []
                for word in tweet_text.split():
                    if word in word2vec_model.vocab:
                        word_embedding = word2vec_model[word]
                        tweet_text_embeddings.append(word_embedding)
                tweet_data["text_embeddings"] = tweet_text_embeddings

            # Extract the username of the tweet
            tweet_author_element = div.find("span", {"class": "username"})
            if tweet_author_element is not None:
                tweet_data["author"] = tweet_author_element.get_text().strip()

            # Extract the timestamp of the tweet
            tweet_timestamp_element = div.find("a", {"class": "tweet-timestamp"})
            if tweet_timestamp_element is not None:
                tweet_data["timestamp"] = tweet_timestamp_element["title"]

            # Add the tweet data to the list of tweets
            if tweet_data:
                tweets.append(tweet_data)
        return tweets


    def extract_followers_count(self, soup):
        followers_count = 0

        # Find the element that contains the followers count
        followers_count_element = soup.find("a", {"data-nav": "followers"})
        if followers_count_element is not None:
            # Extract the text content of the followers count element
            followers_count_text = followers_count_element.find("span", {"class": "css-901oao"}).get_text()

            # Convert the followers count to an integer
            try:
                followers_count = int(followers_count_text.replace(",", ""))
            except ValueError:
                pass

        return followers_count

    def collect_state_metadata(self, user_state):
        # Need to implement-----collect state-specific metadata
    
        state_metadata = ...

        return state_metadata


