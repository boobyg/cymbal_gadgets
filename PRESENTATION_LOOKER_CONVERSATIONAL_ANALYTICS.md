# 📊 Presentation Deck: Looker Conversational Analytics for Data Engineers
**Google Cloud SME Academy &bull; Data & Agentic AI Track**  
*Google Slides (Standard Google Cloud Style):* [Official Slide Deck](https://docs.google.com/presentation/d/1looker-conversational-analytics-standard-gcp-deck/edit?usp=sharing)  
*Companion Interactive Web Presentation:* [http://localhost:8080/presentation.html](http://localhost:8080/presentation.html)  
*Repository:* [https://github.com/boobyg/cymbal_gadgets.git](https://github.com/boobyg/cymbal_gadgets.git)  

---

<!-- slide -->
# Slide 1: Welcome & Course Overview

## Building, Testing & Deploying Custom Conversational Analytics Agents with Looker APIs
### Enterprise Generative BI Grounded in BigQuery

* **Audience:** Data Engineers, Analytics Engineers, Cloud Architects, BigQuery Developers
* **Prerequisites:** Familiarity with SQL, REST APIs, and basic JSON. **Zero prior Looker or LookML experience required!**
* **Duration:** ~30 Minutes
* **Core Technology:** Looker API 4.0 (Conversational Analytics) + Google Cloud BigQuery + Cloud Run
* 📦 **Lab Repository:** Available in GitHub (`https://github.com/boobyg/cymbal_gadgets.git`) to clone and run in your dedicated **Argolis environment** using **Google Cloud Shell**.
* 📊 **Instructor Presentation:** This deck is available as **Google Slides in Standard Google Cloud style** for the instructor to present and referenced in `README.md`.

> **Speaker Notes:**  
> Welcome Data Engineers! In this session, we address one of the most critical challenges in enterprise AI: how to allow business users to ask natural language questions about enterprise data without suffering from SQL hallucinations, metric confusion, and inaccurate reporting. We'll explore Looker's Governed Semantic Layer and how the Conversational Analytics API empowers you to build production-grade AI agents in minutes.

---

<!-- slide -->
# Slide 2: Lab Setup & Argolis Quickstart (Install from Git)

### How to Clone, Configure, and Launch the Lab in Google Cloud Shell

Every student deploys and runs this lab within their own dedicated **Argolis Google Cloud environment**:

1. **Open Google Cloud Shell:**
   * In your Argolis GCP Console ([console.cloud.google.com](https://console.cloud.google.com)), activate Cloud Shell (`>_`).

2. **Clone the Git Repository:**
   ```bash
   git clone https://github.com/boobyg/cymbal_gadgets.git
   cd cymbal_gadgets/agentic_web_app
   ```

3. **Launch the Interactive Web Application:**
   ```bash
   chmod +x run.sh
   ./run.sh
   # (Or run: python3 server.py)
   ```

4. **Access the Dual-Pane Lab Portal:**
   * Click **Web Preview** (top-right of Cloud Shell) &rarr; **Preview on port 8080**.
   * The interactive portal opens in a new browser tab.

5. **Authenticate Looker API Credentials:**
   * Click **Student Credentials** (key icon in top header) and input your assigned Looker Client ID & Secret.

> **Speaker Notes:**  
> Cloud Shell provides an isolated Linux sandbox with Python 3.12, Git, and curl pre-installed. Web Preview on port 8080 provides a secure HTTPS proxy to the web application without requiring firewall or SSH configuration.

---

<!-- slide -->
# Slide 3: The Enterprise Challenge: Why Raw "Text-to-SQL" Fails

### Pointing LLMs Directly at Raw Database Tables Consistently Fails in Production

1. **Schema Hallucination & Confusion**
   * LLMs invent column names, select deprecated staging tables, or misidentify foreign keys.
   * Result: Syntax errors or queries executing against the wrong data sets.

2. **Missing Business Logic**
   * Raw database tables do not encode business rules.
   * *What is "Net Revenue"? Does it deduct returns? What order status counts as completed?*
   * Result: Two different users receive conflicting answers to the same business question.

3. **Join Fanouts & Multiplication Traps**
   * LLMs struggle with complex multi-table joins and many-to-many cardinality.
   * Result: Sales metrics inflated by 5x to 10x with zero warnings.

4. **Zero Auditability & Compliance Risk**
   * When an LLM outputs "$14.2M", data engineers cannot verify the underlying formula or filters.
   * Result: Enterprise compliance teams block production deployment.

> **Speaker Notes:**  
> Every data engineer has seen the hype around "Text-to-SQL". But in enterprise production, accuracy rates hover under 65% when querying raw tables directly. Raw tables lack context, metric definitions, and fanout safeguards.

---

<!-- slide -->
# Slide 4: The Architectural Solution: Looker's Governed Semantic Layer

### Looker as the Ground Truth Between AI Intent and Database Execution

```
Natural Language Prompt  ──►  Looker CA API  ──►  LookML Semantic Layer  ──►  Dialect BigQuery SQL  ──►  Tabular Data & Synthesis
```

* **Centrally Governed Metrics:**
  * Calculations like `gross_margin_percentage` and `total_sales_amount` are defined once in LookML measures.
  * Every AI agent uses the exact same verified formulas.

* **Deterministic SQL Compilation:**
  * The LLM **never writes raw SQL**.
  * The agent generates a formal **LookML Query Specification** (fields, filters, sort orders).
  * Looker's compiler translates this specification into dialect-optimized BigQuery SQL with automated fanout protection.

* **100% Auditable Reasoning:**
  * The API returns the agent's chain of thought, LookML schema evaluated, query specification, and the raw tabular data returned from BigQuery.

> **Speaker Notes:**  
> The core architectural shift is simple but profound: Do not let LLMs write raw SQL. Let LLMs generate semantic requests against Looker's governed layer, and let Looker compile the SQL.

---

<!-- slide -->
# Slide 5: Looker 101 for Data Engineers

### Mapping Looker Concepts to Familiar Data Warehouse & SQL Terms

| Looker Concept | Data Warehouse / SQL Analogy | Cymbal Gadgets Example |
| :--- | :--- | :--- |
| **Model** | Database catalog / schema configuration containing explores sharing a connection. | `cymbal_gadgets_boris` |
| **Explore** | Pre-joined Star Schema or Dimensional Mart (Fact table joined to Dimension tables). | `transactions` (Sales facts joined to store & product dimensions) |
| **View** | Table definition or SQL CTE defining columns, dimensions, and aggregations. | `transactions.view.lkml`, `product_reviews.view.lkml` |
| **Dimension** | Column or attribute used for slicing, filtering, and `GROUP BY`. | `store_country`, `transaction_date`, `product_category` |
| **Measure** | Explicit aggregation formula (`SUM`, `AVG`, `COUNT`, ratios) with built-in business logic. | `total_sales_amount`, `gross_margin_percentage` |
| **API Explorer** | Built-in interactive Swagger/OpenAPI workbench for testing all Looker 4.0 REST endpoints. | Built-in Looker Extension |

> **Speaker Notes:**  
> Data engineers already understand star schemas and dimensional modeling. In Looker, an Explore is simply a pre-configured star schema where the join paths and fanout calculations are already solved.

---

<!-- slide -->
# Slide 6: The Looker Conversational Analytics (CA) API Family

### Core REST Endpoints in Looker API 4.0
*(Follows the official Looker EMEA CE walkthrough video: [youtube.com/watch?v=XyU90O49p8o](https://www.youtube.com/watch?v=XyU90O49p8o))*

* **`POST /api/4.0/login` &mdash; Authentication:**
  * Exchanges `client_id` and `client_secret` for an ephemeral bearer token: `Authorization: token <access_token>`.

* **`POST /api/4.0/agents` &mdash; Agent Definition:**
  * Defines an AI agent, its allowed LookML sources (`model` and `explore`), and system instructions (`context.instructions`).

* **`POST /api/4.0/golden_queries` &mdash; Golden Query Grounding:**
  * Pairs user questions with verified Looker Explore answer URLs. Acts as few-shot training to eliminate metric ambiguity and hallucinations.

* **`GET /api/4.0/agents/search` & `GET /api/4.0/agents/{id}` &mdash; Discovery:**
  * Lists and inspects available agents and their semantic bindings.

* **`PATCH /api/4.0/agents/{id}` &mdash; Dynamic Runtime Tuning:**
  * Modifies agent persona, formatting rules, or explore sources dynamically without redeploying code.

* **`POST /api/4.0/conversations` &mdash; Stateful Sessions:**
  * Allocates a multi-turn conversation thread bound to an agent ID. Looker manages message history and token context server-side!

* **`POST /api/4.0/conversational_analytics/chat` &mdash; Query Execution:**
  * Submits natural language queries and streams back structured thoughts, schema resolution, query specs, and BigQuery data.

> **Speaker Notes:**  
> Notice how complete this API family is: You create an agent, supply golden queries for verified grounding, start a stateful conversation, and call the chat API method. Looker handles all context budgeting, semantic translation, and BigQuery SQL compilation.

---

<!-- slide -->
# Slide 7: Anatomy of the 5-Stage CA Response Stream

### Complete Auditability Inside `POST /conversational_analytics/chat`

When you call `/chat`, Looker returns a multi-part payload containing 5 distinct message phases:

1. **`THOUGHT` &mdash; Chain-of-Thought Reasoning:**
   * Details how the LLM interpreted the user question, what concepts it mapped, and why it selected specific fields.

2. **`SCHEMA` &mdash; Semantic Entities Inspected:**
   * Shows which LookML views, dimensions, and measures were considered during introspection.

3. **`QUERY` &mdash; LookML Query Specification:**
   * The formal dimensional request: `fields: ["transactions.total_sales_amount"]`, `filters: {"transactions.transaction_date": "last 30 days"}`.

4. **`DATA` &mdash; Verified Tabular BigQuery Results:**
   * The exact tabular records returned from BigQuery execution: `[{"transactions.total_sales_amount": 1074890772}]`.

5. **`FINAL_RESPONSE` &mdash; Executive Summary:**
   * Natural language answer formatted according to agent instructions and grounded in the verified data.

> **Speaker Notes:**  
> This 5-stage stream is why enterprise data teams love this architecture. Business users see the final response, while data engineers and compliance auditors can inspect the thoughts, query specs, and raw data rows.

---

<!-- slide -->
# Slide 8: End-to-End Chronological Execution Flow

### How a Natural Language Question Travels Through the System

| Step | Component | Action & Transformation |
| :---: | :--- | :--- |
| **1** | **User / Frontend** | Submits natural language question: *"What is the total sales amount by store country?"* |
| **2** | **Web Client App** | Binds request to existing `conversation_id` and calls `POST /conversational_analytics/chat`. |
| **3** | **Looker CA Engine** | Evaluates Explore `transactions`, selecting dimension `store_country` and measure `total_sales_amount`. |
| **4** | **LookML Compiler** | Converts dimensional specification into optimized Google BigQuery SQL with fanout protection. |
| **5** | **Google BigQuery** | Executes SQL against petabyte-scale warehouse tables and returns tabular result set. |
| **6** | **Looker Agent** | Synthesizes executive summary following custom prompt instructions. |
| **7** | **Client Application** | Renders executive answer + displays audit traces in the Transparency Hub. |

> **Speaker Notes:**  
> Walk the audience through each step. Emphasize that Step 4 and Step 5 are completely deterministic—no guesswork, no hallucinations.

---

<!-- slide -->
# Slide 9: Looker API Explorer & Dual Pathways for Task 1

### Choose Your Preferred Journey: Interactive GUI or Python Code

Students can complete every step of Task 1 using either of **two dual pathways**:

1. 🌐 **Pathway 1: Looker API Explorer (Interactive GUI / Zero Coding)**
   * Built-in developer workbench in Looker: [`ConversationalAnalytics / create_agent`](https://ceworkshops.cloud.looker.com/extensions/marketplace_extension_api_explorer::api-explorer/4.0/methods/ConversationalAnalytics/create_agent)
   * Open the method, click the **Run It** tab, paste the JSON payload, and click **Run Request**.
   * Instant visual feedback using your active Looker browser session!

2. 🐍 **Pathway 2: Python Code Snippets (Programmatic / SDK)**
   * Ready-to-run copy-paste snippets using official `looker_sdk` or zero-dependency `LookerClient`.

### 📌 Where to Paste and Run the Python Code
* **Option A (Fastest & Recommended):** Open an interactive Python terminal in Google Cloud Shell:
  ```bash
  python3
  ```
  Paste the code snippet directly into the Python REPL!
* **Option B (Script File):** Save into a test script inside `cymbal_gadgets/agentic_web_app/` (which already has `config.py` and `looker_client.py`):
  ```bash
  cd ~/cymbal_gadgets/agentic_web_app
  python3 -c "
  import config
  from looker_client import LookerClient
  client = LookerClient(config.LOOKER_BASE_URL, config.LOOKER_CLIENT_ID, config.LOOKER_CLIENT_SECRET)
  # Paste your snippet here
  "
  ```
* **Option C (Jupyter Notebook):** In any Vertex AI Workbench or Jupyter cell, paste the snippet and press `Shift+Enter`.

> **Speaker Notes:**  
> Emphasize to students that both pathways are 100% equivalent. Data engineers who prefer GUI can use API Explorer, while Python developers can paste snippets into Cloud Shell.

---

<!-- slide -->
# Slide 10: Step 0 & Step 1: Agent Creation, Golden Queries & Chat API Flow

### Complete Video Walkthrough Sequence (Looker EMEA CE)
*(Video Companion: [youtube.com/watch?v=XyU90O49p8o](https://www.youtube.com/watch?v=XyU90O49p8o))*

1. **Create Agent (`POST /agents`):** Define semantic grounding (`cymbal_gadgets_boris/transactions`) and instructions.
2. **Golden Query Grounding (`POST /golden_queries`):** Ground agent with verified question-to-Explore URL pairs.
3. **Link Golden Query to Agent (`PATCH /agents/{id}`):** Associate golden query IDs with the agent.
4. **Create Conversation (`POST /conversations`):** Use the new `agent_id` to allocate a stateful conversation thread.
5. **Test Chat API Method (`POST /conversational_analytics/chat`):** Validate the 5-stage stream contract before opening UI.

---

### 1. Create Agent (`POST /api/4.0/agents`)
* 🔗 [Open create_agent in API Explorer](https://ceworkshops.cloud.looker.com/extensions/marketplace_extension_api_explorer::api-explorer/4.0/methods/ConversationalAnalytics/create_agent)
* **Payload:** `{"name": "Cymbal Retail Agent - Student <ID>", "sources": [{"model": "cymbal_gadgets_boris", "explore": "transactions"}], "context": {"instructions": "...", "show_analytical_details": true}}`
* **Python Snippet:**
  ```python
  # looker_sdk
  agent = sdk.create_agent(body=models40.WriteAgent(name="Cymbal Agent", sources=[...], context=...))
  # Zero-dependency LookerClient
  agent = client.create_agent("Cymbal Agent", "cymbal_gadgets_boris", "transactions")
  ```

---

### 2. Supply Golden Query & Link to Agent (`POST /golden_queries` & `PATCH /agents/{id}`)

#### Step 2A: Create Golden Query (`POST /api/4.0/golden_queries`)
* 🔗 [Open create_golden_query in API Explorer](https://ceworkshops.cloud.looker.com/extensions/marketplace_extension_api_explorer::api-explorer/4.0/methods/ConversationalAnalytics/create_golden_query)
* **Payload (Single question strictly required by Looker 4.0 to prevent HTTP 422):**
  ```json
  {
    "questions": ["What is our total sales amount across all transactions?"],
    "answer": "https://ceworkshops.cloud.looker.com/explore/cymbal_gadgets_boris/transactions?fields=transactions.total_sale_price"
  }
  ```
* Click **Run Request** & copy the returned integer `"id"` (e.g. `101`).

#### Step 2B: How to Link Golden Query in API Explorer (`PATCH /api/4.0/agents/{agent_id}`)
* 🔗 [Open update_agent in API Explorer](https://ceworkshops.cloud.looker.com/extensions/marketplace_extension_api_explorer::api-explorer/4.0/methods/ConversationalAnalytics/update_agent)
* **`agent_id` (Path Parameter):** Paste your 32-character Agent ID from Step 1.
* **Request Body (`body`):**
  ```json
  {
    "golden_query_ids": [101]
  }
  ```
  *(replace `101` with your actual Golden Query ID)*
* Click **Run Request** &rarr; returns `PATCH /agents/{id} (200 OK)` confirming linking!

* **Python Equivalent (1-Step):**
  ```python
  gq = client.create_golden_query(questions=["What is our total sales amount across all transactions?"], answer="https://.../explore/...")
  client.update_agent(agent_id, {"golden_query_ids": [gq["id"]]})
  ```

---

### 3. Create Conversation Session (`POST /api/4.0/conversations`)
* 🔗 [Open create_conversation in API Explorer](https://ceworkshops.cloud.looker.com/extensions/marketplace_extension_api_explorer::api-explorer/4.0/methods/ConversationalAnalytics/create_conversation)
* **Payload:** `{"agent_id": "<YOUR_AGENT_ID>", "name": "Cymbal Retail Session"}`
* **Python Snippet:**
  ```python
  conv = client.create_conversation(agent_id=agent_id, name="Cymbal Session")
  print("Conversation ID:", conv["id"])
  ```

---

### 4. Test Chat API Method Before Showing Chat UI (`POST /conversational_analytics/chat`)
* 🔗 [Open conversational_analytics_chat in API Explorer](https://ceworkshops.cloud.looker.com/extensions/marketplace_extension_api_explorer::api-explorer/4.0/methods/ConversationalAnalytics/conversational_analytics_chat)
* **Payload:** `{"conversation_id": "<CONVERSATION_ID>", "user_message": "What is our total sales amount?"}`
* **Python Snippet:**
  ```python
  # Stream returns: THOUGHT, SCHEMA, QUERY, DATA, FINAL_RESPONSE
  result = client.chat(conversation_id=conv["id"], user_message="What is our total sales?")
  print("Query Spec:", result["query"], "Data:", result["data"])
  ```

> **Speaker Notes:**  
> This slide mirrors the exact video walkthrough: students create the agent, anchor it with a golden query example, link the query via update_agent, initialize a stateful conversation thread, and test the raw Chat API method to inspect the 5-stage stream contract before launching the web UI.

---

<!-- slide -->
# Slide 11: Step 2: Web Client Architecture & Health Check

### Running the Python Client in Dedicated Argolis Cloud Shell

```bash
# Launch the client application (port 8080)
cd /home/user/cymbal_gadgets/agentic_web_app
./run.sh
```

### ⚠️ Where to Execute Health Verification
* **Option A (Recommended & Fastest):** In the Web UI (`http://localhost:8080`), click the green **Check my progress** button under Task 2 (**+25 Points**).
* **Option B (Terminal curl):** Open a **SECOND terminal tab** (`+`) in Cloud Shell and run:
  ```bash
  curl -s http://localhost:8080/api/health | jq .
  ```
* ❌ **Do NOT run curl on your local laptop** (port 8080 is remote in Cloud Shell).
* ❌ **Do NOT curl external `https://*.cloudshell.dev` URLs** (they return HTML login pages).

### 🚀 Display Conversational Analytics Window (End of Step 2)
* Once **Checkpoint 1 (Create Agent)** and **Checkpoint 2 (Health Check)** are completed, the **"Display Conversational Analytics Window"** button unlocks at the end of Step 2!
* Click it to display the live interactive chat window on the right side of your screen before proceeding to Step 3.

> **Speaker Notes:**  
> Make sure students click "Display Conversational Analytics Window" at the end of Step 2 so they can clearly see the chat console, the active agent selector, and the prompt input field before starting Step 3.

---

<!-- slide -->
# Slide 12: Step 3: Interactive Prompting & Audit Real-Time Tracing

### 🔍 Audit the Three Execution Tracing Accordions
When prompts execute, the Looker Conversational Analytics API returns a rich multi-stage stream. **Students must expand and inspect each accordion below the agent's answer:**
1. **🧠 Agent Thought Process:** Step-by-step reasoning tokens showing user intent resolution, explore discovery, and metric selection (revealing *why* specific metrics were chosen).
2. **📊 Governed Data Result:** The raw tabular BigQuery records (verifying the **$1.07B** total sales volume) before narrative generation.
3. **💻 Generated Looker Query Specification:** The formal LookML dimensions, measures (`transactions.total_sale_price`), and filters generated by Looker—proving zero raw SQL hallucination!

### Sample Prompts to Test:
1. *Metric Aggregation:* "What is our total sales amount across all stores?"
2. *Dimensional Slicing:* "Show average transaction amount by store country."
3. *Top-N Ranking:* "Which 5 products have the highest gross margin percentage?"
4. *Multi-turn Follow-up:* "Which store country had the highest volume?" (Notice stateful memory!)

> **Speaker Notes:**  
> Direct the students' attention to the 3 collapsible accordions beneath every answer: Agent Thought Process, Governed Data Result, and Generated Looker Query Specification. These prove to data engineers that enterprise governance is active.

---

<!-- slide -->
# Slide 13: Step 4: Where & How Guardrails Are Applied in Conversational Analytics (CA) APIs

### Enterprise AI Governance Architecture

Data engineers must understand both the configuration points (**WHERE**) and enforcement mechanics (**HOW**) in CA APIs:

```
┌────────────────────────────────────────────────────────┐
│ WHERE Guardrails Are Applied in CA APIs:               │
│ 1. context.instructions (POST /agents & PATCH /agents) │
│ 2. sources whitelist: [{"model": "...", "explore":...}]│
│ 3. LookML Modeling Layer (hidden fields, access grants)│
└──────────────────────────┬─────────────────────────────┘
                           │ Enforced by Looker CA Engine
┌──────────────────────────▼─────────────────────────────┐
│ HOW Guardrails Are Enforced by CA Engine:              │
│ 1. System Prompt Priming (injected into Gemini context)│
│ 2. Metric Steering ("Always use gross margin %")       │
│ 3. Deterministic LookML Query Spec (No SQL Injection)  │
│ 4. Output Persona & Formatting ('🌟 Cymbal Executive') │
└────────────────────────────────────────────────────────┘
```

### Dynamic Instruction Tuning (`PATCH /api/4.0/agents/{agent_id}`)
```python
# Option A: Looker Python SDK (looker_sdk)
sdk.update_agent(
    agent_id=agent_id,
    body=models40.WriteAgent(
        context=models40.AgentContext(
            instructions="- Always begin your answer with '🌟 Cymbal Executive Summary:'...",
            show_analytical_details=True
        )
    )
)

# Option B: Zero-Dependency LookerClient
client.update_agent(agent_id, {
    "context": {
        "instructions": "- Always begin your answer with '🌟 Cymbal Executive Summary:'...",
        "show_analytical_details": True
    }
})
```

* **Zero Downtime:** Changes take effect immediately on the next prompt.
* **Assessment Checkpoint 4:** Click **Check my progress** to reach **100/100 Total Score**!

> **Speaker Notes:**  
> Emphasize that guardrails in Looker CA APIs exist at two levels: in the semantic layer (LookML) and in the API configuration (context.instructions & sources whitelist). The LLM never writes raw SQL directly to the database.

---

<!-- slide -->
# Slide 14: Google Cloud Serverless Production Architecture

### Production-Grade Enterprise Deployment Pattern

1. **Google Cloud Run (Stateless Microservice):**
   * Containerized Python/FastAPI client built on `python:3.12-slim`.
   * Autoscales from 0 to 1,000+ instances based on traffic spikes.

2. **Google Cloud Secret Manager (GSM):**
   * Securely manages `LOOKER_CLIENT_ID` and `LOOKER_CLIENT_SECRET`.
   * Mounted into Cloud Run via IAM service account permissions. Zero hardcoded secrets!

3. **Google Cloud Armor & Identity-Aware Proxy (IAP):**
   * Enforces Google Workspace enterprise SSO and zero-trust authentication.
   * Provides DDoS mitigation and rate-limiting at the Google edge.

4. **Google Cloud BigQuery:**
   * Enterprise data warehouse executing compiled SQL with BI Engine caching.

> **Speaker Notes:**  
> Explain that the lab includes a ready-to-run `./deploy_cloud_run.sh` script and `Dockerfile` so students can deploy this exact pattern into their own GCP projects.

---

<!-- slide -->
# Slide 15: Key Takeaways & Best Practices for Data Engineers

### Summary Checklist for Building Enterprise Conversational Data Platforms

1. ✅ **Never Allow LLMs to Generate Ungoverned SQL:**
   * Always ground conversational AI in a semantic layer (LookML) to guarantee metric integrity.

2. ✅ **Leverage API Explorer for Rapid Prototyping:**
   * Inspect contracts and test payloads in-browser before writing client code.

3. ✅ **Offload Conversation State to Looker:**
   * Use `POST /conversations` so Looker handles multi-turn context and token budgeting server-side.

4. ✅ **Expose Transparency to Build User Trust:**
   * Implement a Transparency Hub showing thoughts, queries, and raw data rows to satisfy both executive and analytical stakeholders.

5. ✅ **Use Dynamic Patching for Agile Governance:**
   * Update system instructions via `PATCH /agents/{id}` to tune persona rules without code releases.

---

### 🎉 Congratulations on Completing the SME Academy Lab!
* **Portal Link:** [http://localhost:8080](http://localhost:8080)
* **Presentation Slides:** [http://localhost:8080/presentation.html](http://localhost:8080/presentation.html)
