# Chaos Wealth Navigator

This project is a financial modeling tool designed to simulate wealth accumulation over time, incorporating elements of luck and chaos theory to provide a more dynamic and realistic projection.

## Features

- **Financial Modeling:** Simulate income, expenditure, savings, and debt over a specified period.
- **Luck Factor:** Introduce variability based on a chosen luck level (unlucky, neutral, lucky) to see how random events can impact financial outcomes.
- **Chaos Theory Elements:** Incorporate non-linear dynamics to reflect the unpredictable nature of real-world financial systems.
- **Detailed Results:** View year-by-year breakdown of financial status.
- **Summary Statistics:** Get an overview of the simulation, including total growth, highest/lowest savings, and years in debt.

## Local Setup

To run this project locally, you need to set up both the frontend (React) and the backend (Python).

### Prerequisites

- Node.js and npm/yarn/bun
- Python 3.x
- pip

### Backend Setup

1. Navigate to the backend directory (assuming it's in the project root or a specific backend folder).
   ```bash
   cd /Users/shashank/Desktop/Personal/website/financial_modeling
   # Or if backend is in a subfolder, e.g., api:
   # cd /Users/shashank/Desktop/Personal/website/financial_modeling/api
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the backend server (replace `your_backend_script.py` with the actual entry point, e.g., `api.py` or `financial_modeling.py`):
   ```bash
   python your_backend_script.py
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd /Users/shashank/Desktop/Personal/website/financial_modeling/chaos-wealth-navigator
   ```
2. Install frontend dependencies (using bun as seen in `bun.lockb`):
   ```bash
   bun install
   ```
3. Start the development server:
   ```bash
   bun run dev
   ```

The frontend should now be running, likely accessible at `http://localhost:5173/` or similar.

## Deployment on Vercel

Deploying a project with both a frontend and a Python backend on Vercel requires configuring Vercel to handle both parts. Vercel is primarily designed for serverless functions for backend code.

1. **Project Structure:** Ensure your project structure is suitable for Vercel. A common pattern is to have your frontend in a subdirectory (like `chaos-wealth-navigator`) and your backend code (e.g., API endpoints) structured to be recognized as serverless functions.

2. **Vercel Configuration (`vercel.json`):** You might need a `vercel.json` file in your project root to tell Vercel how to build and serve your application. This file can define routes to forward API requests to your Python functions.

   Example `vercel.json`:
   ```json
   {
     "rewrites": [
       { "source": "/api/(.*)", "destination": "/api" }
     ],
     "builds": [
       { "src": "api/api.py", "use": "@vercel/python" }
     ]
   }
   ```
   *Note: This is a basic example. Your actual configuration will depend on how your Python backend is structured and which framework (Flask, FastAPI, etc.) you use.* Vercel's Python runtime expects a file (like `api.py`) that contains a serverless function handler.

3. **Adapt Python Backend:** Your Python backend code might need modifications to work as Vercel serverless functions. This often involves using a framework compatible with serverless environments (like Flask or FastAPI) and exposing specific handler functions.

4. **Deployment:** Connect your Git repository (GitHub, GitLab, Bitbucket) to Vercel. Vercel will automatically detect the framework and deploy. You may need to adjust build settings or environment variables in the Vercel dashboard.

Refer to the official Vercel documentation for detailed guides on deploying Python applications and configuring monorepos or projects with multiple parts.