from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # 검증 지점 지적
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/inference")
async def inference():
    return {"result": "모델 추론 응답"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8888)




"""
1. 해당 코드 실행

2. 터미널 실행 명령어
curl -X OPTIONS http://127.0.0.1:8888/inference \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: POST" \
  -v

  
3. 터미널 실행 결과(정상)
*   Trying 127.0.0.1:8888...
* Connected to 127.0.0.1 (127.0.0.1) port 8888
> OPTIONS /inference HTTP/1.1
> Host: 127.0.0.1:8888
> User-Agent: curl/8.7.1
> Accept: */*
> Origin: http://localhost:3000
> Access-Control-Request-Method: POST
> 
* Request completely sent off
< HTTP/1.1 200 OK
< date: Fri, 22 May 2026 06:03:27 GMT
< server: uvicorn
< vary: Origin
< access-control-allow-methods: DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT
< access-control-max-age: 600
< access-control-allow-origin: http://localhost:3000
< content-length: 2
< content-type: text/plain; charset=utf-8
< 
* Connection #0 to host 127.0.0.1 left intact
OK%             
"""