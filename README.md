# Enterprise RAG Chatbot for Private Company Data with Role-Based Access Control (RBAC)

An AI-powered question-answering application that retrieves information from sample company policy documents and generates context-aware answers. The project demonstrates Retrieval-Augmented Generation (RAG), role-based document retrieval, query guardrails, and basic monitoring and evaluation.

> **Project status:** This is a learning/demo implementation using sample policy documents. Role selection in the UI is for demonstration and is not production authentication. Cross-role denial must be tested explicitly before claiming that departmental isolation is fully validated.

## Features

- **Retrieval-Augmented Generation:** retrieves relevant document chunks before generating an answer.
- **Role-based document filtering:** applies document-access rules for General, HR, and Finance demo roles.
- **Semantic retrieval:** uses Sentence Transformers embeddings and ChromaDB.
- **LLM responses:** uses a Groq-hosted language model.
- **Query guardrails:** handles selected malicious and out-of-scope prompts.
- **Monitoring and evaluation modules:** includes project components for tracking and evaluating chatbot behavior.
- **Streamlit interface:** provides a simple chat interface for testing.

## Technology Stack

| Area | Technology |
|---|---|
| Language | Python 3.12 |
| UI | Streamlit |
| Embeddings | `all-MiniLM-L6-v2` |
| Vector database | ChromaDB |
| LLM provider | Groq |
| Containerization | Docker |
| Tests | Pytest |

## Architecture

```mermaid
flowchart TD
    A[User] --> B[Streamlit Interface]
    B --> C[Demo Role Selection]
    C --> D[Access Control]
    D --> E[Guardrails]
    E --> F[Retriever]
    F --> G[(ChromaDB)]
    G --> H[Relevant Document Chunks]
    H --> I[RAG Pipeline]
    I --> J[Groq-hosted LLM]
    J --> K[Generated Answer]
    K --> B
```

## Demo document access rules

| Demo role | Documents configured for retrieval |
|---|---|
| General Employee | Company Policy |
| HR Employee | Company Policy and HR Policy |
| Finance Employee | Company Policy and Finance Policy |

The role selector is a demo mechanism. It does not authenticate a real employee or prove production-grade authorization. Cross-role access-denial tests should be run and documented separately.

## Screenshots

The screenshots below show the chatbot's observed responses during manual testing. They are examples from the sample policy dataset, not evidence of production security.

### General Employee

**Policy questions and normal responses**

![General role policy responses](assets/screenshots/general-policy.png)

**Guardrail and unsupported-information responses**

![General role guardrail responses](assets/screenshots/general-guardrails.png)

### HR Employee

**HR policy retrieval**

![HR role policy responses](assets/screenshots/hr-policy.png)

**Guardrail and unsupported-information responses**

![HR role guardrail responses](assets/screenshots/hr-guardrails.png)

### Finance Employee

**Finance policy retrieval**

![Finance role policy responses](assets/screenshots/finance-policy.png)

**Guardrail and unsupported-information responses**

![Finance role guardrail responses](assets/screenshots/finance-guardrails.png)

## Project Structure

```text
Enterprise-RAG-Chatbot/
├── data/
│   └── documents/
│       ├── company_policy.txt
│       ├── finance_policy.txt
│       └── hr_policy.txt
├── src/
│   ├── access_control.py
│   ├── app.py
│   ├── document_loader.py
│   ├── evaluation.py
│   ├── guardrails.py
│   ├── main.py
│   ├── monitoring.py
│   ├── rag_pipeline.py
│   ├── retriever.py
│   ├── text_chunker.py
│   └── vector_store.py
├── tests/
├── .streamlit/
├── .dockerignore
├── .gitignore
├── Dockerfile
├── requirements.txt
└── README.md
```

Generated files and local runtime data such as `.env`, `chroma_db/`, and `logs/` are excluded from version control by the project's ignore rules.

## Setup and Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/KiranKumar674/Enterprise-RAG-Chatbot.git
cd Enterprise-RAG-Chatbot
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Groq API key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

Use your own key locally. **Never commit `.env`, paste API keys into screenshots, or publish secrets.**

### 5. Build the vector database

```bash
python src/vector_store.py
```

### 6. Start the Streamlit application

```bash
streamlit run src/app.py
```

Open the local URL printed by Streamlit (typically `http://localhost:8501`).

## Run with Docker

Build the image:

```bash
docker build -t enterprise-rag-chatbot .
```

Run the container:

```bash
docker run -d \
  --name rag-demo \
  -p 8080:8080 \
  --env-file .env \
  enterprise-rag-chatbot
```

Open `http://localhost:8080`.

Stop and remove the container:

```bash
docker stop rag-demo
docker rm rag-demo
```

## Testing

Run the automated test suite:

```bash
python -m pytest -v
```

The project test run recorded **27 passing tests**. Re-run the command after changes to confirm the current result.

Manual testing shown in the screenshots covered:
- Relevant company-policy questions for General, HR, and Finance demo roles.
- Selected prompt-injection and malicious requests.
- Out-of-scope questions.
- Questions for which the sample documents did not contain sufficient information.

### RBAC validation still required

To verify document isolation, test the following and record the actual results:

| Selected role | Cross-department question |
|---|---|
| General Employee | What is the reimbursement review period? |
| HR Employee | What is the reimbursement review period? |
| Finance Employee | What is the leave policy? |

A secure result should not reveal content from a department's restricted document. Do not describe RBAC as fully validated until these negative tests pass.

## Current Limitations

- Uses sample company policy documents rather than a real enterprise knowledge base.
- Role selection is a demonstration control, not production authentication.
- Guardrails are heuristic and are not a complete security boundary.
- Cross-role denial requires explicit negative testing.
- Production deployment and enterprise-grade security hardening are not yet implemented.

## Future Improvements

- Add secure authentication and server-side authorization.
- Expand document ingestion and support enterprise document sources.
- Improve prompt-injection and sensitive-data defenses.
- Add stronger RBAC isolation tests.
- Deploy to Microsoft Azure.
- Expand evaluation, monitoring, token tracking, and cost alerts.
- Improve scalability, observability, and production reliability.


