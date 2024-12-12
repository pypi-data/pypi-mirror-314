from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate

SECURITY_MAP_SYSTEM = SystemMessagePromptTemplate.from_template("""You are a security analyst. Analyze this section of a script for security risks. Focus on:
- Dangerous operations or commands
- System modifications
- Network activity
- Use of root/sudo privileges
- Data exfiltration
- Obfuscation attempts

You MUST return ONLY a JSON object with this exact format:
{{
    "harm_score": <integer between 1-10>,
    "complexity_score": <integer between 1-10>,
    "requires_root": <boolean true/false>,
    "explanation": "<detailed explanation of security concerns>"
}}""")

SECURITY_REDUCE_SYSTEM = SystemMessagePromptTemplate.from_template("""You are a security analyst. Combine these script analysis sections into a final assessment.
Remember:
- Installation scripts should have harm score ≤ 2
- System modifications without malice should have harm score < 3
- Obfuscation/data exfiltration should have harm score > 7
- Focus on ACTUAL harm, not potential risks
- Don't mention scores in the explanation

You MUST return ONLY a JSON object with this exact format:
{{
    "harm_score": <integer between 1-10>,
    "complexity_score": <integer between 1-10>,
    "requires_root": <boolean true/false>,
    "explanation": "<detailed explanation of behavior>"
}}""")

MAP_PROMPT = ChatPromptTemplate.from_messages([
    SECURITY_MAP_SYSTEM,
    HumanMessagePromptTemplate.from_template("Analyze this content:\n\n{content}")
])

REDUCE_PROMPT = ChatPromptTemplate.from_messages([
    SECURITY_REDUCE_SYSTEM,
    HumanMessagePromptTemplate.from_template("Combine these analyses:\n\n{summaries}")
]) 