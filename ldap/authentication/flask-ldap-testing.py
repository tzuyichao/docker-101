from flask import Flask, request
from flask_ldapconn import LDAP, LDAPException

app = Flask(__name__)

# 設定 LDAP 配置
app.config['LDAP_HOST'] = 'ldap://localhost:389'
app.config['LDAP_BASE_DN'] = 'dc=example,dc=com'
app.config['LDAP_USERNAME'] = 'cn=admin,dc=example,dc=com'
app.config['LDAP_PASSWORD'] = 'admin'
app.config['LDAP_USER_OBJECT_FILTER'] = '(&(objectclass=person)(uid=%s))'

# 初始化 Flask-LDAPConn
ldap_conn = LDAP(app)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    try:
        user = ldap_conn.authenticate(username, password)

        if user is not None:
            return 'Authentication succeeded.'
        else:
            return 'Authentication failed.'

    except LDAPException as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
