# Multi-Agent Workflow for Resume Processing
### Objective

Develop a multi-agent workflow that performs the following tasks:

- Resume Reading: Read and process multi-page resumes in various formats (e.g., PDF, DOCX).

- Entity Extraction: Extract key entities from the resumes, such as personal information, education, work experience, skills, and other pertinent details.

- Entity Validation: Validate the extracted entities for accuracy and completeness. If any issues are detected, the system should flag them and initiate a correction process.


## Table of contents:
- Features
- How does it work?
- Structure
- How to run?

### Features
- **UI**: Streamlit
- **Framework**: Langgraph, Langchain
- **Model**: OpenAI (integrated within Langchain)
- **File Loaders**: PyMuPDFLoader and Docx2txtLoader

### How does it work?
1. The file uploaded is identified by its type and the contents are extracted.

2. File Loading and Parsing
    - Uses PyMuPDFLoader and Docx2txtLoader to read files.
    - Retrieve the content from uploaded files for further processing.

3. Agents:
   - reader : receives the content and makes small changes or beautifies it
   - extractor : extracts the relevant fields from the content
   - validator : reviews the correctness of the extraction

4. A Graph is created using Langgraph with these agents as the nodes and connecting them using edges with termination conditions

5. A router logic is defined as to when to terminate the graph

6. Each agent's output is printed with the final extraction
   

### Structure
project
- `main.py`
- `loaders.py`
- `workflow.py`
- agents
    - `reader_agent.py`
    - `extractor_agent.py`
    - `validator_agent.py`
- uploaded
- `requirements.txt`
- `.env`

### How to run?
1. create a conda environment - `conda create -n <venv> python=3.11`
2. activate - `conda activate <venv>`
3. `pip install -r requirements.txt`
4. create a `.env` file and set your OPENAI_API_KEY=" "
5. `streamlit run main.py` - initiates the workflow
