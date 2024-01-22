import httpx
from parse_olx import extract_details, extract_listings
from ai_parser import query_gpt_model
from bot_telegram import send_message_to_all
from read_config import get_chat_id_list
from persistence import AddItem,UpdateItemProperties
import asyncio
import json

async def send_multiple_msg(listings):
    chat_id_list = get_chat_id_list()
    async with httpx.AsyncClient() as client:
        for listing in listings:
            itemAdded = AddItem(listing['url'])
            if itemAdded == True:
                # Only send when item is not available yet
                message = ""
                print(f"Title: {listing['title']}\nURL: {listing['url']}\nPrice: {listing['price']}\n")
                message += ("URL: " + listing['url'] + "\n")
                response = await client.get(listing['url'])
                print(response)

                html_content = response.text
                item = extract_details(html_content)
                print(item)
                message += ("Luas: " + item["size"] + "\n")
                summary = query_gpt_model(item["size"],item["location"],item["description"])
                UpdateItemProperties(listing['url'],item["size"],item["location"],item["description"],listing['price'],json.dumps(summary))
                message += summary["choices"][0]["message"]["content"].replace("AA","\nHarga per m2").replace("BB","\nHarga total").replace("CC","\nLokasi")
                print(summary["choices"][0]["message"]["content"])
                print(summary["usage"])

                await send_message_to_all(chat_id_list, message)
                break
        if itemAdded == False:
            await send_message_to_all(chat_id_list, "Belum ada listing yang baru nih. Tunggu beberapa saat lagi ya...")

# URL of the web page to be scraped
url = 'https://www.olx.co.id/bali_g2000002/tanah_c4827?filter=p_certificate_eq_shm-sertifikathakmilik%2Ctype_eq_dijual&sorting=desc-creation'  # Replace with the actual URL
url = 'https://www.olx.co.id/ubud_g5000026/tanah_c4827?filter=p_certificate_eq_shm-sertifikathakmilik%2Ctype_eq_dijual&sorting=desc-creation'

def handler(event, context):
    try:
        # Fetching the web page content
        response = httpx.get(url)
        print(response)
        html_content = response.text

        # Extracting listings
        listings = extract_listings(html_content)
        #return {"statusCode": 200, "body": listings} # TODO: test only

        # Displaying the extracted listings (you can replace this with saving to a file or other operations)
        asyncio.run(send_multiple_msg(listings))

        print("\nTotal " + str(len(listings)) + " listings")
        return {"statusCode": 200, "body": "Message sent"}
    except Exception as e:
        # Handle exceptions (logging, retry logic, etc.)
        return {"statusCode": 500, "body": str(e)}
