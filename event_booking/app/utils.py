from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password):
    return generate_password_hash(password)

def verify_password(password, hashed):
    return check_password_hash(hashed, password)

def format_currency(value):
    return "${:,.2f}".format(value)

def is_admin(user):
    return user.role == 'admin'
