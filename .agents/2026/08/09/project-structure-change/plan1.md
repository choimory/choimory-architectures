# 목차

- [개요](#개요)
- [프로젝트 구조 변경사항 분석](#프로젝트-구조-변경사항-분석)
- [Sender API 연결 정책](#sender-api-연결-정책)

---

# 개요

- 프로젝트 구조 변경사항을 반영하기 위한 분석 및 계획 문서

## 변경사항1

- 프론트 하나 추가 (admin)
- member api와 queue를 java로 변경
- article api와 queue를 kotlin로 변경
- sender api를 java로 변경

## 참고

```markdown
# member

- Java 21
- postgres, elastic search, redis

## api

- 외부 요청 처리

## queue

- 내부 요청 처리
- db 싱크

---

# article

- kotlin
- postgres, elastic search

## api

- 외부 요청 처리

## queue

- 내부 요청 처리
- db 싱크

---

# memo

- 개인 메모 도메인
- nest.js
- postgres, mongo db

## api

- 외부 요청 처리

## queue

- 내부 요청 처리
- db 싱크

---

# noti

- nest.js
- postgres, redis-pubsub
- 알림 담당

## api

- 외부 요청 처리

## queue

- 내부 요청 처리
- db 싱크

## socket

- front와의 실시간 알림 소켓통신용

---

# sender

- 메일, sms 발송 담당
- 비동기
- springboot webflux
- postgres, elasticsearch

## api

- 외부 요청 처리

## queue

- 내부 요청 처리
- db 싱크

---

# chat

- ktor
- 챗이 필요한지는 모르겠음
- 챗 대신 할만한 비동기 도메인 생각해보기

## api

- 외부 요청 처리

## queue

- 내부 요청 처리
- db 싱크

## socket

- front와의 소켓통신용
```

--

# 프로젝트 구조 변경사항 분석

> 분석시작

## 답변

현재 반영 대상은 `choimory-dev/choimory-dev-architecture.py`이다.

## 현재 다이어그램 상태

- `Front`: `client` 하나만 있음
- `Member`: `member-api`, `member-queue`가 둘 다 `Kotlin`으로 표시됨
- `Article`: `article-api`, `article-queue`가 둘 다 `Kotlin`으로 표시됨
- `Sender`: `sender-queue`만 있고 `sender-api`는 없음
- `Memo`, `Notification`, `Message broker`, `Logging`, `Monitoring`, `CI/CD`, `Infra`는 기존 구조 유지

## 변경사항 기준 반영 대상

- `admin` 프론트 추가
- `member-api`, `member-queue`: `Kotlin`에서 `Java`로 변경
- `article-api`, `article-queue`: 현재도 이미 `Kotlin`이라 실질 변경 없음
- `sender-api`: 새로 추가하고 `Java`로 표시
- `sender-queue`: `plan1.md`에는 “sender api를 java로 변경”만 있어서 queue는 기존 Kotlin 유지가 자연스러움

## 실제 로컬 저장소 기준 확인

- `/Users/choimory/IdeaProjects/choimory/choimory-dev-member-api`는 Java 21 + Spring Boot로 확인됨
- `/Users/choimory/IdeaProjects/choimory/choimory-dev-sender-queue`는 Kotlin + Spring Boot로 확인됨
- `choimory-dev-admin`, `choimory-dev-article-*`, `choimory-dev-member-queue`, `choimory-dev-sender-api` 저장소는 현재 상위 디렉토리에서 확인되지 않음
- `choimory-dev-manifests`는 관련 파일은 있지만 deployment/kustomization 내용이 비어 있어 배포 구조 근거로 쓰기 어려움

## 제안하는 반영 방향

- 다이어그램은 `plan1.md`의 목표 구조를 기준으로 업데이트
- 실제 로컬에 없는 컴포넌트도 설계상 반영한다는 전제로 `admin`, `sender-api`, `member-queue` Java 변경을 적용
- README는 작업 마무리 시점에만 프로젝트 설명 최신화

## 다음 작업

- `CALENDAR.md` 상태를 `PLAN`에서 `TASK`로 변경
- 다이어그램 코드 수정
- `python3 choimory-dev-architecture.py`로 이미지 재생성
- 결과 이미지 확인
- 작업 내용 설명

--

# Sender API 연결 정책

> sender api도 사용자/어드민 가리지않고 sms, 카톡 발송해야 할게 있을땐 자유롭게 쓸거야

## 답변

`sender-api`는 특정 프론트 전용이 아니라 공용 발송 API로 둔다.

## 조정된 구현 계획

- `Front`에는 `client`, `admin`을 둔다.
- `user >> client`, `user >> admin`을 연결한다.
- `Sender`에는 `sender-api`, `sender-queue`를 둔다.
- `sender-api`는 Java로 표시한다.
- `sender-queue`는 기존 Kotlin을 유지한다.
- `sender-api`는 외부/내부 모두 호출 가능한 발송 요청 진입점으로 표현한다.
- `sender-api >> sender-queue`를 연결한다.

## Sender API 호출 연결

- `client >> sender-api`
- `admin >> sender-api`
- `member-api >> sender-api`
- `article-api >> sender-api`
- `memo-api >> sender-api`
- `noti-api >> sender-api`

## 기존 비동기 연결 정리

- 현재 다이어그램은 `[member_api, article_api, memo_api] >> sender_queue`로 직접 queue에 붙어 있다.
- `sender-api`가 공용 진입점이라면 직접 queue 호출보다는 `sender-api`를 거치는 구조가 더 일관적이다.
- 변경 방향은 `[client, admin, member_api, article_api, memo_api, noti_api] >> sender_api >> sender_queue`이다.

## Sender 저장소 표현

- `plan1.md` 참고 기준 sender는 `postgres, elasticsearch`를 사용한다.
- 현재 다이어그램은 `sender-command = Postgresql`, `sender-query = MongoDB`, `sender-redis = Redis`로 표현되어 있다.
- 변경 방향은 `sender-query`를 `MongoDB`에서 `Elasticsearch`로 변경하는 것이다.
- `sender-redis`는 참고 구조에 없으므로 제거하는 방향이 자연스럽다.

## 최종 반영안

- `admin` 프론트 추가
- `member-api`, `member-queue`를 Java로 변경
- `article-api`, `article-queue`는 Kotlin 유지
- `sender-api`를 Java로 추가
- `sender-api`는 `client`, `admin`, 주요 API들이 자유롭게 호출 가능하게 연결
- `sender-api >> sender-queue` 연결
- `sender-query`는 MongoDB에서 Elasticsearch로 변경
- `sender-redis`는 제거
