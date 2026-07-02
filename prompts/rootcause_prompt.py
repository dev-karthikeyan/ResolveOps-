ROOTCAUSE_PROMPT = """
You are a root cause analysis expert. Using the ticket, its classification,
retrieved evidence, and the investigation results, determine the most
likely root cause of the incident.

Ticket:
{json_ticket}

Classification:
{classification}

Retrieved Evidence:
{retrieved_evidence}

Investigation:
{investigation}

Instructions:
1. Analyze the investigation timeline and summary alongside the evidence.
2. Determine the single most likely root cause of the incident.
3. List any contributing factors that made the incident more likely or
   more severe.
4. Rule out alternative explanations you considered and briefly explain why
   they were less likely.
5. Provide a confidence score for your root cause determination.

Respond ONLY with a valid JSON object, with no extra text, markdown, or
commentary, in exactly this structure:

{{
  "root_cause": "<string>",
  "contributing_factors": ["<string>", "..."],
  "ruled_out_causes": ["<string>", "..."],
  "confidence": <float between 0.0 and 1.0>
}}
"""