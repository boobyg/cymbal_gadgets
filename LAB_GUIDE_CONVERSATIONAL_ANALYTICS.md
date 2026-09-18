# 🎓 SME Academy Lab: Building, Testing & Deploying Custom Conversational Analytics Agents with Looker APIs

**Audience:** Data Engineers, Analytics Engineers, Cloud Architects  
**Prerequisites:** Basic knowledge of SQL, REST APIs, and Python. No prior Looker experience required!  
**Duration:** ~30 Minutes  
**Track:** Google Cloud SME Academy &bull; Agentic & Data Analytics Track  

---

## 🧭 Executive Summary & Architecture

Modern enterprise generative AI applications fail when they hallucinate metrics or query raw database tables without understanding complex business logic (e.g. how gross margin is computed, which order status counts as completed, or how joins must be deduplicated).

**Looker Conversational Analytics APIs** bridge Generative AI with Looker's **Governed Semantic Layer**:
1. **The Semantic Layer is Ground Truth**: The LLM queries Looker Explores (`model` + `explore`), where dimensions, measures, and joins are formally defined and governed in LookML.
2. **Deterministic SQL Generation**: The agent converts natural language into governed Looker queries, which Looker compiles into dialect-optimized BigQuery SQL.
3. **Auditable Chain of Thought**: The API returns full visibility into the agent's reasoning, schema introspection, generated query filters, and raw data tables.

```
┌─────────────────────────────────┐
│   End User / Web Application    │
└────────────────┬────────────────┘
                 │ 1. Natural Language Prompt
                 ▼
┌─────────────────────────────────┐
│   Looker Conversational API     │  POST /conversational_analytics/chat
│   (Agent Context & Reasoning)   │
└────────────────┬────────────────┘
                 │ 2. Schema Discovery & Governed LookML Resolution
                 ▼
┌─────────────────────────────────┐
│     Looker Semantic Layer       │  model: cymbal_gadgets_boris
│   (Dimensions, Measures, Joins) │  explore: transactions
└────────────────┬────────────────┘
                 │ 3. Dialect-Optimized SQL Query
                 ▼
┌─────────────────────────────────┐
│      Google Cloud BigQuery      │  High-Performance Cloud Data Warehouse
└─────────────────────────────────┘
```

---

## ⏱️ Lab Agenda & Timeline (30 Minutes)

| Step | Topic | Duration | Key Deliverable |
| :--- | :--- | :--- | :--- |
| **Step 0** | Student Credentials Setup | 3 mins | Configure and verify your assigned Looker API credentials |
| **Step 1** | Looker API Explorer & Create Agent | 10 mins | First Custom Conversational Agent created via API |
| **Step 2** | Pre-Created Web Application Setup | 5 mins | Launch and verify local full-stack agent app |
| **Step 3** | Consuming API Endpoints in Web App | 10 mins | Live conversational session, query tracing, & data audits |
| **Step 4** | Prompt Tuning, Guardrails & Deployment | 5 mins | Agent instruction updates & Cloud Run production deployment |

---

## 🛠️ Lab Prerequisites & Mandatory Argolis Environment

> [!IMPORTANT]
> **MANDATORY: Deploy & Run in Your Own Argolis Environment**  
> Every student **MUST deploy and run this lab within their own dedicated Google Cloud Argolis environment** (e.g. using **Google Cloud Shell** or **Cloud Workstations** in your personal Argolis project).  
> **Why?**
> 1. **Complete Isolation**: Prevents local port collisions (`8080`), file permission conflicts, and environment variable overwrites across concurrent students.
> 2. **Credential Privacy**: Keeps your personal Looker API credentials securely stored inside your private GCP tenant.
> 3. **Built-in Web Preview**: Argolis Cloud Shell and Cloud Workstations provide instant, authenticated HTTPS web preview proxies to port 8080 without requiring firewall adjustments or local laptop configuration.
> 4. **Zero Local Dependencies**: All scripts run directly in the cloud container—no local Python or Git installation required on your laptop.

* **Looker Instance Base URL:** `https://ceworkshops.cloud.looker.com`
* **LookML Model:** `cymbal_gadgets_boris`
* **LookML Explore:** `transactions` (Cymbal Gadgets Retail Sales & Transactions)
* **API Credentials:** specify your own user id / secret (provided to you before the lab)
* **Git Repository:** `https://github.com/boobyg/cymbal_gadgets.git` (public repository, no password needed)
* **Web Application Port:** `8080` (accessible via Cloud Shell Web Preview)

---

# 📥 Deploying the Lab from Git in Your Argolis Environment

### Step A: Open Cloud Shell in your Argolis Project
1. Log into the Google Cloud Console ([console.cloud.google.com](https://console.cloud.google.com)) and switch to your **Argolis project**.
2. Click the **Activate Cloud Shell** icon (`>_`) in the top navigation bar.

### Step B: Clone the Repository & Launch App
```bash
# 1. Clone the public repository into your Argolis Cloud Shell home
git clone https://github.com/boobyg/cymbal_gadgets.git
cd cymbal_gadgets/agentic_web_app

# 2. Start the web server (automatically prepares .env and sets up server)
./run.sh
```

### Step C: Open the Interactive Lab Portal
In Google Cloud Shell:
1. Click the **Web Preview** button in the upper-right corner of the Cloud Shell toolbar.
2. Select **Preview on port 8080**.
3. Your interactive SkillLabs training portal will open in a new browser tab!

---

# 🔑 Step 0: Student Credentials Setup (3 Mins)

Before beginning the lab, every student must configure their personal Looker API credentials (`client_id` and `client_secret`) provided by the workshop instructor before the lab.

### Option A: Configure in the Interactive SkillLabs Application (Recommended)
1. Open the interactive lab portal in your browser:
   ```text
   http://localhost:8080
   ```
   *(or the Cloud Workstations port 8080 preview URL)*
2. In the top navigation bar, click on **Student Credentials** (or wait for the initial prompt dialog: **"specify your own user id / secret"**).
3. Enter your assigned:
   * **Client ID:** `specify your own user id / secret`
   * **Client Secret:** `specify your own user id / secret`
4. Click **Save & Test Connection**. The portal will authenticate with Looker API 4.0 and display a green connection status badge.

### Option B: Configure via the Command Line (`.env`)
If you prefer configuring credentials in the terminal:
1. Open the `.env` file in the web app directory:
   ```bash
   cd /home/user/cymbal_gadgets/agentic_web_app
   nano .env
   ```
2. Update the credentials using your assigned keys:
   ```env
   # Prompt: specify your own user id / secret
   LOOKER_CLIENT_ID=specify your own user id / secret
   LOOKER_CLIENT_SECRET=specify your own user id / secret
   ```
3. Save the file. The server will automatically use your credentials.

---

# 🚀 Step 1: Looker API Explorer & Creating Your Conversational Agent (10 Mins)

### 1.1 What is the Looker API Explorer?
The **Looker API Explorer** is a built-in, fully interactive developer workbench and documentation environment integrated directly into the Looker platform. It allows data engineers, architects, and developers to:
* **Discover and Inspect All 400+ REST Endpoints:** Browse Looker API 4.0 specifications, including LookML modeling, project validation, query generation, and the modern **Conversational Analytics family** (`/agents`, `/conversations`, and `/conversational_analytics/chat`).
* **Live In-Browser API Execution:** Test requests directly against your Looker instance without setting up local development tools, Postman collections, or curl scripts.
* **Automatic Session Authentication:** When logged into the Looker web UI, API Explorer automatically authenticates using your active user session. No manual token headers or OAuth dance required in the browser.
* **Schema Validation & SDK Code Generation:** Inspect exact JSON schema contracts, parameter types, and auto-generate client code across multiple languages (Python, TypeScript, Kotlin, Swift, C#).

---

### 1.2 Accessing API Explorer in the Looker Web Interface
You can access the API Explorer directly using the link below or via the Looker navigation menu:

👉 **[Launch Looker API Explorer](https://ceworkshops.cloud.looker.com/extensions/marketplace_extension_api_explorer::api-explorer)**

**Manual Navigation Steps:**
1. Open your browser and navigate to your Looker instance:
   ```text
   https://ceworkshops.cloud.looker.com
   ```
2. Log in with your assigned workshop credentials.
3. In the left-hand navigation sidebar, click **Applications** (or **Marketplace / Extensions**) and select **API Explorer**.
   * Direct Link: [API Explorer Extension](https://ceworkshops.cloud.looker.com/extensions/marketplace_extension_api_explorer::api-explorer)
4. In the top-right version selector of the API Explorer header, verify that **Looker API 4.0** is selected.

### 1.3 Understanding Authentication for Data Engineers
Looker APIs use an OAuth2 token workflow:
* External scripts send API3 credentials (`client_id` and `client_secret`) to `POST /api/4.0/login`.
* Looker returns an `access_token`.
* Subsequent requests authenticate using the header:
  ```http
  Authorization: token <access_token>
  ```
> 💡 **Note for Data Engineers:** In Looker, the header is `Authorization: token <token>`, NOT `Authorization: Bearer <token>`. In the API Explorer web UI, you are automatically authenticated using your browser session!

---

### 1.4 Locating the Conversational Analytics API Endpoints
In the API Explorer search bar on the left, type: **`Agent`** or browse to the **Agent** / **Conversational Analytics** tag.

You will see the core Conversational Analytics API family:
* `POST /agents`: **Create Agent** (defines a new conversational agent bound to semantic explores)
* `GET /agents/search`: **Search Agents** (lists all active agents)
* `GET /agents/{agent_id}`: **Get Agent** (retrieves configuration and context)
* `PATCH /agents/{agent_id}`: **Update Agent** (modifies instructions or explores)
* `POST /conversations`: **Create Conversation** (initiates a conversational session state)
* `POST /conversational_analytics/chat`: **Chat** (submits user questions and returns answers, thought traces, and data)

---

### 1.5 Hands-On: Create Your Custom Agent (`POST /agents`)
Let's build an agent tailored for the **Cymbal Gadgets** retail dataset.

> ⚡ **Multi-Student Scaling Rule (500 Concurrent Users):**  
> Because up to 500 students may be creating agents on the same shared Looker instance, **you MUST provide a unique name** for your agent (e.g. appending your name, student ID, or a random number like `Student 42`). This prevents agent discovery clutter and ensures you can easily find your agent!

1. In API Explorer, click on **`POST /agents` (Create Agent)**.
2. Click the **Run It** tab.
3. In the **Request Body** editor, enter the following JSON payload (substituting `<YOUR_NAME_OR_ID>`):

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

#### Why These Parameters Matter:
* **`sources`**: Specifies the LookML model (`cymbal_gadgets_boris`) and explore (`transactions`). This tells the agent which semantic universe it can query.
* **`context.instructions`**: System prompt and persona guidelines. As Data Engineers, this is where you encode business definitions (e.g., "profitability = Gross Margin Percentage") so the LLM doesn't guess column names!
* **`show_analytical_details`**: Instructs the API to return the agent's chain-of-thought and query execution metadata.

4. Click **Run Request**.
5. Inspect the response in the **Response** pane:
   ```json
   {
     "id": "a9b6933c74a045de9ed130ad024cca62",
     "name": "Cymbal Retail Analytics Agent - DE Lab",
     "sources": [
       {
         "model": "cymbal_gadgets_boris",
         "explore": "transactions"
       }
     ],
     "created_at": "2026-09-16T12:01:00.000Z",
     "can": {
       "chat": true,
       "update": true,
       "destroy": true
     }
   }
   ```
6. **Important:** Copy your generated **`id`** (e.g. `a9b6933c74a045de9ed130ad024cca62`). You will use this in Step 2 and Step 3.

---

### 🚩 CHECKPOINT 1: Verify Agent Creation
**Goal:** Confirm your agent exists and is queryable on the Looker instance.

> 💡 **SkillLabs Interactive Check:** In the interactive training application (`http://localhost:8080`), enter your generated **Agent ID** into the Task 1 input field and click **Check my progress** to verify your agent and earn 25 points! *(Note: Explicit Agent ID entry is required to prevent conflicts in 500-student workshops).*

Alternatively, verify via curl in your terminal (prompt: specify your own user id / secret):
```bash
TOKEN=$(python3 -c "
import os, urllib.request, urllib.parse, json
# Prompt: specify your own user id / secret
client_id = os.environ.get('LOOKER_CLIENT_ID') or input('Client ID [specify your own user id / secret]: ')
client_secret = os.environ.get('LOOKER_CLIENT_SECRET') or input('Client Secret [specify your own user id / secret]: ')
data = urllib.parse.urlencode({'client_id': client_id, 'client_secret': client_secret}).encode()
req = urllib.request.Request('https://ceworkshops.cloud.looker.com/api/4.0/login', data=data, method='POST')
print(json.loads(urllib.request.urlopen(req).read().decode())['access_token'])
")

curl -s -H "Authorization: token $TOKEN" "https://ceworkshops.cloud.looker.com/api/4.0/agents/YOUR_AGENT_ID" | jq '{id, name, sources}'
```
**Expected Output:** A JSON object with your agent's `id`, `name`, and `sources`.

#### 🆘 Help & Troubleshooting (Checkpoint 1)
* **Got `422 Unprocessable Entity ("Category 'conversation' is not a supported category")`?**
  * *Fix:* Remove the `"category"` attribute or leave it out of the payload. The API handles categorization automatically.
* **Got `404 Not Found` when fetching explore?**
  * *Fix:* Ensure model is exactly `"cymbal_gadgets_boris"` and explore is `"transactions"`. LookML names are case-sensitive.
* **Got `401 Unauthorized`?**
  * *Fix:* Ensure the header is `Authorization: token <access_token>`, not `Bearer`.

---

# 💻 Step 2: The Pre-Created Web Application Architecture (5 Mins)

To consume these APIs in a real-world enterprise setup, a production-grade Web Application has been pre-created in your workspace under `/home/user/cymbal_gadgets/agentic_web_app`.

### 2.1 Web Application Architecture
```
agentic_web_app/
├── config.py           # Configuration loader (Looker host, credentials, ports)
├── .env                # Environment secrets file
├── looker_client.py    # Zero-dependency Python SDK client for Looker 4.0 APIs
├── server.py           # Threading REST API Server & SPA static host
├── static/
│   └── index.html      # Responsive UI with Agentic Transparency Drawer
├── test_pipeline.py    # CLI verification script
└── run.sh              # One-click startup script
```

### 2.2 Inspecting `looker_client.py`
Open and inspect `looker_client.py` in your editor or terminal:
```bash
cat /home/user/cymbal_gadgets/agentic_web_app/looker_client.py | head -n 45
```
Notice how it handles:
1. **Automatic Token Refresh**: Tokens expire every 3600 seconds. The client caches the token and re-authenticates 60 seconds before expiration.
2. **Conversation Lifecycle**: Creating conversations (`POST /conversations`) and binding them to the agent.
3. **Message Stream Parsing**: Conversational Analytics chat returns a multi-part array. The client categorizes messages into:
   * `thoughts`: Chain-of-Thought reasoning.
   * `schema_events`: Explores inspected.
   * `query`: LookML query dimensions, filters, and measures generated.
   * `data`: The raw tabular query results.
   * `final_response`: The executive markdown summary.

---

### 2.3 Starting the Web Application
Run the startup script in your terminal:
```bash
cd /home/user/cymbal_gadgets/agentic_web_app
./run.sh
```

You should see:
```text
============================================================
🚀 SME Academy Conversational Analytics Web Server Running
   Target Looker URL: https://ceworkshops.cloud.looker.com
   Local UI Address : http://localhost:8080
   Health Check     : http://localhost:8080/api/health
============================================================
```

---

### 🚩 CHECKPOINT 2: Verify Web Server Health
**Goal:** Confirm the web server is running and connected to Looker.

#### ❓ Where Do I Run the curl Command?
A common point of confusion during labs is where to execute the verification `curl` command:
1. **Open a SECOND Terminal Tab in Argolis:**
   * In **Google Cloud Shell**: Click the **`+` (Open new terminal)** icon or split window icon in the top toolbar.
   * In **Cloud Workstations / IDE**: Open a second terminal tab (**Terminal > New Terminal**).
   * **⚠️ DO NOT paste into the first terminal:** The first terminal is busy running `./run.sh` and actively serving HTTP traffic in the foreground. Typing in that window or hitting `Ctrl+C` will terminate the server.
2. **Execute INSIDE Your Argolis Cloud Environment (Not Your Local Laptop):**
   * Execute the curl command inside your Argolis Cloud Shell or Cloud Workstation session.
   * Running `curl http://localhost:8080/api/health` on your local laptop terminal will fail with `Connection refused` because `localhost:8080` is running in your remote Google Cloud environment.
3. **Alternative (Recommended): Use the Interactive UI (No Terminal Needed!):**
   * In the interactive web portal (`http://localhost:8080` via Cloud Shell Web Preview), simply navigate to **Task 2** and click the **Check my progress** button. The portal will automatically test the health endpoint and award your +25 points!

```bash
# In your SECOND Cloud Shell terminal window in Argolis:
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

#### 🆘 Help & Troubleshooting (Checkpoint 2)
* **Port 8080 already in use?**
  * *Fix:* Edit `agentic_web_app/.env` and change `PORT=8080` to `PORT=8085`, then restart `./run.sh`.
* **Looker connection failed or 401 Unauthorized?**
  * *Fix:* Verify your internet connection and ensure you configure your assigned credentials via the **Student Credentials** button in the UI or in `agentic_web_app/.env` (Prompt: specify your own user id / secret).

---

# 🔍 Step 3: Querying Your Step 1 Agent & Tracing Conversational Analytics (10 Mins)

Now, let's walk through how the application consumes each API endpoint in code, and test them live through the interactive Web UI.

> [!IMPORTANT]
> **Must Use Agent Created in Step 1:**  
> In this step, you **must use the custom agent you created in Step 1**. In workshops with up to 500 concurrent students, querying default or arbitrary agents will cause conflicting results, rate limiting, and assessment failure. Make sure to bind your specific `agent_id` from Step 1 before testing queries or running checkpoints!

---

### 3.1 Endpoint Deep-Dive

#### 1. Authentication Handshake (`POST /api/4.0/login`)
* **Endpoint:** `POST https://ceworkshops.cloud.looker.com/api/4.0/login`
* **Content-Type:** `application/x-www-form-urlencoded`
* **Payload:** `client_id=<specify your own user id / secret>&client_secret=<specify your own user id / secret>`
* **Why it matters:** Establishes an ephemeral session token without passing long-lived secrets with every analytical query.

#### 2. Agent Retrieval (`GET /api/4.0/agents/search` & `GET /api/4.0/agents/{agent_id}`)
* **Header:** `Authorization: token <access_token>`
* **Why it matters:** Discovers what semantic sources (models/explores) and system instructions govern the agent's behavior.

#### 3. Conversation Session Initialization (`POST /api/4.0/conversations`)
* **Endpoint:** `POST https://ceworkshops.cloud.looker.com/api/4.0/conversations`
* **Payload:**
  ```json
  {
    "agent_id": "YOUR_STEP_1_AGENT_ID",
    "name": "Cymbal Gadgets Executive Session"
  }
  ```
* **Why it matters:** Looker Conversational Analytics maintains conversation state on the server. You don't need to append all previous chat history to every query—Looker automatically tracks context via the `conversation_id`!

#### 4. Natural Language Execution (`POST /api/4.0/conversational_analytics/chat`)
* **Endpoint:** `POST https://ceworkshops.cloud.looker.com/api/4.0/conversational_analytics/chat`
* **Payload:**
  ```json
  {
    "conversation_id": "730371f2ee85482ebfeb43d62fc20326",
    "user_message": "What is the total sales amount across all stores?"
  }
  ```
* **Payload Unwrapping:**
  Unlike generic chat completions that just return a string of text, Looker returns an array of messages representing the agent's lifecycle:

| Message Type | Field in Payload | Purpose |
| :--- | :--- | :--- |
| **THOUGHT** | `systemMessage.text.textType == "THOUGHT"` | Chain-of-thought: what the agent plans to do |
| **SCHEMA** | `systemMessage.schema` | Explores fetched from the LookML semantic layer |
| **QUERY** | `systemMessage.data.query` | Dimensions, measures, and filters selected by agent |
| **DATA** | `systemMessage.data.result` | Verified tabular data returned from database |
| **FINAL_RESPONSE** | `systemMessage.text.textType == "FINAL_RESPONSE"` | Formatted natural language executive summary |

---

### 3.2 Hands-On: Test Your Agent in the Web UI

1. Open your browser and navigate to:
   ```text
   http://localhost:8080
   ```
2. **Select the Agent You Created in Step 1:**
   * In the top ribbon under **Agent**, either select your uniquely named agent (`Cymbal Retail Analytics Agent - Student <YOUR_NAME_OR_ID>`) from the dropdown, or enter the **`agent_id`** you created in Step 1 into the input field and click **Use Agent**.
   * Notice that the **Conversation State** updates with a fresh `conversation_id` tied specifically to your Step 1 agent.

3. **Submit Query 1 (Basic Aggregation):**
   * In the chat input, type:
     ```text
     What is our total sales amount across all transactions?
     ```
   * Click **Ask**.

4. **Audit the Agentic Transparency Hub:**
   Once the answer appears:
   * Click **Agent Thought Process**: Read the model's reasoning on how it identified the revenue metric in the `transactions` explore.
   * Click **Governed Data Result**: View the exact tabular row returned from Looker.
   * Click **Generated Looker Query Specification**: See the precise fields selected (`transactions.total_sales_amount`).

5. **Submit Query 2 (Dimension Breakdown & Grouping):**
   * Ask:
     ```text
     Show the average transaction amount by store country.
     ```
   * Observe the table generated with countries and averages.

6. **Submit Query 3 (Multi-turn Contextual Follow-up):**
   * Ask:
     ```text
     Which store country had the highest transaction volume?
     ```
   * Because the session is stateful, notice how the agent understands "store country" in context without having to redefine the question!

---

### 🚩 CHECKPOINT 3: Verify Interactive Query Flow
**Goal:** Confirm that questions return governed data and clear reasoning steps against your Step 1 agent.

> 💡 **SkillLabs Interactive Check:** In the interactive training application (`http://localhost:8080`), enter your Step 1 **Agent ID** into the Task 3 input field and click **Check my progress** to execute an analytical verification query and earn 25 points!

Alternatively, run the automated CLI verification script passing your Step 1 Agent ID:
```bash
python3 /home/user/cymbal_gadgets/agentic_web_app/test_pipeline.py YOUR_STEP_1_AGENT_ID
```
**Expected Output:**
```text
=================================================================
🧪 SME Academy: Verifying Looker Conversational Analytics API
=================================================================
[Step 1] Authenticating with Looker 4.0 API...
✅ Logged in successfully. Token prefix: mddgwZ6Y...

[Step 2] Discovering available agents (GET /api/4.0/agents/search)...
✅ Found agents on instance.

[Step 3] Using Agent: 'Cymbal Retail Analytics Agent - Student ...' (YOUR_AGENT_ID)
Creating Conversation (POST /api/4.0/conversations)...
✅ Created Conversation Session: 730371f2...

[Step 4] Submitting Conversational Query: 'What is the total sales amount?'...
Calling POST /api/4.0/conversational_analytics/chat...

=================================================================
📊 RESULTS RECEIVED FROM LOOKER SEMANTIC LAYER:
=================================================================
• Thought Steps Recorded : 3
• Explore Queried        : 1 explore schema calls
• Governed Query Built   : Yes
• Data Returned          : Yes

📝 FINAL SYNTHESIZED RESPONSE:
## Total Sales Overview
* Total Sales (Revenue): The total sales amount across all transactions is $1,074,890,772.
=================================================================
🎉 ALL API CHECKS PASSED! Web app and APIs are verified.
```

#### 🆘 Help & Troubleshooting (Checkpoint 3)
* **Agent returned "I cannot find data for that question"?**
  * *Fix:* The question might refer to fields outside the `transactions` explore. Try: "What is the total sales amount?" or "Show sales by country".
* **Response takes 15–20 seconds?**
  * *Explanation:* The first query initiates schema introspection and LLM compilation against the Looker instance. Subsequent queries in the same conversation are cached and faster.

---

# 🛡️ Step 4: Agent Instruction Tuning & Production Deployment (5 Mins)

### 4.1 Tuning Agent Behavior (`PATCH /api/4.0/agents/{agent_id}`)
In real-world data engineering, stakeholders require strict formatting and guardrails. You can update agent behavior on the fly using `PATCH /agents/{agent_id}`.

Let's update our agent instructions:
```bash
python3 -c "
import urllib.request, json, sys
sys.path.append('/home/user/cymbal_gadgets/agentic_web_app')
import config
from looker_client import LookerClient

client = LookerClient(config.LOOKER_BASE_URL, config.LOOKER_CLIENT_ID, config.LOOKER_CLIENT_SECRET)
agent_id = 'YOUR_AGENT_ID'  # Replace with your Agent ID

new_instructions = '''
- Always begin your answer with '🌟 Cymbal Executive Summary:'
- Format all currency metrics in EUR with thousands separators (e.g. \$1,234,567)
- If asked about gross margin, always state the exact percentage with two decimals
- Keep explanations under 3 sentences
'''

updated = client._request('PATCH', f'/agents/{agent_id}', payload={
    'context': {'instructions': new_instructions, 'show_analytical_details': True}
})
print('Successfully updated instructions for:', updated.get('name'))
"
```
After running this, ask your agent in the web app: *"What is our total gross margin percentage?"*  
Notice that the agent immediately complies with the new persona and formatting rules!

---

### 4.2 Enterprise Production Architecture on GCP

For enterprise deployment, data engineers wrap this pattern into Google Cloud serverless architecture:

```
                      ┌─────────────────────────────────────────┐
                      │            Cloud Armor / IAP            │
                      └────────────────────┬────────────────────┘
                                           │
                                           ▼
                      ┌─────────────────────────────────────────┐
                      │           Google Cloud Run              │
                      │  (FastAPI / Python Web App Container)   │
                      └─────────────┬───────────────────────────┘
                                    │
           ┌────────────────────────┴────────────────────────┐
           ▼                                                 ▼
┌─────────────────────────┐                       ┌─────────────────────────┐
│  Secret Manager (GSM)   │                       │  Looker Conversational  │
│ (LOOKER_CLIENT_SECRET)  │                       │      Analytics API      │
└─────────────────────────┘                       └─────────────┬───────────┘
                                                                │
                                                                ▼
                                                  ┌─────────────────────────┐
                                                  │  Google Cloud BigQuery  │
                                                  │    (Analytical Data)    │
                                                  └─────────────────────────┘
```

#### Production Checklist:
1. **Containerize:** Package `server.py` or FastAPI with Docker into Google Artifact Registry (`gcr.io` or `pkg.dev`).
2. **Secrets via Secret Manager:** Mount `LOOKER_CLIENT_SECRET` as an environment variable in Cloud Run using Google Cloud Secret Manager.
3. **Identity & Access Management (IAM):** Use Cloud Run Service Identity with least-privilege roles to authenticate to internal GCP services.
4. **Embedding:** Use the Web App as an embedded iframe inside internal customer portals, Salesforce, or Google Chat / Slack bots.

---

### 🚩 CHECKPOINT 4: Lab Wrap-Up & SME Academy Takeaways
Congratulations! You have completed the **Looker Conversational Analytics Agent Lab**.

> 💡 **SkillLabs Interactive Check:** In the interactive training application (`http://localhost:8080`), you can click the **Check my progress** button under Task 4 to verify prompt tuning, complete the lab, and earn your final 25 points (100/100)!

### Key Takeaways for Data Engineers:
1. **No Hallucinated SQL:** By pointing LLMs at Looker's semantic layer rather than raw database tables, metric calculations remain governed and auditable.
2. **API Explorer as the First Stop:** The Looker API Explorer is the fastest tool for discovering endpoints, validating schemas, and testing payloads.
3. **Conversational State is Managed Server-side:** `POST /conversations` frees your frontend or microservices from managing token budgets and multi-turn message history.
4. **Full Transparency:** Looker APIs expose the entire chain of thought, explore schema resolution, and raw query output for compliance and debugging.

---
