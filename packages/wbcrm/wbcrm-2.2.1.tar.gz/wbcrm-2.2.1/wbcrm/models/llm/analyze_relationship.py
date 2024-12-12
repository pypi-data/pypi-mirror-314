from typing import TYPE_CHECKING

from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field
from wbcore.contrib.ai.llm.config import LLMConfig
from wbcrm.models.activities import Activity

if TYPE_CHECKING:
    from wbcrm.models import Account


def analyze_relationship_prompt(account: "Account"):
    messages = [
        SystemMessage(
            content="Based on the recent interactions/activities, current relationship health, and planned actions with the customer, provide a status score (1 to 5, where 1 is cold and 5 is hot), a summary of the relationship, and recommended next steps for maintaining or improving the relationship. Keep in mind that more information might become available later to refine these insights. Please include all information that is relevant to the relationship in the summary. Regarding the activities/interactions, older interactions are less relevant than recent ones."
        ),
        HumanMessage(
            content=f"The title of the account: {account.title}",
        ),
    ]
    if account.owner:
        for activity in Activity.objects.filter(companies__id__in=[account.owner.id], status="REVIEWED"):
            messages.append(
                HumanMessage(
                    content=f"Activity: {activity.summary}, with sentiment: {activity.heat}, period: {activity.period}",
                )
            )

    return messages


class AccountRelationshipResponseModel(BaseModel):
    relationship_status: int = Field(
        ...,
        ge=1,
        le=5,
        description="Rate the customer relationship status from 1 to 5. 1 being the cold and 5 being the hot.",
    )
    relationship_summary: str = Field(
        ...,
        description="Briefly summarize the current state of the relationship and recent interactions. Also include any additional information that might be relevant.",
    )
    action_plan: str = Field(
        ..., description="Provide the next recommended actions or steps to engage with the customer."
    )


analyze_relationship = LLMConfig["Account"](
    key="analyze_relationship",
    prompt=analyze_relationship_prompt,
    on_save=True,
    on_condition=lambda act: (act.status == act.Status.OPEN) and act.owner is not None and act.is_root_node(),
    output_model=AccountRelationshipResponseModel,
)
