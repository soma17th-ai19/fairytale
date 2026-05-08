# AI 모듈 명세

> 담당: 이종윤
> 마지막 수정: 2026-05-08

LangGraph 기반 "일기 + 인물 관계 → 맞춤 동화 1편 생성" 모듈의 입출력 명세 및 사용법.

---

## 1. 한 줄 요약

```python
from app.service import generate_story
from app.models.schemas import StoryRequest

story = generate_story(StoryRequest(...))
# → Story(title, body, lesson)
```

내부에서 LangGraph 워크플로우가 LLM(Solar/OpenAI/Fake)을 호출해 동화를 생성한다.

---

## 2. 입력 스키마 — `StoryRequest`

| 필드 | 타입 | 필수 | 설명 |
|---|---|---|---|
| `diary_date` | `date` (YYYY-MM-DD) | ✅ | 일기 날짜 |
| `diary` | `str` | ✅ | 해당 날짜의 일기 본문 (자유 문장) |
| `people` | `list[Person]` | (기본 `[]`) | 일기에 등장하는 주변 인물 목록 |

### `Person`

| 필드 | 타입 | 필수 | 설명 / 가능한 값 |
|---|---|---|---|
| `name` | `str` | ✅ | 인물 이름 (예: "민준", "엄마") |
| `relation` | `str` | ✅ | 자유 표현 (예: "엄마", "짝꿍", "담임선생님") |
| `kind` | `PersonKind` enum | (기본 `"기타"`) | `"가족" \| "친구" \| "선생님" \| "이웃" \| "기타"` |
| `closeness` | `int (1~5)` | optional | 친밀도. `1`=어색함, `2`=조금 거리감, `3`=보통, `4`=가까움, `5`=아주 가까움 |
| `role_today` | `str` | optional | 오늘 일기 속 역할 (예: "블록 갈등 상대", "위로해줌") |
| `traits` | `list[str]` | (기본 `[]`) | 성격/특징 키워드 (예: `["활발함", "장난기 많음"]`) |
| `note` | `str` | optional | 추가 메모 |

### JSON 입력 예시

```json
{
  "diary_date": "2026-05-08",
  "diary": "오늘 어린이집에서 민준이랑 블록 때문에 다퉜다. 선생님이 같이 만들자고 했고 집에서 엄마가 안아줬다.",
  "people": [
    {
      "name": "엄마",
      "relation": "엄마",
      "kind": "가족",
      "closeness": 5,
      "role_today": "저녁에 위로해줌",
      "traits": ["다정함"]
    },
    {
      "name": "민준",
      "relation": "짝꿍",
      "kind": "친구",
      "closeness": 4,
      "role_today": "블록 갈등 상대",
      "traits": ["장난기 많음", "활발함"]
    },
    {
      "name": "지수 선생님",
      "relation": "담임",
      "kind": "선생님",
      "closeness": 3,
      "role_today": "함께 만들기를 제안",
      "traits": ["차분함"]
    }
  ]
}
```

### 입력 가이드

- `kind`는 드롭다운으로 5개 중 선택. 기본값 `"기타"`.
- `closeness`는 1~5 정수. 슬라이더 또는 별점 UI 추천. 미입력 가능 (미입력 시 LLM이 일기 톤으로 추론).
- `role_today`는 한 줄 텍스트. 비워도 됨(권장은 입력).
- `traits`는 태그/칩 입력 형태가 잘 어울림.
- `people`은 비어 있어도 호출 가능 (일기만으로 동화 생성).

---

## 3. 출력 스키마 — `StoryResponse`

| 필드 | 타입 | 설명 |
|---|---|---|
| `story.title` | `str` | 동화 제목 |
| `story.body` | `str` | 동화 본문 (5~7세용 동화풍, 6~10문장) |

### JSON 출력 예시

```json
{
  "story": {
    "title": "블록 성을 함께 쌓은 두 친구",
    "body": "옛날 옛적, 별빛이 흐르는 마을에 활발한 다람쥐 민준이와 호기심 많은 토끼 지우가 살았어요. ..."
  }
}
```

---

## 4. 사용 방법

## 함수로 직접 호출

```python
from datetime import date
from app.service import generate_story
from app.models.schemas import StoryRequest, Person

req = StoryRequest(
    diary_date=date(2026, 5, 8),
    diary="오늘 민준이랑 블록 때문에 다퉜다. 선생님이 같이 만들자고 했다.",
    people=[
        Person(name="민준", relation="짝꿍", kind="친구",
               closeness=4, role_today="블록 갈등 상대",
               traits=["장난기 많음", "활발함"]),
        Person(name="지수 선생님", relation="담임", kind="선생님",
               closeness=3, role_today="함께 만들기 제안",
               traits=["차분함"]),
    ],
)

story = generate_story(req)   # 동기 호출, 평균 2~10초 (LLM 응답 시간 의존)
print(story.title, story.lesson)
```

#### 예외

`app.exceptions` 에서 가져와 라우트에서 잡으면 된다.

| 예외 | 의미 | 권장 HTTP 상태 |
|---|---|---|
| `LLMUnavailableError` | 업스트림 LLM 호출 자체 실패 (timeout / 401 / 429 / 5xx 등). `e.stage` 로 어느 단계(plan/write/critique)인지 알 수 있음 | **503** Service Unavailable |
| `StoryParsingError` | LLM이 응답은 했지만 결과를 추출할 수 없음 | **502** Bad Gateway |
| `StoryGenerationError` | 위 두 개의 베이스. 그 외 생성 실패 일반 | **422** Unprocessable Entity |
| `pydantic.ValidationError` | 입력값이 스키마 위반 (FastAPI가 자동 422 처리) | (FastAPI 자동) |

```python
from fastapi import HTTPException
from app.exceptions import LLMUnavailableError, StoryParsingError, StoryGenerationError

@router.post("/stories", response_model=StoryResponse)
def create_story(req: StoryRequest):
    try:
        story = generate_story(req)
    except LLMUnavailableError as e:
        raise HTTPException(503, detail=str(e))
    except StoryParsingError as e:
        raise HTTPException(502, detail=str(e))
    except StoryGenerationError as e:
        raise HTTPException(422, detail=str(e))
    return StoryResponse(story=story)
```

### 4-2. FastAPI 라우트로 감싸는 예시 (FastAPI 팀이 자체 구현)

이 모듈에는 FastAPI 코드가 포함되어 있지 않다. FastAPI 팀이 자체 라우트에서 아래처럼 감싸 쓰면 된다.

```python
from fastapi import APIRouter
from app.service import generate_story
from app.models.schemas import StoryRequest, StoryResponse

router = APIRouter(prefix="/api", tags=["stories"])

@router.post("/stories", response_model=StoryResponse)
def create_story(req: StoryRequest) -> StoryResponse:
    story = generate_story(req)
    return StoryResponse(story=story)
```

### 4-3. (Advanced) 그래프 직접 호출

FastAPI 팀이 그래프 상태를 더 다루고 싶다면:

```python
from app.graph.builder import graph

state = graph.invoke({
    "diary_date": "2026-05-08",
    "diary": "...",
    "people": [...],   # dict 형태
})
# state["story"] == {"title", "body", "lesson"}
```

단, 입력은 `dict` (TypedDict `GraphState`)로 직접 넣어야 함. 일반적으로는 `generate_story()`를 사용 권장.

---

## 5. 환경 설정

### 5-1. .env

`backend/.env` 에서 LLM 프로바이더를 선택:

```ini
# fake | openai | solar
LLM_PROVIDER=fake

OPENAI_API_KEY=
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o-mini

SOLAR_API_KEY=
SOLAR_BASE_URL=https://api.upstage.ai/v1/solar
SOLAR_MODEL=solar-pro
```

- 키가 없거나 통합 테스트만 할 때는 `fake` 그대로 두면 더미 응답이 반환된다 (그래프 흐름 검증 용도).
- 운영/시연 시에는 `solar` 또는 `openai`로 전환.

### 5-2. 의존성

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

`requirements.txt` 핵심 (AI 모듈 전용):
- `langgraph`, `langchain-core`, `langchain-openai`
- `pydantic`, `pydantic-settings`, `python-dotenv`

> FastAPI/uvicorn은 포함하지 않음. 통합 시 FastAPI 팀의 deps에 추가.

---

## 6. 동작 흐름 (Agentic LangGraph)

```
StoryRequest
   │
   ▼
service.generate_story()
   │
   ▼
LangGraph
  ┌────────┐    ┌────────┐    ┌──────────┐
  │ plan   │ ─▶ │ write  │ ─▶ │ critique │
  └────────┘    └────────┘    └────┬─────┘
                   ▲               │
                   │  (점수 미달)     │ (조건부 라우팅)
                   └───────────────┤
                                   ▼ (통과 또는 최대 재시도 도달)
                                ┌──────────┐
                                │ finalize │ ─▶ END
                                └──────────┘
```

### 노드 역할
| 노드 | 입력 | 출력 (state 변화) | 시스템 프롬프트 요약 |
|---|---|---|---|
| **plan** | 일기 + 인물 | `outline` (JSON 문자열) | 동화 outline 5슬롯: setting / protagonist / companions / magical_element / conflict / resolution |
| **write** | outline + 인물 (+ 이전 critique) | `draft_title`, `draft_body`, `revision_count++` | 동화풍 작성 규칙 따라 본문 작성. 재호출 시 critique 코멘트를 반영 |
| **critique** | draft | `critique{scores, average, comment, passed}` | 4개 기준 채점: fairy_tale / age_vocab / character_mapping / safety (1~5점) |
| **finalize** | draft | `story` 확정 | draft를 Story로 변환 |

### 라우팅 규칙
- `route_after_critique`:
  - `critique.passed == True` (평균 ≥ 4.0) → **finalize**
  - 통과 못했지만 `revision_count > MAX_REVISIONS (=1)` → **finalize** (무한루프 방지)
  - 둘 다 아니면 → **write** (피드백 받아 재집필)

### 일반 호출에서 LLM 호출 횟수
- 통과 시: 3회 (plan + write + critique) — 약 5~7초
- 1회 재시도 시: 4회 (plan + write + critique + write + critique) — 약 8~12초
  - critique은 재시도 시에도 작은 호출이라 1회 추가

LLM에 들어가는 인물 블록 예시:

```
〔가족〕
- 엄마 (엄마)
    · 친밀도: 5/5
    · 오늘의 역할: 저녁에 위로해줌
    · 특징: 다정함

〔친구〕
- 민준 (짝꿍)
    · 친밀도: 4/5
    · 오늘의 역할: 블록 갈등 상대
    · 특징: 장난기 많음, 활발함

〔선생님〕
- 지수 선생님 (담임)
    · 친밀도: 3/5
    · 오늘의 역할: 함께 만들기 제안
    · 특징: 차분함
```


## 8. 모듈 인터페이스 요약 (한 장)

| 항목 | 값 |
|---|---|
| Import path | `from app.service import generate_story` |
| 입력 타입 | `app.models.schemas.StoryRequest` |
| 출력 타입 | `app.models.schemas.Story` |
| FastAPI 라우트 | 이 모듈은 미포함. FastAPI 팀이 4-2 예시 참고해 직접 구현 |
| 환경설정 | `backend/.env` 의 `LLM_PROVIDER` |
| 동기/비동기 | 동기 (필요 시 threadpool) |
| 외부 의존 | LLM API (Solar/OpenAI) — `fake`로 우회 가능 |
