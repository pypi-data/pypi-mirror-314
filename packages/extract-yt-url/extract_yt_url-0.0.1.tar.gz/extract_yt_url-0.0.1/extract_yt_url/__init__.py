import requests
from bs4 import BeautifulSoup
from typing import List, Union
import json

# GPT 피셜 : 파이썬에서는 함수나 클래스에 대한 설명을 주석으로 작성하는 대신,
# 함수 내부에 작성된 docstring을 사용합니다.

class Extract_yt_url:
    def __init__(self, query: str, results: int = 1):
        self.query = query
        self.results = results
        self.url = self._search()

    # def __del__(self):
    #     del self.url
    
    def _search(self) -> List:
        """
        ▶ docstring ◀
        
        query (웹 클라이언트 요청)를 통해 문자열 검색 내용의
        Youtube 링크를 List 형태로 출력하는 함수.

        Parameters:
            query : 검색을 하고자 하는 문자열
            results : 반환할 링크의 수 (기본값 : 1, 범위 1 ~ 10)

        Returns:
            유튜브 링크가 포함된 리스트.
        """
        if not (1 <= self.results <= 10):
            raise ValueError("두 번째 parameter로 입력 가능한 숫자는 1 ~ 10 입니다.")

        # 검색 형식에 맞게 url 검색
        search_url = f"https://www.youtube.com/results?search_query={self.query.replace(' ', '+')}"

        # http 요청을 보내기
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
        }
        response = requests.get(search_url, headers=headers)

        if response.status_code != 200: # 성공적으로 요청을 받지 못함 (상태코드 HTTP 200이 아닌 경우)
            raise ConnectionError(f"Failed to retrieve search results: HTTP {response.status_code}")

        # HTML 전문
        text = requests.get(search_url).text

        start = (
            text.index("ytInitialData")
            + len("ytInitialData")
            + 3
        )
        end = text.index("};", start) + 1
        json_str = text[start:end]
        data = json.loads(json_str)
        links = []
        # Extract video links
        # json 형식 변환을 많이 참조했음. -> YoutubeSearch
        for contents in data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"]:
            for video in contents["itemSectionRenderer"]["contents"]:
                if "videoRenderer" in video.keys():
                    video_data = video.get("videoRenderer", {})
                    video_url = video_data.get("navigationEndpoint", {}).get("commandMetadata", {}).get("webCommandMetadata", {}).get("url", None)
                    video_url = "https://www.youtube.com" + video_url
                    links.append(video_url)
                    self.results -= 1
                    if self.results <= 0:
                        return links
                
        return links

    def to_list(self):
        return self.url
    
    def to_string(self):
        return self.url[0]