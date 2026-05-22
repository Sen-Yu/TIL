# 이번주 주제
---

**Fetch API**를 사용해 서버에 **모델 추론 요청**을 보낼 때, 브라우저 **CORS 정책**이 어떤 제약을 주는지 설명하고, 이를 해결하기 위한 서버/클라이언트 측 전략을 서술하시오.


## 1. 주제 분석
---
- Fetch API
	- fetch
		- 비동기 요청을 진행하고, 응답을 취하는 행동
		- 서버로 요청 메세지를 전송하고, 응답 메세지를 기다리는 텀동안 다른 처리 가능
	- fetch api
		- 외부와 프로그램을 연결해줌
		- 프로그램으로 외부에 요청을 보내고, 외부의 응답을 받아 프로그램이 이를 처리한다
		- ex)python의 HTTP 클라이언트 프레임워크인 HTTPX ,JS는 fetch

- CORS(교차 출처 리소스 공유 정책)
	- 헤더의 URL에서 scheme, host , port 중 하나라도 다르다면 다른 컴퓨터로 취함
	- 보안: 인증되지않은 출처에 대해 데이터 탈취,수정 방지

- 모델 추론 요청: 작업(질문)에 대한 결과(답)요청

## 2. 비슷한 다른 사례     
---
	예) 서비스 도메인에서의 예 
	현재 페이지:  http://payment.com       (결제 도메인)
	요청 목적지:  http://auth.com/verify   (인증 도메인)

	protocol: http  == http   ✅
	host:  payment.com  ≠  auth.com   ❌  ← 여기서 차단

## 3. 문제 분석    
---
1. 클라이언트가 요청을 보내고 응답을 받을때 URL의 도메인(host)이 달라서 CORS정책에 걸린다

	과거에 프론트엔드,백엔드 구분 없어서 같은 도메인 안에서 처리됨    
	-> 다른출처는 보안상 문제로보임    
	-> 클라이언트가 api로 직접 호출하기 시작     
	-> 오늘날 오면서 기능과 운영의 확장으로 구분을 위해서 클라이언트랑 api는 서로 다른 도메인 경우가 많다.


## 4. 문제 해결책  
---
1. 클라이언트에서 프록시 서버 사용  
	중개자를 선언해서 중개자 대신 처리    
	- 동작방식          
		1. 클라이언트의 HTTP 요청 전송    
		2. 프록시서버가 클라이언트의 HTTP 요청을 가로챔    
		3. 목적지 서버로 HTTP 요청 전송   
		4. 목적지 서버는 HTTP 요청을 수행하고 HTTP 응답을 프록시 서버에게 전달    
		5. 프록시 서버는 클라이언트에게 HTTP요청을 보냄     
	- 코드 예시            
		- https://github.com/Sen-Yu/TIL/blob/main/KTB4/Deep_Dive/2nd_Week/proxy_server.py        
		- https://github.com/Sen-Yu/TIL/blob/main/KTB4/Deep_Dive/2nd_Week/middleware_fastapi.py         

2. 서버에서 Access-Control-Allow-Origin 응답 헤더 세팅
	요청을 수락할 출처를 명시적으로 지정(검증된 사람을 목록에 저장)   
	- 동작방식                 
		1.클라이언트는 Origin 헤더와 함께 HTTP 요청    
		2.서버는 HTTP 요청을 수신하고 Access-Control-Allow-Origin헤더와 함께 HTTP 응답 송신            
		3. 클라이언트는 Origin 헤더와 Access-Control-Allow-Origin 헤더를 비교하고 유효하지않으면 CORS 에러 발생시킨다.                
	- 코드 예시              
		- https://github.com/Sen-Yu/TIL/blob/main/KTB4/Deep_Dive/2nd_Week/cors_middleware.py     
	- 그러면 클라이언트에서 강제로 Origin을 위조한다면?               
		- 브라우저에서 이를 감지하고 차단한다.            

![image](.proxy_vs_cors_middleware.svg)



## 5. 해결책 핵심 요약
---
### 프록시 vs CORS 미들웨어 비교

| 구분 | 프록시 서버 | CORS 미들웨어 |
|------|------------|--------------|
| **해결 원리** | CORS를 우회 | CORS를 허용 |
| **적용 위치** | 클라이언트와 서버 사이 | 목적지 서버 내부 |
| **서버 수정 필요** | ❌ 불필요 | ✅ 필요 |
| **브라우저 관여** | 브라우저는 같은 출처로 인식 | 브라우저가 헤더를 보고 허용 |
| **Preflight 처리** | 프록시가 대신 처리 | 미들웨어가 OPTIONS 자동 응답 |
| **보안** | 프록시 서버 보안 별도 관리 필요 | `allow_origins` 로 출처 제한 가능 |
| **적합한 상황** | 외부 API, 수정 불가 서버 | 내가 직접 운영하는 서버 |
| **구현 복잡도** | 높음 (서버 별도 구축) | 낮음 (코드 몇 줄) |
