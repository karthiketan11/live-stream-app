from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('client.html')

if __name__ == '__main__':
    app.run(port=5002)  # Run the client on a different port 