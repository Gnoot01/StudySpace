from libdw import pyrebase

# Copying reference url at the top
dburl = ""
email = ""
password = ""
apikey = ""
authdomain = dburl.replace("https://","")


config = {
    "apiKey": apikey,
    "authDomain": authdomain,
    "databaseURL": dburl,
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
user = auth.sign_in_with_email_and_password(email, password)
db = firebase.database()
user = auth.refresh(user['refreshToken'])

key = "data"
node = db.child(key)

while True:

    user_input = input("Enter a value: ")
    # Setting value in node
    node.set(user_input, user['idToken'])
    
    # Get k (.key()), v(.val()) from node
    # node.get(user['idToken'])




###my_stream.close()

