# 🎓 SME Academy Lab: Building, Testing & Deploying Custom Conversational Analytics Agents with Looker APIs

**Audience:** Data Engineers, Analytics Engineers, Cloud Architects, and BigQuery Developers  
**Prerequisites:** Familiarity with SQL, REST APIs, and basic JSON. **Zero prior Looker or LookML experience required!**  
**Duration:** ~30 Minutes  
**Track:** Google Cloud SME Academy &bull; Agentic & Data Analytics Track  
**Companion Presentations:** [Google Slides (Standard Google Cloud Style)](https://docs.google.com/presentation/d/1Bl7_ApzMmlsCay9NbthnulxUMKXBpLlbUplNXAdqvsk/edit?slide=id.h1097fa95fc4670d5_0_647&resourcekey=0-G10zZ62rbmyYF_-4_1K6JA#slide=id.h1097fa95fc4670d5_0_647) | [Interactive Presentation Slides](http://localhost:8080/presentation.html) | [Markdown Presentation Deck](PRESENTATION_LOOKER_CONVERSATIONAL_ANALYTICS.md)  
**Walkthrough Video:** [Looker Conversational Analytics API (YouTube)](https://www.youtube.com/watch?v=XyU90O49p8o) by Looker EMEA Customer Engineering  

## 🧭 Introduction for Data Engineers: Why Looker Conversational Analytics?

### The Problem Data Engineers Face with Generative AI
Every data engineering team is asked to build generative AI capabilities: *"Let business users chat with our data warehouse."*

However, traditional **"Text-to-SQL"** approaches that connect Large Language Models directly to raw database tables (e.g. BigQuery, Snowflake) consistently fail in enterprise production:
1. **Schema Confusion & Hallucination:** LLMs guess table joins, mistakenly query stale staging tables, or invent columns that do not exist.
2. **Missing Business Logic:** Raw SQL cannot know corporate definitions: *What is "Net Revenue"? Does it exclude refunds? Which order status counts as completed? How are multi-currency conversions handled?*
3. **Fanout & Deduplication Errors:** LLMs struggle with complex many-to-many joins and fanout traps, leading to inflated sums and inaccurate reporting.
4. **No Auditability:** When an LLM outputs a single number, engineers have no auditable trail to verify how the calculation was derived.

### The Solution: Looker as the Governed Semantic Layer
Looker provides an enterprise **Governed Semantic Layer** (defined in LookML). Instead of querying raw database tables directly:
* **Metrics (Measures) are Centrally Defined:** Definitions like `total_revenue`, `gross_margin_pct`, and `active_customers` are defined once in LookML code.
* **Joins are Governed:** Relationships between fact and dimension tables are pre-modeled with automated fanout protection.
* **Deterministic SQL Compilation:** Looker's modeling engine converts high-level dimensional requests into dialect-optimized, performant BigQuery SQL.

### What is the Looker Conversational Analytics (CA) API?
The **Looker Conversational Analytics (CA) API** is an AI-native REST API family in Looker 4.0. It bridges Large Language Models with Looker's Governed Semantic Layer.

When an end user asks a natural language question:
1. The user's question goes to the **Looker CA API**.
2. The agent inspects the **governed LookML Explore**, identifying the formal dimensions, measures, and filters required.
3. The Looker engine compiles and executes **deterministic BigQuery SQL**.
4. The database returns verified tabular numbers.
5. The agent synthesizes an executive summary while returning **full audit transparency** (Thought traces, LookML schema selection, generated Looker query specification, and raw data rows).

---

## 🗺️ Lab Path & Learning Objectives

### End Goal
By the end of this 30-minute lab, you will have created a custom Conversational Analytics Agent connected to the Cymbal Gadgets retail data warehouse, launched a data engineering web application, audited multi-turn queries, and patched runtime agent guardrails.

### The 5-Phase Learning Path

| Phase | Milestone | Learning Objective for Data Engineers | Tool Used |
| :---: | :--- | :--- | :--- |
| **Phase 0** | **Student Credentials Setup** | Authenticate to Looker 4.0 API using assigned API3 client credentials. Clear any legacy credentials. | Web App Portal (`:8080`) / `.env` |
| **Phase 1** | **API Explorer & Core API Methods** | Follow the video journey: create agent (`POST /agents`), supply golden query, create conversation (`POST /conversations`), test chat API (`POST /conversational_analytics/chat`), inspect Python code snippets. | Looker API Explorer & Python SDK |
| **Phase 2** | **Web Client Deployment** | Launch the Python web client in your dedicated Cloud Shell; execute automated health checks. | Cloud Shell Terminal / Web Preview |
| **Phase 3** | **Interactive Queries & Tracing** | Submit natural language queries in the web UI and audit the 5-stage agent response lifecycle (`THOUGHT`, `SCHEMA`, `QUERY`, `DATA`, `FINAL_RESPONSE`). | Web App Dual-Pane Console |
| **Phase 4** | **Prompt Tuning & Productionizing** | Dynamically update agent guardrails using `PATCH /agents/{id}`; review Google Cloud Run serverless deployment architecture. | REST API / Cloud Run Architecture |
| **Phase 5** | **Teardown & Resource Cleanup** | Maintain enterprise multi-tenant hygiene: revert agent patch, delete golden query, conversation session, and custom agent. | API Explorer / Python / 1-Click UI |

---

## 📚 Looker Concepts for Data Engineers (Quick Reference)

If you have never worked with Looker before, here is how Looker concepts map directly to concepts you already know:

| Looker Concept | Data Engineering / Data Warehouse Analogy | Cymbal Gadgets Example |
| :--- | :--- | :--- |
| **Model** | Database catalog / schema configuration containing explores sharing a BigQuery connection. | `cymbal_gadgets_boris` |
| **Explore** | A pre-joined Star Schema or Dimensional Data Mart (fact table joined to dimension tables). | `transactions` (Sales facts joined to store & product dimensions) |
| **View** | A table declaration or SQL CTE defining columns, dimensions, and aggregations. | `transactions.view.lkml`, `product_reviews.view.lkml` |
| **Dimension** | A column or attribute used for slicing, filtering, and `GROUP BY`. | `store_country`, `transaction_date`, `product_category` |
| **Measure** | An explicit aggregate calculation (`SUM`, `AVG`, `COUNT`) with built-in business formulas. | `total_sales_amount`, `gross_margin_percentage` |
| **API Explorer** | An interactive in-browser Swagger/OpenAPI workbench for testing all Looker 4.0 REST endpoints. | Built-in Looker Extension |

---

## 🔄 End-to-End Operational Flow

Rather than a complex diagram, here is the exact chronological sequence of what happens when a question is processed:

1. **Client Authentication:** The client sends API3 credentials (`client_id` and `client_secret`) to `POST /api/4.0/login` to obtain a short-lived token (`Authorization: token <access_token>`).
2. **Agent Definition:** The engineer defines an agent via `POST /api/4.0/agents` bounded to LookML explore `transactions`.
3. **Golden Query Grounding:** The engineer supplies verified question-answer pairs (`POST /api/4.0/golden_queries`) to teach the LLM verified business query paths.
4. **Session Initialization:** The client calls `POST /api/4.0/conversations` with `{ "agent_id": "<your_agent_id>" }`. Looker allocates a server-side session `conversation_id`, managing all conversation history and token context automatically.
5. **Chat Prompt:** The client posts a question to `POST /api/4.0/conversational_analytics/chat`.
6. **Schema Introspection:** The Looker agent searches the designated LookML explore (`transactions`) to identify relevant dimensions and measures matching the user's intent.
7. **Deterministic SQL Compilation:** Looker compiles the formal query parameters into optimized, dialect-specific Google Cloud BigQuery SQL.
8. **BigQuery Execution:** The query executes directly in BigQuery.
9. **Synthesis & Audit Stream:** The API returns a multi-part JSON response containing the agent's chain of thought, the LookML query spec, the raw tabular result rows, and a formatted natural language summary.

---

## 🛠️ Major Functions & Endpoints of the CA API

The Conversational Analytics API family consists of the following primary endpoints:

| Endpoint | Method | Function & Purpose |
| :--- | :---: | :--- |
| `/api/4.0/login` | `POST` | Authenticates with `client_id` and `client_secret`, returning an `access_token`. |
| `/api/4.0/agents` | `POST` | **Create Agent**: Defines agent name, description, semantic sources (model/explore), and prompt instructions. |
| `/api/4.0/golden_queries` | `POST` | **Create Golden Query**: Defines verified question variations and exact Looker Explore answer URLs to anchor agent accuracy. |
| `/api/4.0/agents/search` | `GET` | **Search Agents**: Lists existing agents accessible to the current user. |
| `/api/4.0/agents/{agent_id}` | `GET` | **Get Agent**: Retrieves full configuration, context, and semantic bindings for an agent. |
| `/api/4.0/agents/{agent_id}` | `PATCH` | **Update Agent**: Dynamically modifies agent system instructions, formatting rules, or explore sources. |
| `/api/4.0/conversations` | `POST` | **Create Conversation**: Initializes a stateful multi-turn session bound to a specific agent. |
| `/api/4.0/conversations/{id}` | `GET` | **Get Conversation**: Retrieves message history and context state for a conversation. |
| `/api/4.0/conversational_analytics/chat` | `POST` | **Submit Query**: Sends user prompt and `conversation_id`; streams multi-part reasoning and query results. |

---

## 📦 Anatomy of the Conversational Analytics Response Payload

When calling `POST /conversational_analytics/chat`, the API does not just return a raw text message. It returns a structured multi-part array representing the 5 phases of the agent's execution lifecycle:

| Message Phase | Key in API Response | Purpose & Value for Data Engineers |
| :--- | :--- | :--- |
| **1. THOUGHT** | `systemMessage.text.textType == "THOUGHT"` | Chain-of-Thought reasoning. Shows how the agent interpreted the user's intent. |
| **2. SCHEMA** | `systemMessage.schema` | Semantic entities inspected from the LookML explore. Verifies which views were considered. |
| **3. QUERY** | `systemMessage.data.query` | Formal LookML query specification (fields, filters, sort orders, pivots) chosen by the agent. |
| **4. DATA** | `systemMessage.data.result` | Verified tabular data returned directly from the BigQuery query execution. |
| **5. FINAL_RESPONSE** | `systemMessage.text.textType == "FINAL_RESPONSE"` | Synthesized natural language executive summary presented to business users. |

---

## ⏱️ Lab Agenda & Timeline (30 Minutes)

| Step | Topic | Duration | Assessment Deliverable | Points |
| :---: | :--- | :---: | :--- | :---: |
| **Step 0** | Student Credentials Setup | 3 mins | Enter assigned Looker API credentials; clear previous cache | Required |
| **Step 1** | API Explorer & Create Custom Agent | 10 mins | Create uniquely-named agent via `POST /agents` | 20 pts |
| **Step 2** | Launch Web App & Verify Health | 5 mins | Launch Python client; verify health via terminal or UI | 20 pts |
| **Step 3** | Interactive Queries & Tracing | 10 mins | Submit multi-turn queries; audit 5-stage response lifecycle | 20 pts |
| **Step 4** | Prompt Tuning & Cloud Run Architecture | 5 mins | Patch guardrails via `PATCH /agents/{id}`; review deployment | 20 pts |
| **Step 5** | Teardown & Resource Cleanup | 2 mins | Revert patch, delete golden query, conversation, and agent | 20 pts |
| **Total** | | **35 mins** | **Complete All 5 Checkpoints (Including Teardown)** | **100 pts** |

---

# 🔑 Step 0: Student Credentials Setup (3 Mins)

Every student must authenticate using the Looker API3 credentials (`client_id` and `client_secret`) created during the required prework for this lab.

### 🧹 Ensuring Fresh Credentials
Previous test credentials have been cleared from `.env` and the application to ensure every student begins with a clean slate. You will see the yellow prompt: **"Specify your own user id / secret: Enter the Looker API3 credentials you have created during the required prework for this lab."**

### Option A: Configure in the Interactive Web Portal (Recommended)
> 💡 **User-Centric Flow:** The web portal does **not** interrupt you with an automatic credentials popup when loaded. Instead, you can comfortably read the instructions first, and when you are ready, simply click the **Open Student Credentials Dialog** button in Step 0 or in the top navigation bar.

1. In the opened portal (`http://localhost:8080`), click the button **Open Student Credentials Dialog** (located in the Step 0 card or the top navigation bar).
2. Enter the credentials you created during the required prework for this lab:
   * **Looker Client ID:** *(enter your client ID)*
   * **Looker Client Secret:** *(enter your client secret)*
3. Click **Save & Test Connection**.
4. The portal authenticates against Looker API 4.0 and displays a green badge: `Looker Connected`.

> 💡 **Single Window / Tab Reuse:** All Looker API Explorer links in both the web portal and the slide presentation are configured to open in the **same browser tab** (`looker_api_explorer`). You won't end up with dozens of open tabs as you progress through each API method!
>
> 💡 **Clearing Credentials:** If you ever need to clear or re-enter credentials, open the dialog and click **Clear Saved Credentials** to wipe all stored values.

### Option B: Configure in Terminal (`.env`)
If you prefer configuring credentials in the command line:
1. **Open another Cloud Shell terminal tab first** (click the **`+`** icon in the Cloud Shell terminal bar so you do not stop the running web server in your first terminal).
2. **Run the interactive credential command below:** It navigates to `~/cymbal_gadgets/agentic_web_app`, prompts you for your prework **Looker Client ID** and **Looker Client Secret**, and writes them directly into `.env`:
```bash
cd /home/admin_/cymbal_gadgets/agentic_web_app 2>/dev/null || cd ~/cymbal_gadgets/agentic_web_app; read -p "Enter your Looker Client ID: " CID && read -p "Enter your Looker Client Secret: " CSEC && CID=$(echo "$CID" | tr -d " '\"") && CSEC=$(echo "$CSEC" | tr -d " '\"") && printf "LOOKER_BASE_URL=https://ceworkshops.cloud.looker.com\nLOOKER_CLIENT_ID=%s\nLOOKER_CLIENT_SECRET=%s\nDEFAULT_MODEL=cymbal_gadgets_boris\nDEFAULT_EXPLORE=transactions\nPORT=8080\n" "$CID" "$CSEC" > .env && echo "✅ Saved Looker credentials to $(pwd)/.env"
```

---

# 🚀 Step 1: Conversational Analytics Core API Journey (API Explorer & Python SDK) (10 Mins)

> 📺 **Video Companion:** This hands-on section directly mirrors the official walkthrough demonstrated in **[Looker Conversational Analytics API Walkthrough](https://www.youtube.com/watch?v=XyU90O49p8o)** by the Looker EMEA Customer Engineering team.

### 1.1 The Complete Conversational Analytics Lifecycle
In production applications, building on Looker's Conversational Analytics API follows an auditable 6-stage lifecycle:
1. **Create an Agent (`create_agent` / `POST /api/4.0/agents`):**  
   Configure an agent bounded to Looker's semantic layer (model `cymbal_gadgets_boris`, explore `transactions`), specify business rules, and enable analytical details (`show_analytical_details: true`).
2. **Ground with Golden Queries (`create_golden_query` / `POST /api/4.0/golden_queries`):**  
   Anchor the agent with verified question-and-explore-answer pairs. Golden queries act as ground-truth few-shot examples, teaching the LLM how to resolve complex phrasing, specific filters, and calculations without guessing.
3. **Create a Conversation Session (`create_conversation` / `POST /api/4.0/conversations`):**  
   Initialize a stateful conversation thread bound to the `agent_id` just created. Looker allocates a server-side `conversation_id`, automatically managing token budgeting and conversation history.
4. **Submit Queries via the Chat API Method (`conversational_analytics_chat` / `POST /api/4.0/conversational_analytics/chat`):**  
   Test the core Chat API endpoint in API Explorer. The engine introspects the Explore, generates deterministic BigQuery SQL, executes it, and streams back verified tabular data alongside a complete **5-stage reasoning trace** (`THOUGHT`, `SCHEMA`, `QUERY`, `DATA`, `FINAL_RESPONSE`).
5. **Interactive UI Chat Experience (Web Application):**  
   Launch the web client, connect to the agent, and audit execution traces in real time.
6. **Dynamic Instruction Tuning (`update_agent` / `PATCH /api/4.0/agents/{agent_id}`):**  
   Patch business rules, persona, and formatting guardrails on the fly without restarting services or redeploying code.

---

### 1.2 Dual Pathways for Completing Task 1 & Where to Run Python Code

Students have **two completely equivalent pathways** to execute every step of Task 1 (Create Agent, Golden Query, Conversation Session, Chat API Test):

| Pathway | Interface | Description | Recommended For |
| :--- | :--- | :--- | :--- |
| **Pathway 1: Looker API Explorer** | Interactive GUI in Looker | Built-in browser workbench. Click direct links, open **Run It**, paste JSON, click **Run Request**. | Students who prefer an interactive visual walkthrough without writing code. |
| **Pathway 2: Python Code Snippets** | Terminal / Script / Notebook | Programmatic execution using `looker_sdk` or zero-dependency `LookerClient`. | Students who want hands-on experience scripting against Looker CA APIs. |

#### 📌 Where to Paste and Execute the Python Code:
If you choose Pathway 2, you can run the Python code in any of these convenient ways:

1. **Ready-to-Run Standalone Script (Fastest & Zero Dependencies):**
   * Execute the included standalone script directly in Cloud Shell (uses only standard Python libraries):
     ```bash
     cd ~/cymbal_gadgets
     python3 create_agent.py
     ```
   * Or pass your custom First Name and Last Name (if omitted, the script prompts you to enter your First Name, Last Name):
     ```bash
     python3 create_agent.py --name "Cymbal Retail Agent - First Name Last Name"
     ```
2. **Google Cloud Shell Interactive REPL:**
   * In your Cloud Shell terminal, start an interactive Python 3 session:
     ```bash
     python3
     ```
   * Copy **Option A (Zero-Dependency `LookerClient`)** snippet and paste it directly into the Python REPL prompt (`>>>`).
3. **Cloud Shell Script File:**
   * In Cloud Shell, create a test script file:
     ```bash
     cd ~/cymbal_gadgets/agentic_web_app
     nano test_task1.py
     ```
   * Paste Option A Python code, save (`Ctrl+O`, `Enter`, `Ctrl+X`), and execute:
     ```bash
     python3 test_task1.py
     ```
4. **Jupyter / Vertex AI Workbench Notebook:**
   * Create a new Python 3 notebook cell, paste the code snippet, and run the cell (`Shift+Enter`).

> 💡 **Fixing `ModuleNotFoundError: No module named 'looker_sdk'` in Cloud Shell:**  
> The default Cloud Shell environment does not include the third-party `looker-sdk` package. If you attempt `import looker_sdk` without installing it, Python throws `ModuleNotFoundError: No module named 'looker_sdk'`.  
> * **Zero-Dependency Solution (Recommended):** Use **Option A (`LookerClient`)** or run `python3 create_agent.py`. It uses Python standard library `urllib` and works out-of-the-box without installing anything.  
> * **SDK Solution:** If you wish to use the official Looker SDK, install it first via:  
>   ```bash
>   pip install looker-sdk
>   ```

---

### 1.3 Accessing the `CreateAgent` Method in API Explorer
👉 **Direct Link:** **[CreateAgent Method in API Explorer](https://ceworkshops.cloud.looker.com/extensions/marketplace_extension_api_explorer::api-explorer/4.0/methods/ConversationalAnalytics/create_agent)**

Clicking the direct link takes you directly to the `create_agent` method under the `ConversationalAnalytics` namespace in Looker API Explorer.

*(If navigating manually: In Looker, click **Applications > API Explorer**, ensure **Looker API 4.0** is selected in the top-right dropdown, search for `create_agent` or navigate to `ConversationalAnalytics > create_agent`).*

---

### 1.4 Step-by-Step: How to Run `CreateAgent` in API Explorer

> ⚡ **Multi-Student Naming Rule & Interactive First Name / Last Name JSON Builder:**  
> Because students share the workshop Looker instance, **Step 1, Task 1 in the Lab Guide UI includes a Student Name JSON Builder where you enter your First Name and Last Name once**, and it automatically builds and propagates your name across all Step 1 API Explorer tasks (e.g. `"name": "Cymbal Retail Analytics Agent - Jane Doe"`). You never have to manually edit a placeholder!

1. **Enter Your First Name & Last Name to Build the JSON:**  
   In Step 1, Task 1 of the Lab Guide UI, enter your **First Name** and **Last Name** in the **Student Name Builder** fields and click **Build JSON** (or click **Copy JSON** / **Open create_agent** to be prompted). The portal dynamically builds the JSON payload below with your First Name and Last Name and automatically propagates it to Tasks 2, 3, and 4.

2. **Open the "Run It" Tab:**  
   In the API Explorer view for `create_agent`, click on the **Run It** tab on the right side of the screen.

3. **Where to Paste the Built JSON Payload:**  
   Scroll down to the **Request Body** editor field (labeled `body`). Clear any placeholder text and paste the dynamically built JSON payload from the Lab Guide UI:

```json
{
  "name": "Cymbal Retail Analytics Agent - First Name Last Name",
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
*(Built automatically with your provided **First Name** and **Last Name** in the Step 1 JSON Builder).*

#### Detailed Explanation of What We Are Doing:
* **`name`**: Unique display name for identifying your agent among peers.
* **`sources`**: Semantic grounding. Confines the agent strictly to `cymbal_gadgets_boris/transactions`. The agent cannot touch any other explores or tables.
* **`context.instructions`**: Business guardrails that eliminate metric hallucinations (e.g. mapping "profitability" strictly to `Gross Margin Percentage`).
* **`show_analytical_details: true`**: Tells Looker to expose full reasoning traces. This ensures that **tracing will be available in the application when the prompt is run**!

3. **Execute the Request:** Click the blue **Run Request** button.
4. **What to Expect as an Output:** Status **`POST /agents (200: OK)`** (or `201: Created`).
5. **Where to Find the Newly Created Agent ID:**  
   In the response JSON output, locate the top-level **`"id"`** property on the very first line:  
   `"id": "a9b6933c74a045de9ed130ad024cca62"`  
   **Copy this 32-character hexadecimal string!** You will use this `agent_id` immediately in the next steps.

---

### 1.5 🐍 Alternatively use this Python Code Snippet: Create Agent

If you prefer programmatic execution rather than using API Explorer, **alternatively use this Python code snippet** to create your agent (you will be prompted to enter your First Name, Last Name before the script creates the agent):

#### Option A: Zero-Dependency LookerClient (Recommended - Works in Cloud Shell, interactive Python3 environment)
This option uses Python's standard library (`urllib`) and requires **no external packages or pip installs**:

```python
# Option A: Zero-Dependency LookerClient (Recommended - Works in Cloud Shell, interactive Python3 environment)
import os, sys; sys.path.insert(0, os.path.expanduser("~/cymbal_gadgets/agentic_web_app")); from looker_client import LookerClient; client = LookerClient(); student_name = input("Enter your First Name, Last Name: ").strip() or "First Name Last Name"; agent = client.create_agent(
    name=f"Cymbal Retail Analytics Agent - {student_name}",
    description="Conversational BI agent providing governed retail insights",
    model="cymbal_gadgets_boris",
    explore="transactions",
    instructions="- Always use Gross Margin Percentage for profitability questions."
); agent_id = agent["id"]; print("Agent ID:", agent_id)
```

> ⚡ **Even Simpler: Run the Standalone Script!**  
> You can also run the ready-to-use script directly from your Cloud Shell prompt without copying Python code (it will prompt you for your First Name, Last Name):  
> ```bash
> python3 ~/cymbal_gadgets/create_agent.py
> ```

#### Option B: Looker Python SDK (Requires `pip install looker-sdk`)
> ⚠️ **Note:** If you run this option without installing the SDK first, Python will report `ModuleNotFoundError: No module named 'looker_sdk'`. Run `pip install looker-sdk` before executing:

```python
import looker_sdk
from looker_sdk import models40

# Initialize Looker SDK (reads credentials from looker.ini or environment variables)
sdk = looker_sdk.init40()

student_name = input("Enter your First Name, Last Name: ").strip() or "First Name Last Name"; new_agent = sdk.create_agent(
    body=models40.WriteAgent(
        name=f"Cymbal Retail Analytics Agent - {student_name}",
        description="Conversational BI agent providing governed retail insights for Cymbal Gadgets",
        sources=[
            models40.AgentSource(
                model="cymbal_gadgets_boris",
                explore="transactions"
            )
        ],
        context=models40.AgentContext(
            instructions=(
                "- Always use Gross Margin Percentage when asked about profitability, margin, or sales performance.\n"
                "- When asked for trends over time, group by transaction date or transaction month.\n"
                "- If the user asks for store performance, breakdown by store country.\n"
                "- Keep executive summaries concise with key metrics highlighted in bold."
            ),
            show_analytical_details=True,
            show_debug=False
        )
    )
); print(f"✅ Created Agent ID: {new_agent.id}")
```

---

### 1.6 🌟 Supplying a Golden Query & Linking to Your Agent (`POST /api/4.0/golden_queries` & `PATCH /api/4.0/agents/{agent_id}`)

#### What is a Golden Query (Verified Query)?
In Looker Conversational Analytics, a **Golden Query** (also officially known as a **Verified Query**) is an explicit pair of a natural language question linked directly to a verified Looker Explore answer URL.

**Why Data Engineers Need Golden Queries:**
* **Eliminate Semantic Ambiguity:** When users ask questions with business jargon (e.g. *"What was our total take last quarter?"* or *"Top line volume"*), Golden Queries instruct the agent exactly which measures (`transactions.total_sale_price`) and filters to use.
* **Few-Shot Ground Truth:** Google recommends supplying verified query exemplars to anchor the LLM to known Explore configurations, avoiding guesswork and hallucinations.

> [!WARNING]
> **Looker API 4.0 Rule (Prevents HTTP 422 Error):**  
> Looker API 4.0 strictly validates that **only one question is supported per golden query**. Providing multiple strings in the `questions` array returns `422: only one question is supported per golden query`. To ground multiple phrasing variations, create individual golden queries and link their integer IDs into the agent's `golden_query_ids` array!

#### Golden Query Example for Cymbal Gadgets:
* **Question (`questions`):**
  * `["What is our total sales amount across all transactions?"]`
* **Explore Answer URL (`answer`):**  
  `https://ceworkshops.cloud.looker.com/explore/cymbal_gadgets_boris/transactions?fields=transactions.total_sale_price`

---

#### Step-by-Step: Run `create_golden_query` in API Explorer
👉 **Direct Link:** **[CreateGoldenQuery Method in API Explorer](https://ceworkshops.cloud.looker.com/extensions/marketplace_extension_api_explorer::api-explorer/4.0/methods/ConversationalAnalytics/create_golden_query)**

1. Navigate to `ConversationalAnalytics > create_golden_query` in Looker API Explorer.
2. Click the **Run It** tab.
3. In the **Request Body (`body`)** editor, paste the single-question JSON payload:
```json
{
  "questions": [
    "What is our total sales amount across all transactions?"
  ],
  "answer": "https://ceworkshops.cloud.looker.com/explore/cymbal_gadgets_boris/transactions?fields=transactions.total_sale_price"
}
```
4. Click **Run Request**.  
   * **Status:** `POST /golden_queries (200: OK)` (or `201: Created`).  
   * **Response Body:** Returns the created golden query object with both `"id"` and `"query_id"`.

> [!IMPORTANT]
> **CRITICAL: Looker Returns Two IDs — Use `"id"`, NOT `"query_id"`!**  
> In the response JSON, Looker returns:  
> * **`"id": 142`** &rarr; **THIS IS THE ONE YOU NEED!** (The integer Golden Query record identifier).  
> * **`"query_id": 19284`** &rarr; **DO NOT USE THIS!** (This is Looker's underlying Explore SQL query spec ID).  
> **Copy the integer `"id"`** (e.g. `142`) for linking and teardown!

---

#### Step-by-Step: How to Link the Golden Query to Your Agent in API Explorer
👉 **Direct Link:** **[UpdateAgent Method in API Explorer](https://ceworkshops.cloud.looker.com/extensions/marketplace_extension_api_explorer::api-explorer/4.0/methods/ConversationalAnalytics/update_agent)**

Once the Golden Query is created, you must link its integer ID to your agent:
1. In Step 1, Task 2 in the Lab Guide UI, paste your integer Golden Query `"id"` (e.g. `142`). Your **First Name** and **Last Name** are automatically propagated from Task 1 into the `update_agent` JSON payload.
2. Open the **[UpdateAgent Method in API Explorer](https://ceworkshops.cloud.looker.com/extensions/marketplace_extension_api_explorer::api-explorer/4.0/methods/ConversationalAnalytics/update_agent)** (under `ConversationalAnalytics > update_agent`).
3. Click the **Run It** tab.
4. In the **Parameters** section, locate the `agent_id` field and paste your **32-character Agent ID** from Step 1.4.
5. In the **Request Body (`body`)** editor, paste the built JSON payload:
```json
{
  "name": "Cymbal Retail Analytics Agent - First Name Last Name",
  "sources": [
    {
      "model": "cymbal_gadgets_boris",
      "explore": "transactions"
    }
  ],
  "golden_query_ids": [142]
}
```
*(Automatically built using your **First Name** and **Last Name** propagated from Task 1, plus your numeric Golden Query `"id"`).*
6. Click **Run Request**.  
   * **Status:** `PATCH /agents/{agent_id} (200: OK)`  
   * **Response Body:** The response contains `"golden_query_ids": [142]`, confirming that your agent is now officially anchored by the verified golden query!

---

#### 🐍 Alternatively use this Python Code Snippet: Create & Link Golden Query

If you prefer programmatic execution rather than using API Explorer, **alternatively use this Python code snippet** to create and link the golden query (it will prompt for your First Name, Last Name before updating the agent):

##### Option A: Zero-Dependency LookerClient (Recommended - Works in Cloud Shell, interactive Python3 environment)
```python
# Option A: Zero-Dependency LookerClient (Recommended - Works in Cloud Shell, interactive Python3 environment)
import os, sys; sys.path.insert(0, os.path.expanduser("~/cymbal_gadgets/agentic_web_app")); from looker_client import LookerClient; client = LookerClient(); agent_id = globals().get("agent_id") or input("Enter your Step 1 Agent ID: ").strip(); student_name = input("Enter your First Name, Last Name: ").strip() or "First Name Last Name"; gq = client.create_golden_query(
    questions=["What is our total sales amount across all transactions?"],
    answer="https://ceworkshops.cloud.looker.com/explore/cymbal_gadgets_boris/transactions?fields=transactions.total_sale_price"
); client.update_agent(agent_id, {
    "name": f"Cymbal Retail Analytics Agent - {student_name}",
    "golden_query_ids": [gq["id"]],
    "sources": [{"model": "cymbal_gadgets_boris", "explore": "transactions"}]
}); print("Created & Linked Golden Query ID:", gq["id"])
```

##### Option B: Looker Python SDK (Requires `pip install looker-sdk`)
```python
# 1. Create Golden Query (Single question strictly required by Looker 4.0)
golden_query = sdk.create_golden_query(
    body=models40.WriteGoldenQuery(
        questions=["What is our total sales amount across all transactions?"],
        answer="https://ceworkshops.cloud.looker.com/explore/cymbal_gadgets_boris/transactions?fields=transactions.total_sale_price"
    )
)

# 2. Link to Agent
student_name = input("Enter your First Name, Last Name: ").strip() or "First Name Last Name"; sdk.update_agent(
    agent_id=new_agent.id,
    body=models40.WriteAgent(
        name=f"Cymbal Retail Analytics Agent - {student_name}",
        sources=[models40.AgentSource(model="cymbal_gadgets_boris", explore="transactions")],
        golden_query_ids=[golden_query.id]
    )
); print(f"✅ Linked Golden Query {golden_query.id} to Agent {new_agent.id}")
```

---

### 1.7 💬 Create Conversation Session Using Your New Agent ID (`POST /api/4.0/conversations`)

#### Why Conversations Are Created:
Looker manages stateful conversational threads on the server. Instead of forcing client applications to maintain chat arrays, calculate token windows, and re-transmit historical turns, Looker allocates a persistent `conversation_id`. All multi-turn context and follow-ups are preserved automatically!

👉 **Direct Link:** **[CreateConversation Method in API Explorer](https://ceworkshops.cloud.looker.com/extensions/marketplace_extension_api_explorer::api-explorer/4.0/methods/ConversationalAnalytics/create_conversation)**  
*(Also accessible under `Conversation > create_conversation`)*

#### Step-by-Step: Run `create_conversation` in API Explorer
1. In Step 1, Task 3 in the Lab Guide UI, enter your **Agent ID** from Step 1.4. The JSON payload is automatically built with your **First Name** and **Last Name** (propagated from Task 1) and your **Agent ID**.
2. Navigate to the `create_conversation` method in API Explorer.
3. Click the **Run It** tab.
4. In the **Request Body (`body`)** editor, paste the built JSON payload:
```json
{
  "agent_id": "a9b6933c74a045de9ed130ad024cca62",
  "name": "Cymbal Retail Session - First Name Last Name"
}
```
*(Automatically built using your **First Name** and **Last Name** propagated from Task 1, plus your **Agent ID**).*

5. Click **Run Request**.
6. **What to Expect as an Output:**  
   * **Status:** **`POST /conversations (200: OK)`** (or `201: Created`).
   * **Response Body:**
   ```json
   {
     "id": "c1f2e3d4-5678-90ab-cdef-1234567890ab",
     "name": "Cymbal Retail Session - First Name Last Name",
     "agent_id": "a9b6933c74a045de9ed130ad024cca62",
     "created_at": "2026-09-28T17:30:00.000Z"
   }
   ```
7. **Where to Find the Newly Created Conversation ID:**  
   Look at the top-level **`"id"`** property:  
   `"id": "c1f2e3d4-5678-90ab-cdef-1234567890ab"`  
   **Copy this Conversation ID!** You will pass it directly to the Chat API method in Step 1.8.

#### 🐍 Alternatively use this Python Code Snippet: Create Conversation

If you prefer programmatic execution rather than using API Explorer, **alternatively use this Python code snippet** to initialize the session (it will prompt for your First Name, Last Name):

##### Option A: Zero-Dependency LookerClient (Recommended - Works in Cloud Shell, interactive Python3 environment)
```python
# Option A: Zero-Dependency LookerClient (Recommended - Works in Cloud Shell, interactive Python3 environment)
import os, sys; sys.path.insert(0, os.path.expanduser("~/cymbal_gadgets/agentic_web_app")); from looker_client import LookerClient; client = LookerClient(); agent_id = globals().get("agent_id") or input("Enter your Step 1 Agent ID: ").strip(); student_name = input("Enter your First Name, Last Name: ").strip() or "First Name Last Name"; conv = client.create_conversation(
    agent_id=agent_id,
    name=f"Cymbal Retail Session - {student_name}"
); conv_id = conv["id"]; print("Conversation ID:", conv_id)
```

##### Option B: Looker Python SDK (Requires `pip install looker-sdk`)
```python
student_name = input("Enter your First Name, Last Name: ").strip() or "First Name Last Name"; conversation = sdk.create_conversation(
    body=models40.WriteConversation(
        agent_id=new_agent.id,  # Or replace with your Step 1 Agent ID
        name=f"Cymbal Retail Session - {student_name}"
    )
); print(f"✅ Created Conversation Session ID: {conversation.id}")
```

---

### 1.8 ⚡ Testing the Chat API Method Before Showing the Chat UI (`POST /api/4.0/conversational_analytics/chat`)

Before displaying the interactive web application chat interface, data engineers inspect the core Chat API endpoint directly in API Explorer to understand the underlying HTTP contract and 5-stage stream payload.

👉 **Direct Link:** **[ConversationalAnalyticsChat Method in API Explorer](https://ceworkshops.cloud.looker.com/extensions/marketplace_extension_api_explorer::api-explorer/4.0/methods/ConversationalAnalytics/conversational_analytics_chat)**

#### Step-by-Step: Run `conversational_analytics_chat` in API Explorer
1. In Step 1, Task 4 in the Lab Guide UI, enter your **`conversation_id` from Step 1.7** to automatically build the JSON payload.
2. Navigate to `ConversationalAnalytics > conversational_analytics_chat` in Looker API Explorer.
3. Click the **Run It** tab.
4. In the **Request Body (`body`)** editor, paste the built JSON payload with your `conversation_id` and question:
```json
{
  "conversation_id": "c1f2e3d4-5678-90ab-cdef-1234567890ab",
  "user_message": "What is our total sales amount across all transactions?"
}
```
5. Click **Run Request**.

#### What to Expect: Anatomy of the 5-Stage Response Stream
The API returns an array of structured event objects. Notice how Looker exposes the entire AI execution pipeline:
1. **Stage 1 (THOUGHT):**  
   `systemMessage.text.textType == "THOUGHT"` &mdash; Chain-of-thought tokens demonstrating user intent resolution and Explore mapping.
2. **Stage 2 (SCHEMA):**  
   `systemMessage.schema` &mdash; Semantic entities inspected from Explore `transactions`.
3. **Stage 3 (QUERY):**  
   `systemMessage.data.query` &mdash; Formal LookML Query Specification:  
   `{"model": "cymbal_gadgets_boris", "view": "transactions", "fields": ["transactions.total_sale_price"]}`.  
   *(Proves the LLM never generates un-governed, raw SQL!)*
4. **Stage 4 (DATA):**  
   `systemMessage.data.result` &mdash; Tabular BigQuery data records returned:  
   `[{"transactions.total_sale_price": 1074890772}]`.
5. **Stage 5 (FINAL_RESPONSE):**  
   `systemMessage.text.textType == "FINAL_RESPONSE"` &mdash; Executive summary grounded in the BigQuery tabular results.

#### 🐍 Alternatively use this Python Code Snippet: Submit Analytical Query & Parse Stream

If you prefer programmatic execution rather than using API Explorer, **alternatively use this Python code snippet** to submit your question and parse the 5-stage stream:

##### Option A: Zero-Dependency LookerClient (Recommended - Works in Cloud Shell, interactive Python3 environment)
```python
# Option A: Zero-Dependency LookerClient (Recommended - Works in Cloud Shell, interactive Python3 environment)
import os, sys; sys.path.insert(0, os.path.expanduser("~/cymbal_gadgets/agentic_web_app")); from looker_client import LookerClient; client = LookerClient(); conv_id = globals().get("conv_id") or globals().get("conv", {}).get("id") or input("Enter your Step 3 Conversation ID: ").strip(); result = client.chat(
    conversation_id=conv_id,
    user_message="What is our total sales amount across all transactions?"
); print("🧠 Thoughts:", result.get("thoughts", [])); print("💻 Query Spec:", result.get("query", "")); print("📊 Data:", result.get("data", [])); print("📝 Summary:", result.get("final_response", ""))
```

##### Option B: Looker Python SDK (Requires `pip install looker-sdk`)
```python
chat_messages = sdk.conversational_analytics_chat(
    body=models40.ConversationalAnalyticsChatRequest(
        conversation_id=conversation.id,
        user_message="What is our total sales amount across all transactions?"
    )
)

for msg in chat_messages:
    sys_m = msg.system_message
    if sys_m:
        if sys_m.text:
            print(f"[{sys_m.text.text_type}]: {sys_m.text.parts}")
        if sys_m.data and sys_m.data.query:
            print("Compiled LookML Query:", sys_m.data.query)
        if sys_m.data and sys_m.data.result:
            print("Verified BigQuery Data:", sys_m.data.result)
```

---

### 1.9 🚩 CHECKPOINT 1: Verify Agent Creation (20 Points)
**Goal:** Confirm your agent exists and is queryable on the Looker instance.

* **In the Web App:** Navigate to `http://localhost:8080`, enter your generated **Agent ID** into the **Task 1** checkpoint field, and click **Check my progress** to earn **+20 points**!
* **Via Terminal (Optional):**
```bash
# In Cloud Shell, using your assigned credentials:
TOKEN=$(python3 -c "
import os, urllib.request, urllib.parse, json
client_id = os.environ.get('LOOKER_CLIENT_ID') or input('Client ID: ')
client_secret = os.environ.get('LOOKER_CLIENT_SECRET') or input('Client Secret: ')
data = urllib.parse.urlencode({'client_id': client_id, 'client_secret': client_secret}).encode()
req = urllib.request.Request('https://ceworkshops.cloud.looker.com/api/4.0/login', data=data, method='POST')
print(json.loads(urllib.request.urlopen(req).read().decode())['access_token'])
")

curl -s -H "Authorization: token $TOKEN" "https://ceworkshops.cloud.looker.com/api/4.0/agents/YOUR_AGENT_ID" | jq '{id, name, sources}'
```

---

# 💻 Step 2: Web Application Architecture & Health Check (5 Mins)

### 2.1 Understanding the Architecture: Connecting Step 1 to the Web Application
* In **Step 1**, you used the Looker API Explorer to manually explore Looker's REST primitives: creating an Agent (`POST /agents`), grounding with Golden Queries (`POST /golden_queries`), and initiating a conversation (`POST /conversations`).
* In an enterprise production setting, business analysts do not interact with raw API Explorers. Instead, **data engineers embed Looker Conversational Analytics into custom web applications** (such as this training portal).
* The web backend (`server.py` and `looker_client.py`) interfaces with Looker API 4.0 using the student credentials configured in Step 0. When you chat in the right-pane console, the web app initiates a conversation session (`POST /api/conversations`) bound to your Step 1 agent, maintaining chat context and tracing metadata across turns.

#### Your 3 Action Steps in Task 2:
1. **Verify Server Health:** Run the curl command below in Cloud Shell terminal OR click **Check my progress** in Checkpoint 2 to confirm backend connectivity.
2. **Display Chat Console:** Click the purple **Display Conversational Analytics Window** button at the bottom of Task 2 to unlock the interactive chat UI on the right pane.
3. **Proceed to Task 3:** Your web app will automatically bind your Step 1 Agent to interactive conversations, where you will audit thought processes and LookML query specs!

### 2.2 Codebase Structure
* **`looker_client.py`**: Zero-dependency Python client implementing Looker 4.0 token caching, agent discovery, conversation management, and response stream parsing.
* **`server.py`**: Multi-threaded Python HTTP REST API server and static host for the Single-Page Application.
* **`static/index.html`**: Dual-pane training portal with the Transparency Hub and Assessment Tracker.
* **`static/presentation.html`**: Interactive, standalone presentation slide deck for the lab.
* **`test_pipeline.py`**: Automated CLI verification script.
* **`run.sh`**: One-click startup script.

### 2.3 Starting the Web Server
If not already running, execute:
```bash
cd ~/cymbal_gadgets/agentic_web_app
./run.sh
```

---

### 🚩 CHECKPOINT 2: Verify Web Server Health (20 Points)
**Goal:** Confirm the web server is running and authenticated to Looker.

#### ❓ Crucial Instruction: Where to Execute Health Verification
1. **Option A (Fastest - Recommended): Use the Web UI Button**  
   In the web portal (`http://localhost:8080`), scroll to **Task 2: Checkpoint 2** and click **Check my progress**. The app automatically verifies health and awards **+20 points**!
2. **Option B: Run curl in a SECOND Terminal Tab in Cloud Shell**  
   * Open a **second terminal tab** (`+` icon in Cloud Shell).
   * **Do NOT run in the first terminal** (it is busy running `./run.sh`).
   * **Do NOT run on your local laptop** (`localhost:8080` exists in remote Cloud Shell).
   * **Do NOT curl external `https://*.cloudshell.dev` URLs**:
     > [!CAUTION]
     > **Troubleshooting `jq: parse error: Invalid numeric literal at line 1, column 3`:**  
     > **If you get the error `jq: parse error: Invalid numeric literal at line 1, column 3`, you can safely ignore it and continue directly to clicking "Check my progress" in Task 2!**  
     > **Why this happens:** If you run `curl -s https://<port>-cs-...cloudshell.dev/api/health | jq .` (using the external Cloud Shell Web Preview URL instead of `http://localhost:8080`), the Cloud Shell proxy requires browser SSO cookies and returns an HTTP 302 HTML redirect (`<a href="...">Found</a>.`), which fails `jq` parsing at column 3 (`<a `).  
     > **What to do:** Simply ignore that `jq` error and click **Check my progress** in **Task 2** in the web portal (or run `curl -s http://localhost:8080/api/health | jq .` against local HTTP loopback).
   * In your second Cloud Shell terminal:
   ```bash
   curl -s http://localhost:8080/api/health | jq .
   ```
   **Expected Output:**
   ```json
   {
     "status": "healthy",
     "looker_connected": true,
     "looker_url": "https://ceworkshops.cloud.looker.com",
     "user_email": "api_user@example.com"
   }
   ```

### 2.3 Display the Looker Conversational Analytics Window (End of Step 2)
Now that your agent is created (Step 1) and your backend client is verified healthy (Step 2):
1. In the web portal (`http://localhost:8080`), locate the **"Looker Conversational Analytics Interactive Window"** card at the end of **Task 2**.
2. Notice the badge updates to **"Ready to Display!"** (Prerequisites: 2 of 2 completed).
3. Click **"🚀 Display Conversational Analytics Window"**!
4. The window immediately opens on the right half of your screen in Split View, allowing you to see the active agent selector, conversation feed, and prompt input box before proceeding to Step 3.

---

# 🔍 Step 3: Interactive Prompting & Audit Real-Time Tracing (10 Mins)

### 3.1 What We Are Doing in This Step
In this step, data engineers test the live query execution pipeline using the Looker Conversational Analytics window displayed on the right pane:
1. We execute interactive prompts against the Cymbal Retail dataset.
2. We audit the 3-part execution trace (**Agent Thought Process**, **Governed Data Result**, and **Generated Looker Query Specification**) returned by the API.

---

### 3.2 Audit the Three Execution Tracing Accordions
When prompts execute, Looker returns a multi-stage stream. **Students must inspect all three accordions rendered below the agent's answer:**

1. **🧠 1. Agent Thought Process:**
   * Audits the LLM's step-by-step reasoning chain, user intent resolution, explore discovery, and LookML field mapping.
   * Look here to see *why* the agent chose `transactions.total_sale_price` and how it resolved business terminology.
2. **📊 2. Governed Data Result:**
   * Renders the raw tabular records returned directly from BigQuery via Looker (e.g. verifying the **$1,074,890,772** total sales figure).
   * Confirms metric accuracy and zero hallucination before visualization.
3. **💻 3. Generated Looker Query Specification:**
   * Displays the exact LookML query object (fields: `["transactions.total_sale_price"]`, dimensions, and filters) generated by Looker.
   * Proves that no un-governed, raw SQL was generated by the LLM.

---

### 3.3 Interactive Prompts to Run in the Application

Now test analytical queries in the right-hand chat window and inspect the real-time tracing:

1. **Query 1: Basic Metric Aggregation**
   * Enter:
     ```text
     What is our total sales amount across all transactions?
     ```
   * Click **Send**.
   * Open each tracing accordion beneath the answer:
     * **Agent Thought Process:** Read how the agent mapped the question to `transactions.total_sale_price`.
     * **Governed Data Result:** View the exact tabular number returned from BigQuery (`$1,074,890,772`).
     * **Generated Looker Query Specification:** See the formal LookML fields selected.

2. **Query 2: Dimensional Breakdown & Grouping**
   * Enter:
     ```text
     Show the average transaction amount by store country.
     ```
   * Observe the table generated with countries and averages.

3. **Query 3: Multi-turn Contextual Follow-Up**
   * Enter:
     ```text
     Which store country had the highest transaction volume?
     ```
   * Notice that because the session is stateful, the agent understands the context of "store country" without re-explaining the query!

---

### 🚩 CHECKPOINT 3: Verify Interactive Query Flow (20 Points)
**Goal:** Confirm the complete natural language-to-BigQuery execution pipeline.

* **In the Web App:** Enter your Step 1 `agent_id` into the **Task 3** checkpoint field and click **Check my progress** to earn **+20 points**!
* **Via Automated CLI Script:**
```bash
python3 ~/cymbal_gadgets/agentic_web_app/test_pipeline.py YOUR_STEP_1_AGENT_ID
```

---

# 🛡️ Step 4: Agent Instruction Tuning & Production Deployment (5 Mins)

### 4.1 Tuning Agent Behavior (`PATCH /api/4.0/agents/{agent_id}`)
Data engineers often need to enforce strict formatting, output length, or business terminology. You can update agent behavior on the fly using `PATCH /agents/{agent_id}`.

#### Cymbal Executive Guardrail Rules (Supply These as Prompts / Instructions)
**Important:** You need to **supply these rules as prompts** to your agent! You can supply them either as **system prompt instructions** in `context.instructions` (via API Explorer `update_agent`, the Python snippet below, or the **Apply Cymbal Guardrails** button in Task 4) OR **directly as prompt instructions in the Conversational Analytics chat window** on the right pane:
* Always begin your answer with `'🌟 Cymbal Executive Summary:'`
* Format all currency metrics in EUR with thousands separators (e.g. `€1,234,567`)
* If asked about gross margin, always state the exact percentage with two decimals
* Keep explanations concise (under 3 sentences)

**Example Prompt You Can Paste Directly into the Chat Window or `context.instructions`:**
```text
Please follow these Cymbal Executive Guardrail Rules for your response:
- Always begin your answer with '🌟 Cymbal Executive Summary:'
- Format all currency metrics in EUR with thousands separators (e.g. €1,234,567)
- If asked about gross margin, always state the exact percentage with two decimals
- Keep explanations concise (under 3 sentences)

Question: What is our total sales amount and gross margin percentage across all stores?
```

👉 **Direct Link:** **[UpdateAgent Method in API Explorer](https://ceworkshops.cloud.looker.com/extensions/marketplace_extension_api_explorer::api-explorer/4.0/methods/ConversationalAnalytics/update_agent)**

#### 🐍 Alternatively use this Python Code Snippet: Dynamic Instruction Tuning (Update Agent)

If you prefer programmatic execution rather than using API Explorer, **alternatively use this Python code snippet** to patch your agent's guardrails:

##### Option A: Zero-Dependency LookerClient (Recommended - Works in Cloud Shell, interactive Python3 environment)
```python
# Option A: Zero-Dependency LookerClient (Recommended - Works in Cloud Shell, interactive Python3 environment)
import os, sys; sys.path.insert(0, os.path.expanduser("~/cymbal_gadgets/agentic_web_app")); from looker_client import LookerClient; client = LookerClient(); agent_id = globals().get("agent_id") or input("Enter your Agent ID: ").strip(); student_name = input("Enter your First Name, Last Name: ").strip() or "First Name Last Name"; new_instructions = (
    "- Always begin your answer with '🌟 Cymbal Executive Summary:'\n"
    "- Format all currency metrics in EUR with thousands separators (e.g. €1,234,567)\n"
    "- If asked about gross margin, always state the exact percentage with two decimals\n"
    "- Keep explanations under 3 sentences"
); updated = client.update_agent(agent_id, {
    "name": f"Cymbal Retail Analytics Agent - {student_name}",
    "sources": [{"model": "cymbal_gadgets_boris", "explore": "transactions"}],
    "context": {"instructions": new_instructions, "show_analytical_details": True}
}); print(f"✅ Successfully updated instructions for: {updated.get('name')}")
```

##### Option B: Using Official Looker Python SDK (`looker_sdk`)
```python
import looker_sdk
from looker_sdk import models40

sdk = looker_sdk.init40()

new_instructions = (
    "- Always begin your answer with '🌟 Cymbal Executive Summary:'\n"
    "- Format all currency metrics in EUR with thousands separators (e.g. €1,234,567)\n"
    "- If asked about gross margin, always state the exact percentage with two decimals\n"
    "- Keep explanations under 3 sentences"
)

student_name = input("Enter your First Name, Last Name: ").strip() or "First Name Last Name"; updated_agent = sdk.update_agent(
    agent_id="YOUR_AGENT_ID",  # Replace with your Step 1 Agent ID
    body=models40.WriteAgent(
        name=f"Cymbal Retail Analytics Agent - {student_name}",
        sources=[models40.AgentSource(model="cymbal_gadgets_boris", explore="transactions")],
        context=models40.AgentContext(
            instructions=new_instructions,
            show_analytical_details=True
        )
    )
); print(f"✅ Successfully updated instructions for: {updated_agent.name}")
```

##### Run in Cloud Shell Terminal:
```bash
python3 -c "
import os, sys; sys.path.insert(0, os.path.expanduser('~/cymbal_gadgets/agentic_web_app'))
from looker_client import LookerClient
agent_id = input('Enter your Agent ID: ').strip()
student_name = input('Enter your First Name, Last Name: ').strip() or 'First Name Last Name'
client = LookerClient()
new_instructions = '''- Always begin your answer with \'🌟 Cymbal Executive Summary:\'
- Format all currency metrics in EUR with thousands separators (e.g. €1,234,567)
- If asked about gross margin, always state the exact percentage with two decimals
- Keep explanations under 3 sentences'''
updated = client.update_agent(agent_id, {'name': f'Cymbal Retail Analytics Agent - {student_name}', 'sources': [{'model': 'cymbal_gadgets_boris', 'explore': 'transactions'}], 'context': {'instructions': new_instructions, 'show_analytical_details': True}})
print('Successfully updated instructions for:', updated.get('name'))
"
```

After updating, ask your agent in the web app: *"What is our gross margin percentage?"*  
Notice that the agent immediately complies with the new formatting and persona rules without code redeployment!

---

### 4.2 Where & How Guardrails Are Applied in Conversational Analytics (CA) APIs

Enterprise data engineers must understand both the configuration touchpoints (**WHERE**) and the execution mechanisms (**HOW**) that guarantee AI governance:

#### 📍 WHERE Guardrails Are Applied in CA APIs:
1. **`context.instructions` in API Request Payload (`POST /api/4.0/agents` and `PATCH /api/4.0/agents/{agent_id}`):**
   * Configured directly in the JSON request body when creating or patching agents.
   * Specifies strict business terminology (e.g., *"Always use Gross Margin Percentage for profitability questions"*), output structure, persona prefixes, and constraints.
2. **Explore Boundary Whitelist in `sources` (`POST /api/4.0/agents`):**
   * Limits the agent to explicit model and explore boundaries:
     ```json
     "sources": [
       {"model": "cymbal_gadgets_boris", "explore": "transactions"}
     ]
     ```
   * The CA API engine rejects any attempt to query tables, databases, or schemas outside this whitelist.
3. **LookML Modeling Layer (`lookml_model`):**
   * Field definitions, dimension groups, hidden dimensions (`hidden: yes`), access grants, and user-attribute data filters apply enterprise data governance and row-level security before any query executes.

#### ⚙️ HOW Guardrails Are Enforced by the CA Engine:
1. **System Prompt Priming & Grounding:**
   * Looker CA engine injects `context.instructions` into Gemini's internal system prompt before processing user queries, establishing immutable behavioral boundaries.
2. **Metric & Dimension Steering:**
   * Directs the LLM to resolve ambiguous business phrases to specific LookML measures (e.g. mapping "how profitable are we" strictly to `transactions.gross_margin_percentage` rather than raw sales).
3. **Deterministic LookML Query Specification (Eliminating SQL Injection):**
   * The agent **never** outputs raw SQL text. Instead, it generates a structured LookML Query Specification (`fields`, `filters`, `sorts`). Looker's trusted compiler generates the BigQuery SQL, preventing SQL injection and hallucinations.
4. **Persona & Formatting Enforcement:**
   * Enforces executive persona rules (such as prefixing responses with `🌟 Cymbal Executive Summary:`, formatting currency in EUR, and capping explanations at 3 sentences) during final response synthesis.

---

### 4.3 Enterprise Production Architecture on Google Cloud

For enterprise production, Data Engineers deploy this pattern using Google Cloud serverless infrastructure:

#### Architectural Components & Data Path:
1. **Edge Security:** Google Cloud Armor and Identity-Aware Proxy (IAP) provide DDoS protection, enterprise SSO, and role-based access control.
2. **Application Layer:** Google Cloud Run hosts the stateless containerized web application or FastAPI microservice with automatic autoscaling.
3. **Secret Management:** Google Cloud Secret Manager securely stores `LOOKER_CLIENT_ID` and `LOOKER_CLIENT_SECRET`, mounted into Cloud Run via environment variables or secret volumes.
4. **Governed Intelligence:** Looker Conversational Analytics API handles natural language parsing, stateful session memory, and LookML query resolution.
5. **Data Warehouse:** Google Cloud BigQuery stores the underlying petabyte-scale data warehouse and executes the compiled, optimized SQL queries.

#### Production Deployment Checklist:
* **Containerization:** The repository includes a production-ready `Dockerfile` based on `python:3.12-slim`.
* **One-Click Cloud Run Script:** Execute `./deploy_cloud_run.sh` inside `agentic_web_app` to build and deploy to Google Cloud Run in minutes.
* **IAM Least Privilege:** Assign the Cloud Run service identity only the required Secret Manager accessor role (`roles/secretmanager.secretAccessor`).

---

### 🚩 CHECKPOINT 4: Prompt Guardrails & Tuning (20 Points)
In the interactive portal, click the **Check my progress** button under Task 4 to earn **+20 points** (80/100 Points Total). Complete Task 5 Teardown to earn the final 20 points and achieve 100/100!

---

# 🧹 Step 5: Lab Teardown & Resource Cleanup (Agent, Conversation, Golden Query & Patch) (2 Mins)

In enterprise data platforms and shared training environments, **teardown and resource hygiene are critical**. Leaving orphaned agents, dangling conversation sessions, and unneeded golden queries consumes memory, creates catalog clutter, and violates multi-tenant best practices.

In this step, you will clean up all four artifacts created during this lab:
1. **Revert Agent Patch:** Unlink golden queries (`golden_query_ids: []`) and restore default system instructions.
2. **Delete Golden Query:** Permanently remove the golden query rule via `DELETE /api/4.0/golden_queries/{golden_query_id}`.
3. **Delete Conversation Session:** Free server-side token memory and delete the session thread via `DELETE /api/4.0/conversations?id={conversation_id}`.
4. **Delete Agent Definition:** Remove your custom agent from Looker via `DELETE /api/4.0/agents?id={agent_id}`.

---

### 5.1 Teardown via Looker API Explorer (Pathway 1)

*(All links open in the same `looker_api_explorer` window tab so you don't accumulate dozens of tabs).*

1. **Revert Agent Patch:**
   * 👉 **Direct Link:** [update_agent in API Explorer](https://ceworkshops.cloud.looker.com/extensions/marketplace_extension_api_explorer::api-explorer/4.0/methods/ConversationalAnalytics/update_agent)
   * In Parameters, set `agent_id`: your Agent ID.
   * In Request Body, set:
     ```json
     {
       "golden_query_ids": [],
       "context": {
         "instructions": "Standard retail assistant for Cymbal Gadgets."
       }
     }
     ```
   * Click **Run Request** (`200 OK`).

2. **Delete Golden Query:**
   * 👉 **Direct Link:** [delete_golden_query in API Explorer](https://ceworkshops.cloud.looker.com/extensions/marketplace_extension_api_explorer::api-explorer/4.0/methods/ConversationalAnalytics/delete_golden_query)
   * In Parameters, set `golden_query_id`: your numeric Golden Query ID (e.g. `142`).
   * Click **Run Request** (`204 No Content` or `200 OK`).

3. **Delete Conversation Session:**
   * 👉 **Direct Link:** [delete_conversation in API Explorer](https://ceworkshops.cloud.looker.com/extensions/marketplace_extension_api_explorer::api-explorer/4.0/methods/ConversationalAnalytics/delete_conversation)
   * In Parameters, set `id`: your Conversation ID (passed as query param `?id=...`).
   * Click **Run Request** (`204 No Content` or `200 OK`).

4. **Delete Agent Definition:**
   * 👉 **Direct Link:** [delete_agent in API Explorer](https://ceworkshops.cloud.looker.com/extensions/marketplace_extension_api_explorer::api-explorer/4.0/methods/ConversationalAnalytics/delete_agent)
   * In Parameters, set `id`: your Agent ID (passed as query param `?id=...`).
   * Click **Run Request** (`204 No Content` or `200 OK`).

---

### 5.2 🐍 Alternatively use this Python Code Snippet: Lab Teardown & Resource Cleanup

If you prefer executing the teardown programmatically, you can run the provided CLI script or use the Python client:

#### Option A: Run the Standalone CLI Teardown Script in Cloud Shell
```bash
cd ~/cymbal_gadgets/agentic_web_app

# Usage: python3 cleanup.py <agent_id> <conversation_id> [golden_query_id] [--clear-creds]
python3 cleanup.py YOUR_AGENT_ID YOUR_CONVERSATION_ID YOUR_GOLDEN_QUERY_ID
```

#### Option B: Using the Python LookerClient Directly
```python
from looker_client import LookerClient

client = LookerClient.from_env()

# Orchestrated 4-step teardown:
results = client.cleanup_lab_resources(
    agent_id="YOUR_AGENT_ID",
    conversation_id="YOUR_CONVERSATION_ID",
    golden_query_id="YOUR_GOLDEN_QUERY_ID"  # Optional if none created
)

print("✅ Cleanup results:")
for step, outcome in results.items():
    print(f"  • {step}: {outcome.get('status')} - {outcome.get('message')}")
```

---

### 5.3 Option C: 1-Click Interactive Teardown in the Web Portal

If you are using the interactive portal (`http://localhost:8080`):
1. Click the **Task 5: Teardown** tab in the navigation bar.
2. Click **Auto-Populate Active Lab IDs** &mdash; the portal automatically populates your active `agent_id`, `conversation_id`, and `golden_query_id`.
3. *(Optional)* Check **Reset Credentials to Workshop Placeholder** if you are finished with the workshop.
4. Click **Run Complete Lab Cleanup**.
5. The portal executes the full 4-step teardown, refreshes the available agents catalog, and confirms cleanup completion with green status indicators.

---

### 🚩 CHECKPOINT 5: Verify Lab Teardown & Resource Cleanup (20 Points)
**Goal:** Confirm that your custom agent and test resources have been safely cleaned up.

* **In the Web App:** Navigate to Task 5: Checkpoint 5 and click **Check my progress** (or click **Run Complete Lab Cleanup** in the 1-click teardown card) to earn your final **+20 points** and reach **100/100 Total Score**! The final completion celebration modal will unlock upon completing Checkpoint 5.
* **Via Automated CLI Check:**
```bash
python3 ~/cymbal_gadgets/agentic_web_app/cleanup.py YOUR_AGENT_ID YOUR_CONVERSATION_ID YOUR_GOLDEN_QUERY_ID
```

---

## 🎓 Summary: Key Takeaways for Data Engineers

1. **The Semantic Layer is Essential for GenAI:** LLMs cannot safely query raw database tables without hallucinating. Looker's LookML layer guarantees that metrics, joins, and filters are deterministic and governed.
2. **API Explorer Accelerates Integration:** The Looker API Explorer enables rapid prototyping and contract verification without external tools.
3. **Conversational State is Managed Server-side:** Looker's `/conversations` endpoint removes the burden of managing multi-turn conversation memory and token budgets in client applications.
4. **Complete Auditability:** The 5-stage response stream (`THOUGHT`, `SCHEMA`, `QUERY`, `DATA`, `FINAL_RESPONSE`) gives Data Engineers complete visibility into how answers are derived.

---

## 🖥️ Presentation Slides & Additional Resources
* **Interactive Presentation Slides:** [Launch Presentation Viewer](http://localhost:8080/presentation.html)
* **Markdown Presentation Deck:** [PRESENTATION_LOOKER_CONVERSATIONAL_ANALYTICS.md](PRESENTATION_LOOKER_CONVERSATIONAL_ANALYTICS.md)
* **Looker API 4.0 Reference:** [Looker Developer Portal](https://developers.looker.com/api/explorer/4.0)
* **LookML Modeling Documentation:** [LookML Concepts](https://cloud.google.com/looker/docs/what-is-lookml)
