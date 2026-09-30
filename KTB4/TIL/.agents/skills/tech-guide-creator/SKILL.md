---
name: tech-guide-creator
description: >-
  Creates structured, intuitive, and practical technical guide (TIL) documents for junior developers from a senior developer's perspective.
  Use this skill whenever the user asks to explain a new technology/concept (e.g., Git, Kubernetes, Redis, Kafka, Linux, Networks, Database),
  create a learning guide, summarize knowledge, or write a technical cheatsheet/documentation.
---

# 📚 Tech Guide & TIL Document Creator Skill

이 스킬은 주니어 개발자가 새로운 기술 개념을 빠르고 정확하게 습득할 수 있도록, **시니어 개발자의 멘토링 관점**에서 표준화된 고품질 기술 가이드 마크다운 문서를 작성하는 지침입니다.

---

## 1. 멘토링 원칙 (Core Philosophy)

1. **"Why"를 가장 먼저 설명한다**
   - 기술의 기능부터 나열하지 말고, **"이 기술이 없던 시절에는 어떤 문제가 있었고, 왜 등장했는가?"**를 먼저 짚어줍니다.
2. **직관적인 멘탈 모델(비유) 제공**
   - 추상적인 개념을 일상적이고 친숙한 비유로 모델링합니다. (예: Docker = 레시피-붕어빵틀-붕어빵, Git = 게임 세이브포인트)
3. **비교를 통해 차이점 각인**
   - 기존 방식 vs 신기술, 대안 기술과의 차이점을 명확한 마크다운 표로 비교합니다. (예: VM vs Docker, SQL vs NoSQL)
4. **실무 프로덕션 관점의 모범 사례(Best Practice) 반영**
   - "그냥 돌아가는 코드"가 아닌, 보안·캐싱·확장성·안티패턴이 고려된 실무 표준 코드를 제시합니다.
5. **실무 필수 명령어 / 치트시트 포함**
   - 개발 및 운영 과정에서 매일 쓰게 되는 핵심 명령어와 옵션을 표 형태로 정리합니다.
6. **주니어 빈출 실수 Top 3~4 및 해결책**
   - 실무 현장에서 주니어들이 가장 많이 겪는 함정과 실수, 그리고 그 회피법을 마지막에 꼭 짚어줍니다.

---

## 2. 표준 문서 템플릿 (Document Skeleton)

기술 가이드 문서를 작성할 때는 아래 목차 구조를 따릅니다:

```markdown
# 🚀 [기술명] 핵심 실무 가이드 (Junior to Pro)

> **작성자**: 시니어 개발자  
> **대상**: [기술명]을 처음 접하거나 실무 도입이 필요한 개발자  
> **목표**: [이 문서를 통해 달성할 수 있는 명확한 목표 한 줄]

---

## 1. [기술명]이란 무엇이고, 왜 쓰는가?
- 1.1 등장 배경과 해결하려는 고통(Pain Point)
- 1.2 기존 방식 vs [기술명] 비교 (마크다운 테이블 또는 ASCII 다이어그램)

## 2. 핵심 개념 완벽 이해 (멘탈 모델 & 비유)
- 2.1 핵심 구성 요소 3~4가지 분해
- 2.2 직관적인 일상 비유로 이해하는 동작 원리

## 3. 실무 표준 아키텍처 / 코드 예제
- 주석이 친절하게 달린 실무 레벨 설정 파일 or 코드 예제
- 각 라인/블록별 핵심 포인트 설명

## 4. 핵심 메커니즘 & 심화 원리 (선택적)
- 데이터 흐름, 네트워크, 상태 관리, 동시성 등 필수 내부 동작 원리

## 5. 실무 필수 명령어 / 문법 치트시트 (Cheatsheet)
- 가장 자주 쓰는 명령어, 옵션, 단축키 등을 상황별 표로 정리
- 디버깅/로그 확인/트러블슈팅 명령어 별도 섹션 구성

## 6. 주니어가 실무에서 가장 많이 실수하는 4가지와 꿀팁
1. [흔한 실수 1]: 원인 및 해결책
2. [흔한 실수 2]: 원인 및 해결책
3. [흔한 실수 3]: 원인 및 해결책
4. [흔한 실수 4]: 원인 및 해결책
```

---

## 3. 에이전트 실행 워크플로우

사용자가 특정 기술의 가이드나 정리 문서를 요청했을 때:

1. **파일 명명 규칙**:
   - 워크스페이스 내에 `[기술명]_Guide.md` (예: `Git_Guide.md`, `Redis_Guide.md`, `Kubernetes_Guide.md`) 형식으로 파일을 생성합니다.
2. **문서 작성 (`write_to_file`)**:
   - 위 표준 템플릿에 맞추어 전문성 높고 친절한 톤으로 마크다운 파일을 작성합니다.
3. **대화창 요약 브리핑**:
   - 대화창에서는 전체 내용을 그대로 복사하지 않고,
   - **핵심 요약 (한 줄 정의, 멘탈 모델 비유, 핵심 명령어 Top 3)**을 브리핑한 뒤,
   - 생성된 파일의 clickable link(`[파일명](file:///...)`)를 제공합니다.
