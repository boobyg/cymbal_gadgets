# 🎓 SME Academy: Looker Conversational Analytics & Agentic Web App

[![Google Cloud](https://img.shields.io/badge/Google%20Cloud-Argolis%20Environment-4285F4?logo=google-cloud&logoColor=white)](https://cloud.google.com)
[![Looker API](https://img.shields.io/badge/Looker%20API-4.0%20Conversational%20Analytics-0052CC?logo=looker&logoColor=white)](https://cloud.looker.com)
[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12-3776AB?logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](LICENSE)

An end-to-end, hands-on lab and reference implementation for **Google Cloud SME Academy (Data Analytics & Agentic AI Track)**. 

Students build, test, and deploy a custom **Conversational Analytics Agent** connected to Looker's governed semantic layer (`cymbal_gadgets_boris` model & `transactions` explore) and consume it through a full-stack web application featuring real-time reasoning tracing, governed LookML SQL generation, and interactive assessment checkpoints.

---

## ⚠️ MANDATORY REQUIREMENT: Deploy in Your Own Argolis Environment

> [!IMPORTANT]
> **STUDENT REQUIREMENT:**  
> Every student **MUST deploy and run this lab inside their own dedicated Google Cloud Argolis environment** (e.g., using **Google Cloud Shell** or **Cloud Workstations** in their assigned Argolis GCP project).
>
> **Why is your own Argolis environment required?**
> 1. **Complete Isolation (No Port Collisions):** The web server runs on port `8080`. In shared environments or shared VMs, multiple students will experience port collisions (`Address already in use`) and conflicting session state.
> 2. **Credential Privacy & Security:** Your assigned Looker API credentials (`client_id` and `client_secret`) must remain confidential inside your personal GCP project sandbox.
> 3. **Built-in Cloud Shell Web Preview:** Google Cloud Shell automatically provides a secure HTTPS proxy to preview port `8080` in your web browser with zero firewall configuration or local SSH port forwarding.
> 4. **Zero Local Installation:** Running in Argolis Cloud Shell guarantees that Python 3, Git, curl, and network connectivity to the Looker instance are pre-installed and functional—no local machine setup needed.

---

## 🏛️ Architecture Overview

Looker Conversational Analytics pairs Large Language Models with Looker's **Governed Semantic Layer**:

```
┌───────────────────────────────────────────────┐
│        Student's Argolis Environment          │
│   (Cloud Shell / Workstation / Cloud Run)     │
│                                               │
│   ┌───────────────────────────────────────┐   │
│   │   Interactive Training Web Portal     │   │
│   │   (HTML5 / Tailwind / Event Viewer)   │   │
│   └───────────────────┬───────────────────┘   │
│                       │ HTTP REST (Port 8080) │
│   ┌───────────────────▼───────────────────┐   │
│   │   Fast Zero-Dependency Python Server  │   │
│   │   (ThreadingHTTPServer + SDK Client)  │   │
│   └───────────────────┬───────────────────┘   │
└───────────────────────┼───────────────────────┘
                        │ HTTPS /api/4.0
                        ▼
┌───────────────────────────────────────────────┐
│        Google Cloud Looker Instance           │
│   https://ceworkshops.cloud.looker.com        │
│                                               │
│   ┌───────────────────────────────────────┐   │
│   │  Conversational Analytics Endpoints   │   │
│   │  POST /agents                         │   │
│   │  POST /conversations                  │   │
│   │  POST /conversational_analytics/chat  │   │
│   └───────────────────┬───────────────────┘   │
│                       │ LookML Resolution     │
│   ┌───────────────────▼───────────────────┐   │
│   │        Governed Semantic Model        │   │
│   │        (cymbal_gadgets_boris)         │   │
│   └───────────────────┬───────────────────┘   │
└───────────────────────┼───────────────────────┘
                        │ Optimized Dialect SQL
                        ▼
┌───────────────────────────────────────────────┐
│             Google Cloud BigQuery             │
│          Retail Transactions Dataset          │
└───────────────────────────────────────────────┘
```

---

## 🚀 How to Deploy the Lab from Git in Your Argolis Environment

Follow these steps to deploy and run the lab in your Argolis project:

### Step 1: Open Google Cloud Shell in Argolis
1. Open the [Google Cloud Console](https://console.cloud.google.com).
2. Ensure your active project is your assigned **Argolis project** (e.g. `prj-<user>-argolis` or similar).
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
> * If Git prompts `Username for 'https://github.com':`, you likely mistyped the URL or pointed to a private repository. Double-check that you typed `https://github.com/boobyg/cymbal_gadgets.git`.
> * **Note on GitHub Passwords:** GitHub permanently deprecated account passwords for Git operations on August 13, 2021. If you are cloning a **private** repository or pushing code, you must enter a **GitHub Personal Access Token (PAT)** with `repo` scope when prompted for the password, or use the GitHub CLI (`gh auth login`).


### Step 3: Start the Web Server
Launch the application using the startup script:

```bash
./run.sh
```

*(The script automatically initializes `.env` from `.env.example` and launches the Python HTTP server on port 8080).*

You will see:
```text
============================================================
🚀 SME Academy: Looker Conversational Analytics Agent App
   Directory: /home/.../cymbal_gadgets/agentic_web_app
============================================================
Starting server on port 8080...
If running in Google Cloud Shell in Argolis:
👉 Click the 'Web Preview' icon in the top right -> 'Preview on port 8080'
============================================================
```

### Step 4: Open the Web Application via Cloud Shell Web Preview
1. At the top-right of the **Google Cloud Shell** window, click the **Web Preview** icon:
   
   ![Web Preview Icon](https://cloud.google.com/static/shell/docs/images/web-preview-button.png)
2. Select **Preview on port 8080** from the dropdown menu.
3. A new browser tab opens loading the **Interactive SkillLabs Training Portal**!

### Step 5: Configure Your Student Credentials
In the opened web portal:
1. Click the **Student Credentials** button in the top navigation bar.
2. Enter your assigned:
   * **Looker Client ID:** *(provided by instructor)*
   * **Looker Client Secret:** *(provided by instructor)*
3. Click **Save & Test Connection**. When verified, the status indicator turns green (`Looker Connected`).

---

## 🔍 Task 2: Where to Run the curl Command

> [!CAUTION]
> ### ❓ Crucial Instruction: Where and How to Run the Task 2 curl Command
>
> In **Task 2 / Checkpoint 2**, students verify server health using `curl -s http://localhost:8080/api/health | jq .`.  
> Many students get stuck here. Here is exactly what you need to know:
>
> #### 1. DO NOT Run curl in the First Terminal Window
> In Step 3, you ran `./run.sh`. That terminal is **currently busy** running the Python web server in the foreground and logging incoming HTTP requests.
> * If you try to type the `curl` command into that window, it will not run.
> * If you press `Ctrl + C` in that window, **you will kill the web server**!
>
> #### 2. DO NOT Run curl on Your Local Laptop Terminal
> If you open Terminal / PowerShell on your MacBook or Windows laptop and run `curl http://localhost:8080/api/health`, it will fail with:
> ```text
> curl: (7) Failed to connect to localhost port 8080: Connection refused
> ```
> *Why?* Because `localhost:8080` exists **inside the remote Argolis Cloud Shell container**, not on your personal laptop.
>
> #### 3. DO NOT curl Your External Cloud Shell Preview URL (`https://*.cloudshell.dev`)
> If you copy your browser preview URL and run `curl -s "https://8080-cs-...cloudshell.dev/api/health" | jq .`, it will fail with:
> ```text
> jq: parse error: Invalid numeric literal at line 1, column ...
> ```
> *Why?* The external Cloud Shell preview URL requires Google SSO browser cookies. From the terminal, `curl` receives an HTML login redirect (`<a href=...>`), which `jq` cannot parse as JSON.
> *Fix:* Inside your Cloud Shell terminal, **always** curl `http://localhost:8080/api/health`!
>
> #### 4. The Correct Way: Open a SECOND Terminal Tab in Argolis Cloud Shell
> 1. In Google Cloud Shell, look at the tab bar above the terminal prompt.
> 2. Click the **`+` (Open new tab)** button or press the **Split Window** icon.
> 3. In this fresh, second terminal tab, run:
>    ```bash
>    curl -s http://localhost:8080/api/health | jq .
>    ```
> 4. You will receive the healthy JSON status:
>    ```json
>    {
>      "status": "healthy",
>      "looker_connected": true,
>      "looker_url": "https://ceworkshops.cloud.looker.com",
>      "user_email": "api_user@example.com"
>    }
>    ```
>
> #### 5. Alternative (Fastest): Use the Web UI Button (No Terminal Needed!)
> If you already have the interactive web portal open in your browser (`http://localhost:8080` via Web Preview):
> 1. Scroll to **Task 2: Assessment Checkpoint 2** in the left lab guide panel.
> 2. Click the green **Check my progress** button.
> 3. The web portal directly executes the health check against `/api/health` and automatically awards **+25 points**!

---

## ☁️ Optional: Deploying as a Serverless Container on Google Cloud Run

If you wish to deploy the application as an always-on, serverless Cloud Run service in your Argolis project:

```bash
cd cymbal_gadgets/agentic_web_app

# Deploy using Google Cloud Run
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

Cloud Run will output an HTTPS service URL (e.g. `https://looker-agentic-web-app-xxx-uc.a.run.app`) where you can access the app directly from any browser.

---

## 📂 Repository Contents

```
cymbal_gadgets/
├── README.md                                   # This master deployment & lab guide
├── LAB_GUIDE_CONVERSATIONAL_ANALYTICS.md       # Comprehensive 30-minute student lab curriculum
├── manifest.lkml                               # LookML project manifest
├── agentic_web_app/                            # Pre-built student web application
│   ├── Dockerfile                              # Minimal, secure container definition (Python 3.12-slim)
│   ├── .dockerignore                           # Build ignore file
│   ├── deploy_cloud_run.sh                     # Automated Google Cloud Run deployment script
│   ├── run.sh                                  # Local / Cloud Shell one-click startup script
│   ├── server.py                               # Zero-dependency Python HTTP server & REST API
│   ├── looker_client.py                        # Python SDK for Looker 4.0 Conversational APIs
│   ├── config.py                               # Environment loader & configuration defaults
│   ├── test_pipeline.py                        # Automated CLI validation & query runner
│   ├── .env.example                            # Template configuration for API credentials
│   └── static/
│       └── index.html                          # Single-Page App with dual-pane layout & Transparency Hub
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
| **Task 2** | **Deploy App & Health Check** | 5 mins | Launch app in Argolis Cloud Shell, verify health via curl (in 2nd terminal) or UI | 25 pts |
| **Task 3** | **Interactive Queries & Tracing** | 10 mins | Test multi-turn conversational queries with Step 1 agent and inspect transparency traces | 25 pts |
| **Task 4** | **Prompt Tuning & Guardrails** | 5 mins | Update system instructions via `PATCH /agents/{agent_id}` to enforce executive formatting | 25 pts |

---

## 🆘 Troubleshooting FAQ

| Problem | Root Cause | Solution |
| :--- | :--- | :--- |
| `Address already in use (port 8080)` | Another process is using port 8080 | Edit `.env` and set `PORT=8085`, then restart `./run.sh` |
| `jq: parse error: Invalid numeric literal at line 1, column ...` | Curled external `https://*.cloudshell.dev` URL which requires Google cookies and returns HTML redirect | Curl `http://localhost:8080/api/health` in Cloud Shell terminal tab, or click **Check my progress** in the Web UI |
| Agent dropdown shows agents from other students | Shared Looker instance has multiple students' agents | The web app now automatically filters agents by your user ID (`created_by_user_id == current_user.id`) so you only see your own! |
| `git clone` asks for Username/Password or fails with `Support for password authentication was removed` | Typed incorrect/private repo URL or entered GitHub account password | Clone the public URL: `git clone https://github.com/boobyg/cymbal_gadgets.git` (no credentials needed). For private repos, use a **Personal Access Token (PAT)** with `repo` scope instead of password. |
| `Failed to connect to localhost port 8080` | Ran `curl` in local laptop terminal instead of Argolis Cloud Shell | Open a second terminal tab in **Google Cloud Shell** and run the `curl` command there |
| First terminal unresponsive to commands | Terminal is busy running `./run.sh` | Open a **second terminal tab** (`+`) in Cloud Shell rather than interrupting the server |
| `401 Unauthorized` on Looker API calls | Invalid or missing API3 credentials | Click **Student Credentials** in the UI and verify your Client ID & Secret |
| `422 Unprocessable Entity` when creating agent | Included obsolete `"category"` field in payload | Omit `"category"` attribute; the API categorizes agents automatically |
| Checkpoint 1 or 3 assessment fails | Did not specify unique Step 1 Agent ID | Paste your exact `agent_id` from Step 1 into the Checkpoint input box |

---

## 📄 License
This repository is licensed under the Apache License 2.0. See [LICENSE](LICENSE) for details.
