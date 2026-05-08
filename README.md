# Kid Story · AI 모듈

해당 날짜의 일기와 주변 인물 관계를 입력받아 5~7세용 맞춤 동화를 생성하는 LangGraph 기반 AI 모듈.

> 이 저장소는 **AI 부분만** 포함합니다. FastAPI/프론트엔드는 별도 팀이 담당.
> 외부 인터페이스 명세는 [`docs/AI_MODULE_SPEC.md`](docs/AI_MODULE_SPEC.md) 참고.

## 셋업

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env   # 키 없으면 LLM_PROVIDER=fake 그대로 두면 됨
```

## 사용

```python
from datetime import date
from app.service import generate_story
from app.models.schemas import StoryRequest, Person

story = generate_story(StoryRequest(
    diary_date=date(2026, 5, 8),
    diary="오늘 민준이랑 블록 때문에 다퉜다.",
    people=[Person(name="민준", relation="짝꿍", kind="친구", closeness=4)],
))
print(story.title, story.body, story.lesson)
```

## 디렉토리

```
backend/
  requirements.txt       langgraph / langchain / pydantic 만 포함
  .env.example
  app/
    config.py            .env 로딩
    service.py           ★ 외부 진입점: generate_story(req)
    llm/client.py        LLM 추상화 (Fake/OpenAI/Solar)
    models/schemas.py    StoryRequest / Person / Story / StoryResponse
    graph/
      state.py           GraphState
      nodes.py           generate 노드 (프롬프트 구성)
      builder.py         LangGraph 컴파일
docs/
  AI_MODULE_SPEC.md      입출력 명세 + 사용법 (팀 공유용)
```
