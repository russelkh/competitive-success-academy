from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_mail import Mail, Message
import os
import json
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import uuid


# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'fallback_secret')

# === Flask-Mail Configuration ===
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

mail = Mail(app)

# === Path to JSON Data ===
SITE_DATA_PATH = 'data/site_data.json'

UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def load_site_data():
    with open(SITE_DATA_PATH, 'r') as f:
        return json.load(f)


def save_site_data(data):
    with open(SITE_DATA_PATH, 'w') as f:
        json.dump(data, f, indent=2)

site_data = load_site_data()

@app.context_processor
def inject_layout():
    return dict(layout=site_data.get('layout', {}))

ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')

@app.route('/')
def index():
    return render_template("index.html",
        home_section=site_data.get('home_section', {}),
        about_section=site_data.get('about_section', {}),
        heads_section=site_data.get('heads_section', {}),
        state_toppers=site_data.get('state_toppers', []),
        subject_toppers=site_data.get('subject_toppers', {}),
        ad_section=site_data.get('ad_section', {}),
        map_section=site_data.get('map_section', {})
    )

@app.route('/admission')
def admission():
    return render_template('admission.html',
        admission_section=site_data.get('admission_section', {}),
        hostel_album=site_data.get('hostel_carousel_images', []),
        hostel_features=site_data.get('hostel_features', [])
    )

@app.route('/album')
def album():
    return render_template('album.html', album=site_data.get('album', []))

@app.route('/faculties')
def faculties():
    return render_template('faculties.html', faculties_section=site_data.get('faculties_section', []))

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin_login.html', error="Invalid credentials")
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    data = load_site_data()
    return render_template('admin_dashboard.html', data=data)

@app.route('/admin/update/<section>', methods=['POST'])
def update_section(section):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    try:
        updated_data = request.form['section_data']
        parsed_data = json.loads(updated_data)

        current_data = load_site_data()
        current_data[section] = parsed_data
        save_site_data(current_data)

        flash(f"✅ '{section}' updated successfully!", 'success')
    except Exception as e:
        flash(f"❌ Failed to update '{section}': {str(e)}", 'error')

    return redirect(url_for('admin_dashboard', updated='true'))

@app.route('/admin/update/about_section', methods=['POST'])
def update_about():
    data = load_site_data()

    # Fallback to old data in case parts are missing
    old_about = data.get('about_section', {})

    # === Title ===
    new_title = request.form.get('title', '').strip()
    if new_title:
        old_about['title'] = new_title

    # === Paragraphs ===
    paragraphs = [request.form.get(k) for k in sorted(request.form.keys()) if k.startswith('paragraph_')]
    paragraphs = [p for p in paragraphs if p]  # remove empty ones
    if paragraphs:
        old_about['paragraphs'] = paragraphs

    # === Carousel Images ===
    carousel_images = [request.form.get(k) for k in sorted(request.form.keys()) if k.startswith('carousel_image_')]
    carousel_images = [img for img in carousel_images if img]
    if carousel_images:
        old_about['carousel_images'] = carousel_images

    # Save updated section
    data['about_section'] = old_about
    save_site_data(data)

    return redirect(url_for('admin_dashboard', updated='true'))

@app.route('/admin/update/heads_section', methods=['POST'])
def update_heads_section():
    data = load_site_data()
    cards = []

    idx = 0
    while True:
        name = request.form.get(f'name_{idx}')
        if not name:
            break  # Stop when no more entries

        card = {
            "name": name,
            "role": request.form.get(f'role_{idx}', ''),
            "popup_title": request.form.get(f'popup_title_{idx}', ''),
            "popup_text": request.form.get(f'popup_text_{idx}', ''),
            "side": request.form.get(f'side_{idx}', 'left'),
            "image": data['heads_section']['cards'][idx]['image'] if idx < len(data['heads_section']['cards']) else ''
        }

        # Check if a new image is uploaded
        if f'image_{idx}' in request.files:
            image_file = request.files[f'image_{idx}']
            if image_file and image_file.filename:
                filename = secure_filename(image_file.filename)
                path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image_file.save(path)
                card['image'] = '/' + path.replace("\\", "/")  # Web-safe URL

        cards.append(card)
        idx += 1

    data['heads_section']['cards'] = cards
    save_site_data(data)
    return redirect(url_for('admin_dashboard', updated='true'))
@app.route('/admin/update/subject_toppers', methods=['POST'])
def update_subject_toppers():
    data = load_site_data()
    subject_toppers = {}

    idx = 0
    while True:
        year_key = f'year_{idx}'
        title_key = f'title_{idx}'
        image_key = f'image_{idx}'

        if year_key not in request.form:
            break

        year = request.form.get(year_key)
        title = request.form.get(title_key)
        image = ''

        if year in data['subject_toppers']:
            image = data['subject_toppers'][year].get('image', '')

        if image_key in request.files:
            file = request.files[image_key]
            if file and file.filename:
                filename = secure_filename(file.filename)
                path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(path)
                image = '/' + path.replace("\\", "/")

        subject_toppers[year] = {
            'title': title,
            'image': image
        }
        idx += 1

    data['subject_toppers'] = subject_toppers
    save_site_data(data)
    return redirect(url_for('admin_dashboard', updated='true'))

@app.route('/admin/update/ad_section', methods=['POST'])
def update_ad_section():
    data = load_site_data()

    # Existing image fallback
    left_image = data['ad_section'].get('left_image', '')
    right_image = data['ad_section'].get('right_image', '')

    # Handle left image upload
    if 'left_image' in request.files:
        file = request.files['left_image']
        if file and file.filename:
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            left_image = '/' + path.replace("\\", "/")

    # Handle right image upload
    if 'right_image' in request.files:
        file = request.files['right_image']
        if file and file.filename:
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            right_image = '/' + path.replace("\\", "/")

    # Update in JSON
    data['ad_section']['left_image'] = left_image
    data['ad_section']['right_image'] = right_image

    save_site_data(data)
    return redirect(url_for('admin_dashboard', updated='true'))

@app.route('/admin/update/faculty_edit', methods=['POST'])
def update_faculty():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    data = load_site_data()
    faculty_id = request.form.get('id')

    for faculty in data['faculties_section']:
        if faculty['id'] == faculty_id:
            faculty['name'] = request.form.get('name')
            faculty['subject'] = request.form.get('subject')
            faculty['qualification'] = request.form.get('qualification')

            image_file = request.files.get('image')
            if image_file and image_file.filename:
                filename = f"static/uploads/faculty_{faculty_id}.jpg"
                image_file.save(filename)
                faculty['image'] = '/' + filename

            break

    save_site_data(data)
    flash("✅ Faculty updated successfully", "success")
    return redirect(url_for('admin_dashboard'))
import uuid  # At the top of your file if not already

@app.route('/admin/update/faculty_add', methods=['POST'])
def add_faculty():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    data = load_site_data()

    new_faculty = {
        "id": str(uuid.uuid4()),
        "name": request.form.get('name'),
        "subject": request.form.get('subject'),
        "qualification": request.form.get('qualification'),
        "image": ""
    }

    image_file = request.files.get('image')
    if image_file and image_file.filename:
        filename = f"static/uploads/faculty_{new_faculty['id']}.jpg"
        image_file.save(filename)
        new_faculty['image'] = '/' + filename

    data['faculties_section'].append(new_faculty)
    save_site_data(data)
    flash("✅ New faculty added successfully", "success")
    return redirect(url_for('admin_dashboard'))
@app.route('/admin/delete/faculty/<id>', methods=['POST'])
def delete_faculty(id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    data = load_site_data()
    data['faculties_section'] = [f for f in data['faculties_section'] if f['id'] != id]
    save_site_data(data)
    flash("🗑️ Faculty deleted successfully", "success")
    return '', 204
@app.route('/admin/update/state_toppers', methods=['POST'])
def update_state_toppers():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    data = load_site_data()
    state_toppers = []
    idx = 0
    while True:
        name = request.form.get(f'name_{idx}')
        rank = request.form.get(f'rank_{idx}')
        description = request.form.get(f'description_{idx}')
        image = data['state_toppers'][idx]['image'] if idx < len(data['state_toppers']) else ''
        if f'image_{idx}' in request.files:
            file = request.files[f'image_{idx}']
            if file and file.filename:
                filename = secure_filename(file.filename)
                path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(path)
                image = '/' + path.replace("\\", "/")
        if name and rank and description:
            state_toppers.append({
                'name': name,
                'rank': rank,
                'description': description,
                'image': image
            })
            idx += 1
        else:
            break

    data['state_toppers'] = state_toppers
    save_site_data(data)
    flash("✅ State toppers updated successfully.", "success")
    return redirect(url_for('admin_dashboard', updated='true'))
@app.route('/admin/update/album', methods=['POST'])
def update_album():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    data = load_site_data()
    album = []
    idx = 0

    while True:
        caption = request.form.get(f'caption_{idx}')
        if caption is None:
            break  # No more items

        # Use existing image by default
        image = data['album']['images'][idx]['image'] if idx < len(data['album']['images']) else ''
        if f'image_{idx}' in request.files:
            file = request.files[f'image_{idx}']
            if file and file.filename:
                filename = secure_filename(file.filename)
                path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(path)
                image = '/' + path.replace("\\", "/")

        album.append({
            'id': f'A-{idx+1}',
            'image': image,
            'caption': caption
        })
        idx += 1

    data['album']['images'] = album
    save_site_data(data)
    flash("✅ Album updated successfully.", "success")
    return redirect(url_for('admin_dashboard', updated='true'))

@app.route('/admin/update/admission_section', methods=['POST'])
def update_admission_section():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    data = load_site_data()
    rules = []
    idx = 0
    while True:
        rule_text = request.form.get(f'rule_{idx}')
        if rule_text is None:
            break
        rule_text = rule_text.strip()
        if rule_text:  # Only add non-empty rules
            rules.append({
                "id": f"R-{idx + 1}",
                "text": rule_text
            })
        idx += 1

    data['admission_section']['rules'] = rules
    save_site_data(data)
    flash("✅ Admission rules updated successfully.", "success")
    return redirect(url_for('admin_dashboard', updated='true'))

@app.route('/admin/update/hostel_carousel_images', methods=['POST'])
def update_hostel_carousel_images():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    data = load_site_data()
    hostel_images = []
    idx = 0
    while True:
        # Use previous image if not replaced
        prev_image = data['hostel_carousel_images'][idx] if idx < len(data['hostel_carousel_images']) else ''
        file = request.files.get(f'image_{idx}')
        if file and file.filename:
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            hostel_images.append('/' + path.replace("\\", "/"))
        elif prev_image:
            hostel_images.append(prev_image)
        else:
            # Stop when no more images (no file and no previous image)
            break
        idx += 1

    data['hostel_carousel_images'] = hostel_images
    save_site_data(data)
    flash("✅ Hostel carousel images updated successfully.", "success")
    return redirect(url_for('admin_dashboard', updated='true'))



@app.route('/admin/update/layout', methods=['POST'])
def update_layout():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    data = load_site_data()
    footer = data['layout'].get('footer', {})

    # Update social links
    footer['social_links'] = {
        'facebook': request.form.get('social_facebook', ''),
        'twitter': request.form.get('social_twitter', ''),
        'instagram': request.form.get('social_instagram', '')
    }

    # Update contact info
    footer['contact_email'] = request.form.get('contact_email', '')
    footer['contact_phone'] = request.form.get('contact_phone', '')
    footer['contact_address'] = request.form.get('contact_address', '')

    # Update copyright
    footer['copyright'] = request.form.get('copyright', '')

    data['layout']['footer'] = footer
    save_site_data(data)
    flash("✅ Footer layout & contact info updated successfully.", "success")
    return redirect(url_for('admin_dashboard', updated='true'))
@app.route('/admin/update/map_section', methods=['POST'])
def update_map():
    data = load_site_data()
    map_data = data.get('map_section', {})

    new_title = request.form.get('map_title', '').strip()
    new_iframe = request.form.get('iframe_src', '').strip()

    if new_title:
        map_data['title'] = new_title
    if new_iframe:
        map_data['iframe_src'] = new_iframe

    data['map_section'] = map_data
    save_site_data(data)
    return redirect(url_for('admin_dashboard', updated='true'))

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

@app.route('/send_email', methods=['POST'])
def send_email():
    try:
        full_name = request.form['fullName']
        dob = request.form['dob']
        aadhaar = request.form['aadhaar']
        gender = request.form['gender']
        guardian_name = request.form['guardianName']
        guardian_phone = request.form['guardianPhone']
        guardian_email = request.form.get('guardianEmail', 'Not Provided')
        school_name = request.form['schoolName']

        photo_file = request.files.get('photo')
        marksheet_file = request.files.get('marksheet')

        subject = f"New Admission Form Submission - {full_name}"
        body = f"""
📄 New Admission Application Received:

👤 Full Name: {full_name}
🎂 Date of Birth: {dob}
🆔 Aadhaar: {aadhaar}
♂️ Gender: {gender}

👪 Guardian Name: {guardian_name}
📞 Guardian Phone: {guardian_phone}
📧 Guardian Email: {guardian_email}

🏫 Previous School: {school_name}
📸 Photo: {'Attached' if photo_file else 'Not Uploaded'}
📁 Marksheet: {'Attached' if marksheet_file else 'Not Uploaded'}
        """

        msg = Message(subject, recipients=['yumnamjaichandra1243@gmail.com'])
        msg.body = body

        if photo_file:
            msg.attach(secure_filename(photo_file.filename), photo_file.mimetype, photo_file.read())
        if marksheet_file:
            msg.attach(secure_filename(marksheet_file.filename), marksheet_file.mimetype, marksheet_file.read())

        mail.send(msg)
        return render_template('thankyou.html')

    except Exception as e:
        return f"❌ Error: {str(e)}"

@app.route('/send_hostel_email', methods=['POST'])
def send_hostel_email():
    try:
        full_name = request.form['hostelFullName']
        dob = request.form['hostelDob']
        mobile = request.form['hostelMobile']
        gender = request.form['hostelGender']
        class_applied = request.form['hostelClass']

        subject = f"🏠 Hostel Application - {full_name}"
        body = f"""
📬 Hostel Application Received:

👤 Full Name: {full_name}
🎂 Date of Birth: {dob}
📱 Mobile: {mobile}
♂️ Gender: {gender}
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
