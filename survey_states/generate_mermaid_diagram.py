from langchain_openai import ChatOpenAI
import os
from pathlib import Path

SYSTEM_PROMPT_MERMAID = """
You are a precise assistant that generates a Mermaid flowchart from survey question states.

Requirements:
- Use flowchart TD format
- Start with Start([Survey Start]) node
- Questions as Q1{{current_question}} nodes. Use the current_question string and remove brackets from it, do not use the id.
- DO NOT USE ANY BRACKETS IN THE QUESTION NAMES. REMOVE ANY IF THEY EXIST.
- End nodes as End[END_SURVEY]
- Show answers on edge arrows: |current_question_answer|
- Group multiple answers to same destination
- Do not add any styling, just focus on generating the correct Mermaid code.
Output ONLY the Mermaid code. Do not include backticks or explanations.
"""

def generate_mermaid_with_langchain(
    question_states_json: str,
    output_dir: str,
    api_key: str = None,
    model: str = "gpt-4o-mini",
    filename: str = "survey_flow.mmd",
) -> str:
    """
    Generate Mermaid diagram from question states using message-based invocation and save to file.

    Args:
        question_states_json: JSON string containing question states
        output_dir: Directory to save the Mermaid file
        api_key: OpenAI API key (optional if set in env)
        model: OpenAI model to use
        filename: Output filename

    Returns:
        Path to the generated file (as a string)
    """

    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key

    llm = ChatOpenAI(model=model, temperature=0.0)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT_MERMAID},
        {"role": "user", "content": f"Question states JSON: {question_states_json}",},
    ]

    ai_message = llm.invoke(messages)
    mermaid_code: str = (ai_message.content or "").strip()


    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    output_file = output_path / filename
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(mermaid_code)

    print(f"Mermaid diagram saved to: {output_file}")
    return str(output_file)
