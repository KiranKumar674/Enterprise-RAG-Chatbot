# 🚀 Enterprise RAG Chatbot

### Private Company Knowledge Assistant with Role-Based Access Control

<p align="center">

**An AI-powered chatbot that retrieves answers from private company documents while enforcing role-based document access.**

</p>

<p align="center">

`Python` · `Streamlit` · `ChromaDB` · `Groq` · `Docker` · `Microsoft Azure`

</p>

---

## 📌 Table of Contents

1. [Project Overview](#-project-overview)
2. [Technology Stack](#-technology-stack)
3. [Prerequisites](#-prerequisites)
4. [Local Installation](#-1-local-installation)
5. [Docker Setup](#-2-docker-setup)
6. [Azure Deployment](#-3-azure-deployment)
7. [Role-Based Access Control](#-role-based-access-control-rbac)
8. [Troubleshooting](#-troubleshooting)
9. [Security Considerations](#-security-considerations)
10. [Project Links](#-project-links)

---

## 📖 Project Overview

The **Enterprise RAG Chatbot** is an AI-powered question-answering system designed to retrieve relevant information from private company documents.

It uses Retrieval-Augmented Generation (RAG) to provide context-aware answers while implementing Role-Based Access Control (RBAC) to restrict document retrieval according to user roles.

### ✨ Key Features

- **Retrieval-Augmented Generation:** Retrieves relevant document chunks before generating answers.
- **Role-Based Access Control:** Separates document access for General, HR and Finance users.
- **Vector Database:** Uses ChromaDB to store and retrieve document embeddings.
- **Semantic Search:** Uses Sentence Transformers for document embeddings.
- **AI-Powered Responses:** Uses Groq-hosted language models.
- **Guardrails:** Includes heuristic checks for handling restricted or inappropriate queries.
- **Cloud Deployment:** Deployed using Microsoft Azure Container Apps.
- **Containerization:** Uses Docker for consistent application deployment.

---

## 🛠️ Technology Stack

| Category | Technology |
|---|---|
| Programming Language | Python 3.12 |
| Frontend | Streamlit |
| Vector Database | ChromaDB |
| Embedding Model | all-MiniLM-L6-v2 |
| LLM Provider | Groq |
| Containerization | Docker |
| Cloud Platform | Microsoft Azure |
| Container Registry | Azure Container Registry |
| Deployment | Azure Container Apps |

---

## 📋 Prerequisites

Before starting, make sure you have installed:

- Python 3.12 or later
- Git
- Docker
- Azure CLI (only for Azure deployment)
- Groq API key

---

# 💻 1. Local Installation

Follow these steps to run the chatbot on your local machine.

### Step 1: Clone the Repository

```bash
git clone https://github.com/KiranKumar674/Enterprise-RAG-Chatbot.git

cd Enterprise-RAG-Chatbot
```

### Step 2: Create a Virtual Environment

```bash
python3 -m venv venv
```

**Activate the environment**

Linux / macOS:

```bash
source venv/bin/activate
```

Windows:

```powershell
venv\Scripts\activate
```

### Step 3: Install Dependencies

Upgrade pip and install the required packages.

```bash
pip install --upgrade pip

pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project root.

```bash
touch .env
```

Add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key
```

Replace the placeholder with your actual API key.

> ⚠️ **Important:** Never upload your `.env` file or API keys to GitHub. Make sure `.env` is included in `.gitignore`.

### Step 5: Run the Application

```bash
streamlit run app.py
```

Open the local application in your browser:

```text
http://localhost:8501
```

<details>
<summary><b>Local Setup Checklist</b></summary>

- [ ] Repository cloned successfully.
- [ ] Virtual environment activated.
- [ ] Dependencies installed.
- [ ] Groq API key configured.
- [ ] Streamlit application running.

</details>

---

# 🐳 2. Docker Setup

Docker packages the application and its dependencies into a container, making deployment more consistent across environments.

### Step 1: Build the Docker Image

```bash
docker build -t enterprise-rag-chatbot .
```

### Step 2: Run the Docker Container

```bash
docker run -d \
  --name enterprise-rag \
  -p 8080:8080 \
  --env-file .env \
  enterprise-rag-chatbot
```

### Step 3: Access the Application

Open:

```text
http://localhost:8080
```

> **Note:** This command assumes the Dockerfile configures Streamlit to listen on port `8080`. Check your actual Dockerfile before running it.

### Useful Docker Commands

| Operation | Command |
|---|---|
| List running containers | `docker ps` |
| View container logs | `docker logs enterprise-rag` |
| Stop container | `docker stop enterprise-rag` |
| Remove container | `docker rm enterprise-rag` |
| List images | `docker images` |

---

# ☁️ 3. Azure Deployment

The application is deployed on **Microsoft Azure Container Apps**, with Azure Container Registry used to store the Docker image.

### 🏗️ Azure Architecture

```text
             User
               |
               v
       Azure Container Apps
               |
               v
      Enterprise RAG Chatbot
               |
       +-------+--------+
       |                |
       v                v
    ChromaDB         Groq API
       |
       v
  Company Documents


   Azure Container Registry
               |
               v
       Docker Image
               |
               v
      Azure Container Apps

```

### Azure Resources

| Resource | Configuration |
|---|---|
| Resource Group | `rg-enterprise-rag` |
| Container Registry | `kiranenterpriserag` |
| Container Apps Environment | `env-enterprise-rag` |
| Container App | `app-enterprise-rag` |
| Managed Identity | `id-enterprise-rag-pull` |
| Region | Central India |

### Step 1: Install Azure CLI

Install Azure CLI using the official documentation:

https://learn.microsoft.com/cli/azure/install-azure-cli

Sign in:

```bash
az login
```

View your available subscriptions:

```bash
az account list --output table
```

Select your Azure for Students subscription:

```bash
az account set --subscription "YOUR_SUBSCRIPTION_ID"
```

### Step 2: Build and Push the Docker Image

The Azure deployment uses a Linux AMD64 image with OCI-compatible image layers.

The following Docker Buildx command was used:

```bash
sudo docker buildx build \
  --platform linux/amd64 \
  --tag kiranenterpriserag.azurecr.io/enterprise-rag-chatbot:buildx-oci \
  --output type=image,name=kiranenterpriserag.azurecr.io/enterprise-rag-chatbot:buildx-oci,push=true,oci-mediatypes=true,compression=gzip,force-compression=true \
  --provenance=false \
  .
```

The image is pushed to:

```text
kiranenterpriserag.azurecr.io
```

For subsequent registry operations, authenticate using:

```bash
az acr login --name kiranenterpriserag
```

### Step 3: Configure Container Apps

The deployed application uses the following configuration:

| Configuration | Value |
|---|---|
| Ingress | External |
| Transport | HTTPS |
| Target Port | 8080 |
| CPU | 1 vCPU |
| Memory | 2 GiB |
| Minimum Replicas | 0 |
| Maximum Replicas | 1 |

### Step 4: Configure Application Secrets

The Groq API key is stored securely as an Azure Container Apps secret.

| Setting | Value |
|---|---|
| Secret Name | `groq-api-key` |
| Environment Variable | `GROQ_API_KEY` |

The application references the secret through its environment variable.

**Never hardcode API keys in the source code or commit them to GitHub.**

### Step 5: Configure Managed Identity

A user-assigned managed identity is configured:

```text
id-enterprise-rag-pull
```

The identity has the `AcrPull` role on Azure Container Registry.

This allows the Container App to pull the private Docker image without enabling registry administrator credentials.

### Step 6: Verify the Deployment

Check the Container App:

```bash
az containerapp show \
  --name app-enterprise-rag \
  --resource-group rg-enterprise-rag \
  --output table
```

Check deployment revisions:

```bash
az containerapp revision list \
  --name app-enterprise-rag \
  --resource-group rg-enterprise-rag \
  --output table
```

### Step 7: Access the Live Application

<details>
<summary><b>View Azure deployment details</b></summary>

**Cloud Provider:** Microsoft Azure

**Service:** Azure Container Apps

**Resource Group:** `rg-enterprise-rag`

**Region:** Central India

**Application Name:** `app-enterprise-rag`

</details>

### 🌐 Live Application

**[Open Enterprise RAG Chatbot](https://app-enterprise-rag.victoriousocean-15461cb1.centralindia.azurecontainerapps.io/)**

You can also manage the deployed application through the [Azure Portal](https://portal.azure.com/).

Navigate to:

`Container Apps → app-enterprise-rag → Overview`

---

# 🔐 Role-Based Access Control (RBAC)

The chatbot implements document-level access restrictions using three demonstration roles.

### User Roles and Permissions

| User Role | Accessible Documents |
|---|---|
| General | Company Policy |
| HR | Company Policy + HR Policy |
| Finance | Company Policy + Finance Policy |

### RBAC Testing

The following test cases were used to validate access restrictions.

| Role | Test Question | Expected Result |
|---|---|---|
| General | What is the HR leave policy? | Allowed – available in Company Policy |
| Finance | Explain the HR leave policy. | Allowed – available in Company Policy |
| General | How often are employee performance reviews conducted? | Restricted |
| Finance | Who must approve recruitment requests before a job is published? | Restricted |

### Test Results

<details>
<summary><b>View negative RBAC test responses</b></summary>

**Test 1 – General Role**

Question:

```text
How often are employee performance reviews conducted?
```

Response:

```text
The available company documents do not provide enough information.
```

**Result:** Passed.

**Test 2 – Finance Role**

Question:

```text
Who must approve recruitment requests before a job is published?
```

Response:

```text
The available company documents do not provide enough information.
```

**Result:** Passed.

</details>

> **Security Note:** The role selector is intended for demonstration purposes and is not production-grade authentication. The guardrails are heuristic. Production deployment requires proper identity verification, authorization enforcement and additional security testing.

---

# 🧰 Troubleshooting

### 1. Missing Groq API Key

Verify that:
- `.env` exists in the project root.
- The environment variable is named `GROQ_API_KEY`.
- The Azure secret and environment variable reference are configured correctly.

### 2. Docker Container Not Starting

View container logs:

```bash
docker logs enterprise-rag
```

### 3. Azure Deployment Errors

Check:
- Container App revision health.
- Container logs.
- Registry image availability.
- Managed identity permissions.
- Application secrets and environment variables.

Use:

**Azure Portal → Container Apps → app-enterprise-rag**

### 4. ChromaDB or Embedding Model Issues

Ensure the required dependencies are installed and the environment has access to download the embedding model when needed.

---

# 🛡️ Security Considerations

- Never expose API keys or credentials.
- Keep `.env` out of version control.
- Use Azure secrets for sensitive configuration.
- Use managed identity for private registry access.
- Avoid using real confidential company documents in the demonstration.
- Implement proper authentication before production use.
- Test unauthorized document access and retrieval-source isolation.

---

# 🔗 Project Links

| Resource | Link |
|---|---|
| GitHub Repository | [Enterprise-RAG-Chatbot](https://github.com/KiranKumar674/Enterprise-RAG-Chatbot) |
| Live Application | [Azure Chatbot](https://app-enterprise-rag.victoriousocean-15461cb1.centralindia.azurecontainerapps.io/) |
| Azure Portal | [Microsoft Azure](https://portal.azure.com/) |
| Groq Platform | [Groq Console](https://console.groq.com/) |

---

<p align="center">

### Built with ❤️ using RAG, ChromaDB and Azure

**Enterprise RAG Chatbot – Secure, Context-Aware Document Question Answering**

</p>
