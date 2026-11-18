# 목차

- [개요](#개요)
- [작업 요약](#작업-요약)
  - [1차: python diagrams에서 Mermaid로 전환](#1차-python-diagrams에서-mermaid로-전환)
  - [2차: 최신 프로젝트 구성 반영](#2차-최신-프로젝트-구성-반영)
  - [3차: 영어 변환과 dark 테마 적용 후 롤백](#3차-영어-변환과-dark-테마-적용-후-롤백)
  - [원격 브랜치 merge와 push](#원격-브랜치-merge와-push)
- [최종 결과](#최종-결과)
  - [디렉토리 구조](#디렉토리-구조)
  - [다이어그램 관리 방식](#다이어그램-관리-방식)
  - [다이어그램 목록](#다이어그램-목록)
- [남은 사항](#남은-사항)

---

# 개요

- diagrams(python) + graphviz로 PNG를 생성하던 아키텍처 관리 방식을 Mermaid로 전환함
- choimory-dev 프로젝트의 최신 구성(노션 Back-end, 홈서버 미니PC 세팅 문서 기준)을 다이어그램에 반영함
- 참고 문서: `plan1.md`, `plan2.md`, `task1.md`, `task2.md`

---

# 작업 요약

## 1차: python diagrams에서 Mermaid로 전환

- plan1, task1
- 프로젝트별 디렉토리 안에 관점별 문서를 만들어 Mermaid로 작성하기로 함 (분리 단위는 프로젝트마다 적절히 결정)
- 다이어그램은 관점별 문서(원본) → 프로젝트 README → 루트 README 순서로 복사하고, 복사본에는 출처 주석과 원본 링크를 함께 작성
- 기존 `choimory-dev-architecture.py`, `choimory-dev.png`, `README2.md` 제거

## 2차: 최신 프로젝트 구성 반영

- plan2, task2
- 기존 py 구성을 그대로 따르지 않고, 최신 구성을 기준으로 보기 좋게 재작성
- 구성
  - 클라이언트: front, mobile, admin, AI Agent
  - 서비스 도메인 6개: member, blog, memo, career, feed, scrap
  - 코어 도메인 2개: sender, noti
  - 데브옵스: GitHub Actions, GHCR, gitops 저장소, ArgoCD, 단일 노드 Kubernetes, Loki·Prometheus·Grafana
  - 네트워크: Cloudflare Tunnel(공개), Tailscale(내부 도구, DB)
- 표현 규칙
  - 도메인 간 호출은 "내부 통신 (gRPC / Kafka)" 노드 하나로 묶음
  - 계획 중인 구성 요소는 점선
  - 주소, IP, 네임스페이스 이름, 버전 같은 값은 넣지 않음
- devops 클러스터 구성이 가로로 길어 LR 방향과 역할별 노드 묶음으로 수정

## 3차: 영어 변환과 dark 테마 적용 후 롤백

- 다이어그램 라벨을 영어로 바꾸고 dark 테마를 고정 적용했으나, 결과가 마음에 들지 않아 롤백함
- 다이어그램은 2차 작업 완료 시점 상태로 유지

## 원격 브랜치 merge와 push

- 로컬 `dev`와 `origin/dev`가 갈라져 push가 거부됨
- `git pull`로 merge하며 충돌 정리
  - `README.md`, `choimory-dev`: Mermaid 버전 유지, `.py`·`.png` 삭제
  - `AGENTS.md`, `.agents/rules`: 로컬 harness 버전 유지, 예전 위치의 code-convention 문서 3개 삭제
  - `calendar.md`: 양쪽 항목 모두 유지
  - 원격의 project-structure-change 히스토리 문서는 그대로 반영
- merge 커밋 후 `origin/dev`에 push

---

# 최종 결과

## 디렉토리 구조

```
choimory-architectures/
├── README.md               # 전체 프로젝트 목차 및 프로젝트별 다이어그램
└── choimory-dev/
    ├── README.md           # 프로젝트 개요 및 다이어그램 모음
    ├── service.md          # 서비스 구성 (원본)
    ├── devops.md           # 배포, 클러스터, 로그·메트릭 (원본)
    └── network.md          # 접속 경로 (원본)
```

## 다이어그램 관리 방식

- 수정은 항상 관점별 문서(원본)에서 하고, 프로젝트 README → 루트 README 순서로 복사하여 동기화
- 복사본에는 `<!-- source: {project}/{view}.md -->` 주석과 원본 링크를 함께 작성
- 계획 중인 구성 요소는 점선으로 표시

## 다이어그램 목록

| 문서 | 다이어그램 |
|---|---|
| `service.md` | 전체 구성, 도메인 공통 구조 (+ 도메인 목록 표) |
| `devops.md` | 배포 흐름, 클러스터 구성, 로그·메트릭 |
| `network.md` | 접속 경로 (+ 경로별 공개 범위 표) |

---

# 남은 사항

- 로컬에 Node가 없어 Mermaid 렌더링은 GitHub에서 직접 확인 필요
- 3차 작업의 분석 문서 `plan3.md`는 작업 폴더에서 사라져 남아 있지 않음
