#!/bin/bash
set -e

HBA="$PGDATA/pg_hba.conf"

cat >> "$HBA" <<'EOF'
host  replication  repl_r2_phy  0.0.0.0/0  scram-sha-256
host  all          all          0.0.0.0/0  scram-sha-256
EOF
