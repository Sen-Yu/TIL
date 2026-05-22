# 이번주 주제
Fetch API를 사용해 서버에 모델 추론 요청을 보낼 때, 브라우저 CORS 정책이 어떤 제약을 주는지 설명하고, 이를 해결하기 위한 서버/클라이언트 측 전략을 서술하시오.
---

## 1. 주제 분석
----

- Fetch API
	- fetch
		- 비동기 요청을 진행하고, 응답을 취하는 행동
		- 서버로 요청 메세지를 전송하고, 응답 메세지를 기다리는 텀동안 다른 처리 가능
	- fetch api
		- 외부와 프로그램을 연결해줌
		- 프로그램으로 외부에 요청을 보내고, 외부의 응답을 받아 프로그램이 이를 처리한다
		- ex)python의 HTTP 클라이언트 프레임워크인 HTTPX ,JS는 fetch

```
import httpx
import asyncio

async def fetch_data(url):
    # 1. 비동기 HTTP/2프로토콜로 비동기 HTTP 요청하기
    async with httpx.AsyncClient(http2=True) as client:
        # 2. 비동기 통신 대기 (이 동안 CPU는 멈추지 않고 다른 일을 처리함)
        response = await client.get(url)
        return response.status_code

async def main():
    # 3. 100개의 요청을 동시에 날리기! (비동기 병렬 처리)
    urls = ["https://httpbin.org/get" for _ in range(10)]
    results = await asyncio.gather(*(fetch_data(url) for url in urls))
    print("비동기 동시 완료 결과:", results)

if __name__ == "__main__":
    asyncio.run(main())

```

url ="https://example.com"
response = request.get(url)


- CORS(교차 출처 리소스 공유 정책)
	- 헤더의 URL에서 scheme, host , port 중 하나라도 다르다면 다른 컴퓨터로 취함
	- 보안: 인증되지않은 출처에 대해 데이터 탈취,수정 방지
	- 데이터 공유: 
- 모델 추론 요청: 작업(질문)에 대한 결과(답)요청

## 2. 주제 요약
python에서 HTTPX를 이용해서  CORS정책은 위반되는 경우 또는 기능이 제한되는 경우 

## 3. 문제 분석
1. 클라이언트가 요청을 보내고 응답을 받았을때 scheme, host , port 중 하나라도 다르다.
		- http로 요청을 보냈는데 https로 응답할때,


과거에 프론트엔드,백엔드 구분 없어서 같은 도메인 안에서 처리됨-> 다른출처는 보안상 문제로보임
-> 클라이언트가 api로 직접 호출하기 시작 -> 클라이언트랑 api는 서로 다른 도메인 경우가 많다.
-> 출처가 다르더라도 통신이 가능하게 서버에 리소스 호출이 허용된출처(Origin)을 명시해서


## 4. 문제 해결책
1. 서버에서 Access-Control-Allow-Origin 응답 헤더 세팅
	1. 요청을 수락할 출처를 명시적으로 지정(범용적인 추)
		예)검증된 사람을 목록에 저장
		동작방식 
		클라이언트는 Origin 헤더와 함께 요청하고, 서버는 Access-Control-Allow-Origin헤더아 함께 응답한다.클라이언트는 둘을 비교하고 유효하지않으면 CORS 에러 발생시킨다.
		그러면 클라이언트에서 강제로 Origin을 위조한다면? 브라우저에서 이를 감지하고 차단한다.
2. 프록시 서버 사용
	1. 웹 어플리케이션이 직접 요청
	2. 에)http://example.com 의 웹어플리케이션(브라우저)이 httl://api.com에 데이터 요청하면, 웹어플리케이션이 직접 요청하는대신 프록시서버를 만들어서 api요청을 중계하도록 설정
