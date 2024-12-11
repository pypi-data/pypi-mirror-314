FROM australia-southeast1-docker.pkg.dev/analysis-runner/images/driver:latest
COPY --from=ghcr.io/astral-sh/uv:0.5.5 /uv /uvx /bin/

# Set up working directory for the project
WORKDIR /cpg-flow

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Install the project's dependencies using the lockfile and settings
# Copy `pyproject.toml` and `uv.lock` into `/cpg-flow` explicitly
COPY pyproject.toml uv.lock /cpg-flow/

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

# Add the project source code from src/cpg-flow
ADD . /cpg-flow
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

# Place executables in the environment at the front of the path
ENV PATH="/cpg-flow/.venv/bin:$PATH"
ENV PYTHONPATH="/cpg-flow:${PYTHONPATH}"
