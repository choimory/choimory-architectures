# choimory-dev

- [개요](#개요)
- [service](#service)
  - [전체 구성](#전체-구성)
  - [도메인 공통 구조](#도메인-공통-구조)
- [devops](#devops)
  - [배포 흐름](#배포-흐름)
  - [클러스터 구성](#클러스터-구성)
  - [로그·메트릭](#로그메트릭)
- [network](#network)
  - [접속 경로](#접속-경로)

---

# 개요

- 토이 프로젝트 choimory-dev의 전체 구성
- 클라이언트(front, mobile, admin)와 서비스 도메인(member, blog, memo, career, feed, scrap), 코어 도메인(sender, noti)으로 구성
- 모든 도메인은 api / grpc / queue / mcp 모듈을 기본으로 가지며, gRPC(동기)와 Kafka(비동기)로 서로 호출
- 미니 PC의 단일 노드 Kubernetes에 GitHub Actions + ArgoCD(GitOps)로 배포하고, Cloudflare Tunnel(공개)과 Tailscale(내부)로 접속

| 문서 | 내용 |
|---|---|
| [service.md](./service.md) | 클라이언트, 도메인 구성, 도메인 공통 구조, 도메인 목록 |
| [devops.md](./devops.md) | 배포 흐름, 클러스터 구성, 로그·메트릭 |
| [network.md](./network.md) | 공개 / 내부 접속 경로 |

> 점선: 계획 중인 구성 요소

---

# service

## 전체 구성

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

- 상세: [service.md](./service.md)

## 도메인 공통 구조

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

- 상세: [service.md](./service.md)

---

# devops

## 배포 흐름

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

- 상세: [devops.md](./devops.md)

## 클러스터 구성

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

- 상세: [devops.md](./devops.md)

## 로그·메트릭

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

- 상세: [devops.md](./devops.md)

---

# network

## 접속 경로

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

- 상세: [network.md](./network.md)

