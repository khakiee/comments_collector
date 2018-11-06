## Comment Collector
### requirements
* Chrome driver - https://chromedriver.storage.googleapis.com/index.html?path=2.43/
* PhantomJS - http://phantomjs.org/download.html
* Selenium - included in .venv
* bs4(Beautiful soap) - included in .venv

### Introduce
* 네이버 기사 댓글 수집기입니다.
* INITIAL_URL로 설정된 news 페이지(https://entertain.naver.com/ranking)에서 1위부터 30위까지의 뉴스를 차례로 클릭하며 댓글을 수집합니다.
* 30위까지의 수집이 끝나면 하루 전의 랭크로 이동하여 반복 작업합니다.

### How to run
1. requirements의 Chrome driver 혹은 PhantomJS를 운영체제에 맞는 버전으로 다운로드
2. requirements.txt 로 python package install

    ```pip install -r requirements.txt```

3. collector.py를 실행
4. 파일 생성시의 time으로 라벨이 붙어 파일 생성