# ==============================================================================
# Brainstorm E5 Clean-Room Scientific Reproduction Container (ARCH-RFC-001/006)
# ==============================================================================
# Reproduces all deterministic simulations, invariant proofs, and verification
# gates in a fresh environment without host dependencies.
#
# Build & Run:
#   docker build -t brainstorm-repro -f sim/Dockerfile .
#   docker run --rm brainstorm-repro
# ==============================================================================

FROM python:3.11-slim

WORKDIR /workspace

# Install minimal system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install pinned simulation dependencies
COPY sim/requirements.lock /workspace/sim/requirements.lock
RUN pip install --no-cache-dir -r /workspace/sim/requirements.lock

# Copy repository tree
COPY . /workspace/

ENV PYTHONPATH=/workspace
ENV PYTHONUNBUFFERED=1

# Execute master reproducibility verification
CMD ["python", "sim/run_all_reproducibility.py"]
