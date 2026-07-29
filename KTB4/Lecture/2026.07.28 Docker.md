# FastAPI 챗봇 프로젝트 — Docker & EC2 배포 공부자료

> KTB4 LLM Application Project (재료 기반 레시피 챗봇)
> Ollama → Claude API 마이그레이션 + Docker 배포 과정

---

## 사전 작업: Ollama → Claude API 마이그레이션

- EC2에 Ollama(로컬 LLM)를 올리면 GPU 인스턴스 비용 부담이 커서, 외부 API(Claude)로 전환
- `anthropic` SDK 패키지 추가, `{ANTHROPIC_API_KEY 환경변수명}` 방식으로 변경
- 작업 브랜치에서 작업 후 `main`으로 병합

---

## 1단계: Docker 컨테이너 패키징 + Compose 실행

### 1-1. 로컬(Mac)에서 이미지 빌드

```bash
docker build --platform linux/amd64 -t {Docker Hub 사용자명}/{이미지명}:latest .
```

- `--platform linux/amd64`: Mac(Apple Silicon, arm64)에서 빌드해도 EC2(x86_64)에서 실행 가능하도록 아키텍처 지정
- `{Docker Hub 사용자명}`: Docker Hub 가입 시 정한 아이디
- `{이미지명}`: 원하는 이미지 이름 (예: chatbot-project)

### 1-2. Docker Hub 로그인 및 push

```bash
docker login
docker push {Docker Hub 사용자명}/{이미지명}:latest
```

- 비밀번호 대신 Docker Hub Access Token 사용 (Account Settings → Security → New Access Token)

### 1-3. EC2에 Docker Compose 설치

우분투 최신 버전(코드네임에 따라 다름)에서 Docker 공식 저장소가 아직 지원하지 않는 경우, 플러그인 설치(`docker-compose-plugin`) 대신 독립 실행형 바이너리로 설치.

```bash
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version
```

### 1-4. compose.yml 작성

```yaml
services:
  chatbot:
    build:
      context: {Dockerfile이 있는 프로젝트 경로}
      dockerfile: Dockerfile
    image: {Docker Hub 사용자명}/{이미지명}:latest
    ports:
      - "{호스트 포트}:{컨테이너 포트}"
    env_file:
      - .env
    volumes:
      - {호스트 벡터DB 경로}:{컨테이너 벡터DB 경로}
    restart: unless-stopped
```

### 1-5. 실행 및 확인

```bash
docker-compose up -d
docker-compose ps
docker-compose logs -f
```

---

## 2단계: EC2 배포 + 외부 접근 구성

### 2-1. EC2 접속

퍼블릭 IP로 접속해야 함 (프라이빗 IP로 접속 시 응답 없이 멈춤).

```bash
ssh -i "{pem 키 파일 경로}" {EC2 사용자명}@{EC2 퍼블릭 IP}
```

- `{EC2 사용자명}`: AMI에 따라 다름 (Ubuntu는 `ubuntu`, Amazon Linux는 `ec2-user`)

### 2-2. EC2에 Docker 설치 (Ubuntu 기준, yum 아닌 apt 사용)

```bash
sudo apt update
sudo apt install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker {EC2 사용자명}
exit
# 재접속 후 확인
ssh -i "{pem 키 파일 경로}" {EC2 사용자명}@{EC2 퍼블릭 IP}
docker --version
```

### 2-3. Docker Hub 로그인 및 이미지 pull

```bash
docker login
docker pull {Docker Hub 사용자명}/{이미지명}:latest
```

### 2-4. 로컬 벡터DB(Chroma) EC2로 전송

로컬에서 이미 임베딩 완료된 Chroma 벡터DB를 그대로 옮겨 재생성 방지.

```bash
# EC2에 폴더 미리 생성 (scp는 중간 경로 자동 생성 안 함)
ssh -i "{pem 키 파일 경로}" {EC2 사용자명}@{EC2 퍼블릭 IP} "mkdir -p {EC2 내 벡터DB 상위 경로}"

# Mac에서 scp로 전송
scp -i "{pem 키 파일 경로}" -r {로컬 벡터DB 경로} {EC2 사용자명}@{EC2 퍼블릭 IP}:{EC2 내 벡터DB 경로}
```

### 2-5. `.env` 파일 작성 (EC2)

```bash
nano .env
```

```
ANTHROPIC_API_KEY={Anthropic 콘솔에서 발급받은 API 키}
DB_PATH={컨테이너 내부에서 코드가 참조하는 벡터DB 경로}
```

> ⚠️ **주의**: `docker --env-file`은 값에 큰따옴표(`"`)를 포함해도 그대로 값의 일부로 읽어버림 (로컬 python-dotenv와 다름).
> `KEY="value"` ❌ → `KEY=value` ✅
> 검증: `cat -A .env` 로 따옴표·공백·탭 여부 확인

### 2-6. 컨테이너 실행

```bash
docker run -d \
  -p {호스트 포트}:{컨테이너 포트} \
  --env-file .env \
  -v {EC2 내 벡터DB 경로}:{컨테이너 내 벡터DB 경로} \
  {Docker Hub 사용자명}/{이미지명}:latest
```

### 2-7. 정상 작동 확인

```bash
docker ps
docker logs -f {컨테이너 ID}
```

### 2-8. 보안 그룹 인바운드 규칙 설정 (외부 접근 허용)

AWS 콘솔 → EC2 → 보안 탭 → 보안 그룹 → 인바운드 규칙 편집

| 유형 | 프로토콜 | 포트 범위 | 소스 |
|---|---|---|---|
| 사용자 지정 TCP | TCP | {서비스 포트} | 0.0.0.0/0 |

> 참고: SSH(22번 포트)는 가급적 "내 IP"로 제한 권장. 서비스 포트는 외부 공개 목적이라 0.0.0.0/0 사용 가능.

### 2-9. 외부 접속 확인

```
http://{EC2 퍼블릭 IP}:{서비스 포트}/docs
```

---

## 남은 작업 (3단계)

- [ ] GitHub Actions를 활용한 CI/CD 파이프라인 구축 (push 시 자동 빌드 → Docker Hub push → EC2 자동 배포)

---

## EC2 재시작 시 체크리스트

- [ ] 퍼블릭 IP 재확인 (Elastic IP 미할당 시 재시작마다 변경됨)
- [ ] `docker ps`로 컨테이너 자동 실행 여부 확인
- [ ] 자동 실행 안 되어 있으면 `docker-compose up -d`로 수동 실행

---

## 내게 발생한 문제점

이번 배포 과정에서 실제로 겪었던, 일반적인 절차만으로는 안 보이는 개인적인 이슈들.

### 1. Git — `.DS_Store`가 계속 충돌을 일으킴
- **증상**: `git checkout` 시 `.DS_Store`가 로컬 변경사항으로 덮어써질 위기라는 에러로 체크아웃이 막힘
- **원인**: Mac Finder가 폴더를 열 때마다 자동 생성하는 파일인데, 이미 git이 추적 중이었음
- **1차 삽질**: `.gitignore`에 추가하고 push/pull 해도 전혀 해결 안 됨 → `.gitignore`는 "새 파일"만 막아주고, 이미 추적 중인 파일에는 효과 없다는 걸 몰랐음
- **2차 삽질**: `git rm --cached -r .` 실행 후 `git add .` 없이 바로 commit해버려서, 프로젝트 전체 파일(main.py, nodes/ 등)이 통째로 untracked 상태가 되어버림 → 다른 브랜치로 체크아웃 시 "untracked 파일이 덮어써질 것"이라는 에러로 또 막힘
- **해결**: 같은 브랜치에서 `git add .` + commit으로 파일들을 다시 정상 추적 상태로 되돌린 뒤 진행

### 2. Docker — 아키텍처(Mac arm64 vs EC2 x86_64) 문제
- **증상**: `docker buildx build`가 인자 누락 에러를 내거나, 빌드는 됐는데 EC2에서 이미지가 안 맞을 수 있는 상황
- **원인**: Apple Silicon Mac은 arm64, EC2는 보통 amd64라서 아무 옵션 없이 빌드하면 아키텍처가 안 맞음
- **해결**: `--platform linux/amd64` 옵션을 빌드 명령에 명시

### 3. EC2 OS 착각 — yum vs apt
- **증상**: Docker 설치 가이드대로 `yum` 명령을 쳤는데 "그런 명령어 없음" 에러
- **원인**: EC2가 Amazon Linux가 아니라 Ubuntu였음 (접속 계정이 `ubuntu@...`인데도 처음엔 인지 못함)
- **해결**: `apt` 기반 설치 명령으로 전환

### 4. SSH — 프라이빗 IP로 접속 시도해서 무한 대기
- **증상**: `ssh ubuntu@172.31.x.x`로 접속했는데 응답 없이 터미널이 멈춤
- **원인**: AWS 콘솔에서 프라이빗 IP를 복사해서 씀 — 프라이빗 IP는 VPC 내부 전용이라 외부(Mac)에서는 라우팅 자체가 안 됨
- **해결**: 퍼블릭 IP(또는 퍼블릭 DNS)로 재접속

### 5. Docker Hub 토큰과 Anthropic API 키를 헷갈림
- **증상**: `.env`의 `ANTHROPIC_API_KEY`에 뭘 넣어야 할지 헷갈려서, 방금 발급한 Docker Hub 토큰을 넣으려고 함
- **원인**: 비슷한 시점에 두 개의 다른 서비스 토큰/키를 발급받아서 혼동
- **해결**: 서비스별로 키의 용도가 완전히 다르다는 것 확인 후 정확한 Claude API 키로 교체

### 6. `.env` 파일 값에 따옴표를 넣는 습관
- **증상**: `DB_PATH="./data/vdb/"`, `ANTHROPIC_API_KEY="sk-ant-..."`처럼 값에 따옴표를 넣어서, 두 번이나 각각 다른 에러로 발생
  - 1차: `docker: invalid env file (.env): variable 'DB_PATH ' contains whitespaces`
  - 2차: API 키가 "유효하지 않다"는 에러 (따옴표까지 키 값으로 인식됨)
- **원인**: 로컬에서 `python-dotenv` 등으로 `.env`를 읽을 때는 따옴표를 자동으로 벗겨주는 경우가 많아 문제없이 동작했지만, `docker run --env-file`은 따옴표를 벗기지 않고 그대로 값에 포함시킴
- **교훈**: Docker의 `--env-file`은 아주 단순한 `KEY=VALUE` 파서라서, 따옴표·공백이 있으면 안 됨. `cat -A .env`로 숨은 공백/따옴표를 눈으로 직접 확인하는 습관 필요

### 7. 벡터DB(Chroma)가 컨테이너 안에 없어서 매번 새로 생성 시도
- **증상**: `ValueError: Expected Embeddings to be non-empty list or numpy array, got []` 에러로 컨테이너가 죽음
- **원인**: `.gitignore`에 원본 데이터/벡터DB 폴더가 제외되어 있어 GitHub에도, Docker 이미지 안에도 데이터가 없었음. 코드는 "DB가 없으면 새로 생성" 로직이라 빈 문서로 임베딩을 시도해버림
- **해결**: 로컬에 이미 만들어둔 벡터DB를 `scp`로 EC2에 직접 전송하고, 볼륨 마운트로 컨테이너에 연결. (이 과정에서 scp 목적지 폴더가 미리 없으면 실패한다는 것도 같이 알게 됨 — `mkdir -p`로 먼저 생성 필요)

### 8. Docker Compose 플러그인 설치 실패 (우분투 버전 이슈)
- **증상**: `docker compose up -d`가 `-d`를 인식 못 하는 에러 → Compose 플러그인 자체가 없는 상태였음. `docker-compose-plugin` 패키지도 "찾을 수 없음"
- **원인**: EC2의 Ubuntu 버전이 아주 최신(26.04, resolute)이라 Docker 공식 apt 저장소가 아직 이 코드네임을 지원하지 않음 → 저장소 추가 시 GPG 서명 검증까지 실패
- **해결**: apt 저장소 방식을 포기하고, GitHub Releases에서 독립 실행형 `docker-compose` 바이너리를 직접 다운로드해서 설치 (`docker-compose`, 하이픈 방식으로 명령어 사용)
