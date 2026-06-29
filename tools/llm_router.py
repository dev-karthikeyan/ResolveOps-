from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_mistralai import ChatMistralAI

gemini_llm = ChatGoogleGenerativeAI(

      model = "gemini-2.5-flash" ,
      temperature = 0 ,
)

groq_llm = ChatGroq(
      model = "openai/gpt-oss-120b" ,
      temperature = 0 ,
)

mistral_llm = ChatMistralAI(
      model = "mistral-small-2603" ,
      temperature = 0 ,
)

deepseek_llm = mistral_llm 

TASK_MODEL_MAP = {

   "classification" : groq_llm ,
   "retrival" : groq_llm ,

   "investigation" : deepseek_llm ,
   "root_cause" : deepseek_llm ,
   "refelction" : deepseek_llm ,

   "solution" : gemini_llm ,
   "jira_update": gemini_llm,
   "slack_notification": gemini_llm,
}

FALLBACK_MODEL_MAP = {
    "classification": gemini_llm,
    "retrieval": gemini_llm,

    "investigation": mistral_llm,
    "root_cause": mistral_llm,
    "reflection": mistral_llm,

    "solution": groq_llm,

    "jira_update": groq_llm,
    "slack_notification": groq_llm,
}

def get_model(task: str):
    """
    Return primary model for task.
    """

    if task not in TASK_MODEL_MAP:
        raise ValueError(
            f"Unknown task: {task}"
        )

    return TASK_MODEL_MAP[task]


def get_fallback_model(task: str):
    """
    Return fallback model for task.
    """

    if task not in FALLBACK_MODEL_MAP:
        raise ValueError(
            f"Unknown task: {task}"
        )

    return FALLBACK_MODEL_MAP[task]


def invoke_with_fallback(task: str, prompt: str):
    """
    Invoke primary model.
    If it fails, invoke fallback model.
    """

    primary = get_model(task)
    fallback = get_fallback_model(task)

    try:
        return primary.invoke(prompt)

    except Exception as e:

        print(
            f"[Router] Primary model failed: {e}"
        )

        return fallback.invoke(prompt)


def available_tasks():
    """
    Return all supported tasks.
    """

    return list(TASK_MODEL_MAP.keys())