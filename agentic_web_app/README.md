# 🌐 Agentic Web App: Looker Conversational Analytics

This directory contains the student web application for the **Google Cloud SME Academy: Looker Conversational Analytics Lab**.

---

## 🎯 Purpose & Objectives for Data Engineers
This web application demonstrates how modern data engineering workflows consume Looker Conversational Analytics APIs in real-world applications:
* Authenticates to Looker 4.0 using client credentials.
* Manages stateful conversation threads (`POST /conversations`).
* Submits natural language queries and parses the 5-phase agent lifecycle (`THOUGHT`, `SCHEMA`, `QUERY`, `DATA`, `FINAL_RESPONSE`).
* Provides real-time query tracing, SQL auditability, and interactive lab assessment checkpoints.

---

## 🖥️ Presentation Slides & Materials
* **Interactive Presentation:** Accessible at `http://localhost:8080/presentation.html` once the server is started.
* **Markdown Slide Deck:** `../PRESENTATION_LOOKER_CONVERSATIONAL_ANALYTICS.md`
* **Student Lab Guide:** `../LAB_GUIDE_CONVERSATIONAL_ANALYTICS.md`

---

## ⚠️ MANDATORY REQUIREMENT: Deploy in Your Own Argolis Environment

> [!IMPORTANT]
> **STUDENT REQUIREMENT:**  
> Every student **MUST deploy and run this lab inside their own dedicated Google Cloud Argolis environment** (using **Google Cloud Shell** inside their assigned Argolis project).
>
> **Why is your own Argolis environment required?**
> 1. **Complete Isolation (No Port Collisions):** The web server runs on port `8080`. In shared environments, multiple students will experience port collisions (`Address already in use`) and conflicting session state.
> 2. **Credential Privacy & Security:** Your assigned Looker API credentials (`client_id` and `client_secret`) remain confidential inside your personal GCP project sandbox.
> 3. **Built-in Cloud Shell Web Preview:** Google Cloud Shell automatically provides a secure HTTPS proxy to preview port `8080` in your web browser with zero firewall configuration or local SSH port forwarding.
> 4. **Zero Local Installation:** Running in Argolis Cloud Shell guarantees that Python 3, Git, curl, and network connectivity to the Looker instance are pre-installed.

---

## 🚀 How to Deploy & Run from Git in Your Argolis Environment

### Step 1: Open Google Cloud Shell in Your Argolis Project
1. Navigate to the [Google Cloud Console](https://console.cloud.google.com).
2. Ensure the top project selector displays your personal **Argolis project**.
3. Click the **Activate Cloud Shell** icon (`>_`) in the top navigation bar.

### Step 2: Clone the Git Repository
In your Cloud Shell terminal:
```bash
# Clone the public repository (no password required)
git clone https://github.com/boobyg/cymbal_gadgets.git
cd cymbal_gadgets/agentic_web_app
```

### Step 3: Launch the Web Server
```bash
./run.sh
```
*(The startup script automatically initializes `.env` from `.env.example` if not already present and starts the Python web server on port 8080).*

### Step 4: Access via Cloud Shell Web Preview
1. In the top-right of your Cloud Shell panel, click the **Web Preview** button.
2. Select **Preview on port 8080**.
3. The interactive web application loads directly in your browser.

### Step 5: Configure Credentials
1. Click the yellow **Student Credentials** button in the top navigation bar.
2. Enter your assigned Looker Client ID and Client Secret.
3. Click **Save & Test Connection**.
*(Note: Any previous test credentials are automatically cleared; you can also click "Clear Saved Credentials" at any time).*

---

## 🔍 Task 2: Where to Run the Health Check curl Command

> [!CAUTION]
> ### ❓ Crucial Instruction: Where and How to Run the Task 2 curl Command
>
> In **Task 2 / Checkpoint 2**, students verify server health using:
> ```bash
> curl -s http://localhost:8080/api/health | jq .
> ```
>
> ❌ **DO NOT run curl in the first terminal window:**  
> The terminal where you ran `./run.sh` is busy running the Python web server in the foreground. Typing there will not execute commands, and pressing `Ctrl+C` will kill the server.
>
> ❌ **DO NOT run curl on your local laptop terminal:**  
> `localhost:8080` is listening inside the **remote Argolis Cloud Shell container**, not on your personal laptop. Running curl locally returns `Connection refused`.
>
> ❌ **DO NOT curl your external Cloud Shell Web Preview URL (`https://*.cloudshell.dev`):**  
> External Cloud Shell URLs require Google OAuth login cookies and return an HTML redirect page which `jq` cannot parse as JSON.
>
> ✅ **WHERE TO RUN IT (Option A - Second Terminal Tab):**  
> 1. In Google Cloud Shell, click the **`+` (Open new tab)** button in the terminal tab bar.
> 2. In this new tab, run:
>    ```bash
>    curl -s http://localhost:8080/api/health | jq .
>    ```
>
> ✅ **WHERE TO RUN IT (Option B - Web UI Button - Fastest!):**  
> 1. In the web portal (`http://localhost:8080`), scroll to **Task 2: Checkpoint 2** in the left lab guide pane.
> 2. Click the green **Check my progress** button to verify health and earn **+25 points** instantly!

---

## ☁️ Optional: Deploying to Google Cloud Run

To deploy this app as a serverless container service:
```bash
./deploy_cloud_run.sh
```
Or with `gcloud`:
```bash
gcloud run deploy looker-agentic-web-app \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars LOOKER_BASE_URL="https://ceworkshops.cloud.looker.com",LOOKER_CLIENT_ID="YOUR_CLIENT_ID",LOOKER_CLIENT_SECRET="YOUR_CLIENT_SECRET"
```
