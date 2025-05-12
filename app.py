from flask import Flask, render_template, request
from flask_mail import Mail, Message
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Flask-Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'khdundun@gmail.com'
app.config['MAIL_PASSWORD'] = 'aygu geql ldxn fiam'
app.config['MAIL_DEFAULT_SENDER'] = 'khdundun@gmail.com'

# Enable file uploads
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admission')
def admission():
    return render_template('admission.html')

@app.route('/album')
def album():
    return render_template('album.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    try:
        # Collect form data
        full_name = request.form['fullName']
        dob = request.form['dob']
        aadhaar = request.form['aadhaar']
        gender = request.form['gender']
        guardian_name = request.form['guardianName']
        guardian_phone = request.form['guardianPhone']
        guardian_email = request.form.get('guardianEmail', 'Not Provided')
        school_name = request.form['schoolName']

        # Handle file uploads
        photo_file = request.files.get('photo')
        marksheet_file = request.files.get('marksheet')

        photo_path = ''
        marksheet_path = ''

        if photo_file:
            photo_filename = secure_filename(photo_file.filename)
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_filename)
            photo_file.save(photo_path)

        if marksheet_file:
            marksheet_filename = secure_filename(marksheet_file.filename)
            marksheet_path = os.path.join(app.config['UPLOAD_FOLDER'], marksheet_filename)
            marksheet_file.save(marksheet_path)

        # Email content
        subject = f"New Admission Form Submission - {full_name}"
        body = f"""
📄 New Admission Application Received:

👤 Full Name: {full_name}
🎂 Date of Birth: {dob}
🆔 Aadhaar: {aadhaar}
⚧️ Gender: {gender}

👪 Guardian Name: {guardian_name}
📞 Guardian Phone: {guardian_phone}
📧 Guardian Email: {guardian_email}

🏫 Previous School: {school_name}
📸 Photo: {photo_path or 'Not Uploaded'}
📑 Marksheet: {marksheet_path or 'Not Uploaded'}
        """

        # Send email
        msg = Message(subject, recipients=['yumnamjaichandra1243@gmail.com'])
        msg.body = body

        # Attach files
        if photo_path:
            with open(photo_path, 'rb') as f:
                msg.attach(photo_filename, photo_file.mimetype, f.read())
        if marksheet_path:
            with open(marksheet_path, 'rb') as f:
                msg.attach(marksheet_filename, marksheet_file.mimetype, f.read())

        mail.send(msg)
        return "✅ Application submitted successfully!"

    except Exception as e:
        return f"❌ Error: {str(e)}"

@app.route('/send_hostel_email', methods=['POST'])
def send_hostel_email():
    try:
        # Collect hostel form data
        full_name = request.form['hostelFullName']
        dob = request.form['hostelDob']
        mobile = request.form['hostelMobile']
        gender = request.form['hostelGender']
        class_applied = request.form['hostelClass']

        # Email content
        subject = f"🏠 Hostel Application - {full_name}"
        body = f"""
📬 Hostel Application Received:

👤 Full Name: {full_name}
🎂 Date of Birth: {dob}
📱 Mobile: {mobile}
⚧️ Gender: {gender}
🎓 Class Applied: {class_applied}
        """

        msg = Message(subject, recipients=['yumnamjaichandra1243@gmail.com'])
        msg.body = body
        mail.send(msg)

        return render_template('thankyou.html')

    except Exception as e:
        return f"❌ Hostel form error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
