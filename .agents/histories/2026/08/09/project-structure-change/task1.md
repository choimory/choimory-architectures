# 목차

- [개요](#개요)
- [작업 내용](#작업-내용)
- [구현 상세](#구현-상세)
- [검증](#검증)

---

# 개요

- `choimory-dev` 프로젝트 구조 변경사항을 `python diagrams` 기반 아키텍처 다이어그램에 반영한다.
- `Front`, `Member`, `Sender` 영역을 중심으로 코드와 생성 이미지를 갱신한다.

---

# 작업 내용

- `.agents/CALENDAR.md`의 작업 상태를 `PLAN`에서 `TASK`로 변경했다.
- `Front` 클러스터에 `admin`을 추가했다.
- `user`가 `client`, `admin`을 모두 사용할 수 있도록 연결했다.
- `Member` 클러스터의 `member-api`, `member-queue`를 `Kotlin`에서 `Java`로 변경했다.
- `client`, `admin`이 `member-api`, `article-api`, `memo-api`, `noti-api`를 호출하도록 연결을 확장했다.
- `Sender` 클러스터에 `Java` 기반 `sender-api`를 추가했다.
- `sender-api`를 공용 발송 API로 두고 `client`, `admin`, 주요 API가 호출할 수 있도록 연결했다.
- `sender-api`와 `sender-queue` 사이의 직접 호출 연결은 두지 않았다.
- `sender-queue`는 기존처럼 message broker와 연결되는 비동기 처리 컴포넌트로 유지했다.
- `sender-query`를 `MongoDB`에서 `Elasticsearch`로 변경했다.
- 참고 구조에 없는 `sender-redis`를 제거했다.
- `choimory-dev/choimory-dev.png` 이미지를 재생성했다.
- 다이어그램 선 교차를 줄이기 위해 `public-api` 논리 노드를 추가했다.
- `client`, `admin`의 API 호출선을 `public-api`로 모아 각 도메인 API에 연결되도록 조정했다.
- `sender-api`는 `public-api`에서 호출되는 공용 발송 API로 표현하고, 도메인 API에서 `sender-api`로 향하는 직접 연결선은 가독성을 위해 생략했다.
- Graphviz 레이아웃 옵션 `splines`, `nodesep`, `ranksep`을 추가해 선 라우팅과 간격을 조정했다.

---

# 구현 상세

## 대상 파일

- `choimory-dev/choimory-dev-architecture.py`
- `choimory-dev/choimory-dev.png`

## Front

- 기존 `client` 단일 프론트 구조에서 `client`, `admin` 2개 프론트 구조로 변경했다.
- `public-api` 논리 노드를 추가해 `client`, `admin`에서 각 API로 향하는 호출선을 한 곳으로 모았다.
- 최종 흐름은 `user >> [client, admin] >> public-api`이다.

## Member

- `member-api`를 `Kotlin`에서 `Java`로 변경했다.
- `member-queue`를 `Kotlin`에서 `Java`로 변경했다.
- `member-command`, `member-query`, `member-redis`는 기존 구성을 유지했다.
- `public-api >> member-api`로 외부 요청 진입선을 정리했다.

## Article

- `article-api`, `article-queue`는 기존처럼 `Kotlin`으로 유지했다.
- `article-command`, `article-query`, `article-redis`는 기존 구성을 유지했다.
- `public-api >> article-api`로 외부 요청 진입선을 정리했다.

## Memo

- `memo-api`, `memo-queue`는 기존처럼 `Nodejs`로 유지했다.
- `memo-command`, `memo-query`, `memo-redis`는 기존 구성을 유지했다.
- `public-api >> memo-api`로 외부 요청 진입선을 정리했다.

## Sender

- `sender-api`를 `Java`로 새로 추가했다.
- `sender-queue`는 기존처럼 `Kotlin`으로 유지했다.
- `sender-api`는 SMS, 카카오톡 등 발송 요청을 받는 공용 API로 표현했다.
- `sender-api`와 `sender-queue` 사이에는 직접 호출선을 두지 않았다.
- `sender-queue`는 message broker와 연결되는 비동기 처리 컴포넌트로 유지했다.
- `sender-query`를 `MongoDB`에서 `Elasticsearch`로 변경했다.
- `sender-redis`는 현재 참고 구조에 없으므로 제거했다.

## Notification

- `noti-api`, `noti-queue`, `noti-socket`은 기존처럼 `Nodejs`로 유지했다.
- `client`, `admin`이 `noti-socket`과 연결되도록 변경했다.
- `public-api >> noti-api`로 외부 요청 진입선을 정리했다.
- `noti-queue >> noti-redis-pubsub >> noti-socket` 흐름과 `noti-queue >> noti-fcm` 흐름은 유지했다.

## Message Broker

- `member-queue`, `article-queue`, `memo-queue`, `sender-queue`, `noti-queue`가 기존처럼 `broker`와 연결되도록 유지했다.
- `sender-api`는 broker나 `sender-queue`에 직접 연결하지 않았다.

## Layout

- 다이어그램 방향은 `TB`를 유지했다.
- 선 교차를 줄이기 위해 `graph_attr`를 추가했다.
- `splines="ortho"`로 직교 라우팅을 적용했다.
- `nodesep="0.8"`, `ranksep="1.1"`로 노드 간격과 랭크 간격을 조정했다.

---

# 검증

- 시스템 `python3 choimory-dev-architecture.py` 실행은 `diagrams` 모듈이 없어 실패했다.
- 프로젝트 가상환경 Python으로 `../choimory-dev/venv/bin/python choimory-dev-architecture.py`를 실행해 성공했다.
- 생성된 `choimory-dev/choimory-dev.png`에서 `admin`, Java 기반 `member-api`, Java 기반 `member-queue`, Java 기반 `sender-api`, Kotlin 기반 `sender-queue`, Elasticsearch 기반 `sender-query`가 표시되는 것을 확인했다.
- `sender-api`가 `sender-queue`를 직접 호출하지 않는 구조로 표현되는 것을 확인했다.
- 재생성된 이미지에서 `public-api` 기준으로 외부 호출선이 정리되고, 중앙부 선 교차가 줄어든 것을 확인했다.
