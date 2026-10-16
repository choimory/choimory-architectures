# 목차

- [개요](#개요)
- [완료 내용](#완료-내용)
- [최종 아키텍처](#최종-아키텍처)
- [검증](#검증)
- [프로젝트 구조 평가](#프로젝트-구조-평가)

---

# 개요

- `choimory-dev` 프로젝트 구조 변경사항을 `python diagrams` 기반 아키텍처 다이어그램에 반영했다.
- 최종 산출물은 `choimory-dev/choimory-dev-architecture.py`와 `choimory-dev/choimory-dev.png`이다.
- 작업 기록은 `plan1.md`, `plan2.md`, `task1.md`, `task2.md`에 나누어 작성했다.

---

# 완료 내용

- `CALENDAR.md` 상태를 `TASK`에서 `DONE`으로 변경했다.
- `Front`에 `admin`을 추가했다.
- `Front`와 백엔드 도메인 서비스 사이에 별도 `API Gateway` 클러스터를 추가했다.
- `member-api`, `member-queue`, `sender-api`, `sender-queue`를 Java 기반 컴포넌트로 표현했다.
- `sender-api`와 `sender-queue` 사이의 직접 호출선은 두지 않았다.
- `sender-query`를 Elasticsearch로 변경하고 `sender-redis`를 제거했다.
- CI 흐름을 `github -> github-actions -> dockerhub / k8s-gitops-repo`로 표현했다.
- CD 흐름을 `k8s-gitops-repo -> argo-cd -> k8s deploy -> k8s set -> k8s pod`로 표현했다.
- 기존 Logging/Monitoring 영역을 `Observability`로 통합했다.
- 로그 흐름을 `k8s pod -> fluent-bit -> loki -> grafana`로 표현했다.
- 로그 장기 보관 흐름을 `fluent-bit -> s3`로 표현했다.
- 메트릭 흐름을 `k8s pod -> prometheus -> grafana`로 표현했다.
- `Front`와 `API Gateway`가 같은 수직 축에 가깝게 배치되도록 `Edge(weight="100")`을 적용했다.
- `choimory-dev/choimory-dev.png` 이미지를 재생성했다.
- 루트 `README.md`에 최종 아키텍처와 실행 방법을 반영했다.

---

# 최종 아키텍처

- 사용자는 `client`, `admin` 프론트를 사용한다.
- `client`, `admin`은 `api-gateway`를 통해 `member-api`, `article-api`, `memo-api`, `sender-api`, `noti-api`를 호출한다.
- `noti-socket`은 실시간 연결이므로 `client`, `admin`과 직접 연결된다.
- 각 도메인의 queue 컴포넌트는 message broker와 연결된다.
- GitHub Actions는 DockerHub 이미지 push와 K8s GitOps 리포지토리 이미지 태그 갱신을 담당한다.
- ArgoCD는 K8s GitOps 리포지토리 변경사항을 기준으로 K8s 배포를 수행한다.
- Observability는 Fluent Bit, Loki, Prometheus, Grafana로 구성된다.

---

# 검증

- 프로젝트 가상환경 Python으로 `choimory-dev-architecture.py`를 실행해 PNG 재생성에 성공했다.
- 생성된 이미지에서 `admin`, `api-gateway`, Java 기반 `member-api`, `member-queue`, `sender-api`, `sender-queue`가 표시되는 것을 확인했다.
- 생성된 이미지에서 CI/CD, Observability 흐름이 최종 구조대로 표시되는 것을 확인했다.
- Git commit과 push는 수행하지 않았다.

--

# 프로젝트 구조 평가

> 그럼 작업 외적인 질문인데 프로젝트 구조 평가해봐

## 답변

전체적으로는 작은 개인/토이 프로젝트를 MSA 스타일로 실험하는 구조로 보면 방향은 괜찮다. 다만 지금 설계는 “학습/실험용”으로는 좋고, “운영 가능한 제품 구조”로는 아직 과분하게 쪼개진 부분이 있다.

## 좋은 점

- `front`, `admin`, `api-gateway`, 도메인 API/queue 분리가 명확하다.
- `api`와 `queue`를 분리한 것은 외부 요청 처리와 비동기 처리를 나누려는 의도가 보여서 좋다.
- CI/CD를 GitOps + ArgoCD로 잡은 것은 구조적으로 깔끔하다.
- Observability를 Loki/Prometheus/Grafana로 정리한 것도 현재 Kubernetes 기반 구조와 잘 맞다.
- `sender-api`와 `sender-queue`를 직접 연결하지 않은 것도 괜찮다. API는 동기 발송 요청 진입점, queue는 broker 기반 비동기 처리자로 분리되기 때문이다.

## 걱정되는 점

- 도메인마다 `api`, `queue`, `command DB`, `query DB`, `redis`를 전부 두면 운영 복잡도가 빠르게 커진다.
- `member`, `article`, `memo`, `noti`, `sender`, `chat`까지 각각 분리하면 서비스 수가 너무 많다. 개인 프로젝트 기준으로는 배포, 설정, 모니터링, 장애 대응 비용이 크다.
- CQRS처럼 `command`, `query` 저장소를 모든 도메인에 적용하는 것은 과할 수 있다. 실제 조회 성능/검색 요구가 있는 도메인에만 적용하는 것이 낫다.
- Java, Kotlin, Node.js, Ktor, Nest.js, WebFlux가 섞여 있어서 학습 목적이면 좋지만, 유지보수 관점에서는 부담이 크다.
- `api-gateway`가 단순 라우팅인지, 인증/인가/토큰 검증/레이트리밋까지 담당하는지 경계가 더 필요하다.

## 평가

- 학습/포트폴리오 목적: 좋음
- 장기 운영 목적: 현재는 과분산
- 구조 실험 목적: 매우 적합
- 생산성 목적: 단일 백엔드 또는 2~3개 서비스로 줄이는 것이 나음

## 현실적인 개선 방향

- `member`, `article`, `memo` 정도만 우선 핵심 도메인으로 둔다.
- `sender`, `noti`는 공통 인프라성 서비스로 유지한다.
- `chat`은 당장 필요 없으면 보류한다.
- 모든 도메인에 Redis/Elasticsearch를 기본 탑재하지 말고 필요할 때만 붙인다.
- 언어는 가능하면 Java/Kotlin 계열 또는 Node 계열 중 하나로 줄인다.
- `api-gateway` 책임을 명확히 정의한다.
- `api-gateway` 책임 후보는 라우팅, 인증/인가, rate limit, BFF 역할 포함 여부이다.

## 한 줄 평가

아키텍처 학습용으로는 잘 쪼갠 구조지만, 실제 운영 기준으로는 서비스와 기술스택이 꽤 무겁다.
