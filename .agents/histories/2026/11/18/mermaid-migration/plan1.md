# 목차

- [개요](#개요)
  - [계획](#계획)
- [plan1 계획 검토](#plan1-계획-검토)
  - [답변](#답변)
  - [다이어그램 중복 문제](#다이어그램-중복-문제)
  - [문서 분리 단위](#문서-분리-단위)
  - [영역 간 연결 표현](#영역-간-연결-표현)
  - [기존 파일 처리](#기존-파일-처리)
- [Markdown include, 문서 분리 기준, 기존 파일 처리](#markdown-include-문서-분리-기준-기존-파일-처리)
  - [답변](#답변-1)
  - [Markdown include 여부](#markdown-include-여부)
  - [문서 분리 기준](#문서-분리-기준)
  - [기존 파일 처리 결정](#기존-파일-처리-결정)
  - [결정 사항 정리](#결정-사항-정리)
- [다이어그램 중복 처리 방식 결정](#다이어그램-중복-처리-방식-결정)
  - [답변](#답변-2)
  - [동기화 관리 방법](#동기화-관리-방법)
  - [작업 순서](#작업-순서)

---

# 개요

- 현재 프로젝트는 diagrams(mingrammer) 라이브러리를 이용해 파이썬 코드로 아키텍처를 작성하고, graphviz로 PNG 이미지를 생성하는 구조임
  - `choimory-dev/choimory-dev-architecture.py` → `choimory-dev/choimory-dev.png`
  - 환경 구성(python, graphviz, venv, pip install diagrams)이 필요하며, 수정할 때마다 이미지를 재생성해야 함
- 이를 Mermaid 기반으로 전환하는 작업을 진행해야 함
  - 별도 런타임 없이 Markdown 안에서 GitHub가 바로 렌더링 가능
  - 코드(텍스트)와 결과물(다이어그램)이 한 곳에서 관리됨
- 참고 대상
  - `choimory-dev/choimory-dev-architecture.py` (Front, Member, Article, Memo, Sender, Notification, Message broker, Logging, Monitoring, CI, CD, Infra 클러스터 구성)
  - `README.md`, `README2.md`, `choimory-dev/README.md`
  - `.agents/rules/readme.md` (README 목차 작성, Mermaid 다이어그램 권장 규칙)
- 그 외
  - 기존 python 파일 / PNG / 환경구성 문서의 유지 또는 제거 여부, README 통합 방식 등은 분석하며 결정

## 계획

- 루트에는 프로젝트별 디렉토리
- 프로젝트별로 front-end.md, back-end.md, infrastructure.md network.md 등등을 만들고 mermaid로 각각의 구성도 작성
- 프로젝트별로 README.md 만들고 위의 내용 한곳에 작성
- 루트 README.md에는 목차, choimory-architecture 리포지토리 설명 작성 후, 그 뒤의 섹션들은 모두 프로젝트별 섹션을 작성하고 그 하위에 프로젝트별 mermaid를 넣음

---

# plan1 계획 검토

> plan1 확인

## 답변

- 계획 방향은 좋으나, 바로 진행하기 전에 몇 가지 정리가 필요함

## 다이어그램 중복 문제

- 현재 계획대로라면 같은 mermaid가 분리 문서(`front-end.md` 등), 프로젝트 README, 루트 README 세 곳에 들어감
- Markdown은 다른 파일을 불러오는 include 기능이 없어 전부 복사본이 되고, 하나를 수정하면 세 곳 모두 수정해야 함
- 제안: 역할 분리

| 위치 | 담는 내용 |
|---|---|
| `{project}/front-end.md` 등 | 영역별 상세 다이어그램 (원본) |
| `{project}/README.md` | 프로젝트 전체 개요 다이어그램 1개 + 영역별 문서 링크 |
| 루트 `README.md` | 프로젝트별 섹션에 간략 개요 다이어그램 + 프로젝트 README 링크 |

- 상세 내용은 한 곳에만 있고, 위로 갈수록 요약만 남는 구조
- 한곳에서 모든 내용을 보는 것이 목적이라면 중복을 감수하는 방법도 있음

## 문서 분리 단위

- 기존 `.py` 기준 매핑
  - front-end.md: Front (Next.js client)
  - back-end.md: Member, Article, Memo, Sender, Notification, Kafka broker
    - 도메인마다 api/queue/command DB/query DB/redis 구조가 반복되어 한 그림에 넣으면 복잡해짐
    - 전체 흐름 1개 + 도메인별 상세로 나누는 것을 제안
  - infrastructure.md: CI(GitHub, Actions), CD(Docker, k8s), EC2, S3
  - observability.md(추가 제안): Logging(ELK), Monitoring(Prometheus, Grafana)
  - network.md: 기존 `.py`에는 네트워크 정보(Ingress, LB, DNS, VPC 등)가 없음. 새로 설계할지 이번 작업에서 제외할지 결정 필요
- 프로젝트 공통 문서 목록을 정해두면 다른 프로젝트를 추가할 때도 같은 틀을 쓸 수 있음

## 영역 간 연결 표현

- front → api, api → sender, queue → kafka 등 영역을 넘나드는 연결이 많음
- 분리 문서에서는 외부 요소를 점선 노드 정도로만 표시하고, 전체 연결은 프로젝트 README의 개요 다이어그램에서 보여줌

## 기존 파일 처리

- `choimory-dev-architecture.py`, `choimory-dev.png`: 제거 또는 보관 결정 필요
- `README2.md`: diagrams 환경 구성 내용이라 전환 후 불필요. 제거 후 루트 README로 통합 제안

---

# Markdown include, 문서 분리 기준, 기존 파일 처리

> 1. 마크다운에 include가 왜 없어 `@.foo/bar/name.md` 있지 않아?
> 2. 하긴 프론트 백엔드 db 등등은 하나의 아키텍처에 묶이기 마련이긴 해. 그럼 service(front, backend, db, k8s, kafka..), devops(k8s, ci, cd, monitoring) 등으로 할까? 근데 정해진건 없어. 프로젝트마다 구성이 다를거니까 이것도 어느정도 적절히 분리만 하면 돼 
> 3.기존파일은 제거함

## 답변

- `@경로`는 Markdown 표준이 아니므로 GitHub 기준으로 include는 불가
- 문서는 service / devops처럼 관점 기준으로 분리하며, 프로젝트마다 적절히 분리
- 기존 파일은 제거

## Markdown include 여부

- `@.foo/bar/name.md`는 Markdown 표준 문법이 아니라, Claude Code가 `CLAUDE.md`를 읽을 때 사용하는 import 문법임 (예: 이 프로젝트 `CLAUDE.md`의 `@AGENTS.md`)
  - Claude Code는 이 줄을 보고 해당 파일 내용을 불러옴
  - GitHub, IDE 미리보기는 `@AGENTS.md`를 그냥 텍스트로 보여줌
- include를 지원하는 도구는 MkDocs 플러그인, Docusaurus(MDX) 등 문서 사이트 빌더이며, 별도 빌드가 필요하고 GitHub README에는 적용되지 않음
- 따라서 GitHub 기준으로는 복사해 넣거나 링크를 거는 방법뿐이며, 중복 문제는 여전히 남음
  - A. 역할 분리 (추천): 상세 다이어그램은 분리 문서에만, 프로젝트/루트 README에는 개요 다이어그램 + 링크
  - B. 전부 복사: 루트 README 한곳에서 전부 볼 수 있으나, 수정 시 여러 곳을 함께 수정해야 함

## 문서 분리 기준

- 고정된 파일 목록이 아니라 "관점에 따라 나눈다"는 원칙만 정하고, 프로젝트마다 구성에 맞게 적절히 분리
- choimory-dev 적용 예시
  - service.md: 실제로 돌아가는 구성. front, 도메인별 api/queue, DB, redis, Kafka, FCM
    - 도메인마다 같은 구조가 반복되므로 전체 흐름 1개 + 도메인별 상세로 분리 추천
  - devops.md: 만들고, 배포하고, 운영하는 구성. CI(GitHub, Actions), CD(Docker, k8s), EC2/S3, Logging(ELK), Monitoring(Prometheus, Grafana)
- k8s가 양쪽에 걸치는 경우
  - service에서는 "k8s 위에서 돌아간다" 정도로 묶음만 표시
  - 배포 흐름(deploy → replicaset → pod → EC2)은 devops에서 표현

## 기존 파일 처리 결정

- 아래 파일들은 제거
  - `choimory-dev/choimory-dev-architecture.py`
  - `choimory-dev/choimory-dev.png`
  - `README2.md`

## 결정 사항 정리

- 결정됨
  - 루트에 프로젝트별 디렉토리 구성
  - 프로젝트별로 관점 기준(service, devops 등) 문서를 나누어 mermaid로 작성하며, 분리 단위는 프로젝트마다 적절히 결정
  - 프로젝트별 README.md 작성, 루트 README.md는 목차 + 리포지토리 설명 + 프로젝트별 섹션 구성
  - 기존 `.py`, `.png`, `README2.md` 제거
- 미결정
  - 다이어그램 중복 처리 방식 (A. 역할 분리 / B. 전부 복사)

---

# 다이어그램 중복 처리 방식 결정

> 링크만 쓰면 시각적으로 보이는게 없으니까 좀 그런데..
> 프로젝트별 상세 mermaid -> 프로젝트별 readme -> 루트 readme 이렇게 똑같이 복사 붙여넣기 하는거니까 링크랑 mermaid 같이 적고 싱크 안맞으면 복붙해서 그냥 맞추기만 하면 되지 않을까

## 답변

- B안(전부 복사) + 링크 병기로 결정
- 다이어그램이 바로 보이므로 README로서는 더 적합하며, 복사 방향이 상세 문서 → 프로젝트 README → 루트 README로 항상 같아서 동기화가 어렵지 않음

## 동기화 관리 방법

- 원본은 상세 문서 하나로 정하기
  - 수정은 항상 상세 문서(`service.md` 등)에서 하고, 프로젝트 README → 루트 README 순서로 붙여넣음
  - README에서 직접 수정하지 않아 어느 쪽이 맞는지 헷갈리지 않음
- 복사본에 출처 주석 달기
  - 예: `<!-- source: choimory-dev/service.md -->` + mermaid 블록 + `[상세 보기](./choimory-dev/service.md)`
  - 주석은 화면에 보이지 않으며, 검색으로 복사본 위치를 바로 찾을 수 있음
- 루트 README가 길어질 때 (선택)
  - 프로젝트별 다이어그램을 `<details>`로 접어둘 수 있음 (GitHub는 접힌 안에서도 mermaid 렌더링)
  - 현재는 프로젝트가 하나뿐이라 펼쳐두고, 늘어나면 적용

## 작업 순서

1. `choimory-dev/service.md`, `choimory-dev/devops.md`에 mermaid 작성
2. `choimory-dev/README.md` 작성 (목차, 프로젝트 설명, 다이어그램 복사, 링크)
3. 루트 `README.md` 재작성 (목차, 리포지토리 설명, 프로젝트별 섹션 - 다이어그램 복사, 링크)
4. 기존 `choimory-dev/choimory-dev-architecture.py`, `choimory-dev/choimory-dev.png`, `README2.md` 제거