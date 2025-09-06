import json
import argparse
from pathlib import Path
from typing import Optional

from langchain_openai import ChatOpenAI

from models import StateList
from generate_mermaid_diagram import generate_mermaid_with_langchain



SYSTEM_PROMPT = """
You are a precise assistant that extracts a survey state diagram from a
survey design document. Return states strictly conforming to the schema.


# Rules:
- depth is 0 for the starting question and null for terminal states.
- You should create only one terminal state. For terminal states, depth and next question should be null. id should be "endingid".
- For non-start states, depth = previous state's depth + 1.
- prev_question is null for the start state; otherwise, set to the previous question.
- current_question_answer is the options chosen in the current question (null for start). If multiple options lead to the same next question, collect them in a list and use that as the current question answer.
- current_question is the question at this state.
- next_question is the precise next question from the document. Use "endingid" if the next step is to end the survey.
- Only include states that are explicitly supported by the document; do not invent content.
- Assign an 8-letter UUID per question.
- It is possible to arrive at the same question from different previous questions. In such cases, you should keep the id the same and update the rest of the fields.

For example, if the document says:
- Question 1: "Are you a student?"

Options:
- Yes
- No
- Maybe

Branching Logic:
  - If No → TERMINATE survey with message "Thank you for your interest. This survey is for students only"
  - If Yes or Maybe → Continue to Q2

- Question 2: "What are you studying?"
Options:
- Math or Science
- Arts


- Question 3: "What is your gender?"
Options:
- Male
- Female
- Other

The states are:

{
  "question_states": [
    {
      "id": "1a2b3c4d",
      "depth": 0,
      "prev_question": null,
      "current_question_answer": "No",
      "current_question": "Are you a student?",
      "next_question": "endingid"
    },
    {
      "id": "1a2b3c4d",
      "depth": 0,
      "prev_question": null,
      "current_question_answer": "Yes, Maybe",
      "current_question": "Are you a student?",
      "next_question": "3a4b5c6d"
    },
    {
      "id": "endingid",
      "depth": null,
      "prev_question": "1a2b3c4d",
      "current_question_answer": null,
      "current_question": "END_SURVEY",
      "next_question": null
    },
    {
      "id": "3a4b5c6d",
      "depth": 1,
      "prev_question": "1a2b3c4d",
      "current_question_answer": "Math, Science, Arts",
      "current_question": "What are you studying?",
      "next_question": "4a5b6c7d"
    },
    {
      "id": "4a5b6c7d",
      "depth": 2,
      "prev_question": "3a4b5c6d",
      "current_question_answer": "Male, Female, Other",
      "current_question": "What is your gender?",
      "next_question": "endingid"
    },
}


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
        default="gpt-5",
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

    json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    # Generate Mermaid diagram from the states JSON
    generate_mermaid_with_langchain(
        question_states_json=json.dumps(data, ensure_ascii=False, indent=2),
        output_dir=str(outdir),
        model=model,
        filename=f"{base}.mmd",
    )



if __name__ == "__main__":
    main()

