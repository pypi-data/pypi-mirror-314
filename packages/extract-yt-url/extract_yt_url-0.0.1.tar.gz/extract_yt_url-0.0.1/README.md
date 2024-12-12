# extract_yt_url
training module

## 추가 설명
사용자로부터 문자열을 입력받으면 해당 문자열과 관련된   
유튜브 링크를 찾아 문자열 또는 리스트로 반환하는   
기능을 구현한 라이브러리 모듈

## 사용 전 주의사항
```
pip install extract_yt_url
```
파이썬 버전은 3.6 이상 지원

## 기본 사용법
```
import Extract_yt_url from extract_yt_url
text1 = Extract_yt_url("Break Out").to_string()
list1 = Extract_yt_url("Break Out").to_list()
print(text1)
print(list1)
```

## 참고 자료
https://packaging.python.org/en/latest/tutorials/packaging-projects/#uploading-your-project-to-pypi   
https://github.com/joetats/youtube_search   
(MIT License - Copyright (c) 2019 joe tats)   
https://wikidocs.net/197255   

