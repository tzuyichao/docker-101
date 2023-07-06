# Memo

## Running

```bash=
docker build -t ldap-test .
```


```bash=
docker run --env LDAP_ORGANISATION="My Organisation" --env LDAP_DOMAIN="example.com" --env LDAP_ADMIN_PASSWORD="admin" --env LDAP_CONFIG_PASSWORD="config" -p 389:389 -p 636:636 --rm -d ldap-test
```