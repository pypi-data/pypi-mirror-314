from typing import TYPE_CHECKING

from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field
from wbcore.contrib.ai.llm.config import LLMConfig

if TYPE_CHECKING:
    from wbcrm.models import Activity


def analyze_activity_prompt(activity: "Activity"):
    return [
        SystemMessage(
            content="You are a manager in a company and there are activities, both internal as well as external, meaning between service providers, clients and ourselves. We want to analyze these activities in regards of their sentiment and summarize them in English. The summary should be a very short bottom-line focussed text."
        ),
        HumanMessage(
            content=f"title={activity.title}, description={activity.description}, period={activity.period}, participants={activity.participants.all()}, companies={activity.companies.all()}, review={activity.result}"
        ),
    ]


class ActivityLLMResponseModel(BaseModel):
    heat: int = Field(..., ge=1, le=4, description="The sentiment heat.")
    summary: str = Field(..., description="A summary of the activity in English.")


analyze_activity = LLMConfig["Activity"](
    key="analyze",
    prompt=analyze_activity_prompt,
    on_save=True,
    on_condition=lambda instance: instance.status == "REVIEWED",
    output_model=ActivityLLMResponseModel,
)
