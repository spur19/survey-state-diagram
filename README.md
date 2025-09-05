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
python -m survey_states.cli --input path/to/survey_doc.txt --outdir outputs --model gpt-4o-mini
```

Outputs in `--outdir`:
- `<input_stem>.json`
- `<input_stem>.mmd` (Mermaid flowchart)

Flags:
- `--input`: path to the survey design document (text/markdown/HTML/PDF pre-text)
- `--outdir`: directory to write outputs (required)
- `--model`: OpenAI model that supports structured output (default `gpt-4o-mini`)

The tool uses LangChain structured outputs to return a list of survey states with fields:

- `depth`
- `prev_question`
- `prev_question_answer`
- `current_question`
- `next_question`
