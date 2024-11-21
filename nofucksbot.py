import openai
import os
import pyttsx3
import requests
import speech_recognition as sr
import json
import time

# Load OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1)  # Volume level

# Initialize Speech Recognition
recognizer = sr.Recognizer()

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen_command():
    """Listen for voice command."""
    with sr.Microphone() as source:
        print("Listening for command...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
            return ""
        except sr.RequestError as e:
            print(f"Error with the speech recognition service: {e}")
            return ""

def get_crypto_info(coin="bitcoin"):
    """Fetch live crypto prices using CoinGecko API."""
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
        response = requests.get(url)
        data = response.json()
        
        if coin in data:
            price = data[coin]["usd"]
            return f"The price of {coin.capitalize()} is ${price}. Don't waste your money."
        else:
            return "Error fetching crypto data."
    except Exception as e:
        return f"Failed to fetch crypto data: {str(e)}"

def convert_currency(amount, from_currency="usd", to_currency="btc"):
    """Convert between fiat and crypto currencies using CoinGecko API."""
    try:
        url = f"https://api.coingecko.com/api/v3/simple/convert?amount={amount}&from={from_currency}&to={to_currency}"
        response = requests.get(url)
        data = response.json()
        
        if 'error' not in data:
            return f"{amount} {from_currency} is equivalent to {data[to_currency]} {to_currency}."
        else:
            return "Error in currency conversion."
    except Exception as e:
        return f"Failed to convert currency: {str(e)}"

def fetch_crypto_news():
    """Fetch the latest cryptocurrency news."""
    url = "https://cryptonews-api.com/api/v1/category?section=top"
    headers = {"Authorization": "Bearer YOUR_API_KEY"}  # Add your News API key here
    response = requests.get(url, headers=headers)
    news = response.json()
    
    if news.get('status') == 'ok':
        articles = news['data']['news']
        return "\n".join([f"{article['title']} - {article['source']['name']}" for article in articles[:5]])
    else:
        return "Could not fetch crypto news."

def generate_meme(sarcasm_level=0.8):
    """Generate a sarcastic meme based on the sarcasm level."""
    prompt = f"Generate a meme about investing in crypto with a sarcasm level of {sarcasm_level}"
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        temperature=0.8
    )
    
    return response.choices[0].text.strip()

def sentiment_analysis(text):
    """Basic sentiment analysis using OpenAI to check if the tone is sarcastic or positive."""
    prompt = f"Analyze the sentiment of the following text. Is it sarcastic or positive?\n\n{text}"
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50,
        temperature=0.5
    )
    
    return response.choices[0].text.strip()

def user_profile(user_id):
    """Simulate a basic user profile system (saving preferences or past actions)."""
    user_data = {
        "crypto_preferences": ["bitcoin", "ethereum"],
        "sarcasm_level": 0.8,
        "news_subscriptions": True
    }
    return user_data

def fetch_weather(city="New York"):
    """Fetch the weather info from a weather API."""
    url = f"http://api.weatherstack.com/current?access_key=YOUR_API_KEY&query={city}"
    response = requests.get(url)
    weather_data = response.json()

    if "current" in weather_data:
        temp = weather_data['current']['temperature']
        description = weather_data['current']['weather_descriptions'][0]
        return f"The current temperature in {city} is {temp}°C with {description}."
    else:
        return "Couldn't fetch weather data."

def fetch_random_joke():
    """Fetch a random joke."""
    url = "https://official-joke-api.appspot.com/random_joke"
    response = requests.get(url)
    joke_data = response.json()
    
    return f"Here’s a joke: {joke_data['setup']} - {joke_data['punchline']}"

def main():
    """Main bot interaction loop."""
    print("NoF***sBot: Ready for your sarcastic chaos. Type 'crypto' for price info, 'meme' for memes, 'sentiment' to analyze tone, 'news' for crypto news, 'weather' for weather, 'joke' for a random joke, or 'exit' to quit.")
    
    while True:
        # Wait for voice or text input
        user_input = listen_command() or input("You: ").lower()

        if "crypto" in user_input:
            coin = input("Enter cryptocurrency name (e.g., bitcoin, ethereum): ").lower()
            crypto_info = get_crypto_info(coin)
            print("NoF***sBot: " + crypto_info)
            speak(crypto_info)

        elif "convert" in user_input:
            amount = float(input("Enter amount to convert: "))
            from_currency = input("From currency (usd, eur, btc): ").lower()
            to_currency = input("To currency (usd, eur, btc): ").lower()
            conversion = convert_currency(amount, from_currency, to_currency)
            print("NoF***sBot: " + conversion)
            speak(conversion)

        elif "meme" in user_input:
            sarcasm_level = float(input("Enter sarcasm level (0-1): "))
            meme = generate_meme(sarcasm_level)
            print("NoF***sBot: " + meme)
            speak(meme)

        elif "sentiment" in user_input:
            text_to_analyze = input("Enter text for sentiment analysis: ")
            sentiment = sentiment_analysis(text_to_analyze)
            print(f"NoF***sBot: {sentiment}")
            speak(sentiment)

        elif "news" in user_input:
            news = fetch_crypto_news()
            print(f"NoF***sBot: Here are the latest crypto news:\n{news}")
            speak(news)

        elif "weather" in user_input:
            city = input("Enter city for weather update: ")
            weather_info = fetch_weather(city)
            print("NoF***sBot: " + weather_info)
            speak(weather_info)

        elif "joke" in user_input:
            joke = fetch_random_joke()
            print("NoF***sBot: " + joke)
            speak(joke)

        elif "exit" in user_input:
            print("NoF***sBot: Goodbye, come back when you need more chaos.")
            speak("Goodbye, come back when you need more chaos.")
            break
        else:
            response = "NoF***sBot: Try asking about crypto, memes, sentiment analysis, news, weather, or jokes."
            print(response)
            speak(response)

if __name__ == "__main__":
    main()
