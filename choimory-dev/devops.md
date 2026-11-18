# choimory-dev devops

- [배포 흐름](#배포-흐름)
- [클러스터 구성](#클러스터-구성)
- [로그·메트릭](#로그메트릭)

> 점선: 계획 중인 구성 요소

---

# 배포 흐름

```mermaid
flowchart LR
    dev([Developer])

    subgraph github[GitHub]
        app_repo[앱 저장소]
        actions[GitHub Actions]
        ghcr[(GHCR)]
        gitops_repo[gitops 저장소]
    end

    subgraph cluster[Kubernetes]
        argocd[ArgoCD]
        apps["앱<br/>stg / prod"]
    end

    dev -->|push| app_repo
    app_repo -->|"Run workflow"| actions
    actions -->|"이미지 push"| ghcr
    actions -->|"이미지 태그 커밋"| gitops_repo
    gitops_repo -->|"변경 감지"| argocd
    argocd -->|배포| apps
    ghcr -->|"이미지 pull"| apps
```

- CI: 앱 저장소에서 GitHub Actions를 실행하여 테스트, 이미지 빌드 후 GHCR에 push
- CD: Actions가 gitops 저장소의 이미지 태그를 커밋하면, 클러스터 안의 ArgoCD가 변경을 감지하여 배포 (pull 방식, 인바운드 불필요)

---

# 클러스터 구성

```mermaid
flowchart LR
    subgraph cluster["Kubernetes (미니 PC, 단일 노드)"]
        subgraph infra[공용 도구]
            deploy["배포<br/>ArgoCD"]
            traffic["트래픽<br/>Envoy Gateway · cloudflared<br/>Tailscale Operator · cert-manager"]
            ops["운영<br/>Sealed Secrets · CloudNativePG<br/>local-path · metrics-server"]
        end

        subgraph stg["앱 (stg)"]
            stg_app["front · member-api"]
            stg_etc[기타 도메인]
            stg_db[("PostgreSQL · Redis")]
        end

        subgraph prod["앱 (prod)"]
            prod_app["front · member-api"]
            prod_etc[기타 도메인]
            prod_db[("PostgreSQL · Redis")]
        end
    end

    infra --> stg
    infra --> prod

    classDef planned stroke-dasharray: 5 5
    class stg_etc,prod_etc planned
```

- 공용 도구는 여러 프로젝트가 함께 사용하며, 프로젝트 앱은 환경(stg, prod)별로 분리
- PostgreSQL, Redis는 앱과 같은 환경 안에 프로젝트별·환경별로 하나씩 둠

---

# 로그·메트릭

```mermaid
flowchart LR
    apps["앱 / 공용 도구"]

    subgraph observability[Observability]
        loki[(Loki)]
        prometheus[(Prometheus)]
        grafana[Grafana]
    end

    apps -.->|로그| loki
    apps -.->|메트릭| prometheus
    loki -.-> grafana
    prometheus -.-> grafana

    classDef planned stroke-dasharray: 5 5
    class loki,prometheus,grafana planned
```

- 로그는 Loki, 메트릭은 Prometheus로 수집하고 Grafana로 시각화
