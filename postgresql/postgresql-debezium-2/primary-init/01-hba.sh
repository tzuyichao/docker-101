#!/bin/bash
set -e

HBA="$PGDATA/pg_hba.conf"

cat >> "$HBA" <<'EOF'
# --- lab allow physical replication ---
host  replication  repl  0.0.0.0/0  scram-sha-256

# --- lab allow logical replication (publisher side uses replication too) ---
host  replication  dbz  0.0.0.0/0  scram-sha-256

# --- (optional) allow normal connections for debugging ---
host  all          all          0.0.0.0/0  scram-sha-256
EOF