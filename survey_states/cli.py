import json
import argparse
from pathlib import Path
from typing import Optional

from langchain_openai import ChatOpenAI

from .models import StateList



SYSTEM_PROMPT = 
"""
You are a precise assistant that extracts a survey state diagram from a
survey design document. Return states strictly conforming to the schema.

Rules:
- depth is 0 for the starting question.
- For non-start states, depth = previous state's depth + 1.
- prev_question is null for the start state; otherwise, set to the previous question.
- prev_question_answer is the answer chosen in the previous question that led here (null for start).
- current_question is the question at this state.
- next_question is the next question if known from the document; otherwise null (for terminal states or when unspecified).
- Only include states that are explicitly supported by the document; do not invent content.
- If branching occurs, create one state per distinct branch.
- Assign an 8-letter UUID per question.


You will be given a survey design document and you will need to return a dictionary that maps question ids to a list of all possible survey states for that question, with an 8-letter UUID per question.
"""

HUMAN_PROMPT = "Survey design document: {doc}"


def generate_states_from_doc(
    document_text: str, model: str, temperature: float
) -> StateList:

    structured_llm = ChatOpenAI(model=model, temperature=temperature).with_structured_output(StateList)

    result: StateList = structured_llm.invoke(
        [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": HUMAN_PROMPT.format(doc=document_text)},
        ]
    )
    return result

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate survey states from a design document using OpenAI structured output.",
    )
    parser.add_argument(
        "--input",
        required=True,
        type=Path,
        help="Path to the survey design document (text/markdown/HTML/PDF pre-text).",
    )
    parser.add_argument(
        "--outdir",
        required=True,
        type=Path,
        help="Directory to write outputs (JSON and Mermaid diagram).",
    )
    parser.add_argument(
        "--model",
        default="gpt-4o-mini",
        help="OpenAI model name that supports structured output.",
    )

    args = parser.parse_args()

    input_path: Path = args.input
    outdir: Path = args.outdir
    model: str = args.model
    temperature: float = 0.0

    document_text = input_path.read_text(encoding="utf-8")
    states = generate_states_from_doc(
        document_text=document_text,
        model=model,
        temperature=temperature,
    )

    data = states.model_dump()

    outdir.mkdir(parents=True, exist_ok=True)
    base = input_path.stem
    json_path = outdir / f"{base}.json"
    diagram_path = outdir / f"{base}.mmd"

    json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    diagram_path.write_text(mermaid, encoding="utf-8")



if __name__ == "__main__":
    main()

