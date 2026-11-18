# 목차

- [개요](#개요)
- [문서 분리 방식 재검토](#문서-분리-방식-재검토)
  - [답변](#답변)
  - [choimory-dev 기준 분리안](#choimory-dev-기준-분리안)
  - [원본에 없는 연결](#원본에-없는-연결)
- [기존 분리 방식으로 확정](#기존-분리-방식으로-확정)
  - [답변](#답변-1)
- [작업 진행](#작업-진행)
  - [답변](#답변-2)
  - [신규 작성](#신규-작성)
  - [재작성](#재작성)
  - [삭제](#삭제)
  - [히스토리](#히스토리)
  - [검증](#검증)

---

# 개요

- plan1에서 결정한 내용을 기준으로 diagrams(python) 기반 아키텍처를 Mermaid로 전환하는 작업 진행
- 프로젝트별 관점 문서(원본) → 프로젝트 README → 루트 README 순서로 다이어그램을 복사하고, 원본 링크를 함께 작성
- 기존 `.py`, `.png`, `README2.md` 제거

---

# 문서 분리 방식 재검토

> 말하지만 service.md, devops.md 등은 고정적인게 아니야 프로젝트를 보고 판단해서 적절하게 만들어줘. 네이밍도 적절한걸로 정해주고

## 답변

- choimory-dev의 특징(도메인별 CQRS 구조 반복, Kafka 기반 비동기 흐름, 단순한 운영 파이프라인)을 기준으로 분리안을 제안

## choimory-dev 기준 분리안

| 파일 | 내용 | 다이어그램 종류 |
|---|---|---|
| `service-topology.md` | 전체 서비스 구성과 서비스 간 통신 | flowchart |
| `domain-cqrs.md` | 도메인별 내부 구조 (api/queue와 command, query, cache 관계) | flowchart |
| `event-flow.md` | api → queue → Kafka → sender → noti-queue → redis pub/sub → socket / FCM 흐름 | sequenceDiagram |
| `operations.md` | 빌드·배포, S3, 로깅, 모니터링 | flowchart |

## 원본에 없는 연결

- 원본 `.py`에는 api, queue와 DB / ES / Redis 사이의 연결선이 없어 `domain-cqrs.md` 작성 시 추론이 필요하다는 점을 공유

---

# 기존 분리 방식으로 확정

> 구리다 아까 방식이 낫다

## 답변

- 처음 방식대로 `service.md` / `devops.md`로 확정
  - service.md: front, 도메인별 api/queue, DB, redis, Kafka, notification(socket, FCM)
  - devops.md: CI, CD(Docker → k8s → EC2), S3, Logging(ELK), Monitoring(Prometheus, Grafana)
- 연결선은 추론하지 않고 원본 `.py`에 있는 것만 그대로 옮기며, DB와 Redis 등은 연결선 없이 도메인 그룹 안에 배치

---

# 작업 진행

> plan1에 아까내용 적었으니까 그냥 바로 작업 시작해줘

## 답변

- plan1의 작업 순서(1~4단계)대로 진행 완료

## 신규 작성

- `choimory-dev/service.md`
  - Front, Member, Article, Memo, Sender, Notification, Message broker(Kafka) 구성도
  - DB(PostgreSQL, Elasticsearch, MongoDB), Redis는 원본처럼 연결선 없이 도메인 subgraph 안에 배치
  - 구성 요소 표 추가
- `choimory-dev/devops.md`
  - CI(GitHub → GitHub Actions), CD(Docker → Deployment → ReplicaSet → Pod), Infra(EC2, S3), Logging(Logstash → Elasticsearch → Kibana), Monitoring(Prometheus → Grafana) 구성도
  - 구성 요소 표 추가

## 재작성

- `choimory-dev/README.md`
  - 목차, 개요, 문서 안내 표, service / devops 다이어그램 복사본, 원본 링크
- `README.md`
  - 목차, 리포지토리 개요, 디렉토리 구조
  - 다이어그램 관리 방식 (원본 → 프로젝트 README → 루트 README 복사 흐름을 Mermaid로 표현)
  - choimory-dev 섹션 (service / devops 다이어그램 복사본, 원본 링크)
- 모든 복사본에는 `<!-- source: choimory-dev/{view}.md -->` 출처 주석 작성

## 삭제

- `choimory-dev/choimory-dev-architecture.py`
- `choimory-dev/choimory-dev.png`
- `README2.md`

## 히스토리

- `calendar.md`를 `TASK:Mermaid 전환 작업(mermaid-migration)`으로 변경

## 검증

- 다이어그램은 원본 파일에서 추출하여 붙여넣었으며, 프로젝트 README의 복사본 2개가 원본과 동일함을 확인
- 루트 README는 출처 주석 2개가 들어간 것까지만 확인
- 로컬에 Node가 없어 Mermaid 렌더링은 확인하지 못함. GitHub에서 렌더링 확인 필요
- 커밋은 진행하지 않음
