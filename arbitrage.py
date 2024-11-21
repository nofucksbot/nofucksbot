import requests
import time
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Setup logging for debugging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class ArbitrageBot:
    def __init__(self, crypto='bitcoin', exchanges=None):
        self.crypto = crypto.lower()
        self.exchanges = exchanges if exchanges else ['binance', 'coinbase', 'kraken']
        self.api_urls = {
            "binance": f"https://api.coingecko.com/api/v3/simple/price?ids={self.crypto}&vs_currencies=usd",
            "coinbase": f"https://api.coinbase.com/v2/prices/{self.crypto}-USD/spot",
            "kraken": f"https://api.coingecko.com/api/v3/simple/price?ids={self.crypto}&vs_currencies=usd"
        }
        self.price_history = {}

    def fetch_prices(self):
        """Fetch prices from multiple exchanges and store them."""
        prices = {}
        for exchange in self.exchanges:
            try:
                response = requests.get(self.api_urls[exchange])
                data = response.json()
                if exchange == "coinbase":
                    price = float(data['data']['amount'])
                else:
                    price = float(data[self.crypto]['usd'])
                prices[exchange] = price
                logging.info(f"Fetched price from {exchange}: ${price}")
            except Exception as e:
                logging.error(f"Error fetching from {exchange}: {str(e)}")
                prices[exchange] = None
        self.price_history = prices
        return prices

    def detect_arbitrage_opportunity(self):
        """Check for arbitrage opportunities by comparing prices."""
        prices = self.fetch_prices()
        if None in prices.values():
            return "Error in fetching prices from some exchanges."

        max_price = max(prices, key=prices.get)
        min_price = min(prices, key=prices.get)
        price_diff = prices[max_price] - prices[min_price]
        
        if price_diff > 50:  # Example: Arbitrage is viable if difference is more than $50
            return f"Arbitrage opportunity detected! Buy on {min_price.capitalize()} for ${prices[min_price]} and sell on {max_price.capitalize()} for ${prices[max_price]}. Profit: ${price_diff}"
        
        return f"No arbitrage opportunity. Price diff: ${price_diff} between {max_price.capitalize()} and {min_price.capitalize()}"

    def send_email_alert(self, message, to_email="example@example.com"):
        """Send an email alert when arbitrage opportunity is found."""
        from_email = "your_email@example.com"
        subject = "Arbitrage Opportunity Alert"
        
        # Setup the email server
        try:
            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(from_email, "your_password")  # Use an app password here for Gmail
            text = msg.as_string()
            server.sendmail(from_email, to_email, text)
            server.quit()
            logging.info("Alert sent successfully via email.")
        except Exception as e:
            logging.error(f"Error sending email: {str(e)}")

    def monitor_arbitrage(self, interval=300, alert_email="example@example.com"):
        """Monitor arbitrage opportunities at regular intervals."""
        logging.info("Starting arbitrage monitoring...")
        while True:
            opportunity = self.detect_arbitrage_opportunity()
            if "Arbitrage opportunity detected" in opportunity:
                logging.info(f"Arbitrage detected: {opportunity}")
                self.send_email_alert(opportunity, alert_email)
            else:
                logging.info(f"No arbitrage: {opportunity}")
            time.sleep(interval)  # Wait for the next check (in seconds)

if __name__ == "__main__":
    # Initialize the ArbitrageBot with the selected crypto and exchanges
    bot = ArbitrageBot(crypto='bitcoin', exchanges=['binance', 'coinbase', 'kraken'])

    # Start monitoring arbitrage every 5 minutes (300 seconds)
    bot.monitor_arbitrage(interval=300, alert_email="your_alert_email@example.com")
