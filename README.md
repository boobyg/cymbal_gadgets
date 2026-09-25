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

## 🤖 Task 1: Creating Your Custom Agent via Conversational Analytics API

### The Typical Conversational Analytics Lifecycle Scenario
In enterprise applications, interacting with Looker's Conversational Analytics API follows a consistent, 3-stage lifecycle:
1. **Agent Creation (`create_agent` / `POST /api/4.0/agents`):**  
   You define an AI agent bounded to Looker's semantic layer (specifying the model `cymbal_gadgets_boris` and explore `transactions`), along with persona guardrails and business rules (e.g., "profitability = Gross Margin Percentage").
2. **Conversation Initialization (`POST /api/4.0/conversations`):**  
   The application creates a dedicated, stateful conversation thread bound to the agent ID. Looker handles conversation state, token budgeting, and message history automatically on the server.
3. **Prompt Execution & Tracing (`POST /api/4.0/conversational_analytics/chat`):**  
   The user submits a natural language question (e.g., *"What is total sales amount by store country?"*). The API introspects the Explore, compiles BigQuery SQL, executes it, and returns the verified numbers along with the **full 5-stage reasoning trace** (`THOUGHT`, `SCHEMA`, `QUERY`, `DATA`, `FINAL_RESPONSE`).  
   *Note: This complete tracing will be available directly in the web application's Transparency Hub when the prompt is run!*

### Step-by-Step: Run `create_agent` in Looker API Explorer

1. **Open the `create_agent` Method Directly:**  
   👉 Navigate to: **[CreateAgent in API Explorer](https://ceworkshops.cloud.looker.com/extensions/marketplace_extension_api_explorer::api-explorer/4.0/methods/ConversationalAnalytics/create_agent)**  
   *(Ensure you are logged into Looker with API 4.0 selected).*

2. **Open the "Run It" Tab:**  
   In the API Explorer method view for `create_agent`, click on the **Run It** tab in the right panel.

3. **Where to Paste the JSON Payload:**  
   Locate the **Request Body** editor field (labeled `body`). Clear any placeholder text and paste the following JSON payload:

```json
{
  "name": "Cymbal Retail Analytics Agent - Student <YOUR_NAME_OR_ID>",
  "description": "Conversational BI agent providing governed retail insights for Cymbal Gadgets",
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
*(Make sure to replace `<YOUR_NAME_OR_ID>` with your unique identifier, e.g., `Student 42`, so you can identify your agent on the shared instance).*

4. **Execute the Request:**  
   Click the blue **Run Request** button.

5. **What to Expect as an Output:**  
   In the **Response** section below the button, verify the status code:  
   **`POST /agents (200: OK)`** (or `201: Created`).

6. **Where to Find the Newly Created Agent ID:**  
   In the response JSON output, locate the top-level **`"id"`** field on the very first line:
   ```json
   {
     "id": "a9b6933c74a045de9ed130ad024cca62",
     "name": "Cymbal Retail Analytics Agent - Student 42",
     "sources": [ ... ]
   }
   ```
   **Copy this 32-character Agent ID.** You will paste this ID into Checkpoint 1 and Checkpoint 3 in the web portal to verify your agent and earn points.

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
>    curl -s http://localhost:8080/api/health | jq .
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
