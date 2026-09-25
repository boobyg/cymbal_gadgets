# 🎓 SME Academy Lab: Building, Testing & Deploying Custom Conversational Analytics Agents with Looker APIs

**Audience:** Data Engineers, Analytics Engineers, Cloud Architects, and BigQuery Developers  
**Prerequisites:** Familiarity with SQL, REST APIs, and basic JSON. **Zero prior Looker or LookML experience required!**  
**Duration:** ~30 Minutes  
**Track:** Google Cloud SME Academy &bull; Agentic & Data Analytics Track  
**Companion Presentations:** [Google Slides (Standard Google Cloud Style)](https://docs.google.com/presentation/d/1looker-conversational-analytics-standard-gcp-deck/edit?usp=sharing) | [Interactive Presentation Slides](http://localhost:8080/presentation.html) | [Markdown Presentation Deck](PRESENTATION_LOOKER_CONVERSATIONAL_ANALYTICS.md)  

> [!WARNING] The complete lab and application are available in the GitHub repository (`https://github.com/boobyg/cymbal_gadgets.git`) for students to clone and run in their own dedicated **Argolis environment** (using **Google Cloud Shell** in their assigned Argolis GCP project).
>

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
| **Phase 1** | **API Explorer & Agent Creation** | Master the Looker API Explorer developer workbench; create your custom agent (`POST /agents`) bound to `cymbal_gadgets_boris`. | Looker API Explorer (Web UI) |
| **Phase 2** | **Web Client Deployment** | Launch the Python web client in your dedicated Argolis Cloud Shell; execute automated health checks. | Cloud Shell Terminal / Web Preview |
| **Phase 3** | **Interactive Queries & Tracing** | Submit natural language queries and audit the 5-stage agent response lifecycle (`THOUGHT`, `SCHEMA`, `QUERY`, `DATA`, `FINAL_RESPONSE`). | Web App Dual-Pane Console |
| **Phase 4** | **Prompt Tuning & Productionizing** | Dynamically update agent guardrails using `PATCH /agents/{id}`; review Google Cloud Run serverless deployment architecture. | REST API / Cloud Run Architecture |

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
2. **Session Initialization:** The client calls `POST /api/4.0/conversations` with `{ "agent_id": "<your_agent_id>" }`. Looker allocates a server-side session `conversation_id`, managing all conversation history and token context automatically.
3. **Chat Prompt:** The client posts a question to `POST /api/4.0/conversational_analytics/chat`.
4. **Schema Introspection:** The Looker agent searches the designated LookML explore (`transactions`) to identify relevant dimensions and measures matching the user's intent.
5. **Deterministic SQL Compilation:** Looker compiles the formal query parameters into optimized, dialect-specific Google Cloud BigQuery SQL.
6. **BigQuery Execution:** The query executes directly in BigQuery.
7. **Synthesis & Audit Stream:** The API returns a multi-part JSON response containing the agent's chain of thought, the LookML query spec, the raw tabular result rows, and a formatted natural language summary.

---

## 🛠️ Major Functions & Endpoints of the CA API

The Conversational Analytics API family consists of the following primary endpoints:

| Endpoint | Method | Function & Purpose |
| :--- | :---: | :--- |
| `/api/4.0/login` | `POST` | Authenticates with `client_id` and `client_secret`, returning an `access_token`. |
| `/api/4.0/agents` | `POST` | **Create Agent**: Defines agent name, description, semantic sources (model/explore), and prompt instructions. |
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
| **Step 1** | API Explorer & Create Custom Agent | 10 mins | Create uniquely-named agent via `POST /agents` | 25 pts |
| **Step 2** | Launch Web App & Verify Health | 5 mins | Launch Python client; verify health via terminal or UI | 25 pts |
| **Step 3** | Interactive Queries & Tracing | 10 mins | Submit multi-turn queries; audit 5-stage response lifecycle | 25 pts |
| **Step 4** | Prompt Tuning & Cloud Run Architecture | 5 mins | Patch guardrails via `PATCH /agents/{id}`; review deployment | 25 pts |
| **Total** | | **30 mins** | **Complete All 4 Checkpoints** | **100 pts** |

---

## 🛠️ Mandatory Environment: Deploy in Your Own Argolis Project

> [!IMPORTANT]
> **Every student MUST deploy and run this lab within their own dedicated Google Cloud Argolis environment** (e.g. using **Google Cloud Shell** in your personal Argolis GCP project).  
> **Why?**
> 1. **Complete Isolation:** Prevents local port collisions (`8080`) and conflicting session state across concurrent students.
> 2. **Credential Privacy:** Keeps your Looker API credentials securely stored inside your private GCP sandbox.
> 3. **Built-in Web Preview:** Cloud Shell provides an instant, secure HTTPS proxy to preview port 8080 without requiring firewall rules or SSH port forwarding.
> 4. **Zero Local Dependencies:** All tools (Python 3, Git, curl, jq) are pre-installed in Cloud Shell.

* **Looker Instance Base URL:** `https://ceworkshops.cloud.looker.com`
* **LookML Model:** `cymbal_gadgets_boris`
* **LookML Explore:** `transactions` (Cymbal Gadgets Retail Sales & Transactions)
* **API Credentials:** Assigned to you by the instructor (Client ID & Client Secret)
* **Git Repository:** `https://github.com/boobyg/cymbal_gadgets.git` (Public repository; no password required)
* **Web Application Port:** `8080` (accessible via Cloud Shell Web Preview)

---

# 📥 Getting Started: Clone & Launch in Argolis Cloud Shell

### Step A: Open Cloud Shell in your Argolis Project
1. Open the Google Cloud Console: [console.cloud.google.com](https://console.cloud.google.com).
2. Ensure your active project is your assigned **Argolis project**.
3. Click the **Activate Cloud Shell** icon (`>_`) in the top navigation bar.

### Step B: Clone the Repository & Launch App
In your Cloud Shell terminal:
```bash
# 1. Clone the public repository
git clone https://github.com/boobyg/cymbal_gadgets.git

# 2. Navigate to the web application directory
cd cymbal_gadgets/agentic_web_app

# 3. Start the web server (initializes environment and runs on port 8080)
./run.sh
```

### Step C: Open the Interactive Lab Portal
In Google Cloud Shell:
1. Click the **Web Preview** icon in the upper-right corner of the Cloud Shell toolbar.
2. Select **Preview on port 8080**.
3. The interactive training portal will open in a new browser tab!

---

# 🔑 Step 0: Student Credentials Setup (3 Mins)

Every student must authenticate using their assigned Looker API credentials (`client_id` and `client_secret`) provided by the workshop instructor.

### 🧹 Ensuring Fresh Credentials
Previous test credentials have been cleared from `.env` and the application to ensure every student begins with a clean slate. You will see the yellow prompt: **"Specify your own user id / secret"**.

### Option A: Configure in the Interactive Web Portal (Recommended)
1. In the opened portal (`http://localhost:8080`), click the yellow **Student Credentials** button in the top navigation bar (or wait for the prompt modal).
2. Enter your assigned:
   * **Looker Client ID:** *(enter your assigned client ID)*
   * **Looker Client Secret:** *(enter your assigned client secret)*
3. Click **Save & Test Connection**.
4. The portal authenticates against Looker API 4.0 and displays a green badge: `Looker Connected`.

> 💡 **Clearing Credentials:** If you ever need to clear or re-enter credentials, open the dialog and click **Clear Saved Credentials** to wipe all stored values.

### Option B: Configure via Terminal (`.env`)
If you prefer configuring credentials in the command line:
```bash
cd /home/user/cymbal_gadgets/agentic_web_app
nano .env
```
Update the lines:
```env
LOOKER_CLIENT_ID=your_assigned_client_id
LOOKER_CLIENT_SECRET=your_assigned_client_secret
```
Save and exit (`Ctrl+O`, `Enter`, `Ctrl+X`).

---

# 🚀 Step 1: Conversational Analytics API & Creating Your Custom Agent (10 Mins)

### 1.1 The Typical Conversational Analytics Lifecycle Scenario
In production applications, interacting with Looker's Conversational Analytics API follows a 3-step sequence:
1. **Create an Agent (`CreateAgent` / `POST /api/4.0/agents`):**  
   You configure an agent bounded to Looker's semantic layer (specifying the model `cymbal_gadgets_boris` and explore `transactions`), establish business rules, and enable analytical details (`show_analytical_details: true`).
2. **Create a Conversation Session (`POST /api/4.0/conversations`):**  
   The application initializes a stateful multi-turn conversation thread associated with your `agent_id`. Looker allocates a server-side `conversation_id`, managing token budgeting and chat history automatically.
3. **Pass a Prompt & Query (`POST /api/4.0/conversational_analytics/chat`):**  
   The user sends a business prompt (e.g., *"What is total sales amount by store country?"*). The API introspects the Explore, generates deterministic BigQuery SQL, executes it, and returns verified tabular data alongside a complete **5-stage reasoning trace** (`THOUGHT`, `SCHEMA`, `QUERY`, `DATA`, `FINAL_RESPONSE`).

> 💡 **What We Are Doing in This Step & Tracing in the App:**  
> In this step, you will create your dedicated agent with `show_analytical_details: true`. This setting is critical because **the tracing will be available in the application when the prompt is run**! In Step 3, when you submit queries through the web app, you will be able to inspect each stage of the agent's internal thought process, the LookML query spec, and the raw BigQuery data rows in real-time.

---

### 1.2 Accessing the `CreateAgent` Method in API Explorer
👉 **Direct Link:** **[CreateAgent Method in API Explorer](https://ceworkshops.cloud.looker.com/extensions/marketplace_extension_api_explorer::api-explorer/4.0/methods/ConversationalAnalytics/create_agent)**

Clicking the direct link will take you directly to the `CreateAgent` method under the `ConversationalAnalytics` namespace in Looker API Explorer.

*(If navigating manually: In Looker, click **Applications > API Explorer**, ensure **Looker API 4.0** is selected in the top-right dropdown, search for `create_agent` or navigate to `ConversationalAnalytics > create_agent`).*

---

### 1.3 Step-by-Step: How to Run `CreateAgent` in Conversational Analytics API

> ⚡ **Multi-Student Naming Rule (500 Concurrent Students):**  
> Because students share the workshop Looker instance, **you MUST provide a unique name** for your agent (e.g. appending your name, initials, or student ID, such as `Student 42`). This ensures you can easily find and query your agent!

1. **Open the "Run It" Tab:**  
   In the API Explorer view for `create_agent`, click on the **Run It** tab located on the right side of the screen.

2. **Where to Paste the JSON Payload:**  
   Scroll down to the **Request Body** editor field (labeled `body`).  
   Click inside the `body` textarea, delete any existing braces or sample placeholder text, and paste the following JSON payload:

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
*(Replace `<YOUR_NAME_OR_ID>` with your unique identifier, e.g. `Student 42`).*

#### Detailed Explanation of What We Are Doing:
* **`name`**: Unique display name for identifying your agent among peers.
* **`sources`**: Semantic grounding. Confines the agent strictly to `cymbal_gadgets_boris/transactions`. The agent cannot touch any other explores or tables.
* **`context.instructions`**: Business guardrails that eliminate metric hallucinations (e.g. mapping "profitability" strictly to `Gross Margin Percentage`).
* **`show_analytical_details: true`**: Tells Looker to expose full reasoning traces. This ensures that **tracing will be available in the application when the prompt is run**!

3. **Execute the Request:**  
   Click the blue **Run Request** button.

4. **What to Expect as an Output:**  
   Inspect the **Response** section below the Run button:  
   * **Status:** You should see **`POST /agents (200: OK)`** (or `201: Created`).  
   * **Response Body:** A JSON representation of your created agent:
     ```json
     {
       "id": "a9b6933c74a045de9ed130ad024cca62",
       "name": "Cymbal Retail Analytics Agent - Student 42",
       "sources": [
         {
           "model": "cymbal_gadgets_boris",
           "explore": "transactions"
         }
       ],
       "created_at": "2026-09-23T15:30:00.000Z"
     }
     ```

5. **Where to Find the Newly Created Agent ID:**  
   In the response JSON output, look at the very top line for the **`"id"`** property:  
   `"id": "a9b6933c74a045de9ed130ad024cca62"`  
   **Copy this 32-character hexadecimal string!** You will need this Agent ID to verify Checkpoint 1, configure the web app, and verify queries in Step 3.

---

### 🚩 CHECKPOINT 1: Verify Agent Creation (25 Points)
**Goal:** Confirm your agent exists and is queryable on the Looker instance.

* **In the Web App:** Navigate to `http://localhost:8080`, enter your generated **Agent ID** into the **Task 1** checkpoint field, and click **Check my progress** to earn **+25 points**!
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

In your workspace under `/home/user/cymbal_gadgets/agentic_web_app`, a complete data engineering client application has been pre-created.

### 2.1 Codebase Structure
* **`looker_client.py`**: Zero-dependency Python client implementing Looker 4.0 token caching, agent discovery, conversation management, and response stream parsing.
* **`server.py`**: Multi-threaded Python HTTP REST API server and static host for the Single-Page Application.
* **`static/index.html`**: Dual-pane training portal with the Transparency Hub and Assessment Tracker.
* **`static/presentation.html`**: Interactive, standalone presentation slide deck for the lab.
* **`test_pipeline.py`**: Automated CLI verification script.
* **`run.sh`**: One-click startup script.

### 2.2 Starting the Web Server
If not already running, execute:
```bash
cd /home/user/cymbal_gadgets/agentic_web_app
./run.sh
```

---

### 🚩 CHECKPOINT 2: Verify Web Server Health (25 Points)
**Goal:** Confirm the web server is running and authenticated to Looker.

#### ❓ Crucial Instruction: Where to Execute Health Verification
1. **Option A (Fastest - Recommended): Use the Web UI Button**  
   In the web portal (`http://localhost:8080`), scroll to **Task 2: Checkpoint 2** and click **Check my progress**. The app automatically verifies health and awards **+25 points**!
2. **Option B: Run curl in a SECOND Terminal Tab in Cloud Shell**  
   * Open a **second terminal tab** (`+` icon in Cloud Shell).
   * **Do NOT run in the first terminal** (it is busy running `./run.sh`).
   * **Do NOT run on your local laptop** (`localhost:8080` exists in remote Cloud Shell).
   * **Do NOT curl external `https://*.cloudshell.dev` URLs** (they return HTML login pages).
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

### 🚩 CHECKPOINT 3: Verify Interactive Query Flow (25 Points)
**Goal:** Confirm the complete natural language-to-BigQuery execution pipeline.

* **In the Web App:** Enter your Step 1 `agent_id` into the **Task 3** checkpoint field and click **Check my progress** to earn **+25 points**!
* **Via Automated CLI Script:**
```bash
python3 /home/user/cymbal_gadgets/agentic_web_app/test_pipeline.py YOUR_STEP_1_AGENT_ID
```

---

# 🛡️ Step 4: Agent Instruction Tuning & Production Deployment (5 Mins)

### 4.1 Tuning Agent Behavior (`PATCH /api/4.0/agents/{agent_id}`)
Data engineers often need to enforce strict formatting, output length, or business terminology. You can update agent behavior on the fly using `PATCH /agents/{agent_id}`.

In Cloud Shell, update your agent's instructions:
```bash
python3 -c "
import urllib.request, json, sys
sys.path.append('/home/user/cymbal_gadgets/agentic_web_app')
import config
from looker_client import LookerClient

client = LookerClient(config.LOOKER_BASE_URL, config.LOOKER_CLIENT_ID, config.LOOKER_CLIENT_SECRET)
agent_id = 'YOUR_AGENT_ID'  # Replace with your Step 1 Agent ID

new_instructions = '''
- Always begin your answer with '🌟 Cymbal Executive Summary:'
- Format all currency metrics in EUR with thousands separators (e.g. €1,234,567)
- If asked about gross margin, always state the exact percentage with two decimals
- Keep explanations under 3 sentences
'''

updated = client._request('PATCH', f'/agents/{agent_id}', payload={
    'context': {'instructions': new_instructions, 'show_analytical_details': True}
})
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

### 🚩 CHECKPOINT 4: Lab Wrap-Up & Scoring (25 Points)
In the interactive portal, click the **Check my progress** button under Task 4 to earn your final **+25 points** (100/100 Total Score)!

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
