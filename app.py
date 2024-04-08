import http.client
import json
import random
import boto3
import requests
from dotenv import dotenv_values

load_dotenv()
config = dotenv_values(".env")


def fetch_quotes_from_api():
    # conn = http.client.HTTPSConnection("zenquotes.io")
    # conn.request("GET", "/api/quotes")
    # res = conn.getresponse()
    # data = res.read()
    # quotes = json.loads(data.decode("utf-8"))p

    response= requests.get("https://zenquotes.io/api/quotes")
    return response.json()


def find_random_quote(quotes):
    index = random.randint(0, len(quotes) - 1)
    return quotes[index]

def send_email(random_quote):
    sns_client = boto3.client('sns',
        aws_access_key_id=config["aws_access_key_id"],
        aws_secret_access_key=config["aws_secret_access_key"],
        region_name=config["region_name"])

    response = sns_client.publish(
        TopicArn="arn:aws:sns:us-west-2:381731343673:DailyQuote",
        Subject="Motivational Quote by Shreyas!",
        Message=random_quote['q'],
    )


def main():
    quotes = fetch_quotes_from_api()
    random_quote = find_random_quote(quotes)
    #print(f"\n\n{random_quote['q']=}")
    send_email(random_quote)


main()
