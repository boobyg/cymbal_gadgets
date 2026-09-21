# 🌐 Agentic Web App: Looker Conversational Analytics

This directory contains the student web application for the **Google Cloud SME Academy: Looker Conversational Analytics Lab**.

---

## ⚠️ MANDATORY REQUIREMENT: Deploy in Your Own Argolis Environment

> [!IMPORTANT]
> **STUDENT REQUIREMENT:**  
> Every student **MUST deploy and run this lab inside their own dedicated Google Cloud Argolis environment** (using **Google Cloud Shell** or **Cloud Workstations** inside their assigned Argolis project).
>
> **Why is your own Argolis environment required?**
> 1. **Complete Isolation (No Port Collisions):** The web server runs on port `8080`. In shared environments or multi-user VMs, multiple students will experience port collisions (`Address already in use`) and conflicting session state.
> 2. **Credential Privacy & Security:** Your assigned Looker API credentials (`client_id` and `client_secret`) must remain confidential inside your personal GCP project sandbox.
> 3. **Built-in Cloud Shell Web Preview:** Google Cloud Shell automatically provides a secure HTTPS proxy to preview port `8080` in your web browser with zero firewall configuration or local SSH port forwarding.
> 4. **Zero Local Installation:** Running in Argolis Cloud Shell guarantees that Python 3, Git, curl, and network connectivity to the Looker instance are pre-installed and functional—no local machine setup needed.

---

## 🚀 How to Deploy & Run from Git in Your Argolis Environment

### Step 1: Open Google Cloud Shell in Your Argolis Project
1. Navigate to the [Google Cloud Console](https://console.cloud.google.com).
2. Ensure the top project selector displays your personal **Argolis project**.
3. Click the **Activate Cloud Shell** icon (`>_`) in the top navigation bar.

### Step 2: Clone the Git Repository
In your Cloud Shell terminal:
```bash
# Clone the public repository (no password or token required)
git clone https://github.com/boobyg/cymbal_gadgets.git
cd cymbal_gadgets/agentic_web_app
```

> [!TIP]
> **No GitHub Password Needed:**  
> The repository `https://github.com/boobyg/cymbal_gadgets.git` is public and clones directly without credentials. If you are prompted for a password or see `Support for password authentication was removed`, ensure you did not mistype the URL. For private repos, GitHub requires a **Personal Access Token (PAT)** rather than an account password.


### Step 3: Launch the Web Server
```bash
./run.sh
```
*(The startup script automatically initializes `.env` from `.env.example` if not already present and starts the Python web server on port 8080).*

### Step 4: Access via Cloud Shell Web Preview
1. In the top-right of your Cloud Shell panel, click the **Web Preview** button:
   
   ![Web Preview](https://cloud.google.com/static/shell/docs/images/web-preview-button.png)
2. Select **Preview on port 8080**.
3. The interactive web application loads directly in your browser.

### Step 5: Configure Credentials
1. Click **Student Credentials** in the top navigation bar.
2. Enter your assigned Looker Client ID and Client Secret.
3. Click **Save & Test Connection**.

---

## 🔍 Task 2: Where to Run the curl Command

> [!CAUTION]
> ### ❓ Crucial Instruction: Where and How to Run the Task 2 curl Command
>
> In **Task 2 / Checkpoint 2**, students verify server health using:
> ```bash
> curl -s http://localhost:8080/api/health | jq .
> ```
>
> **Common student pitfalls and exactly where to run this:**
>
> ❌ **DO NOT run curl in the first terminal window:**  
> The terminal where you ran `./run.sh` is currently busy executing the Python web server in the foreground. If you attempt to type commands there, they will not run. If you press `Ctrl+C`, you will kill the web server.
>
> ❌ **DO NOT run curl on your local laptop terminal:**  
> If you open Terminal or PowerShell on your personal Mac or Windows laptop and run `curl http://localhost:8080/api/health`, it will fail with:
> `curl: (7) Failed to connect to localhost port 8080: Connection refused`  
> *Reason:* Port 8080 is listening inside your **remote Argolis Cloud Shell container**, not on your personal machine!
>
> ❌ **DO NOT curl your external Cloud Shell Web Preview URL (`https://*.cloudshell.dev`):**  
> If you copy your browser preview URL and run `curl -s "https://8080-cs-...cloudshell.dev/api/health" | jq .`, it will fail with:  
> `jq: parse error: Invalid numeric literal at line 1, column ...`  
> *Reason:* External Cloud Shell preview URLs require Google OAuth login cookies. Terminal `curl` does not carry your Google browser cookies, so Cloud Shell returns an HTML redirect page (`<a href=...>`), which `jq` cannot parse as JSON. Inside your Cloud Shell terminal, **always curl `http://localhost:8080/api/health`** directly!
>
> ✅ **WHERE TO RUN IT (Option A - Second Terminal Tab):**  
> 1. In Google Cloud Shell, look at the tab bar above the terminal prompt.
> 2. Click the **`+` (Open new terminal tab)** button.
> 3. In this new second terminal tab, run:
>    ```bash
>    curl -s http://localhost:8080/api/health | jq .
>    ```
> 4. Expected response:
>    ```json
>    {
>      "status": "healthy",
>      "looker_connected": true,
>      "looker_url": "https://ceworkshops.cloud.looker.com",
>      "user_email": "api_user@example.com"
>    }
>    ```
>
> ✅ **WHERE TO RUN IT (Option B - Web UI Button - Fastest!):**  
> If you are viewing the web app in your browser via Web Preview:
> 1. Scroll to **Task 2: Checkpoint 2** in the left lab guide pane.
> 2. Click the green **Check my progress** button.
> 3. The web portal executes the health check against `/api/health` directly and awards your assessment points without opening any additional terminal!

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
