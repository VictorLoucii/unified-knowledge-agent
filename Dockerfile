# backend.Dockerfile in root
# Use Python 3.12 (matching your __pycache__ version)
FROM python:3.12-slim

# Install uv directly from the official Astral image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set the working directory inside the container
WORKDIR /app

# Step 1: Copy ONLY the dependency files first. 
# This leverages Docker's layer caching so you don't redownload packages every time you change a line of code.
COPY pyproject.toml uv.lock ./

# Step 2: Install dependencies.
# The --frozen flag forces uv to strictly use the uv.lock file (guaranteeing the CPU-only PyTorch!).
# The --no-install-project flag skips installing the project directory itself as a package.
RUN uv sync --frozen --no-install-project

# Step 3: Copy your actual backend application code
COPY backend/ ./backend/

# Step 4: Copy the data folder so the RAG engine has its source files
COPY data/ ./data/

# Make sure the virtual environment created by uv is on the system PATH
ENV PATH="/app/.venv/bin:$PATH"

# Expose the port FastAPI runs on
EXPOSE 7860

# Start the server (pointing to app.py inside the backend folder)
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "7860"]