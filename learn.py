import bcrypt
print("start")
h = bcrypt.hashpw(b"testpassword", bcrypt.gensalt())
print("done", h)