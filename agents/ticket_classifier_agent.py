from langchain_core.output_parsers import JsonOutputParser

from prompts.classifier_prompt import CLASSIFIER_PROMPT
from tools.litellm_router import invoke_with_fallback_model


def ticket_classifier_agent(state):

    ticket = state["ticket"]

    prompt = CLASSIFIER_PROMPT.format(
        ticket_json=ticket
)

    response = invoke_with_fallback_model(
        task="classification",
        prompt=prompt
)

    parser = JsonOutputParser()

    classification = parser.parse(response.content)

    state["classification"] = classification

    return state

    