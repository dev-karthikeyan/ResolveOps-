from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import JsonOutputParser

from prompts.investigation_prompt import INVESTIGATION_SYSTEM_PROMPT
from tools.investigation_tools import investigation_tools
from tools.litellm_router import get_model, get_fallback_model


def _build_agent(model):
    return create_react_agent(model, tools=investigation_tools)


def investigation_agent(state):
    """
    Build incident timeline and investigation summary using a
    tool-calling agent that can query GitHub and Confluence for
    additional context beyond what RAG retrieval already gathered.
    """

    ticket = state["ticket"]
    classification = state["classification"]
    retrieved_evidence = state["retrieved_evidence"]

    user_message = (
        f"Ticket:\n{ticket}\n\n"
        f"Classification:\n{classification}\n\n"
        f"Retrieved Evidence:\n{retrieved_evidence}\n\n"
        "Investigate this incident. Use tools if you need more context. "
        "Respond ONLY with the final JSON object described in your instructions."
    )

    messages = [
        SystemMessage(content=INVESTIGATION_SYSTEM_PROMPT),
        HumanMessage(content=user_message),
    ]

    primary_model = get_model("investigation")
    fallback_model = get_fallback_model("investigation")

    try:
        agent = _build_agent(primary_model)
        result = agent.invoke({"messages": messages})

    except Exception as primary_error:
        print(f"Primary model failed for investigation agent: {primary_error}")

        try:
            agent = _build_agent(fallback_model)
            result = agent.invoke({"messages": messages})

        except Exception as fallback_error:
            raise RuntimeError(
                f"Both primary and fallback models failed for investigation agent.\n"
                f"Primary Error: {primary_error}\n"
                f"Fallback Error: {fallback_error}"
            )

    final_message = result["messages"][-1]

    parser = JsonOutputParser()
    investigation = parser.parse(final_message.content)

    state["investigation"] = investigation

    return state