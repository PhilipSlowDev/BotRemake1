# [[ LIBRARIES ]]
import time
import os
from discord_webhook import DiscordWebhook, DiscordEmbed
from vintedAPI import Vinted
import utils


# [[ CONFIG ]]
WEBHOOK_URL = "https://discord.com/api/webhooks/1268119483810185307/5XzCCrSHH4xR3Iib-97pcB-zIMCl4EhlUaSlBWuDOMOIac5mxI6nfSngvx3TOC8sl9M4"
os.system("title Vinted Scraping $_$ By N0RZE")

banner = r"""
            /$$             /$$                     /$$
           |__/            | $$                    | $$
 /$$    /$$ /$$ /$$$$$$$  /$$$$$$    /$$$$$$   /$$$$$$$
|  $$  /$$/| $$| $$__  $$|_  $$_/   /$$__  $$ /$$__  $$
 \  $$/$$/ | $$| $$  \ $$  | $$    | $$$$$$$$| $$  | $$
  \  $$$/  | $$| $$  | $$  | $$ /$$| $$_____/| $$  | $$
   \  $/   | $$| $$  | $$  |  $$$$/|  $$$$$$$|  $$$$$$$
    \_/    |__/|__/  |__/   \___/   \_______/ \_______/

                🤑 Vinted Bot v1
                    By Norze

""".replace("$", utils.PURPLE + "$" + utils.WHITE).replace("_", utils.RED + "_" + utils.WHITE).replace("|", utils.RED + "|" + utils.WHITE).replace("/", utils.RED + "/" + utils.WHITE).replace("\\", utils.RED + "\\" + utils.WHITE)
print(banner)

sent_items = []
allowed_brands = [
    "Burberry", "Balenciaga", "Louis Vuitton", "Givenchy", "Gucci", "Arcteryx",
    "Valentino", "Valentino Garavani", "Yeezy", "Dolce & Gabbana", "Dior", "Fendi",
    "Palm Angels", "Off white", "Moncler", "Golden Goose", "Prada", "Loro Piana",
    "Brioni", "Kiton"
]

allowed_country_code = "pl"
allowed_price = 100


# [[ MAIN CODE ]]
def main():
    while True:
        try:
            time.sleep(3)
            vinted = Vinted(country_code=allowed_country_code)
            search_url = f"https://www.vinted.{allowed_country_code}/vetements?order=newest_first&price_to={allowed_price}"
            items = vinted.items.search(search_url, 10, 1)
            
            if not items:
                print("[INFO] No items fetched.")
                continue
            
            for item in items:
                brand_title = item.brand_title.lower() if item.brand_title else ""
                print(f"[DEBUG] Processing item: {item.id}, Brand: {brand_title}")

                if any(brand.lower() == brand_title for brand in allowed_brands) and item.id not in sent_items:
                    print(f"[INFO] Matched item: {item.id}, Brand: {brand_title}")
                    sent_items.append(item.id)
                    
                    title = item.title or "Not found"
                    screen = item.photo or "Not found"
                    brand = item.brand_title or "Not found"
                    price = f"{item.price}€" or "Not found"
                    url = item.url or "Not found"
                    create = item.created_at_ts.strftime("%Y-%m-%d %H:%M:%S") if item.created_at_ts else "Not found"

                    print(f"[DEBUG] Sending webhook: title={title}, price={price}, brand={brand}, url={url}, create={create}")
                    
                    webhook = DiscordWebhook(url=WEBHOOK_URL)
                    embed = DiscordEmbed(title="", description=f"**[{title}]({url})**", color=3447003)
                    embed.add_embed_field(name="Publication", value=create, inline=True)
                    embed.add_embed_field(name="Marque", value=brand, inline=True)
                    embed.add_embed_field(name="Prix", value=price, inline=True)
                    embed.set_thumbnail(url="https://media.tenor.com/zSLwaBJxfXcAAAAM/oh-my-god.gif")
                    embed.set_image(url=screen)
                    embed.set_footer(text="Bot Vinted by Norze")

                    webhook.add_embed(embed)
                    response = webhook.execute()

                    if response.status_code == 200:
                        print('[+] Embed sent successfully.')
                    else:
                        print('[-] Failed to send embed. Status code:', response.status_code)
                else:
                    print(f"[INFO] Item {item.id} already shown or not a target brand (Brand: {brand_title})")

        except Exception as e:
            print("[ERROR] Exception occurred:", str(e))


# [[ ALIVE ]]
if __name__ == "__main__":
    main()