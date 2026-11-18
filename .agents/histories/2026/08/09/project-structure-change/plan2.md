# 목차

- [개요](#개요)
- [Plan2 내용 검토](#plan2-내용-검토)
- [Plan2 구현 계획](#plan2-구현-계획)

---

# 개요

- public-api를 api-gateway로 변경
- api-gateway를 프론트와 백엔드 사이에 있는 별도 영역으로 
- CI/CD/Monitoring/Logging 수정
- CI 프로세스: Github 푸시 -> Github actions 구동 -> Docker 이미지 빌드하여 Dockerhub 푸시 -> K8s GitOps 리포지토리의 Kustomize를 edit하여  GitOps 리포지토리 신규 이미지 버전 반영
- CD 프로세스: ArgoCD가 K8s GitOps 리포지토리 폴링 -> 변경사항 감지 -> K8s 배포
- Logging: fluent-bit으로 Pod 로그 내용을 Loki로 수집, Grafana로 로그 확인
- Monitoring: Prometheus로 메트릭 정보 수집, Grafana로 메트릭 정보 확인

--

# Plan2 내용 검토

> 내용 괜찮은지 봐봐

## 답변

내용 방향은 괜찮다. 현재 다이어그램에서 흐릿하게 표현되어 있던 부분을 더 명확하게 만드는 계획이다. 다만 몇 군데는 표현을 정리하면 더 정확하다.

## 좋은 점

- `public-api`를 `api-gateway`로 바꾸는 것은 적절하다.
- `public-api`는 너무 추상적이고, 프론트와 백엔드 사이의 경계 컴포넌트라면 `api-gateway`가 더 명확하다.
- `api-gateway`를 별도 영역으로 분리하는 것도 좋다.
- 현재는 `Front` 클러스터 안에 있어서 역할이 어색하다.
- CI/CD를 GitHub Actions, DockerHub, GitOps repo, ArgoCD, K8s 배포 흐름으로 나누는 것은 현재보다 실제 운영 구조에 가깝다.
- Logging을 Fluent Bit, Loki, Grafana로 표현하는 것도 좋다.
- 기존 `Logstash -> Elasticsearch -> Kibana`보다 계획 내용과 더 잘 맞는다.

## 수정하면 좋은 점

- “K8s GitOps 리포지토리의 Kustomize를 edit”보다는 “K8s GitOps 리포지토리의 Kustomize 이미지 태그를 갱신”이 더 명확하다.
- “ArgoCD가 K8s GitOps 리포지토리 폴링”은 맞지만, 다이어그램 표현은 `ArgoCD`가 `GitOps Repo`를 감시하고 `K8s Cluster`에 sync/apply하는 식이 더 자연스럽다.
- Logging은 `Pod logs -> Fluent Bit -> Loki -> Grafana` 흐름으로 표현하면 명확하다.
- S3 장기 보관을 추가할 경우 `Fluent Bit -> S3`를 별도 가지로 표현한다.
- Monitoring은 `Prometheus -> Grafana`까지 표현하는 것이 좋다.
- Grafana는 로그와 메트릭을 둘 다 보는 UI로 두는 것이 자연스럽다.

## 정리된 구현 계획

```markdown
# 개요

- `public-api`를 `api-gateway`로 변경한다.
- `api-gateway`를 `Front`와 백엔드 도메인 서비스 사이의 별도 영역으로 분리한다.
- CI/CD, Monitoring, Logging 영역을 실제 운영 흐름 기준으로 수정한다.

## API Gateway

- `client`, `admin`은 `api-gateway`를 통해 백엔드 API를 호출한다.
- `api-gateway`는 `member-api`, `article-api`, `memo-api`, `sender-api`, `noti-api`로 요청을 라우팅한다.
- `noti-socket`은 실시간 연결이므로 `client`, `admin`과 직접 연결한다.

## CI

- GitHub push를 트리거로 GitHub Actions가 실행된다.
- GitHub Actions는 Docker 이미지를 빌드한다.
- 빌드한 이미지를 DockerHub에 push한다.
- GitHub Actions는 K8s GitOps 리포지토리의 Kustomize 이미지 태그를 갱신한다.

## CD

- ArgoCD는 K8s GitOps 리포지토리를 감시한다.
- GitOps 리포지토리 변경사항을 감지하면 K8s 클러스터에 sync/apply한다.
- K8s는 갱신된 이미지로 서비스를 배포한다.

## Logging

- Pod 로그는 Fluent Bit이 수집한다.
- Fluent Bit은 로그를 Loki로 전송한다.
- Grafana에서 Loki 로그를 조회한다.
- 장기 보관이 필요하면 Fluent Bit이 S3에도 로그를 업로드한다.

## Monitoring

- Prometheus가 K8s와 애플리케이션 메트릭을 수집한다.
- Grafana에서 Prometheus 메트릭을 확인한다.
```

--

# Plan2 구현 계획

> 구현계획

## 답변

Plan2 구현은 `api-gateway` 분리, CI/CD 흐름 재구성, Logging/Monitoring 재구성을 중심으로 진행한다.

## API Gateway

- 현재 `Front` 클러스터 안의 `Nginx("public-api")`를 제거한다.
- 별도 `API Gateway` 클러스터를 생성한다.
- `api_gateway = Nginx("api-gateway")`로 표현한다.
- `user >> [client, admin]` 흐름을 유지한다.
- `[client, admin] >> api_gateway`로 프론트와 API Gateway를 연결한다.
- `api_gateway >> member_api`로 회원 API 요청을 표현한다.
- `api_gateway >> article_api`로 게시글 API 요청을 표현한다.
- `api_gateway >> memo_api`로 메모 API 요청을 표현한다.
- `api_gateway >> sender_api`로 발송 API 요청을 표현한다.
- `api_gateway >> noti_api`로 알림 API 요청을 표현한다.

## Notification Socket

- 실시간 소켓은 API Gateway를 거치지 않는 표현을 유지한다.
- `[client, admin] - noti_socket` 연결을 유지한다.

## CI

- 현재 `github >> github_actions`만 있는 단순 표현을 확장한다.
- `github = Github("github")`로 애플리케이션 소스 리포지토리를 표현한다.
- `github_actions = GithubActions("github-actions")`로 CI 실행기를 표현한다.
- `dockerhub = Docker("dockerhub")`로 Docker 이미지 저장소를 표현한다.
- `gitops_repo = Github("k8s-gitops-repo")`로 K8s GitOps 리포지토리를 표현한다.
- CI 흐름은 `github >> github_actions >> dockerhub`이다.
- GitOps 이미지 태그 갱신 흐름은 `github_actions >> gitops_repo`이다.

## CD

- 현재 `github_actions >> docker >> deploy >> replica >> pod` 흐름을 GitOps 중심으로 변경한다.
- `argo_cd`를 추가한다.
- `gitops_repo >> argo_cd`로 ArgoCD가 GitOps 리포지토리를 감시하는 흐름을 표현한다.
- `argo_cd >> deploy`로 ArgoCD가 K8s 배포를 sync/apply하는 흐름을 표현한다.
- `deploy >> replica >> pod` 흐름은 유지한다.
- Docker 이미지 빌드/푸시는 CI에 두고, CD는 GitOps/ArgoCD/K8s 배포 중심으로 표현한다.

## Logging

- 현재 `logstash >> elasticsearch >> kibana` 흐름을 제거한다.
- `fluent-bit`, `loki`, `grafana` 기반으로 변경한다.
- 기본 로그 흐름은 `pod >> fluent_bit >> loki >> grafana`이다.
- S3 장기 보관을 표현할 경우 `fluent_bit >> s3`를 별도 가지로 연결한다.
- 기존 `Infra` 클러스터에도 `s3`가 있으므로 중복 노드를 만들지 않고 기존 `s3`로 연결하는 편이 좋다.

## Monitoring

- 현재 `prometheus >> grafana` 흐름은 유지하되 수집 대상을 명확히 한다.
- `pod >> prometheus >> grafana`로 K8s Pod 메트릭 수집과 조회 흐름을 표현한다.
- Grafana는 Logging/Monitoring에서 같이 쓰는 UI로 표현한다.

## Observability 통합 제안

- `Logging`, `Monitoring`을 따로 두면 Grafana가 중복되거나 선이 복잡해질 수 있다.
- `Observability` 클러스터 하나로 통합하는 방향을 추천한다.
- 구성은 `fluent-bit`, `loki`, `prometheus`, `grafana`이다.
- 로그 흐름은 `pod >> fluent_bit >> loki >> grafana`이다.
- 메트릭 흐름은 `pod >> prometheus >> grafana`이다.
- 장기 보관이 필요하면 `fluent_bit >> s3`를 추가한다.

## 이미지 재생성

- `choimory-dev` 디렉토리에서 프로젝트 가상환경 Python으로 실행한다.

```shell
../choimory-dev/venv/bin/python choimory-dev-architecture.py
```

- 실행 결과 `choimory-dev/choimory-dev.png`가 갱신된다.

## 검증

- 생성된 PNG를 확인한다.
- `api-gateway`가 `Front`와 백엔드 도메인 서비스 사이 별도 영역에 있는지 확인한다.
- `public-api`가 제거됐는지 확인한다.
- CI가 `GitHub -> GitHub Actions -> DockerHub / GitOps repo` 흐름인지 확인한다.
- CD가 `GitOps repo -> ArgoCD -> K8s deploy/set/pod` 흐름인지 확인한다.
- Logging이 `Fluent Bit -> Loki -> Grafana` 흐름인지 확인한다.
- Monitoring이 `Prometheus -> Grafana` 흐름인지 확인한다.

## 문서 기록

- 구현 시작 후 `task1.md`에 이어서 작업 내용을 추가한다.
- 최종 구현안은 Logging/Monitoring을 `Observability` 클러스터로 통합하는 방향을 우선한다.
