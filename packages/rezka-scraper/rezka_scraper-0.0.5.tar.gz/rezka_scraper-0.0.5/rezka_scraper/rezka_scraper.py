# rezka_scraper.py

import aiohttp
from bs4 import BeautifulSoup

class RezkaScraper:
    def __init__(self):
        self.base_url = "https://rezka.ag"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
        }

    async def search_rezka(self, name):
        search_url = f"{self.base_url}/search/?do=search&subaction=search&q={name}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(search_url, headers=self.headers) as response:
                    if response.status == 200:
                        text = await response.text()
                        soup = BeautifulSoup(text, "html.parser")
                        results = soup.find_all("div", class_="b-content__inline_item")
                        for result in results:
                            title_tag = result.find("div", class_="b-content__inline_item-link").find("a")
                            if title_tag:
                                title = title_tag.text.strip()
                                link = title_tag["href"]
                                if name.lower() in title.lower():
                                    return title, link
                        return None, None
                    else:
                        print("Ошибка: Не удалось выполнить поиск. Код статуса:", response.status)
                        return None, None
        except aiohttp.ClientError as e:
            print("Ошибка соединения с сервером:", str(e))
        except Exception as e:
            print("Произошла ошибка при обработке поиска:", str(e))
        return None, None

    async def search_anime(self, page=1):
        return await self._search_category("animation", page)

    async def search_movies(self, page=1):
        return await self._search_category("films", page)

    async def search_series(self, page=1):
        return await self._search_category("series", page)

    async def search_cartoons(self, page=1):
        return await self._search_category("cartoons", page)

    async def _search_category(self, category, page):
        url = f"{self.base_url}/{category}/page/{page}/"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, "html.parser")
                        results = soup.find_all("div", class_="b-content__inline_item")
                        matches = []
                        for result in results:
                            title_tag = result.find("div", class_="b-content__inline_item-link").find("a")
                            if title_tag:
                                title = title_tag.text.strip()
                                link = title_tag["href"]
                                matches.append((title, link))
                        return matches
                    else:
                        print("Ошибка: Не удалось загрузить категорию. Код статуса:", response.status)
                        return None
        except aiohttp.ClientError as e:
            print("Ошибка соединения с сервером:", str(e))
        except Exception as e:
            print("Произошла ошибка при обработке категории:", str(e))
        return None
