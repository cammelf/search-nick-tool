#привет, зачем ты смотришь мой код, лан подпишись на t.me/cybertoolsteam !!! Прога работает чуток коряво.
import aiohttp
import asyncio
import json
import os
import re
from urllib.parse import quote
from colorama import Fore, Style, init

init(autoreset=True)

class UsernameSearch:
    def __init__(self):
        self.username = ""
        self.results = {}
        self.platforms = {
            "Twitter": "https://twitter.com/",
            "Instagram": "https://instagram.com/",
            "Facebook": "https://facebook.com/",
            "Reddit": "https://www.reddit.com/user/",
            "LinkedIn": "https://linkedin.com/in/",
            "TikTok": "https://tiktok.com/@",
            "Pinterest": "https://pinterest.com/",
            "VK": "https://vk.com/",
            "Odnoklassniki": "https://ok.ru/",
            "Flickr": "https://www.flickr.com/people/",
            
            
            "GitHub": "https://github.com/",
            "GitLab": "https://gitlab.com/",
            "StackOverflow": "https://stackoverflow.com/users/",
            "Bitbucket": "https://bitbucket.org/",
            "Dev.to": "https://dev.to/",
            "HackerRank": "https://hackerrank.com/",
            "LeetCode": "https://leetcode.com/",
            "Kaggle": "https://www.kaggle.com/",
            
            
            "Steam": "https://steamcommunity.com/id/",
            "Epic Games": "https://www.epicgames.com/account/",
            "Xbox": "https://xboxgamertag.com/search/",
            "PlayStation": "https://psnprofiles.com/",
            "Roblox": "https://www.roblox.com/user.aspx?username=",
            "Twitch": "https://twitch.tv/",
            
            
            "Яндекс.Дзен": "https://zen.yandex.ru/user/",
            "Habr": "https://habr.com/ru/users/",
            "VC.ru": "https://vc.ru/u/",
            "Pikabu": "https://pikabu.ru/@",
            "Rutube": "https://rutube.ru/channel/",
            
            
            "Telegram": "https://t.me/",
            "Spotify": "https://open.spotify.com/user/",
            "eBay": "https://www.ebay.com/usr/",
            "Amazon": "https://www.amazon.com/gp/profile/amzn1.account.",
            "Quora": "https://www.quora.com/profile/",
            "Medium": "https://medium.com/@",
            "Wikipedia": "https://en.wikipedia.org/wiki/User:"
        }

    async def check_platform(self, session, platform, url):
        try:
            full_url = url + quote(self.username)
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9"
            }
            
            async with session.get(full_url, headers=headers, timeout=6) as response:
                if response.status == 200:
                    text = await response.text()
                    
                    if not any(e in text.lower() for e in ["not found", "doesn't exist", "404", "error", "не найдено"]):
                        self.results[platform] = full_url
                        print(f"{Fore.GREEN}[+] {platform}: {full_url}{Style.RESET_ALL}")
                        
        except Exception:
            pass

    async def search_all(self):
        self.results = {}
        print(f"\n{Fore.CYAN}🔍 Поиск аккаунтов для: {self.username}{Style.RESET_ALL}")
        
        connector = aiohttp.TCPConnector(limit=50, force_close=True)
        timeout = aiohttp.ClientTimeout(total=30)
        
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            tasks = []
            for platform, url in self.platforms.items():
                tasks.append(self.check_platform(session, platform, url))
            
           
            for i in range(0, len(tasks), 50):
                await asyncio.gather(*tasks[i:i+50])
        
        print(f"\n{Fore.GREEN}✅ Найдено аккаунтов: {len(self.results)}{Style.RESET_ALL}")
        self.save_results()

    def save_results(self):
        if not self.results:
            return
            
        filename = f"{self.username}_found.json"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2, ensure_ascii=False)
            print(f"{Fore.CYAN}📁 Результаты сохранены в {filename}{Style.RESET_ALL}")
        except Exception:
            pass

def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""
{Fore.CYAN}
╔═╗╦ ╦╔═╗╔╗╔╔╦╗  ╔═╗╔═╗╔╦╗╔═╗╦═╗╔╦╗
╚═╗║ ║╠═╣║║║ ║║  ╚═╗║╣  ║ ║╣ ╠╦╝ ║ 
╚═╝╚═╝╩ ╩╝╚╝═╩╝  ╚═╝╚═╝ ╩ ╚═╝╩╚═ ╩ 
{Style.RESET_ALL}
{Fore.YELLOW}Поиск по нику
150+ платформ | Только реальные аккаунты{Style.RESET_ALL}
""")

async def main():
    print_banner()
    searcher = UsernameSearch()
    
    while True:
        username = input(f"\n{Fore.YELLOW}Введите никнейм (или 'exit' для выхода): {Style.RESET_ALL}").strip()
        if username.lower() == 'exit':
            break
            
        if username:
            searcher.username = username
            await searcher.search_all()
            input(f"\n{Fore.CYAN}Нажмите Enter для продолжения...{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Ошибка: введите никнейм{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Выход...{Style.RESET_ALL}")