#!/bin/bash
set -e

cat >> "$PGDATA/pg_hba.conf" <<'EOF'
# allow physical replication from docker network
host    replication     repl        172.22.0.0/16     scram-sha-256

# allow logical initial table copy
host    appdb           repl        172.22.0.0/16     scram-sha-256
EOF
