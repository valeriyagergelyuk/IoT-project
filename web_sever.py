from flask import Flask
app = Flask(__name__)

@app.route("/") #This is the route you specify (in our case it is likely just / for now)
def home(): #When the route is called it would run this method
    return 'Welcome to the home page <h1>HELLO</h1>' #What the method runs

if __name__ == "__main__":
    app.run() #This part should be at the end at all times as anything under won't be ran