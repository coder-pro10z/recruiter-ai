# Deployment Guide: Recruiter AI

This guide outlines two different strategies for deploying the Recruiter AI platform into production:
1. **Managed Platforms (Recommended)**: Vercel (Frontend) + Render/Railway (Backend)
2. **Self-Hosted VPS**: Deploying anywhere via Docker Compose (e.g., DigitalOcean, AWS EC2)

---

## How the CI/CD Pipeline Works

There are **two separate layers** — a quality gate (GitHub Actions) and the actual deployment (Render + Vercel). They work together but are independent.

```
git push origin main
        │
        ├──► GitHub Actions (ci.yml)         ← Quality gate only
        │       ├── Frontend: lint, type-check, build
        │       ├── Backend: pip install, (future: pytest)
        │       └── Docker: docker-compose build check
        │
        ├──► Render (auto-detects push)       ← Deploys backend
        │       └── Builds Dockerfile → runs container with env vars from Render dashboard
        │
        └──► Vercel (auto-detects push)       ← Deploys frontend
                └── Builds Next.js → injects env vars from Vercel dashboard
```

### Key facts:
- **GitHub Actions does NOT deploy** — it only checks code quality. If the checks fail, it's a warning, not a blocker.
- **Render and Vercel deploy independently** on every push to `main` via GitHub webhooks.
- **Your current branch is `setup-and-host`** — pushes here do NOT trigger CI or deployment. You must merge to `main` first.
- **`.env` files are NEVER deployed** — env vars are configured directly in Render/Vercel dashboards.

---

### Environment Variables: Where They Live

| Variable | Local Dev | Render (Production) | Vercel (Production) |
|----------|-----------|---------------------|---------------------|
| `DATABASE_URL` | `.env` (root) | Render Dashboard → Environment | — |
| `FRONTEND_URL` | `.env` (root) | Render Dashboard → Environment | — |
| `TELEGRAM_BOT_TOKEN` | `.env` (root) | Render Dashboard → Environment | — |
| `NOTION_API_KEY` | `.env` (root) | Render Dashboard → Environment | — |
| `NEXT_PUBLIC_BACKEND_URL` | `frontend/.env.local` | — | Vercel Dashboard → Settings → Env Vars |

> **The `.env` file only exists on your local machine. It is gitignored and never sent anywhere.**  
> Render and Vercel each have their own secure env var storage that gets injected at build/runtime.

---

## Prerequisites
Before you begin with either method, ensure you have:
1. A live **Supabase** project with your schema applied.
2. All necessary API keys ready (Apollo, Hunter, Gmail, Notion, Telegram, etc.).
3. Your codebase pushed to a GitHub repository.

---

## Option 1: Managed Platforms (Recommended)

This is the easiest and most robust path. It offers automatic SSL, CI/CD integration on every push, and zero server maintenance.

### 1. Database (Supabase)
Your database is already managed in the cloud. Just ensure you have the `DATABASE_URL` ready.

### 2. Backend Deployment (Render or Railway)
We recommend **Render** or **Railway** for hosting the Python FastAPI backend.

**Using Render:**
1. Create an account at [Render](https://render.com).
2. Click **New +** > **Web Service**.
3. Connect your GitHub repository.
4. Set the following configuration:
   - **Root Directory**: `backend`
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 10000`
5. Go to the **Environment** tab and add all the environment variables from your `.env.example` file.
6. Click **Create Web Service**. Render will build and deploy your API. 
7. Note down the public URL (e.g., `https://recruiter-ai-api.onrender.com`).

### 3. Frontend Deployment (Vercel)
**Vercel** is the native hosting platform for Next.js and provides the absolute best experience.

1. Create an account at [Vercel](https://vercel.com).
2. Click **Add New** > **Project**.
3. Import your GitHub repository.
4. Set the following configuration:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
5. Open the **Environment Variables** section and add:
   - `NEXT_PUBLIC_BACKEND_URL`: The public URL of your backend from the previous step.
   - Any other frontend-specific keys.
6. Click **Deploy**. Vercel will build and assign you a public URL.

---

## Option 2: Self-Hosted VPS (Docker Compose)

If you prefer to run everything on a single virtual private server (e.g., DigitalOcean Droplet, AWS EC2, or Hetzner), you can use the provided `docker-compose.yml`.

### 1. Server Setup
1. Provision a Linux server (Ubuntu 22.04 recommended) with at least 2GB RAM.
2. SSH into your server.
3. Install Git, Docker and Docker Compose:
   ```bash
   sudo apt update
   sudo apt install git docker.io docker-compose -y
   ```

### 2. Clone the Repository
```bash
git clone https://github.com/yourusername/recruiter-ai.git
cd recruiter-ai
```

### 3. Configure Environment Variables
1. Copy the example files:
   ```bash
   cp .env.example .env
   cp frontend/.env.local.example frontend/.env.local
   ```
2. Edit `.env` and `frontend/.env.local` (e.g., using `nano .env`) and fill in your actual production keys.
3. **Important**: Change `NEXT_PUBLIC_BACKEND_URL` in `frontend/.env.local` to point to your server's public IP or domain name, rather than `localhost`.

### 4. Build and Run
```bash
# Run in detached mode so it stays up when you close SSH
sudo docker-compose up -d --build
```
Your application is now running. The backend is exposed on port `8000` and the frontend on port `3000`.

### 5. Setting up a Reverse Proxy (Nginx) & SSL
For production, you should never serve raw ports. You need to expose your app on standard HTTP/HTTPS ports (80/443) using a domain name:
1. Point your domain A records (e.g., `app.yourdomain.com` and `api.yourdomain.com`) to your server's IP address.
2. Install Nginx:
   ```bash
   sudo apt install nginx -y
   ```
3. Configure Nginx virtual hosts to proxy traffic to ports `3000` (frontend) and `8000` (backend).
4. Use **Certbot** to automatically install Let's Encrypt SSL certificates:
   ```bash
   sudo apt install certbot python3-certbot-nginx -y
   sudo certbot --nginx
   ```

---

## Your Live Deployment

| Service | URL |
|---------|-----|
| **Frontend** | https://recruiter-ai-wine.vercel.app |
| **Backend API** | https://recruiter-ai-api-f75t.onrender.com |
| **API Health Check** | https://recruiter-ai-api-f75t.onrender.com/health |
| **API Docs** | https://recruiter-ai-api-f75t.onrender.com/docs |

---

## Step-by-Step: Commit Code & Configure Env Vars for Production

### Step 1 — Commit Your Code (Never Commit `.env`)

Your `.gitignore` already excludes `.env`. Always verify before pushing:

```bash
git status
```

You should **NOT** see `.env` listed. If it appears, remove it from tracking:
```bash
git rm --cached .env
```

Then commit and push all code changes:
```bash
git add .
git commit -m "fix: db connection, ssl config, windows asyncio policy"
git push origin main
```

> **Never commit your `.env` file.** It contains real passwords and API keys. Only `.env.example` (with placeholder values) should be in git.

---

### Step 2 — Add Environment Variables on Render (Backend)

Render does **not** read your local `.env`. You must add each variable manually in the dashboard.

1. Go to [Render Dashboard](https://dashboard.render.com) → open your backend service.
2. Click **Environment** in the left sidebar.
3. Add each variable below:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | `postgresql+asyncpg://postgres.lwvthtzojxhfivndkxyq:Supabase%40123@aws-1-ap-south-1.pooler.supabase.com:5432/postgres` |
| `SUPABASE_URL` | `https://lwvthtzojxhfivndkxyq.supabase.co` |
| `SUPABASE_ANON_KEY` | *(copy from Supabase Dashboard → Settings → API)* |
| `TELEGRAM_BOT_TOKEN` | *(your bot token)* |
| `TELEGRAM_CHAT_ID` | *(your chat ID)* |
| `NOTION_API_KEY` | *(your Notion integration key)* |
| `NOTION_DATABASE_ID` | *(your Notion DB ID)* |
| `ANTHROPIC_API_KEY` | *(optional — for AI outreach generation)* |
| `APOLLO_API_KEY` | *(optional — for recruiter scraping)* |
| `HUNTER_API_KEY` | *(optional — for email finding)* |
| `FRONTEND_URL` | `https://recruiter-ai-wine.vercel.app` |
| `BACKEND_URL` | `https://recruiter-ai-api-f75t.onrender.com` |
| `APP_ENV` | `production` |

4. Click **Save Changes** — Render will automatically redeploy. Wait for the **"Live"** status badge.

---

### Step 3 — Add Environment Variables on Vercel (Frontend)

1. Go to [Vercel Dashboard](https://vercel.com/dashboard) → open your frontend project.
2. Click **Settings** → **Environment Variables**.
3. Add this variable:

| Key | Value |
|-----|-------|
| `NEXT_PUBLIC_BACKEND_URL` | `https://recruiter-ai-api-f75t.onrender.com` |

4. Click **Save**.
5. Go to **Deployments** → click `···` next to your latest deployment → **Redeploy**.

> A redeploy is **mandatory** — Next.js bakes `NEXT_PUBLIC_` variables into the build bundle, so just saving them is not enough.

---

### Step 4 — Verify Everything Works

```bash
# 1. Backend health check
curl https://recruiter-ai-api-f75t.onrender.com/health
# Expected: {"status":"ok","version":"1.0.0","env":"production"}

# 2. Open API docs in browser
# https://recruiter-ai-api-f75t.onrender.com/docs

# 3. Open frontend and check DevTools → Network tab
# API calls should go to recruiter-ai-api-f75t.onrender.com — NOT localhost
```

> **Note:** Render free-tier services spin down after 15 minutes of inactivity. The first request after a spin-down can take 30–60 seconds. This is normal on the free plan.

