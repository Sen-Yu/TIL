# 🐳 주니어 개발자를 위한 Docker 핵심 실무 가이드

> **작성자**: 시니어 개발자  
> **대상**: Docker를 처음 접하거나 실무 도입이 필요한 주니어 개발자  
> **목표**: "내 로컬에서는 잘 돌아가는데 왜 서버에서는 안 되지?"라는 문제를 완벽히 해결하고, 컨테이너 기반 개발의 기본기를 다진다.

---

## 1. Docker란 무엇이고, 왜 쓰는가?

### 1.1 Docker의 등장 배경
전통적인 개발 환경에서는 흔히 이런 문제가 발생합니다:
- **"내 컴퓨터(Mac)에서는 잘 되는데, 팀원 컴퓨터(Windows)나 운영 서버(Linux)에서는 에러가 나요."**
- OS 차이, 설치된 라이브러리/런타임 버전(예: Node 18 vs Node 20, Python 3.9 vs 3.11), 환경 변수 불일치 때문입니다.

**Docker(도커)**는 애플리케이션과 이를 실행하는 데 필요한 모든 종속성(런타임, 시스템 도구, 라이브러리, 설정 등)을 하나로 묶어 **어떤 환경에서든 동일하게 실행되도록 보장하는 컨테이너 가상화 플랫폼**입니다.

### 1.2 가상머신(VM) vs Docker 컨테이너

| 구분 | 가상머신 (VM, e.g. VMware, VirtualBox) | 도커 컨테이너 (Docker Container) |
| :--- | :--- | :--- |
| **구조** | Host OS 위 하이퍼바이저 + **게스트 OS 전체 포함** | Host OS의 **커널(Kernel)을 공유**하고 프로세스만 격리 |
| **무게/용량** | 수 GB ~ 수십 GB (OS 전체가 포함되므로 매우 무거움) | 수십 MB ~ 수백 MB (필요한 파일과 바이너리만 포함) |
| **부팅 속도** | 분 단위 (OS 부팅 과정 필요) | 초/밀리초 단위 (단순 프로세스 실행 수준) |
| **성능 오버헤드**| 하이퍼바이저 레이어로 인한 성능 저하 발생 | 네이티브에 가까운 거의 무손실 성능 |

```
[가상머신 (VM)]                     [도커 컨테이너 (Docker)]
+---------------------------+       +---------------------------+
| App A   | App B   | App C |       | App A   | App B   | App C |
+---------+---------+-------+       +---------+---------+-------+
| GuestOS | GuestOS | GuestOS|       |  Bins / Libs / Deps       |
+---------+---------+-------+       +---------------------------+
|      Hypervisor           |       |       Docker Engine       |
+---------------------------+       +---------------------------+
|         Host OS           |       |          Host OS          |
+---------------------------+       +---------------------------+
|        하드웨어            |       |         하드웨어           |
+---------------------------+       +---------------------------+
```

---

## 2. Docker 핵심 3대 개념 (레시피 - 빵틀 - 빵)

도커를 이해할 때 가장 유명하고 직관적인 비유는 **"레시피 - 붕어빵 틀 - 붕어빵"**입니다.

1. **Dockerfile (레시피)**
   - 컨테이너 이미지를 어떻게 빌드할지 단계별로 작성한 텍스트 설정 파일.
2. **Docker Image (붕어빵 틀 / 불변의 템플릿)**
   - 애플리케이션과 실행 환경이 패키징된 정적 스냅샷.
   - 읽기 전용(Read-Only)이며 한 번 생성되면 변경되지 않습니다.
3. **Docker Container (붕어빵 / 실행 인스턴스)**
   - 이미지를 기반으로 격리된 환경에서 실행되는 실제 프로세스.
   - 하나의 이미지로 여러 개의 독립된 컨테이너를 찍어낼 수 있습니다.
   - 실행 중 생성/수정되는 파일은 컨테이너만의 쓰기 가능한 레이어(Read-Write Layer)에 기록됩니다.

---

## 3. Dockerfile 문법 & 예제

Dockerfile은 위에서 아래로 한 줄씩 실행되며, 각 단계마다 레이어(Layer) 캐시를 생성합니다.

### 3.1 주요 키워드

| 키워드 | 역할 | 실무 팁 |
| :--- | :--- | :--- |
| `FROM` | 베이스 이미지 지정 | 경량화된 `alpine`이나 `slim` 태그 사용 권장 |
| `WORKDIR` | 작업 디렉토리 설정 | `RUN cd /app` 대신 반드시 `WORKDIR` 사용 |
| `COPY` | 로컬 파일들을 이미지 내부로 복사 | 캐시 효율을 위해 자주 변경되지 않는 종속성 파일(e.g., `package.json`, `requirements.txt`)을 소스코드보다 먼저 복사 |
| `RUN` | 이미지 빌드 시점에 실행할 쉘 명령어 | 레이어 수를 줄이기 위해 `&&`로 연결 권장 |
| `ENV` | 컨테이너 환경 변수 설정 | 빌드 시점 및 런타임에 모두 유지됨 |
| `EXPOSE` | 컨테이너가 리스닝할 포트 문서화 | 실제 포트 개방은 `docker run -p` 옵션으로 수행 |
| `CMD` | 컨테이너 실행 시 기본 명령 | `docker run` 실행 시 인자로 덮어쓰기 가능 |
| `ENTRYPOINT`| 컨테이너가 실행될 때 무조건 실행될 명령어 | `CMD`와 함께 사용하여 기본 인자를 전달하는 구조로 자주 활용 |

### 3.2 Dockerfile 예제 (Node.js 웹 서버 기준)

```dockerfile
# 1. 가볍고 안전한 베이스 이미지 선택
FROM node:20-alpine

# 2. 컨테이너 내부 작업 폴더 지정
WORKDIR /app

# 3. 의존성 파일 먼저 복사 (소스코드 수정 시 의존성 설치 캐시 재활용)
COPY package*.json ./
RUN npm ci --only=production

# 4. 소스 코드 복사
COPY . .

# 5. 포트 노출 선언 (문서화 목적)
EXPOSE 3000

# 6. 컨테이너 기동 시 실행할 커맨드
CMD ["node", "server.js"]
```

---

## 4. 데이터 영속성 (Docker Volume) & 네트워크

### 4.1 데이터 볼륨 (Volume)
컨테이너는 기본적으로 **Stateless(무상태)** 지향입니다. 즉, 컨테이너가 삭제되면 컨테이너 내부에서 생성되거나 변경된 데이터도 함께 사라집니다.  
DB 데이터나 업로드 파일처럼 **영구 저장되어야 하는 데이터**는 호스트 시스템에 마운트해야 합니다.

1. **Named Volume (도커가 관리하는 영역에 저장)**
   - `docker run -v my_db_data:/var/lib/mysql mysql:8`
   - 도커 관리 영역(`/var/lib/docker/volumes/...`)에 안전하게 저장되며 성능이 우수함.
2. **Bind Mount (호스트의 특정 디렉토리를 직접 연결)**
   - `docker run -v /Users/dev/project:/app my-image`
   - 로컬 코드를 실시간으로 컨테이너에 반영하며 개발할 때 매우 유용.

### 4.2 네트워크 (Network)
- 컨테이너들은 기본적으로 독립된 네트워크 네임스페이스를 가집니다.
- 별도 설정을 하지 않으면 기본 `bridge` 네트워크를 사용합니다.
- 여러 컨테이너 간 안전하고 편리한 통신(IP 대신 컨테이너 이름으로 통신)을 위해 **사용자 정의 네트워크(Custom Bridge Network)** 또는 **Docker Compose**를 사용합니다.

---

## 5. Docker Compose: 여러 컨테이너 묶어 관리하기

현대 애플리케이션은 단일 컨테이너로 끝나지 않습니다. (예: Web App + MySQL + Redis)  
이들을 매번 복잡한 `docker run` 명령어로 실행하는 대신, 하나의 YAML 파일로 정의하고 일괄 제어하는 도구가 **Docker Compose**입니다.

### 5.1 `docker-compose.yml` 예제

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8080:3000"       # 호스트 8080 -> 컨테이너 3000
    environment:
      - DB_HOST=db
      - DB_PORT=3306
    depends_on:
      - db
    networks:
      - app-network

  db:
    image: mysql:8.0
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: secretpassword
      MYSQL_DATABASE: myapp
    volumes:
      - db_data:/var/lib/mysql
    networks:
      - app-network

volumes:
  db_data:

networks:
  app-network:
    driver: bridge
```

> **핵심 포인트**: `web` 컨테이너는 IP를 몰라도 서비스 이름인 `db`라는 도메인으로 MySQL에 바로 접속할 수 있습니다 (Docker 내장 DNS 기능).

---

## 6. 실무 필수 Docker 명령어 치트시트 (Cheatsheet)

### 6.1 이미지(Image) 명령어

| 명령어 | 설명 | 예시 |
| :--- | :--- | :--- |
| `docker build` | Dockerfile로부터 이미지 빌드 | `docker build -t myapp:1.0 .` |
| `docker images` | 로컬 이미지 목록 확인 | `docker images` |
| `docker pull` | 원격 저장소(Docker Hub 등)에서 이미지 다운로드 | `docker pull redis:alpine` |
| `docker rmi` | 로컬 이미지 삭제 | `docker rmi myapp:1.0` |

### 6.2 컨테이너(Container) 라이프사이클 명령어

| 명령어 | 설명 | 예시 |
| :--- | :--- | :--- |
| `docker run` | 새 컨테이너 생성 및 실행 | `docker run -d -p 8080:80 --name my-nginx nginx` |
| `docker ps` | 실행 중인 컨테이너 목록 조회 | `docker ps` |
| `docker ps -a` | 종료된 컨테이너를 포함한 전체 목록 조회 | `docker ps -a` |
| `docker stop` | 실행 중인 컨테이너 정상 종료 (SIGTERM) | `docker stop my-nginx` |
| `docker start` | 멈춰 있는 컨테이너 재시작 | `docker start my-nginx` |
| `docker restart` | 컨테이너 재시동 | `docker restart my-nginx` |
| `docker rm` | 컨테이너 삭제 (정지 상태여야 함) | `docker rm my-nginx` |
| `docker rm -f` | 실행 중인 컨테이너 강제 삭제 (SIGKILL) | `docker rm -f my-nginx` |

#### `docker run`의 핵심 옵션 모음
- `-d` (Detached): 백그라운드에서 실행
- `-p 호스트포트:컨테이너포트`: 포트 포워딩 (예: `-p 3000:80`)
- `-v 호스트경로:컨테이너경로`: 볼륨 마운트
- `--name 컨테이너명`: 컨테이너에 알아보기 쉬운 이름 부여
- `-e KEY=VALUE`: 환경 변수 주입
- `--rm`: 컨테이너가 종료되면 자동으로 컨테이너 삭제

### 6.3 운영 & 디버깅 필수 명령어

| 명령어 | 설명 | 예시 |
| :--- | :--- | :--- |
| `docker logs -f` | 컨테이너의 표준 출력 로그를 실시간 추적 | `docker logs -f my-nginx` |
| `docker exec -it` | 실행 중인 컨테이너 내부에 쉘로 접속 | `docker exec -it my-nginx /bin/sh` |
| `docker inspect` | 컨테이너/이미지의 상세 메타데이터(IP, 환경변수 등) JSON 출력 | `docker inspect my-nginx` |
| `docker stats` | 실행 중인 컨테이너들의 CPU, 메모리 실시간 사용량 모니터링 | `docker stats` |

### 6.4 리소스 정리 명령어 (디스크 용량 확보)

| 명령어 | 설명 |
| :--- | :--- |
| `docker system prune -a` | 사용하지 않는 모든 컨테이너, 네트워크, 이미지 일괄 삭제 |
| `docker volume prune` | 연결되지 않은 고아 볼륨 일괄 삭제 |

### 6.5 Docker Compose 명령어

| 명령어 | 설명 |
| :--- | :--- |
| `docker compose up -d` | 백그라운드로 모든 정의된 서비스 빌드 및 실행 |
| `docker compose down` | 실행 중인 모든 서비스 정지 및 컨테이너/네트워크 삭제 |
| `docker compose down -v`| 볼륨 데이터까지 완전히 초기화하며 종료 |
| `docker compose ps` | Compose로 구동된 서비스들의 상태 확인 |
| `docker compose logs -f [서비스명]` | Compose 특정 서비스(또는 전체) 로그 실시간 확인 |

---

## 7. 주니어가 실무에서 가장 많이 실수하는 4가지와 꿀팁

1. **포트 매핑 방향 헷갈림 (`-p A:B`)**
   - 앞쪽(`A`)이 **내 로컬 컴퓨터(호스트) 포트**, 뒤쪽(`B`)이 **컨테이너 내부 포트**입니다.
   - 예: `-p 8080:80`은 브라우저에서 `localhost:8080`으로 접속했을 때 컨테이너 내부의 `80`번 포트로 전달하겠다는 뜻입니다.

2. **`.dockerignore` 파일 빼먹기**
   - `.gitignore`처럼 이미지 빌드 시 불필요한 파일(`node_modules`, `.git`, `.env` 등)을 제외해야 합니다.
   - 제외하지 않으면 빌드 컨텍스트가 수백 MB로 커져 빌드가 매우 느려지고 보안상 민감한 파일이 이미지에 포함될 수 있습니다.

3. **컨테이너 지웠더니 DB 데이터가 사라지는 문제**
   - DB 컨테이너는 반드시 `-v` 옵션이나 Docker Compose의 `volumes`를 설정해 데이터 영속성을 보장해야 합니다.

4. **루트(root) 권한으로 컨테이너 실행 지양**
   - 보안상 컨테이너 내부에서도 비특권 사용자(Non-root user)를 생성하여 실행하는 것이 Best Practice입니다.
