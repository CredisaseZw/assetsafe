#!/bin/bash
# entrypoint.sh – Docker/CI entrypoint for AssetSafe.
#
# Steps:
#   1. Wait for PostgreSQL to be ready.
#   2. Run `python manage.py migrate`.
#   3. Optionally run seed_locations, seed_currencies, seed_roles.
#   4. Collect static files.
#   5. Exec the main process.
#
# If the first command argument is "celery", steps 1-4 are skipped so that
# worker/beat containers start immediately without re-running migrations.
#
# Seeding is controlled by:
#   --seed flag      – explicitly enable seeding for this run.
#   SEED_DATA=true   – environment variable that enables seeding.
#   DEVELOPMENT=true – seeding runs by default in development unless
#                      SEED_DATA is explicitly set to "false".
set -e

SEED=false
REMAINING_ARGS=()

# ── Parse flags ───────────────────────────────────────────────────────────────
for arg in "$@"; do
    case "$arg" in
        --seed)
            SEED=true
            ;;
        *)
            REMAINING_ARGS+=("$arg")
            ;;
    esac
done

if [ "${#REMAINING_ARGS[@]}" -eq 0 ]; then
    echo "Error: no command provided to entrypoint.sh." >&2
    exit 1
fi

# ── Skip migration/seeding for celery workers and beat ───────────────────────
# Celery services depend on `app` which already ran migrations at startup.
MAIN_CMD="${REMAINING_ARGS[0]}"
if [ "$MAIN_CMD" = "celery" ]; then
    exec "${REMAINING_ARGS[@]}"
fi

# ── Determine whether seeding should run ──────────────────────────────────────
# Priority: --seed flag > SEED_DATA env var > DEVELOPMENT default
if [ "$SEED" != "true" ]; then
    if [ "${SEED_DATA:-}" = "true" ]; then
        SEED=true
    elif [ "${SEED_DATA:-}" = "false" ]; then
        SEED=false
    elif [ "${DEVELOPMENT:-false}" = "true" ]; then
        # In development, seed by default unless SEED_DATA=false was explicit
        SEED=true
    fi
fi

# ── 1. Wait for PostgreSQL ────────────────────────────────────────────────────
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
MAX_RETRIES=60
RETRIES=0

echo "Waiting for PostgreSQL at ${DB_HOST}:${DB_PORT}..."
until pg_isready -h "${DB_HOST}" -p "${DB_PORT}" -q 2>/dev/null; do
    RETRIES=$((RETRIES + 1))
    if [ "$RETRIES" -ge "$MAX_RETRIES" ]; then
        echo "Error: PostgreSQL at ${DB_HOST}:${DB_PORT} did not become ready after ${MAX_RETRIES} retries." >&2
        exit 1
    fi
    echo "  PostgreSQL not ready yet – retrying in 2s... (${RETRIES}/${MAX_RETRIES})"
    sleep 2
done
echo "PostgreSQL is ready."

# ── 2. Apply migrations ───────────────────────────────────────────────────────
echo "Applying database migrations..."
python manage.py migrate --noinput
echo "Migrations applied."

# ── 3. Seed data (optional, idempotent) ──────────────────────────────────────
if [ "$SEED" = "true" ]; then
    echo "Seeding: locations..."
    python manage.py seed_locations

    echo "Seeding: currencies..."
    python manage.py seed_currencies

    echo "Seeding: roles..."
    python manage.py seed_roles

    echo "Seeding complete."
fi

# ── 4. Collect static files ───────────────────────────────────────────────────
echo "Collecting static files..."
python manage.py collectstatic --noinput

# ── 5. Hand off to the main process ──────────────────────────────────────────
exec "${REMAINING_ARGS[@]}"
