from ldap3 import Server, Connection, ALL, SIMPLE

def findUser(address, username, password, user):
    server = Server(address, get_info=ALL)
    conn = Connection(server, user=username, password=password, authentication=SIMPLE)
    if not conn.bind():
        print('Failed to authenticate.')
        return False
    if not conn.search('ou=users,dc=example,dc=com', f'(uid={user})'):
        print('Not found.')
        return False
    else:
        print('Found.')
        return True


def authenticate(address, username, password):
    server = Server(address, get_info=ALL)
    # conn = Connection(server, user='cn=admin,dc=example,dc=com', password='admin', auto_bind=True)

    # if not conn.bind():
    #     print('Failed to bind to server.')
    #     return False

    # if not conn.search('ou=users,dc=example,dc=com', f'(uid=testuser)'):
    #     print('Not found.')
    #     return False
    conn = Connection(server, user=username, password=password, authentication=SIMPLE)
    if not conn.bind():
        print('Failed to authenticate.')
        return False

    return True

address = 'ldap://localhost:389'
# username = 'uid=testuser,ou=users,dc=example,dc=com'
# password = 'password'
username = 'cn=admin,dc=example,dc=com'
password = 'admin'
if authenticate(address, username, password):
    print('Authentication succeeded.')
    findUser(address, username, password, 'testuser')
else:
    print('Authentication failed.')
