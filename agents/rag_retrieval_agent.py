from langchain_core.output_parsers import JsonOutputParser

from prompts.retrieval_prompt import RETRIEVAL_PROMPT
from rag.retriever import Retriever
from tools.litellm_router import invoke_with_fallback_model


def rag_retrieval_agent(state):
    """
    Retrieve relevant evidence from the vector database
    and summarize it using the LLM.
    """

    classification = state["classification"]
    ticket = state["ticket"]

    retriever = Retriever()

    documents = retriever.retrieve(
        query=ticket["description"],
        k=5,
        search_type="mmr",
    )

    retrieved_documents = "\n\n".join(
        [doc.page_content for doc in documents]
    )

    prompt = RETRIEVAL_PROMPT.format(
        classification=classification,
        ticket_json=ticket,
        retrieved_documents=retrieved_documents,
    )

    response = invoke_with_fallback_model(
        task="retrieval",
        prompt=prompt,
    )

    parser = JsonOutputParser()

    retrieved_evidence = parser.parse(response.content)

    state["retrieved_evidence"] = retrieved_evidence

    return state