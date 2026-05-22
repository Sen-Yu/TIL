# 먼저 터미널에 설치 필요: pip install fastapi uvicorn httpx
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import httpx

app = FastAPI()

# 실제 목적지 서버 정보 (소켓 코드 설정 계승)
SERVER_HOST = 'example.com'  
SERVER_PORT = 80
TARGET_HOST = "https://example.com" 

class ModelInferenceProxyMiddleware(BaseHTTPMiddleware):
    """
    [프록시 미들웨어 클래스]
    기능: 소켓 handle_client 함수처럼 모든 HTTP 요청을 중간에 가로채서 
          '클라이언트 -> 미들웨어 -> 목적지 서버 -> 미들웨어 -> 클라이언트' 구조로 중계합니다.
    """
    async def dispatch(self, request: Request, call_next):
        # ----------------------------------------------------------------
        # 1. 클라이언트로부터 들어오는 요청 경로 확인 및 가로채기
        # ----------------------------------------------------------------
        path = request.url.path
        
        # 💡 [핵심 교정] curl -x 프록시 모드로 요청이 오면 path 변수에 'http://example.com' 주소가 통째로 꼬여서 들어옵니다.
        # 따라서 단순 일치(== "/")가 아닌, 포함 관계("example.com" in path)를 추가하여 어떤 유입이든 완벽하게 낚아챕니다.
        if path == "/" or "example.com" in path:
            print(f"[*] 클라이언트 요청 가로챔: {path}")

            # 클라이언트가 보낸 본문(Body) 데이터 읽어오기
            body = await request.body()
            # 클라이언트가 보낸 헤더 복사
            headers = dict(request.headers)
            
            # 호스트 헤더를 목적지 서버 주소 규격에 맞춥니다 (부호 '://'가 없는 순수 도메인 형태)
            headers["host"] = SERVER_HOST

            # ----------------------------------------------------------------
            # 2 & 3. 실제 목적지 서버(TARGET_HOST)에 연결 및 요청 전달
            # ----------------------------------------------------------------
            # [httpx.AsyncClient()] 
            # - 기능: 소켓의 socket() 및 connect() 역할을 하는 비동기 HTTP 클라이언트 생성
            async with httpx.AsyncClient() as target_socket:
                # 내부적으로 경로가 꼬여서 주소가 무너지지 않도록, 타겟 주소를 확실하게 빌드합니다.
                target_url = f"{TARGET_HOST}/"
                
                # [target_socket.request()]
                # - 기능: 소켓의 sendall() 역할. 가로챈 데이터와 헤더를 목적지 서버로 토스합니다.
                target_response = await target_socket.request(
                    method=request.method,
                    url=target_url,
                    headers=headers,
                    content=body,
                    params=request.query_params
                )

            # ----------------------------------------------------------------
            # 4. 목적지 서버가 준 응답을 받아오기 (소켓의 recv 역할)
            # ----------------------------------------------------------------
            print("[*] 목적지 서버로부터 응답 수신 완료")
            
            # 목적지 서버가 돌려준 결과를 FastAPI의 Response 객체로 패킹
            response = Response(
                content=target_response.content,
                status_code=target_response.status_code,
                headers=dict(target_response.headers)
            )
            
            # ----------------------------------------------------------------
            # 5. 최종 응답을 클라이언트에게 반환 및 자원 해제
            # ----------------------------------------------------------------
            return response

        # 지정한 경로가 아닌 일반 내부 요청 등은 본래 가려던 라우터로 그대로 통과시킵니다.
        response = await call_next(request)
        return response

# ----------------------------------------------------------------
# 미들웨어 등록 (서버 시작 시 이 파이프라인을 가장 먼저 거치게 됨)
# ----------------------------------------------------------------
app.add_middleware(ModelInferenceProxyMiddleware)

# 테스트용 로컬 엔드포인트
@app.get("/")
async def index():
    return {"message": "프록시 미들웨어가 작동 중입니다."}

if __name__ == "__main__":
    import uvicorn
    # 127.0.0.1 주소와 8888 포트로 올바르게 바인딩하여 서버 구동
    uvicorn.run(app, host="127.0.0.1", port=8888)


"""

                    [테스트 방법]

    1. 해당 미들웨어 파일 실행 (uv run python main.py)

    2. 터미널 에서 아래 명령어 입력 (질문자님이 요구하신 원본 형태 그대로)
        # 프록시 서버(127.0.0.1:8888)를 거쳐 실제 웹사이트(http://example.com)의 HTML 데이터를 가져오라고 명령
        curl -x http://127.0.0.1:8888 http://example.com

"""
