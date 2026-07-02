SOLUTION_PROMPT = """
You are a senior engineer generating the final incident resolution. Use the
ticket, classification, retrieved evidence, investigation, root cause, and
reflection to produce a clear, actionable solution.

Ticket:
{json_ticket}

Classification:
{classification}

Retrieved Evidence:
{retrieved_evidence}

Investigation:
{investigation}

Root Cause:
{root_cause}

Reflection:
{reflection}

Instructions:
1. Restate the confirmed root cause concisely.
2. Provide a clear, actionable recommended solution to resolve the
   incident, including any specific steps the team should take.
3. Provide a confidence score (0.0-1.0) reflecting how certain you are that
   this solution will resolve the issue, taking the reflection findings
   into account.
4. Write a concise, professional Jira comment summarizing the root cause
   and solution, suitable for posting directly on the ticket.

Respond ONLY with a valid JSON object, with no extra text, markdown, or
commentary, in exactly this structure:

{{
  "root_cause": "<string>",
  "solution": "<string>",
  "confidence": <float between 0.0 and 1.0>,
  "jira_comment": "<string>"
}}
"""