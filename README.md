# 🎓 SME Academy: Looker Conversational Analytics & Agentic Web App

[![Google Cloud](https://img.shields.io/badge/Google%20Cloud-Argolis%20Environment-4285F4?logo=google-cloud&logoColor=white)](https://cloud.google.com)
[![Looker API](https://img.shields.io/badge/Looker%20API-4.0%20Conversational%20Analytics-0052CC?logo=looker&logoColor=white)](https://cloud.looker.com)
[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12-3776AB?logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](LICENSE)

An end-to-end, hands-on lab and reference implementation for **Google Cloud SME Academy (Data Analytics & Agentic AI Track)**. 

> [!NOTE]
> The lab is available in this GitHub repository (`https://github.com/boobyg/cymbal_gadgets.git`) for students to clone and run in their own dedicated **Argolis environment** (using **Google Cloud Shell** in their assigned Argolis GCP project).
> * Running in your own Argolis Cloud Shell guarantees complete isolation, avoids port collisions on port `8080`, keeps your student API credentials private, and gives you instant browser access via Cloud Shell Web Preview.

Students build, test, and deploy a custom **Conversational Analytics Agent** connected to Looker's governed semantic layer (`cymbal_gadgets_boris` model & `transactions` explore) and consume it through a full-stack web application featuring real-time reasoning tracing, governed LookML SQL generation, and interactive assessment checkpoints.

---

## 🎯 Lab Objectives & Path for Data Engineers

### Why Data Engineers Need Looker Conversational Analytics
Generative AI applications that attempt direct **"Text-to-SQL"** on raw database tables (e.g. BigQuery) fail in production because LLMs lack business context:
* They hallucinate column names or query outdated staging tables.
* They misinterpret business definitions (e.g., confusing gross revenue with net sales).
* They create join fanouts on multi-table relationships.

**Looker Conversational Analytics (CA) API** bridges Large Language Models with Looker's **Governed Semantic Layer**:
* **LookML as Single Source of Truth:** Dimensions, measures, and joins are defined once in LookML code with built-in fanout protection.
* **Deterministic SQL Compilation:** Instead of generating risky SQL, the agent produces a governed LookML query specification, which Looker compiles into dialect-optimized BigQuery SQL.
* **Full Auditability & Tracing:** The API returns the complete reasoning trace, explored schema, generated query parameters, and verified tabular results directly inside the application.

### The 5-Phase Learning Roadmap

| Phase | Title | Focus for Data Engineers | Deliverable |
| :---: | :--- | :--- | :--- |
| **Phase 0** | **Credentials Setup** | Configure assigned Looker API credentials and verify fresh session. | Fresh credentials verified |
| **Phase 1** | **API Explorer & Custom Agent** | Use Looker's interactive API Explorer workbench to create an agent (`POST /agents`). | Unique custom agent created (25 pts) |
| **Phase 2** | **Web Client Deployment** | Run the Python web client in Argolis Cloud Shell and test health (`/api/health`). | Server running & healthy (25 pts) |
| **Phase 3** | **Interactive Queries & Tracing** | Submit multi-turn queries; audit Thought, Schema, Query, and BigQuery Data payloads. | Multi-turn queries audited (25 pts) |
| **Phase 4** | **Prompt Tuning & Production** | Dynamically update agent instructions (`PATCH /agents/{id}`) and review Cloud Run architecture. | Instruction tuning applied (25 pts) |

---

## 🖥️ Presentation Slides & Lab Materials

This lab includes a complete slide deck and presentation for instructors and self-paced students:

* 📊 **[Google Slides Presentation (Standard Google Cloud Style)](https://docs.google.com/presentation/d/1looker-conversational-analytics-standard-gcp-deck/edit?usp=sharing)**: Official presentation deck in **Standard Google Cloud style** for the instructor to present and guide the session.
* 🌐 **[Interactive Web Presentation](http://localhost:8080/presentation.html)**: Standalone, browser-based slide deck with arrow navigation, table of contents, and speaker notes. Accessible directly through the web application.
* 📄 **[Markdown Presentation Deck (PRESENTATION_LOOKER_CONVERSATIONAL_ANALYTICS.md)](PRESENTATION_LOOKER_CONVERSATIONAL_ANALYTICS.md)**: Standard markdown format compatible with GitHub, Marp, and presentation generators.
* 📖 **[Detailed Student Lab Guide (LAB_GUIDE_CONVERSATIONAL_ANALYTICS.md)](LAB_GUIDE_CONVERSATIONAL_ANALYTICS.md)**: Full 30-minute step-by-step curriculum with deep dives and troubleshooting.

---

## 🔄 End-to-End Operational Architecture & Data Flow

When a user submits a natural language question, the system executes through the following sequence:

1. **User Request:** The user or frontend application sends a question (e.g. *"What is the total sales amount by store country?"*) to the web client.
2. **Session Context:** The client initializes or references a stateful conversation thread via `POST /api/4.0/conversations`, receiving a `conversation_id`.
3. **Conversational Analytics Execution:** The client calls `POST /api/4.0/conversational_analytics/chat`.
4. **Schema Introspection & Resolution:** Looker's agent inspects the assigned LookML explore (`transactions` within model `cymbal_gadgets_boris`), identifying appropriate dimensions (`store_country`) and measures (`total_sales_amount`).
5. **Deterministic SQL Compilation:** Looker compiles the formal LookML query specification into optimized, dialect-specific Google Cloud BigQuery SQL.
6. **BigQuery Query Execution:** BigQuery runs the query and returns verified tabular records.
7. **Multi-Part Response Stream:** Looker synthesizes an executive summary while returning the full 5-stage audit payload (`THOUGHT`, `SCHEMA`, `QUERY`, `DATA`, `FINAL_RESPONSE`).

---

## 🛠️ Major Looker CA API Functions & Endpoints

| Endpoint | Method | Purpose in Architecture |
| :--- | :---: | :--- |
| `/api/4.0/login` | `POST` | Authenticates using API3 credentials (`client_id` + `client_secret`) and generates an ephemeral session token. |
| `/api/4.0/agents` | `POST` | Defines an AI agent, its bound LookML model/explore, and business instructions/guardrails. |
| `/api/4.0/agents/search` | `GET` | Discovers active agents on the Looker instance. |
| `/api/4.0/agents/{agent_id}` | `GET` | Retrieves full configuration, explore bindings, and instructions for an agent. |
| `/api/4.0/agents/{agent_id}` | `PATCH` | Updates agent persona, instructions, or formatting guardrails dynamically at runtime. |
| `/api/4.0/conversations` | `POST` | Creates a stateful conversation thread bound to an agent ID. |
| `/api/4.0/conversational_analytics/chat` | `POST` | Submits natural language queries and streams back reasoning, schema, query, and data payloads. |

---

## ⚠️ MANDATORY REQUIREMENT: Deploy in Your Own Argolis Environment

> [!IMPORTANT]
> **STUDENT REQUIREMENT:**  
> Every student **MUST deploy and run this lab inside their own dedicated Google Cloud Argolis environment** (e.g., using **Google Cloud Shell** in their assigned Argolis GCP project).
>
> **Why is your own Argolis environment required?**
> 1. **Complete Isolation (No Port Collisions):** The web server runs on port `8080`. In shared environments or shared VMs, multiple students will experience port collisions (`Address already in use`) and conflicting session state.
> 2. **Credential Privacy & Security:** Your assigned Looker API credentials (`client_id` and `client_secret`) must remain confidential inside your personal GCP project sandbox.
> 3. **Built-in Cloud Shell Web Preview:** Google Cloud Shell automatically provides a secure HTTPS proxy to preview port `8080` in your web browser with zero firewall configuration or local SSH port forwarding.
> 4. **Zero Local Installation:** Running in Argolis Cloud Shell guarantees that Python 3, Git, curl, and network connectivity to the Looker instance are pre-installed and functional—no local machine setup needed.

---

## 🚀 How to Deploy the Lab from Git in Your Argolis Environment

Follow these steps to deploy and run the lab in your Argolis project:

### Step 1: Open Google Cloud Shell in Argolis
1. Open the [Google Cloud Console](https://console.cloud.google.com).
2. Ensure your active project is your assigned **Argolis project** (e.g. `prj-<user>-argolis`).
3. Click the **Activate Cloud Shell** button (`>_`) in the top-right toolbar.

### Step 2: Clone the Git Repository
In your Cloud Shell terminal, run:

```bash
# Clone the public repository (no password or token required)
git clone https://github.com/boobyg/cymbal_gadgets.git

# Navigate to the web application directory
cd cymbal_gadgets/agentic_web_app
```

> [!TIP]
> **Did Git ask for a Username or Password?**
> * The public repository `https://github.com/boobyg/cymbal_gadgets.git` **does NOT require any username or password to clone**.
> * If Git prompts `Username for 'https://github.com':`, you likely mistyped the URL. Double-check that you typed `https://github.com/boobyg/cymbal_gadgets.git`.

### Step 3: Start the Web Server
Launch the application using the startup script:

```bash
./run.sh
```

*(The script automatically initializes `.env` from `.env.example` and launches the Python HTTP server on port 8080).*

### Step 4: Open the Web Application via Cloud Shell Web Preview
1. At the top-right of the **Google Cloud Shell** window, click the **Web Preview** icon.
2. Select **Preview on port 8080**.
3. A new browser tab opens loading the **Interactive SkillLabs Training Portal**!

### Step 5: Configure Your Student Credentials
In the opened web portal:
1. Click the yellow **Student Credentials** button in the top navigation bar.
2. Enter your assigned:
   * **Looker Client ID:** *(provided by instructor)*
   * **Looker Client Secret:** *(provided by instructor)*
3. Click **Save & Test Connection**. When verified, the status indicator turns green (`Looker Connected`).

---

## 🤖 Task 1: Conversational Analytics API & Core Lifecycle (Video Walkthrough)

> [!NOTE]
> **Companion Video Walkthrough:**  
> This task follows the official Looker EMEA CE team enablement video: **[Looker Conversational Analytics API Walkthrough](https://www.youtube.com/watch?v=XyU90O49p8o)**.  
> It guides you through the end-to-end lifecycle: Grounded Semantic Model &rarr; API Explorer &rarr; `create_agent` &rarr; `create_golden_query` &rarr; `create_conversation` &rarr; `conversational_analytics_chat` &rarr; Python client integration.

### The Complete Conversational Analytics Lifecycle
In enterprise applications, interacting with Looker's Conversational Analytics API follows an auditable 6-stage lifecycle:
1. **Agent Creation (`POST /api/4.0/agents` / `create_agent`):**  
   Define an AI agent bounded to Looker's semantic layer (model `cymbal_gadgets_boris`, explore `transactions`), persona guardrails, and analytical tracing enabled (`show_analytical_details: true`).
2. **Ground with Golden Queries (`POST /api/4.0/golden_queries` / `create_golden_query`):**  
   Anchor user question variations with verified Looker Explore answer URLs. This eliminates metric hallucinations and join ambiguity.
3. **Conversation Initialization (`POST /api/4.0/conversations` / `create_conversation`):**  
   Using the `agent_id` created in Step 1, allocate a stateful conversation thread. Looker manages multi-turn history and token budgeting on the server.
4. **Chat API Verification (`POST /api/4.0/conversational_analytics/chat` / `conversational_analytics_chat`):**  
   Test the raw Chat API method in API Explorer *before* launching the web UI. Inspect the 5-stage stream (`THOUGHT`, `SCHEMA`, `QUERY`, `DATA`, `FINAL_RESPONSE`).
5. **Interactive UI Chat & Tracing:**  
   Launch the web app, select your agent, run natural language questions, and audit the 3 execution accordions in real time.
6. **Dynamic Instruction Tuning (`PATCH /api/4.0/agents/{id}` / `update_agent`):**  
   Update persona rules and formatting without redeploying code.

---

### Step 1.1: Run `create_agent` in API Explorer
1. **Open Method:** 👉 **[CreateAgent in API Explorer](https://ceworkshops.cloud.looker.com/extensions/marketplace_extension_api_explorer::api-explorer/4.0/methods/ConversationalAnalytics/create_agent)**
2. Click **Run It** tab &rarr; scroll to **Request Body (`body`)**.
3. Paste JSON Payload:
```json
{
  "name": "Cymbal Retail Analytics Agent - Student <YOUR_NAME_OR_ID>",
  "description": "Conversational agent for Cymbal Gadgets retail sales & transactions",
  "sources": [
    {
      "model": "cymbal_gadgets_boris",
      "explore": "transactions"
    }
  ],
  "context": {
    "instructions": "- Always use Gross Margin Percentage when asked about profitability, margin, or sales performance.\n- When asked for trends over time, group by transaction date or transaction month.\n- If the user asks for store performance, breakdown by store country.\n- Keep executive summaries concise with key metrics highlighted in bold.",
    "show_analytical_details": true,
    "show_debug": false
  }
}
```
4. Click blue **Run Request** button. Look for status `POST /agents (200: OK)`.
5. Copy the 32-character `"id"` from the top of the JSON response.

**🐍 Python Snippets for Create Agent:**
```python
# Option A: Looker Python SDK (looker_sdk)
import looker_sdk
from looker_sdk import models40
sdk = looker_sdk.init40()
new_agent = sdk.create_agent(
    body=models40.WriteAgent(
        name="Cymbal Retail Analytics Agent - Student 42",
        sources=[models40.AgentSource(model="cymbal_gadgets_boris", explore="transactions")],
        context=models40.AgentContext(instructions="...", show_analytical_details=True)
    )
)
print("Agent ID:", new_agent.id)

# Option B: Zero-Dependency LookerClient
from looker_client import LookerClient
client = LookerClient(config.LOOKER_BASE_URL, config.LOOKER_CLIENT_ID, config.LOOKER_CLIENT_SECRET)
agent = client.create_agent(name="Cymbal Agent", model="cymbal_gadgets_boris", explore="transactions")
print("Agent ID:", agent["id"])
```

---

### Step 1.2: Supplying a Golden Query Example (`POST /golden_queries`)
1. **Open Method:** 👉 **[CreateGoldenQuery in API Explorer](https://ceworkshops.cloud.looker.com/extensions/marketplace_extension_api_explorer::api-explorer/4.0/methods/ConversationalAnalytics/create_golden_query)**
2. Click **Run It** &rarr; paste into **Request Body (`body`)**:
```json
{
  "questions": [
    "What is our total sales amount across all transactions?",
    "Total sales across all stores",
    "What is our overall sales revenue?"
  ],
  "answer": "https://ceworkshops.cloud.looker.com/explore/cymbal_gadgets_boris/transactions?fields=transactions.total_sale_price"
}
```
3. Click **Run Request** and copy the returned `"id"`.

**🐍 Python Snippets for Golden Query:**
```python
# Create and link golden query to your agent
gq = client.create_golden_query(
    questions=["What is our total sales amount across all transactions?"],
    answer="https://ceworkshops.cloud.looker.com/explore/cymbal_gadgets_boris/transactions?fields=transactions.total_sale_price"
)
client.update_agent(agent_id, {"golden_query_ids": [gq["id"]]})
```

---

### Step 1.3: Create Conversation Using Your Agent ID (`POST /conversations`)
1. **Open Method:** 👉 **[CreateConversation in API Explorer](https://ceworkshops.cloud.looker.com/extensions/marketplace_extension_api_explorer::api-explorer/4.0/methods/ConversationalAnalytics/create_conversation)**
2. Click **Run It** &rarr; paste into **Request Body (`body`)**:
```json
{
  "agent_id": "<YOUR_AGENT_ID_FROM_STEP_1.1>",
  "name": "Cymbal Retail Session - Student <YOUR_NAME_OR_ID>"
}
```
3. Click **Run Request** and copy the returned `"id"` (`conversation_id`).

**🐍 Python Snippets for Create Conversation:**
```python
conv = client.create_conversation(agent_id=agent_id, name="Cymbal Analysis Session")
print("Conversation ID:", conv["id"])
```

---

### Step 1.4: Test Chat API Method Before Showing Chat UI (`POST /conversational_analytics/chat`)
1. **Open Method:** 👉 **[ConversationalAnalyticsChat in API Explorer](https://ceworkshops.cloud.looker.com/extensions/marketplace_extension_api_explorer::api-explorer/4.0/methods/ConversationalAnalytics/conversational_analytics_chat)**
2. Click **Run It** &rarr; paste into **Request Body (`body`)**:
```json
{
  "conversation_id": "<YOUR_CONVERSATION_ID_FROM_STEP_1.3>",
  "user_message": "What is our total sales amount across all transactions?"
}
```
3. Click **Run Request** and observe the 5-stage stream (`THOUGHT`, `SCHEMA`, `QUERY`, `DATA`, `FINAL_RESPONSE`).

**🐍 Python Snippets for Chat API:**
```python
# Execute query and parse 5-stage stream
result = client.chat(conversation_id=conv["id"], user_message="What is our total sales amount?")
print("🧠 Thoughts:", result["thoughts"])
print("💻 Query Spec:", result["query"])
print("📊 Data:", result["data"])
print("📝 Summary:", result["final_response"])
```

**🚩 Checkpoint 1:** Paste your Agent ID into the **Assessment Checkpoint 1** field on the portal (`http://localhost:8080`) and click **Check my progress** (+25 Points).

---

## 🔍 Task 2: Where to Run the Health Check curl Command

> [!CAUTION]
> ### ❓ Crucial Instruction: Where and How to Run the Task 2 curl Command
>
> In **Task 2 / Checkpoint 2**, students verify server health. Many students get stuck here. Here is exactly what you need to know:
>
> #### 1. DO NOT Run curl in the First Terminal Window
> In Step 3, you ran `./run.sh`. That terminal is **currently busy** running the Python web server in the foreground.
> * If you try to type commands into that window, they will not run.
> * If you press `Ctrl + C`, **you will kill the web server**!
>
> #### 2. DO NOT Run curl on Your Local Laptop Terminal
> If you open Terminal / PowerShell on your personal laptop and run `curl http://localhost:8080/api/health`, it will fail with `Connection refused` because `localhost:8080` is running in your **remote Argolis Cloud Shell container**.
>
> #### 3. DO NOT curl Your External Cloud Shell Preview URL (`https://*.cloudshell.dev`)
> The external Cloud Shell preview URL requires Google SSO browser cookies. Terminal `curl` receives an HTML login redirect, which `jq` cannot parse as JSON.
>
> #### 4. The Correct Way: Open a SECOND Terminal Tab in Cloud Shell
> 1. In Google Cloud Shell, click the **`+` (Open new tab)** button in the terminal tab bar.
> 2. In this fresh second tab, run:
>    ```bash
>    curl http://localhost:8080/api/health | jq .
>    ```
> 3. Expected response:
>    ```json
>    {
>      "status": "healthy",
>      "looker_connected": true,
>      "looker_url": "https://ceworkshops.cloud.looker.com",
>      "user_email": "api_user@example.com"
>    }
>    ```
>
> #### 5. Alternative (Fastest - Recommended): Use the Web UI Button
> In the interactive web portal (`http://localhost:8080` via Web Preview):
> 1. Scroll to **Task 2: Assessment Checkpoint 2** in the left lab guide panel.
> 2. Click the green **Check my progress** button.
> 3. The portal directly queries `/api/health` and automatically awards **+25 points**!

---

## ☁️ Optional: Deploying as a Serverless Container on Google Cloud Run

To deploy the application as an always-on, serverless Cloud Run service in your Argolis project:

```bash
cd cymbal_gadgets/agentic_web_app

# Deploy using the automated script
./deploy_cloud_run.sh
```

Or deploy directly via `gcloud`:

```bash
gcloud run deploy looker-agentic-web-app \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars LOOKER_BASE_URL="https://ceworkshops.cloud.looker.com",LOOKER_CLIENT_ID="YOUR_CLIENT_ID",LOOKER_CLIENT_SECRET="YOUR_CLIENT_SECRET"
```

---

## 📂 Repository Contents

```
cymbal_gadgets/
├── README.md                                   # Master deployment & lab guide
├── LAB_GUIDE_CONVERSATIONAL_ANALYTICS.md       # Comprehensive 30-minute student lab curriculum
├── PRESENTATION_LOOKER_CONVERSATIONAL_ANALYTICS.md # Complete presentation slide deck (Markdown)
├── manifest.lkml                               # LookML project manifest
├── agentic_web_app/                            # Student web application
│   ├── Dockerfile                              # Minimal, secure container definition (Python 3.12-slim)
│   ├── deploy_cloud_run.sh                     # Automated Google Cloud Run deployment script
│   ├── run.sh                                  # Local / Cloud Shell one-click startup script
│   ├── server.py                               # Zero-dependency Python HTTP server & REST API
│   ├── looker_client.py                        # Python SDK client for Looker 4.0 Conversational APIs
│   ├── config.py                               # Environment loader & configuration defaults
│   ├── test_pipeline.py                        # Automated CLI validation & query runner
│   ├── .env.example                            # Template configuration for API credentials
│   └── static/
│       ├── index.html                          # Single-Page App with dual-pane layout & Transparency Hub
│       └── presentation.html                   # Interactive browser-based presentation viewer
├── models/
│   └── cymbal_gadgets_boris.model.lkml         # LookML Model definition with transactions explore
├── views/
│   ├── transactions.view.lkml                  # Core retail sales view with dimensions & measures
│   ├── product_reviews.view.lkml               # Product review facts
│   └── marketing_campaign_impact.view.lkml     # Marketing attribution data
└── dashboards/
    ├── cymbal_gadgets_2025_kpis.dashboard.lookml
    └── powerbi_replication.dashboard.lookml
```

---

## 🎯 Lab Tasks & Scoring (100 Points Total)

| Task | Title | Time | Description | Points |
| :---: | :--- | :---: | :--- | :---: |
| **Task 1** | **Create Custom Agent** | 10 mins | Use Looker API Explorer to create your uniquely-named agent against `cymbal_gadgets_boris` | 25 pts |
| **Task 2** | **Deploy App & Health Check** | 5 mins | Launch app in Argolis Cloud Shell, verify health via curl or UI | 25 pts |
| **Task 3** | **Interactive Queries & Tracing** | 10 mins | Test multi-turn queries with Step 1 agent and inspect transparency traces | 25 pts |
| **Task 4** | **Prompt Tuning & Guardrails** | 5 mins | Update system instructions via `PATCH /agents/{agent_id}` to enforce executive formatting | 25 pts |

---

## 🆘 Troubleshooting FAQ

| Problem | Root Cause | Solution |
| :--- | :--- | :--- |
| `Address already in use (port 8080)` | Another process is using port 8080 | Edit `.env` and set `PORT=8085`, then restart `./run.sh` |
| `jq: parse error: Invalid numeric literal` | Curled external `https://*.cloudshell.dev` URL which requires Google cookies | Curl `http://localhost:8080/api/health` in Cloud Shell terminal tab, or click **Check my progress** in the Web UI |
| Credentials window shows previous credentials | Browser or server cached previous credentials | Credentials are now cleared by default. You can also click **Clear Saved Credentials** in the dialog |
| First terminal unresponsive to commands | Terminal is busy running `./run.sh` | Open a **second terminal tab** (`+`) in Cloud Shell rather than interrupting the server |
| `401 Unauthorized` on Looker API calls | Invalid or missing API3 credentials | Click **Student Credentials** in the UI and verify your Client ID & Secret |
| `422 Unprocessable Entity` when creating agent | Included obsolete `"category"` field in payload | Omit `"category"` attribute; the API categorizes agents automatically |
| Checkpoint 1 or 3 assessment fails | Did not specify unique Step 1 Agent ID | Paste your exact `agent_id` from Step 1 into the Checkpoint input box |

---

## 📄 License
This repository is licensed under the Apache License 2.0. See [LICENSE](LICENSE) for details.
