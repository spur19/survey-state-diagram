# Survey State Diagram
Given a user spec for a survey, we aim to generate the state diagram for it

## Setup

1. Ensure Python 3.10+
2. Install dependencies:

```
pip install -r requirements.txt
```

3. Set your API key for OpenAI:

```
export OPENAI_API_KEY=your_key_here
```


## Usage

Generate states from a survey design document and write both the raw JSON and a Mermaid diagram (`.mmd`) to a folder:

```
python -m survey_states.cli --input path/to/survey_doc.txt --outdir outputs --model gpt-5
```

Outputs in `--outdir`:
- `<input_stem>.json`
- `<input_stem>.mmd` (Mermaid flowchart)

Flags:
- `--input`: path to the survey design document (text/markdown/HTML/PDF pre-text)
- `--outdir`: directory to write outputs (required)
- `--model`: OpenAI model that supports structured output (default `gpt-5`)

The tool uses LangChain structured outputs to return a list of survey states with fields:

- `depth`
- `prev_question`
- `prev_question_answer`
- `current_question`
- `next_question`

## Example

For a survey spec like this:

### Question 1: "Are you a student?"

Options:
- Yes
- No
- Maybe

Branching Logic:
  - If No → TERMINATE survey with message "Thank you for your interest. This survey is for students only"
  - If Yes or Maybe → Continue to Q2

### Question 2: "What are you studying?"
Options:
- Math
- Science
- Arts


### Question 3: "What is your gender?"
Options:
- Male
- Female
- Other

We should generate the following state diagram:

<img width="637" height="804" alt="Screenshot 2025-09-05 at 2 15 03 PM" src="https://github.com/user-attachments/assets/6889d73b-1bd3-4f9c-b2ca-1e48e6b42e8f" />



The raw states generated would be:

```
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

