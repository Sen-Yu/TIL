import socket
import threading

# 프록시 설정
PROXY_HOST = '127.0.0.1'
PROXY_PORT = 8888
# 요청을 전달할 실제 목적지 서버(Ai model server)
TARGET_HOST = 'example.com'  
TARGET_PORT = 80



"""
    [워커 스레드 함수]
    기능: 연결된 개별 클라이언트와 1:1로 매칭되어 
          '클라이언트 -> 프록시 -> 목적지 서버 -> 프록시 -> 클라이언트' 구조로 데이터를 중계합니다.    
"""

def handle_client(client_socket):
    # 1. 클라이언트로부터 요청 데이터 수신(가로챔)
    # 데이터 수신시, 클라이언트 소켓에서 데이터의 4096바이트만큼 읽음(read)
    request = client_socket.recv(4096)

    # 데이터가 빈경우로 클라이언트가 종료한경우
    if not request:
        client_socket.close()
        return

    #
    print(f"[*] 클라이언트 요청 가로챔:\n{request.decode('utf-8', errors='ignore')[:200]}...")

    # 2. 실제 목적지 서버(Target)에 연결 및 요청 전달
    target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    target_socket.connect((TARGET_HOST, TARGET_PORT))
    target_socket.sendall(request)

    # 3. 목적지 서버로부터 응답 수신
    while True:
        response = target_socket.recv(4096)
        if len(response) > 0:
            # 4. 클라이언트에게 응답 송신
            client_socket.sendall(response)
        else:
            break

    # 소켓 닫기
    target_socket.close()
    client_socket.close()

def start_proxy():
    # 소켓 생성 및 초기화()
    #socket.AF_INET: IPv4체계 사용, socket.SOCK_STREAM: 전송방식 TCP사용
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 소켓에 host와 port 할당
    server.bind((PROXY_HOST, PROXY_PORT))
    # 소켓을 클라이언트의 접속 요청 대기상태로 설정(요청 대기 큐의 크기를 5개 설정)
    server.listen(5)
    print(f"[*] 프록시 서버 시작됨 ({PROXY_HOST}:{PROXY_PORT}) -> 목적지: {TARGET_HOST}")

    while True:
        # 클라이언트의 접속 요청을 수락 -> 접속 성공하면 클라이언트의 소켓과 주소정보를 튜플 방식으로 할당받음
        client_sock, addr = server.accept()
        # ip:prot
        print(f"[*] 연결 접수됨: {addr[0]}:{addr[1]}")
        # 동시 처리를 위해 스레드 생성
        proxy_thread = threading.Thread(target=handle_client, args=(client_sock,))
        proxy_thread.start()

if __name__ == "__main__":
    start_proxy()


"""

                    [테스트 방법]

    1. 해당 프록시 서버 파일 실행

    2. 터미널 에서 아래 명령어 입력
        # 프록시 서버(127.0.0.1:8888)를 거쳐 실제 웹사이트(http://example.com)의 HTML 데이터를 가져오라고 명령
        curl -x http://127.0.0.1:8888 http://example.com

"""