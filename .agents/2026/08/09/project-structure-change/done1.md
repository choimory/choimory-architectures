# 목차

- [개요](#개요)
- [완료 내용](#완료-내용)
- [최종 아키텍처](#최종-아키텍처)
- [검증](#검증)

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
