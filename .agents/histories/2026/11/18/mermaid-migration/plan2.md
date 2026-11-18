# 목차

- [개요](#개요)
- [추가1](#추가1)
  - [프론트](#프론트)
  - [백엔드](#백엔드)
  - [데브옵스](#데브옵스)
  - [네트워크](#네트워크)
- [추가1 분석](#추가1-분석)
  - [답변](#답변)
  - [정리한 구성](#정리한-구성)
  - [다이어그램 구성안](#다이어그램-구성안)
  - [확인할 것](#확인할-것)
- [추가2](#추가2)
- [추가2 분석](#추가2-분석)
  - [답변](#답변-1)
  - [노션에서 바뀐 점](#노션에서-바뀐-점)
  - [반영한 구성](#반영한-구성)
  - [추가2 결정사항 적용 방식](#추가2-결정사항-적용-방식)
  - [다이어그램 구성 (최종안)](#다이어그램-구성-최종안)

---

# 개요

- plan1에서 분석한 내용을 기준으로 task1에서 Mermaid 전환 1차 작업을 완료함
  - `choimory-dev/service.md`, `choimory-dev/devops.md` 원본 다이어그램 작성
  - `choimory-dev/README.md`, 루트 `README.md`에 다이어그램 복사본 + 원본 링크 작성
  - 기존 `.py`, `.png`, `README2.md` 제거
- 1차 작업 결과를 바탕으로 추가 분석 및 보완 작업을 진행함
- 참고 대상
  - `.agents/histories/2026/11/18/mermaid-migration/plan1.md`
  - `.agents/histories/2026/11/18/mermaid-migration/task1.md`

---

# 추가1

- 프로젝트 구성이 업데이트 안된게 많아 업데이트 해줌
- Mermaid는 예전 py의 구성을 그대로 따라갈 필요 없음. 구성만 이해하면 되지 TB 같은거까지 따라할 필요 없음. 보기 좋게 깔끔하게 만드는게 최우선임.

## 프론트

- choimory-dev-front: 사용자 웹페이지, Next.js
- choimory-dev-mobile: 사용자 모바일, React-naitve
- choimory-dev-admin: 관리자 웹페이지, Next.js
- 향후 서비스별로 분리할 계획도 있으나 일단은 이렇게 구성할 생각

## 백엔드

- https://app.notion.com/p/Back-end-30587e6bf65280ff8226d25b659c13ad?v=3df87e6bf65280da9611000c9a3c010c&source=copy_link
- 회원
  - 사이트 회원 관리 도메인
  - choimory-dev-member-api
  - choimory-dev-member-grpc
  - choimory-dev-member-queue
  - choimory-dev-member-mcp
  - choimory-dev-member-batch
- 블로그
  - 블로그 관련 도메인
  - choimory-dev-blog-api
  - choimory-dev-blog-grpc
  - choimory-dev-blog-queue
  - choimory-dev-blog-mcp
- 메모
  - 개인 메모장 도메인 
  - choimory-dev-memo-api
  - choimory-dev-memo-grpc
  - choimory-dev-memo-queue
  - choimory-dev-memo-mcp
- 커리어
  - 경력, 이력서 도메인
  - choimory-dev-career-api
  - choimory-dev-career-grpc
  - choimory-dev-career-queue
  - choimory-dev-career-mcp
- 피드
  - 아이템, 가격, 아티스트 앨범 모니터링 도메인
  - choimory-dev-feed-api
  - choimory-dev-feed-grpc
  - choimory-dev-feed-queue
  - choimory-dev-feed-mcp
  - choimory-dev-feed-batch
- 수집
  - 동영상, pdf 수집 도메인
  - choimory-dev-scrap-api
  - choimory-dev-scrap-grpc
  - choimory-dev-scrap-queue
  - choimory-dev-scrap-mcp
  - choimory-dev-scrap-batch
- 알림
  - 웹페이지 알림 도메인
  - choimory-dev-noti-api
  - choimory-dev-noti-grpc
  - choimory-dev-noti-queue
  - choimory-dev-noti-mcp
  - choimory-dev-noti-socket
- 발송
  - 이메일, 메신저(디스코드..) 등의 메시지 발송 도메인
  - choimory-dev-sender-api
  - choimory-dev-sender-grpc
  - choimory-dev-sender-queue
  - choimory-dev-sender-mcp
- 향후 api-gateway를 도입할 계획도 있으나 일단은 자유롭게 호출하는 식으로 구성할 생각

## 데브옵스

- https://app.notion.com/p/PC-3fe87e6bf6528071ad2af10621fab4dc?v=20c87e6bf652809ab76f000cf4e368b8&source=copy_link
- Cluster: Kubernetes
- CI: Github actions
- CD: ArgoCD
- CR: GHCR
- Log: Loki, Grafana
- Metrics: Prometheus

## 네트워크

- https://app.notion.com/p/PC-3fe87e6bf6528071ad2af10621fab4dc?v=20c87e6bf652809ab76f000cf4e368b8&source=copy_link
- Cloudflare > Tailscale > 원룸 공유기 > 미니 PC

---

# 추가1 분석

> plan2 확인

## 답변

- 추가1 내용과 노션 문서(Back-end, 홈서버 미니PC 세팅 및 하위 5차·6차 작업 진행 문서)를 함께 참고하여 구성을 정리함
- 다이어그램 구성안과 작업 전 확인할 것들을 정리함

## 정리한 구성

### 프론트

- `front`(Next.js), `mobile`(React Native), `admin`(Next.js) 3개

### 백엔드

- 공통 규칙: facade 패턴, CQRS, PK는 UUIDv7
- 모든 도메인은 아래 모듈을 기본으로 가지며, 필요한 도메인만 `batch`, `socket`을 추가함
  - `api`: 프론트 호출
  - `grpc`: 내부 동기 호출
  - `queue`: Kafka 기반 내부 비동기 호출, DB 동기화
  - `mcp`: AI 에이전트 호출

| 도메인 | 추가 모듈 | 스택 | 저장소·외부 연동 |
|---|---|---|---|
| member | batch | Java 21, Spring Boot | PostgreSQL, ES, Redis |
| blog | - | Kotlin, Spring Boot | PostgreSQL, ES, Redis |
| feed | batch | Kotlin, Ktor | PostgreSQL, ES, Redis, Discord |
| scrap | batch | 미정 | Discord |
| noti | socket | NestJS | PostgreSQL, Redis pub/sub, Firebase |
| sender | - | Spring WebFlux | PostgreSQL, ES, Firebase, 메일·Discord |

### 데브옵스

- 클러스터: kubeadm 노드 1대 (미니PC)
- 배포: GitHub Actions → GHCR → gitops 저장소 이미지 태그 커밋 → ArgoCD
- 네임스페이스
  - 공용 도구 `choimory-infra`: ArgoCD, Envoy Gateway, Sealed Secrets, CNPG, cert-manager, Tailscale Operator, cloudflared
  - 앱 `choimory-dev-stg`, `choimory-dev-prod`
- 로그·메트릭: Loki + Grafana, Prometheus

### 네트워크

- 노션 6차 기준, 외부에서 들어오는 경로는 세 갈래
  - 공개: 브라우저 → Cloudflare → Tunnel → cloudflared → gateway-proxy(Envoy) → HTTPRoute → 앱
  - 내부 도구: 내 기기(Tailscale) → `*.infra.choimory.dev` → infra-gateway-proxy → ArgoCD 등
  - DB: 내 기기(Tailscale) → tailnet 기기 → PostgreSQL / Redis
- "Cloudflare > Tailscale > 공유기 > 미니PC"는 한 줄 경로처럼 보이나, 실제로는 Cloudflare(공개)와 Tailscale(내부)이 따로 있는 경로임
  - 둘 다 미니PC에서 바깥으로 연결을 여는 방식이라 공유기는 포트포워딩 없이 지나가는 구간
  - 다이어그램은 경로를 갈래별로 나눠서 표현

## 다이어그램 구성안

- 보기 좋은 것을 우선으로, 방향(LR 등)은 다이어그램마다 알맞게 정함
- 6개 도메인 × 4~5개 모듈을 한 그림에 넣으면 노드가 30개를 넘으므로 아래처럼 분리

| 문서 | 다이어그램 |
|---|---|
| `service.md` | ① 전체 구성: 클라이언트(front/mobile/admin, AI 에이전트) → 도메인 6개(도메인마다 노드 하나) → Kafka / 외부(Discord, Firebase)<br>② 도메인 공통 구조: api/grpc/queue/mcp/batch/socket과 PostgreSQL·ES·Redis 관계를 한 번만 그림<br>③ 도메인별 모듈·스택은 표로 정리 |
| `devops.md` | ① 배포 흐름(LR): Actions → GHCR → gitops → ArgoCD → 클러스터<br>② 클러스터 구성: 네임스페이스별 구성 요소<br>③ 로그·메트릭: Loki, Grafana, Prometheus |
| `network.md` | 공개 / 내부 도구 / DB 세 갈래의 접속 경로 |

## 확인할 것

1. memo 도메인: 노션에는 있으나 추가1 목록에는 없음. 제외하는 것이 맞는지
2. feed 모듈: 노션에는 `socket`, 추가1에는 `batch`. 둘 다 있는지, batch만 있는지
3. 도메인 간 호출 관계: 어느 도메인이 누구를 gRPC나 Kafka로 호출하는지 아직 정해진 것이 없어 보임. 지금은 "gRPC / Kafka로 서로 통신한다" 정도로만 그리고, 구체적인 관계는 정해지면 추가하는 것을 추천
4. 구현된 것과 계획 중인 것 구분: 현재 배포된 것은 front와 member-api뿐이며, Loki·Prometheus·mobile·admin 등은 계획 단계. 계획 중인 노드를 점선이나 흐린 색으로 구분할지
5. 공개 범위: 저장소가 public이면 tailnet IP 같은 값은 넣지 않음. 도메인 이름(`choimory.dev`, `*.infra.choimory.dev`)은 넣어도 되는지

---

# 추가2 

- 메모, 피드 도메인은 노션 다시 확인
- 모든 도메인이 나머지 모든 도메인을 필요에 따라 자유롭게 grpc 혹은 queue로 부를수 있음
- 계획중인건 점선으로 
- 값은 넣지 말고 구성만 대충 보여주면 됨

---

# 추가2 분석

> 추가2 확인

## 답변

- 추가2 내용과 노션 Back-end 문서를 다시 확인하여 구성을 갱신함
- 도메인 간 호출, 계획 중인 구성 요소 표시, 값 제외 방식을 정하고 다이어그램 최종안을 정리함

## 노션에서 바뀐 점

- memo: 다시 포함됨. NestJS, PostgreSQL / MongoDB
- career: 새로 생긴 도메인. 경력·이력서 소개용, 스택 미정. queue 설명에 "PostgreSQL ↔ MongoDB 동기화"가 있어 저장소는 이 두 개로 봄
- feed: socket은 없어지고 batch(관찰 대상 주기 감시)만 있음
- sender, noti: "서비스 도메인이 아닌 내부 코어용"으로 명시됨. sender의 발송 대상에 SMS, 메신저 추가

## 반영한 구성

### 서비스 도메인 6개

| 도메인 | 추가 모듈 | 스택 | 저장소·외부 연동 |
|---|---|---|---|
| member | batch | Java 21, Spring Boot | PostgreSQL, ES, Redis |
| blog | - | Kotlin, Spring Boot | PostgreSQL, ES, Redis |
| memo | - | NestJS | PostgreSQL, MongoDB |
| career | - | 미정 | PostgreSQL, MongoDB |
| feed | batch | Kotlin, Ktor | PostgreSQL, ES, Redis, Discord |
| scrap | batch | 미정 | PostgreSQL, ES, Discord |

### 코어 도메인 2개

| 도메인 | 추가 모듈 | 스택 | 저장소·외부 연동 |
|---|---|---|---|
| sender | - | Spring WebFlux | PostgreSQL, ES, Firebase, 메일·SMS·메신저 |
| noti | socket | NestJS | PostgreSQL, Redis pub/sub, Firebase |

## 추가2 결정사항 적용 방식

- 도메인 간 호출
  - 도메인끼리 선을 모두 이으면 8개 도메인이라 선이 수십 개가 됨
  - 가운데에 "내부 통신 (gRPC / Kafka)" 노드 하나를 두고 모든 도메인을 연결하여, 누구나 누구든 부를 수 있다는 의미를 표현
- 계획 중인 것은 점선
  - 계획 단계인 노드는 점선 테두리, 연결선은 점선 화살표
  - 현재 구현된 것: front, member(api), PostgreSQL, Redis, k8s, GitHub Actions, GHCR, ArgoCD, Cloudflare Tunnel, Envoy Gateway, Tailscale
  - 나머지(mobile, admin, member 외 도메인, Kafka, ES, Loki, Grafana, Prometheus 등)는 점선
- 값은 넣지 않음
  - 도메인 주소, IP, 네임스페이스 이름, 버전 제외
  - 구성 요소는 "Cloudflare Tunnel", "Envoy Gateway", "공용 도구 / 앱(stg, prod)" 정도로만 표시

## 다이어그램 구성 (최종안)

| 문서 | 다이어그램 |
|---|---|
| `service.md` | ① 전체 구성: 클라이언트(front/mobile/admin, AI 에이전트) → 서비스 도메인 6개 / 코어 도메인 2개 ↔ 내부 통신(gRPC/Kafka), 외부(Discord, Firebase, 메일·SMS)<br>② 도메인 공통 구조: api/grpc/queue/mcp(+batch/socket)와 command / query / cache 저장소<br>③ 도메인 표 |
| `devops.md` | ① 배포 흐름: Actions → GHCR → gitops 저장소 → ArgoCD → 클러스터<br>② 클러스터 구성: 공용 도구 / 앱(stg, prod)<br>③ 로그·메트릭: Loki, Grafana, Prometheus (점선) |
| `network.md` | 공개(Cloudflare Tunnel) / 내부 도구(Tailscale) / DB(Tailscale) 세 갈래 경로 |

- 작업 순서: 세 문서를 새로 쓰고, `choimory-dev/README.md`와 루트 `README.md`의 다이어그램 복사본을 다시 맞춤