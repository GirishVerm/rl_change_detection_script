import requests
import asyncio
import httpx
from bs4 import BeautifulSoup
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
URL = 'https://rl.insider.gg/en/pc/cars/fennec'

last_prices = {}

async def send_discord_message(content):
    webhook_url = 'https://discord.com/api/webhooks/1107420897981255730/JuApgcKhy0XdHuwIPcDKhcu8N8hgHKERC1m5vvyI80pD9rrBr7htfnwrK3-txnWwFG2y'
    data = {
        'content': content
    }
    response = requests.post(webhook_url, data=json.dumps(data), headers={"Content-Type": "application/json"})
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Payload delivered successfully, code {}.".format(response.status_code))

async def check_price(url):
    
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    try:
        async with httpx.AsyncClient() as client:

            page = await client.get(url, headers=headers)
            soup = BeautifulSoup(page.content, 'html.parser')
            price_range = soup.find('td', attrs={'class': "pfData"}).text.strip()
            print(price_range)

            if url in last_prices and price_range != last_prices[url]:
                await send_discord_message("The price for ITEM_TAG has been changed, take a look\n" + url)
                last_prices[url] = price_range
                return
        
            last_prices[url] = price_range
    except httpx.ConnectError as e:
        print(f'Connection error when trying to get {url}: {e}')
        return
    except Exception as e:
        print(f'An unexpected error occurred: {e}')
        return
    


urls_to_monitor = [
    'https://rl.insider.gg/en/pc/cars/fennec',
    'https://rl.insider.gg/en/pc/antennas/beta_reward_gold_nugget',
    'https://rl.insider.gg/en/pc/wheels/dieci/uncommon/black'

]

async def main():
    while True:
        await asyncio.gather(*(check_price(url) for url in urls_to_monitor))
        await asyncio.sleep(15*60)

asyncio.run(main())