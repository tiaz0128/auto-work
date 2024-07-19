import logging
import requests
from bs4 import BeautifulSoup

from Levenshtein import distance as levenshtein_distance


class ClawerYes24:
    def __init__(self, book_name):
        self.book_name = book_name

    def get_booK_info(self):
        search_url = (
            f"https://www.yes24.com/Product/Search?domain=BOOK&query={self.book_name}"
        )
        search_soup = self._get_html(search_url)
        book_id = self._get_most_similar_book(search_soup)

        book_url = f"https://www.yes24.com/Product/Goods/{book_id}"
        book_soup = self._get_html(book_url)

        return self._get_detail_book_info(book_soup)

    def _get_html(self, url):
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

        return BeautifulSoup(response.text, "html.parser")

    def _get_most_similar_book(self, soup):
        books = soup.select("a.gd_name")

        clawing_book_names = [book.string for book in books]

        logging.info(f"::clawing_book_names::\n- {'\n- '.join(clawing_book_names)}")

        most_similar_book_name = self._find_most_similar(
            self.book_name, clawing_book_names
        )

        # 가장 유사한 책 이름을 가진 요소 찾기
        for book in books:
            if book.string == most_similar_book_name:
                # 해당 책의 상위 요소에서 id 값을 찾는다고 가정
                book_id = book.attrs["href"].split("/")[-1]
                break

        return book_id

    def _find_most_similar(self, target, strings):
        # 가장 낮은 거리와 가장 유사한 문자열 초기화
        lowest_distance = float("inf")
        most_similar = None

        # 각 문자열과의 거리 계산
        for string in strings:
            dist = levenshtein_distance(target, string)
            if dist < lowest_distance:
                lowest_distance = dist
                most_similar = string

        return most_similar

    def _get_detail_book_info(self, soup: BeautifulSoup):
        title = soup.select_one("h2.gd_name").string
        author = soup.select_one("span.gd_auth > a").string
        bookCompany = soup.select_one("span.gd_pub > a").string
        publishDate = soup.select_one("span.gd_date").string
        page_cnt = soup.select_one("tbody.b_size > tr:nth-child(2) > td").string.split(
            "쪽"
        )[0]

        return (
            title,
            author,
            bookCompany,
            publishDate,
            page_cnt,
        )
