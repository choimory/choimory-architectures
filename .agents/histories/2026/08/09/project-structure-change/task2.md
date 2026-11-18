# 목차

- [개요](#개요)
- [작업 내용](#작업-내용)
- [구현 상세](#구현-상세)
- [검증](#검증)

---

# 개요

- `plan2.md` 기준으로 `api-gateway`, CI/CD, Observability 구조 변경사항을 아키텍처 다이어그램에 반영한다.
- `public-api`를 제거하고 `api-gateway`를 별도 영역으로 분리한다.
- CI/CD 흐름을 GitHub Actions, DockerHub, K8s GitOps 리포지토리, ArgoCD 기반으로 재구성한다.
- Logging/Monitoring 영역을 `Observability`로 통합한다.

---

# 작업 내용

- `public-api`를 `api-gateway`로 변경했다.
- `api-gateway`를 `Front`와 백엔드 도메인 서비스 사이의 별도 클러스터로 분리했다.
- CI 영역을 `github -> github-actions -> dockerhub`와 `github-actions -> k8s-gitops-repo` 흐름으로 변경했다.
- CD 영역을 `k8s-gitops-repo -> argo-cd -> k8s deploy -> k8s set -> k8s pod` 흐름으로 변경했다.
- 기존 `Logging`, `Monitoring` 클러스터를 `Observability` 클러스터로 통합했다.
- 기존 `logstash -> elasticsearch -> kibana` 로그 흐름을 제거했다.
- 로그 흐름을 `k8s pod -> fluent-bit -> loki -> grafana`로 변경했다.
- 로그 장기 보관 흐름으로 `fluent-bit -> s3`를 추가했다.
- 메트릭 흐름을 `k8s pod -> prometheus -> grafana`로 변경했다.
- `sender-queue`를 `Kotlin`에서 `Java`로 변경했다.
- `Entry` 클러스터 없이 `Front`와 `API Gateway`를 별도 클러스터로 유지했다.
- `Front` 아래에 `API Gateway`가 오는 수직 흐름으로 배치했다.
- `Front -> API Gateway` 연결에 높은 edge weight를 적용해 두 클러스터가 같은 수직 축에 배치되도록 유도했다.
- `choimory-dev/choimory-dev.png` 이미지를 재생성했다.

---

# 구현 상세

## 대상 파일

- `choimory-dev/choimory-dev-architecture.py`
- `choimory-dev/choimory-dev.png`

## API Gateway

- `public-api`를 제거하고 `api-gateway`로 변경했다.
- `api-gateway`는 `Front` 클러스터 밖의 별도 `API Gateway` 클러스터로 유지했다.
- `Front`와 `API Gateway`는 위아래 수직 흐름으로 배치했다.
- `Front`에서 `API Gateway`로 향하는 연결은 `Edge(weight="100")`을 사용해 수직 정렬 우선순위를 높였다.
- `client`, `admin`은 `api-gateway`를 통해 `member-api`, `article-api`, `memo-api`, `sender-api`, `noti-api`를 호출하도록 표현했다.
- `noti-socket`은 실시간 연결이므로 `client`, `admin`과 직접 연결되는 구조를 유지했다.

## CI/CD

- CI는 애플리케이션 소스 리포지토리 기준 `github -> github-actions` 흐름으로 시작한다.
- `github-actions`가 Docker 이미지를 빌드하고 `dockerhub`로 push하는 흐름을 추가했다.
- `github-actions`가 `k8s-gitops-repo`의 Kustomize 이미지 태그를 갱신하는 흐름을 추가했다.
- CD는 `k8s-gitops-repo -> argo-cd -> k8s deploy -> k8s set -> k8s pod` 흐름으로 변경했다.
- 기존 `github-actions -> docker -> k8s deploy` 직접 배포 표현은 제거했다.

## Observability

- 기존 `Logging`, `Monitoring` 클러스터를 하나의 `Observability` 클러스터로 통합했다.
- `fluent-bit`, `loki`, `prometheus`, `grafana`를 추가했다.
- 로그 수집과 조회는 `k8s pod -> fluent-bit -> loki -> grafana`로 표현했다.
- 로그 장기 보관은 `fluent-bit -> s3`로 표현했다.
- 메트릭 수집과 조회는 `k8s pod -> prometheus -> grafana`로 표현했다.
- 기존 `logstash`, `elasticsearch`, `kibana` 기반 로그 흐름은 제거했다.

## Sender

- `sender-queue`를 `Kotlin`에서 `Java`로 변경했다.
- `sender-api`와 `sender-queue` 사이에는 직접 호출선을 두지 않는 기존 정책을 유지했다.
- `sender-queue`는 message broker와 연결되는 비동기 처리 컴포넌트로 유지했다.

---

# 검증

- 프로젝트 가상환경 Python으로 `choimory-dev-architecture.py`를 실행해 성공했다.
- 생성된 `choimory-dev/choimory-dev.png`에서 `api-gateway`가 별도 클러스터로 분리된 것을 확인했다.
- 생성된 이미지에서 CI가 `github -> github-actions -> dockerhub / k8s-gitops-repo` 흐름으로 표현되는 것을 확인했다.
- 생성된 이미지에서 CD가 `k8s-gitops-repo -> argo-cd -> k8s deploy -> k8s set -> k8s pod` 흐름으로 표현되는 것을 확인했다.
- 생성된 이미지에서 Observability가 `fluent-bit`, `loki`, `prometheus`, `grafana`로 구성된 것을 확인했다.
- 생성된 이미지에서 `sender-queue`가 Java 기반 컴포넌트로 표시되는 것을 확인했다.
- 생성된 이미지에서 `Entry` 클러스터가 제거된 것을 확인했다.
- 생성된 이미지에서 `Front` 아래에 `API Gateway`가 배치된 것을 확인했다.
- 생성된 이미지에서 `Front`와 `API Gateway`가 같은 수직 축에 가깝게 정렬된 것을 확인했다.
