# 목차

- [개요](#개요)
- [plan2 기반 다이어그램 재작성](#plan2-기반-다이어그램-재작성)
  - [답변](#답변)
  - [service.md](#servicemd)
  - [devops.md](#devopsmd)
  - [network.md](#networkmd)
  - [README](#readme)
  - [히스토리](#히스토리)
  - [임의로 정한 것](#임의로-정한-것)
  - [검증](#검증)
- [devops 클러스터 구성 가로 길이 수정](#devops-클러스터-구성-가로-길이-수정)
  - [답변](#답변-1)
  - [원인](#원인)
  - [수정 내용](#수정-내용)
  - [수정 결과](#수정-결과)

---

# 개요

- plan2(추가1, 추가2 분석)에서 정한 최종안을 기준으로 choimory-dev 다이어그램을 재작성함
- 최신 프로젝트 구성(프론트 3개, 서비스 도메인 6개, 코어 도메인 2개, k8s 기반 데브옵스, Cloudflare·Tailscale 네트워크)을 반영
- 계획 중인 구성 요소는 점선으로 표시하고, 주소·IP·네임스페이스 이름·버전 같은 값은 넣지 않음
- 문서 분리: `service.md`, `devops.md`, `network.md`(신규)

---

# plan2 기반 다이어그램 재작성

> 작업 시작해줘

## 답변

- plan2 최종안대로 다이어그램 문서 3개를 작성하고, 프로젝트 README와 루트 README의 복사본을 다시 맞춤

## service.md

- 다이어그램 2개, 표
- 전체 구성
  - 클라이언트(front, mobile, admin, AI Agent), 서비스 도메인 6개(member, blog, memo, career, feed, scrap), 코어 도메인 2개(sender, noti)
  - 도메인 간 호출은 "내부 통신 (gRPC / Kafka)" 노드 하나로 묶음
  - 외부 연동(Discord, Firebase, 메일·SMS) 연결
- 도메인 공통 구조
  - api, grpc, queue, mcp와 선택 모듈 batch, socket이 command / query / cache 저장소와 연결되는 구조를 한 번만 그림
  - 모듈 역할 표 추가
- 도메인 목록
  - 서비스 도메인, 코어 도메인 표 정리
  - scrap 저장소는 PostgreSQL, ES로 반영

## devops.md

- 다이어그램 3개
- 배포 흐름: 앱 저장소 → GitHub Actions → GHCR, gitops 저장소 → ArgoCD → 앱
- 클러스터 구성: 공용 도구(ArgoCD, Envoy Gateway, cloudflared, Tailscale Operator, cert-manager, Sealed Secrets, CloudNativePG, local-path, metrics-server)와 앱 stg, prod
- 로그·메트릭: Loki, Prometheus, Grafana (전부 점선)

## network.md

- 신규 작성. 다이어그램 1개, 표
- 공개 경로: 사용자 → Cloudflare → Tunnel → cloudflared → 공개용 Gateway → 앱
- 내부 경로: 내 기기 → Tailscale → 내부용 Gateway → 인프라 도구 / Tailscale → DB
- 공유기는 노드로 두지 않고 "포트포워딩 없음" 표시를 단 그룹으로 감쌈

## README

- `choimory-dev/README.md`
  - 개요를 새 구성에 맞게 수정
  - 문서 안내 표에 network.md 추가
  - 다이어그램 6개 복사본과 원본 링크
- 루트 `README.md`
  - choimory-dev 섹션에 service, devops, network 복사본과 원본 링크
  - 다이어그램 관리 방식 섹션에 "계획 중인 구성 요소는 점선" 규칙 추가

## 히스토리

- `calendar.md`를 `TASK:Mermaid 전환 작업(mermaid-migration)`으로 변경

## 임의로 정한 것

- 점선 기준
  - 실선: front, member, k8s, 배포 흐름, Cloudflare Tunnel, Tailscale
  - 점선: 그 외 클라이언트·도메인, 내부 통신(Kafka), 외부 연동, 로그·메트릭, 각 환경의 "기타 도메인"
- Tailscale DB 접속: 노션상 5단계가 진행 중(push 대기)이지만 거의 끝난 상태라 실선으로 표시
- 도메인 공통 구조: 계획·구현 구분 없이 목표 구조로 그리고, batch와 socket은 점선 대신 "(선택)"으로 표시
- 값 제외: 주소, IP, 네임스페이스 이름, 버전은 넣지 않음

## 검증

- 다이어그램 6개 모두 프로젝트 README, 루트 README의 복사본이 원본과 동일함을 확인
- 로컬에 Node가 없어 Mermaid 렌더링은 확인하지 못함. GitHub에서 렌더링 확인 필요
- 커밋은 진행하지 않음

---

# devops 클러스터 구성 가로 길이 수정

> devops의 클러스터구성쪽 머메이드가 너무 가로로 길어

## 답변

- 방향을 LR로 바꾸고, 노드를 역할별로 묶어 가로 길이를 줄임

## 원인

- TB 방향에서는 서로 연결선이 없는 노드들이 한 줄에 옆으로 늘어섬
- 공용 도구 9개, stg 5개, prod 5개가 모두 가로로 펼쳐짐
- 연결선 라벨("배포 · 라우팅 · 비밀값 · DB 관리")도 길어서 가로 길이를 늘림

## 수정 내용

- 방향을 LR로 변경: 공용 도구가 왼쪽, stg와 prod가 오른쪽에 위아래로 놓이고, 각 그룹 안의 노드도 세로로 쌓임
- 공용 도구 9개를 역할별 노드 3개로 묶음
  - 배포: ArgoCD
  - 트래픽: Envoy Gateway, cloudflared, Tailscale Operator, cert-manager
  - 운영: Sealed Secrets, CloudNativePG, local-path, metrics-server
- 환경별 노드 5개를 앱(front · member-api) / 기타 도메인(점선) / DB(PostgreSQL · Redis) 3개로 묶음
- 연결선 라벨 제거

## 수정 결과

- `choimory-dev/devops.md` 클러스터 구성 다이어그램 수정 (원본)
- `choimory-dev/README.md`, 루트 `README.md`의 복사본도 같은 내용으로 교체. 세 파일 모두 예전 노드가 남아 있지 않음을 확인
- 렌더링은 로컬에서 확인하지 못함. GitHub에서 폭 확인 필요
