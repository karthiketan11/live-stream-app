from flask import Flask, render_template, request, redirect, url_for, session, Response
import cv2
import secrets

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# Store the generated key
generated_key = None

@app.route('/login', methods=['GET', 'POST'])
def login():
    global generated_key
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'password':  # Example check
            generated_key = secrets.token_hex(16)  # Generate a secure random key
            session['logged_in'] = True
            return redirect(url_for('stream'))
    return render_template('login.html')

@app.route('/stream')
def stream():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('stream.html', key=generated_key)

@app.route('/video_feed/<key>')
def video_feed(key):
    if key != generated_key:
        return "Access Denied", 403
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def generate_frames():
    camera = cv2.VideoCapture(0)  # Open the default camera
    while True:
        success, frame = camera.read()  # Read a frame from the camera
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # Yield the frame

# Remove the following block for Vercel deployment
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5001)  # Allow access from other devices 