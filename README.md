# choimory-architectures

- [개요](#개요)
- [디렉토리 구조](#디렉토리-구조)
- [다이어그램 관리 방식](#다이어그램-관리-방식)
- [choimory-dev](#choimory-dev)
  - [service](#service)
  - [devops](#devops)
  - [network](#network)

---

# 개요

- 다양한 프로젝트의 아키텍처를 [Mermaid](https://mermaid.js.org)로 작성하여 관리하는 리포지토리
- 별도 빌드나 이미지 생성 없이 GitHub에서 Markdown 그대로 다이어그램이 렌더링됨

---

# 디렉토리 구조

```
choimory-architectures/
├── README.md               # 전체 프로젝트 목차 및 프로젝트별 다이어그램
└── {project}/
    ├── README.md           # 프로젝트 개요 및 프로젝트 다이어그램 모음
    └── {view}.md           # 관점별 상세 다이어그램 (원본)
```

- 관점별 문서(`{view}.md`)는 고정되어 있지 않으며, 프로젝트 구성에 맞게 적절히 분리함 (예: service, devops, network)

---

# 다이어그램 관리 방식

```mermaid
flowchart LR
    view["{project}/{view}.md<br/>(원본)"] -->|복사| project_readme["{project}/README.md"] -->|복사| root_readme["README.md"]
```

- 다이어그램 수정은 항상 관점별 문서(원본)에서 하고, 프로젝트 README → 루트 README 순서로 복사하여 동기화함
- 복사본에는 `<!-- source: {project}/{view}.md -->` 주석과 원본 링크를 함께 작성함
- 계획 중인 구성 요소는 점선으로 표시함

---

# choimory-dev

- 토이 프로젝트 choimory-dev의 전체 구성
- 상세: [choimory-dev/README.md](./choimory-dev/README.md)

## service

### 전체 구성

<!-- source: choimory-dev/service.md -->
```mermaid
flowchart LR
    subgraph clients[Client]
        front["front<br/>Next.js"]
        mobile["mobile<br/>React Native"]
        admin["admin<br/>Next.js"]
        agent["AI Agent"]
    end

    subgraph service[Service domain]
        member[member]
        blog[blog]
        memo[memo]
        career[career]
        feed[feed]
        scrap[scrap]
    end

    subgraph core[Core domain]
        sender[sender]
        noti[noti]
    end

    internal{{"내부 통신<br/>gRPC / Kafka"}}

    subgraph external[External]
        discord[Discord]
        firebase[Firebase]
        mail["메일 / SMS"]
    end

    clients -->|"api / mcp"| service
    clients -.->|"api / socket"| core

    service <-.-> internal
    core <-.-> internal

    feed -.-> discord
    scrap -.-> discord
    sender -.-> discord
    sender -.-> mail
    sender -.-> firebase
    noti -.-> firebase

    classDef planned stroke-dasharray: 5 5
    class mobile,admin,agent,blog,memo,career,feed,scrap,sender,noti,internal,discord,firebase,mail planned
```

- 상세: [service.md](./choimory-dev/service.md)

### 도메인 공통 구조

<!-- source: choimory-dev/service.md -->
```mermaid
flowchart LR
    client([Client])
    agent([AI Agent])
    other([다른 도메인])
    kafka{{Kafka}}

    subgraph domain[Domain]
        api[api]
        grpc[grpc]
        queue[queue]
        mcp[mcp]
        batch["batch (선택)"]
        socket["socket (선택)"]
    end

    subgraph storage[Storage]
        command[("command<br/>PostgreSQL")]
        query[("query<br/>Elasticsearch / MongoDB")]
        cache[("cache<br/>Redis")]
    end

    client -->|HTTP| api
    client <-->|WebSocket| socket
    agent -->|MCP| mcp
    other -->|gRPC| grpc
    other --> kafka --> queue

    domain --> storage
    command -->|"동기화 (queue)"| query
```

- 상세: [service.md](./choimory-dev/service.md)

## devops

### 배포 흐름

<!-- source: choimory-dev/devops.md -->
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

- 상세: [devops.md](./choimory-dev/devops.md)

### 클러스터 구성

<!-- source: choimory-dev/devops.md -->
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

- 상세: [devops.md](./choimory-dev/devops.md)

### 로그·메트릭

<!-- source: choimory-dev/devops.md -->
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

- 상세: [devops.md](./choimory-dev/devops.md)

## network

### 접속 경로

<!-- source: choimory-dev/network.md -->
```mermaid
flowchart LR
    user([사용자])
    me(["내 기기<br/>Tailscale"])

    cloudflare["Cloudflare<br/>DNS · Tunnel"]
    tailnet{{Tailscale}}

    subgraph home["원룸 공유기 (포트포워딩 없음)"]
        subgraph server["미니 PC · Kubernetes"]
            cloudflared[cloudflared]
            public_gw["Envoy Gateway<br/>공개용"]
            infra_gw["Envoy Gateway<br/>내부용"]
            apps["앱<br/>front / api"]
            tools["인프라 도구<br/>ArgoCD 등"]
            db[("PostgreSQL / Redis")]
        end
    end

    user -->|HTTPS| cloudflare
    cloudflare -->|Tunnel| cloudflared
    cloudflared --> public_gw --> apps

    me --> tailnet
    tailnet --> infra_gw --> tools
    tailnet --> db
```

- 상세: [network.md](./choimory-dev/network.md)

