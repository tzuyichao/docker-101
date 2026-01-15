#!/bin/bash
set -euo pipefail

# 等 primary 起來
until pg_isready -h region2_primary -p 5432 -U postgres >/dev/null 2>&1; do
  echo "waiting for region2_primary ..."
  sleep 1
done

# 確保資料目錄權限正確（以防第一次是 root 建的目錄）
mkdir -p /var/lib/postgresql/data
chown -R postgres:postgres /var/lib/postgresql/data
chmod 700 /var/lib/postgresql/data

# 如果 data dir 是空的，做 basebackup（用 postgres 身分）
if [ -z "$(ls -A /var/lib/postgresql/data 2>/dev/null || true)" ]; then
  echo "running pg_basebackup..."
  export PGPASSWORD=repl_r2_phy_pwd
  gosu postgres pg_basebackup \
    -h region2_primary -p 5432 -U repl_r2_phy \
    -D /var/lib/postgresql/data \
    -Fp -Xs -P -R
fi

echo "starting region2 standby..."
exec gosu postgres postgres -c hot_standby=on -c wal_level=replica -c max_wal_senders=10 -c max_replication_slots=10 -c listen_addresses='*'
