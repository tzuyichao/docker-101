$body = @{
  name   = "pg16-appdb-items"
  config = @{
    "connector.class"                = "io.debezium.connector.postgresql.PostgresConnector"
    "topic.prefix"                   = "lab"

    "database.hostname"              = "postgres"
    "database.port"                  = "5432"
    "database.user"                  = "dbz"
    "database.password"              = "dbz"
    "database.dbname"                = "appdb"

    "plugin.name"                    = "pgoutput"
    "slot.name"                      = "dbz_slot"
    "publication.name"               = "dbz_pub"
    "publication.autocreate.mode"    = "disabled"

    "table.include.list"             = "public.items"
  }
} | ConvertTo-Json -Depth 5

Invoke-RestMethod `
  -Method Post `
  -Uri http://localhost:8083/connectors `
  -ContentType "application/json" `
  -Body $body
