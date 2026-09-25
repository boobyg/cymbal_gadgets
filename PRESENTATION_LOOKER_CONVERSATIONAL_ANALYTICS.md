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
# Slide 2: The Enterprise Challenge: Why Raw "Text-to-SQL" Fails

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
# Slide 3: The Architectural Solution: Looker's Governed Semantic Layer

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
# Slide 4: Looker 101 for Data Engineers

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
# Slide 5: The Looker Conversational Analytics (CA) API Family

### Core REST Endpoints in Looker API 4.0

* **`POST /api/4.0/login` &mdash; Authentication:**
  * Exchanges `client_id` and `client_secret` for an ephemeral bearer token: `Authorization: token <access_token>`.

* **`POST /api/4.0/agents` &mdash; Agent Definition:**
  * Defines an AI agent, its allowed LookML sources (`model` and `explore`), and system instructions (`context.instructions`).

* **`GET /api/4.0/agents/search` & `GET /api/4.0/agents/{id}` &mdash; Discovery:**
  * Lists and inspects available agents and their semantic bindings.

* **`PATCH /api/4.0/agents/{id}` &mdash; Dynamic Runtime Tuning:**
  * Modifies agent persona, formatting rules, or explore sources dynamically without redeploying code.

* **`POST /api/4.0/conversations` &mdash; Stateful Sessions:**
  * Allocates a multi-turn conversation thread bound to an agent. Looker manages message history and token context server-side!

* **`POST /api/4.0/conversational_analytics/chat` &mdash; Query Execution:**
  * Submits natural language queries and streams back structured thoughts, schema resolution, query specs, and BigQuery data.

> **Speaker Notes:**  
> Notice how clean this API family is: You create an agent, start a conversation, and send chat prompts. Looker handles the heavy lifting of context management and semantic routing.

---

<!-- slide -->
# Slide 6: Anatomy of the 5-Stage CA Response Stream

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
# Slide 7: End-to-End Chronological Execution Flow

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
# Slide 8: Looker API Explorer: Built-in Developer Workbench

### Interactive API Discovery & In-Browser Execution

* **What is API Explorer?**
  * Looker's built-in developer workbench (similar to Swagger/OpenAPI).
  * Direct method link: [`ConversationalAnalytics / create_agent`](https://ceworkshops.cloud.looker.com/extensions/marketplace_extension_api_explorer::api-explorer/4.0/methods/ConversationalAnalytics/create_agent)

* **Key Features for Data Engineers:**
  * **Interactive Testing ("Run It"):** Test requests directly in your browser without writing curl or Python scripts.
  * **Zero-Setup Authentication:** Uses your active browser session automatically.
  * **Multi-Language Code Generation:** Automatically generates client code snippets in Python, TypeScript, Kotlin, and Swift.
  * **Looker API 4.0 Selection:** Switch between API versions and search endpoints instantly.

> **Speaker Notes:**  
> In Task 1, students navigate directly to the `create_agent` method in API Explorer. It provides an immediate visual feedback loop for testing the API contract before touching code.

---

<!-- slide -->
# Slide 9: Step 0 & Step 1: Authentication & Creating Your Custom Agent

### Typical 3-Step Lifecycle Scenario
1. **Create Agent (`CreateAgent`):** Define semantic grounding (`cymbal_gadgets_boris/transactions`) and instructions.
2. **Create Conversation (`POST /conversations`):** Looker allocates a server-side stateful conversation thread.
3. **Pass Prompt & Query (`POST /conversational_analytics/chat`):** Looker compiles BigQuery SQL and streams back data + **5-stage tracing**.

### Step 1 Step-by-Step: Run `CreateAgent` in API Explorer
* 🔗 **Direct URL:** [create_agent method](https://ceworkshops.cloud.looker.com/extensions/marketplace_extension_api_explorer::api-explorer/4.0/methods/ConversationalAnalytics/create_agent)
* **Where to Paste Payload:** Click the **Run It** tab &rarr; scroll to the **Request Body (`body`)** editor textarea.
* **Paste JSON Payload:**
  ```json
  {
    "name": "Cymbal Retail Analytics Agent - Student <YOUR_ID>",
    "description": "Conversational BI agent providing governed retail insights",
    "sources": [{"model": "cymbal_gadgets_boris", "explore": "transactions"}],
    "context": {
      "instructions": "Always use Gross Margin Percentage when asked about profitability. Format numbers clearly.",
      "show_analytical_details": true
    }
  }
  ```
* **Click:** **Run Request** button.
* **Expected Output:** Status **`POST /agents (200: OK)`** (or `201: Created`).
* **Where to Find the Newly Created Agent ID:** Top line of response JSON: `"id": "a9b6933c..."`. Copy this 32-character ID!
* 💡 **Tracing in the App:** Setting `show_analytical_details: true` ensures that **full tracing will be available in the application when prompts are run**!

> **Speaker Notes:**  
> Emphasize where to paste the payload in the `body` field of the Run It tab. Point out the `200: OK` response and the `"id"` line. Remind students that the full execution tracing will be visible in the web app during Step 3.

---

<!-- slide -->
# Slide 10: Step 2: Web Client Architecture & Health Check

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
# Slide 11: Step 3: Interactive Prompting & Audit Real-Time Tracing

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
# Slide 12: Step 4: Where & How Guardrails Are Applied in Conversational Analytics (CA) APIs

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
# Dynamically patch agent instructions at runtime
client._request("PATCH", f"/agents/{agent_id}", payload={
    "context": {
        "instructions": """
        - Always begin your answer with '🌟 Cymbal Executive Summary:'
        - Format all currency metrics in EUR with thousands separators
        - Always state gross margin percentages with two decimals
        - Keep explanations under 3 sentences
        """,
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
# Slide 13: Google Cloud Serverless Production Architecture

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
# Slide 14: Key Takeaways & Best Practices for Data Engineers

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
