

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_mail import Mail, Message
import os
import json
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import uuid
app = Flask(__name__)

app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False

# Load environment variables
load_dotenv()

app.secret_key = os.getenv('SECRET_KEY', 'fallback_secret')

# === Flask-Mail Configuration ===
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

mail = Mail(app)

SITE_DATA_PATH = 'data/site_data.json'
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# === Load & Save Site Data ===
def load_site_data():
    with open(SITE_DATA_PATH, 'r') as f:
        return json.load(f)

def save_site_data(data):
    with open(SITE_DATA_PATH, 'w') as f:
        json.dump(data, f, indent=2)

# === Inject layout ===
@app.context_processor
def inject_layout():
    site_data = load_site_data()
    return dict(layout=site_data.get('layout', {}))

ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')

@app.route('/')
def index():
    site_data = load_site_data()
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
    site_data = load_site_data()
    return render_template('admission.html',
        admission_section=site_data.get('admission_section', {}),
        hostel_album=site_data.get('hostel_carousel_images', []),
        hostel_features=site_data.get('hostel_features', [])
    )

@app.route('/album')
def album():
    site_data = load_site_data()
    return render_template('album.html', album=site_data.get('album', []))

@app.route('/faculties')
def faculties():
    site_data = load_site_data()
    return render_template('faculties.html', faculties_section=site_data.get('faculties_section', []))

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            session.permanent = True  # ✅ This ensures session survives across multiple requests
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin_login.html', error="Invalid credentials")
    return render_template('admin_login.html')


@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    site_data = load_site_data()
    return render_template('admin_dashboard.html', data=site_data)

# === Utility for saving images ===
def save_uploaded_file(file):
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    return filepath



# === Dynamic JSON update (textarea based) ===
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
def update_about_section():
    try:
        site_data = load_site_data()

        site_data['about_section']['title'] = request.form['title']
        site_data['about_section']['paragraphs'] = request.form.getlist('paragraphs')

        # Handle file uploads
        if 'carousel_images' in request.files:
            new_images = []
            for file in request.files.getlist('carousel_images'):
                if file.filename:
                    filepath = save_uploaded_file(file)
                    if filepath:
                        new_images.append(filepath)
            if new_images:
                site_data['about_section']['carousel_images'] = new_images

        save_site_data(site_data)
        flash('About section updated successfully!', 'success')
    except Exception as e:
        flash(f'Error updating about section: {str(e)}', 'error')

    return redirect(url_for('admin_dashboard', _anchor='tab-about_section'))


@app.route('/admin/update/heads_section', methods=['POST'])
def update_heads_section():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    try:
        updated_cards = []
        i = 0
        while f'name_{i}' in request.form:
            card = {
                'name': request.form[f'name_{i}'],
                'role': request.form[f'role_{i}'],
                'popup_title': request.form[f'popup_title_{i}'],
                'popup_text': request.form[f'popup_text_{i}'],
                'side': request.form[f'side_{i}'],
                'image': request.form.get(f'image_{i}', '')  # fallback to existing
            }

            if f'image_file_{i}' in request.files:
                file = request.files[f'image_file_{i}']
                if file and file.filename:
                    filepath = save_uploaded_file(file)
                    if filepath:
                        card['image'] = filepath

            updated_cards.append(card)
            i += 1

        data = load_site_data()
        data['heads_section']['cards'] = updated_cards
        save_site_data(data)
        flash("✅ Heads section updated successfully", "success")

    except Exception as e:
        flash(f"❌ Error updating heads section: {str(e)}", "error")

    return redirect(url_for('admin_dashboard', _anchor='heads_section'))

def ordinal(n):
    """Return ordinal string like '1st Position', '2nd Position'."""
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return f"{n}{suffix} Position"

@app.route("/admin/update/state_toppers", methods=["POST"])
def update_state_toppers():
    with open("data/site_data.json", "r") as f:
        data = json.load(f)

    updated = []
    index = 0
    while True:
        name_key = f"name_{index}"
        rank_key = f"rank_{index}"
        image_key = f"image_existing_{index}"
        file_key = f"image_file_{index}"

        if name_key not in request.form:
            break

        name = request.form.get(name_key, "").strip()
        rank_raw = request.form.get(rank_key, "").strip()
        existing_image = request.form.get(image_key, "")

        # Convert to ordinal rank
        try:
            rank_int = int(rank_raw)
            rank = ordinal(rank_int)
        except ValueError:
            rank = rank_raw  # Fallback if not integer

        # Image handling
        if file_key in request.files and request.files[file_key].filename:
            file = request.files[file_key]
            filename = secure_filename(file.filename)
            file_path = os.path.join("static/images", filename)
            file.save(file_path)
            image_url = f"/static/images/{filename}"
        else:
            image_url = existing_image

        updated.append({
            "name": name,
            "rank": rank,
            "image": image_url
        })
        index += 1

    data["state_toppers"] = updated

    with open("data/site_data.json", "w") as f:
        json.dump(data, f, indent=2)

    flash("✅ State Toppers Updated Successfully", "success")
    return redirect(url_for('admin_dashboard', _anchor='tab-state_toppers'))


def ordinal(n):
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return f"{n}{suffix} Position"

@app.route("/admin/update/state_topper_add", methods=["POST"])
def add_state_topper():
    with open("data/site_data.json", "r") as f:
        data = json.load(f)

    name = request.form.get("new_name", "").strip()
    rank_input = request.form.get("new_rank", "").strip()
    image_url = ""

    # Convert rank input to ordinal
    try:
        rank_int = int(rank_input)
        rank = ordinal(rank_int)
    except ValueError:
        rank = rank_input  # fallback in case input is not valid int

    if "new_image" in request.files and request.files["new_image"].filename:
        file = request.files["new_image"]
        filename = secure_filename(file.filename)
        file_path = os.path.join("static/images", filename)
        file.save(file_path)
        image_url = f"/static/images/{filename}"

    new_topper = {
        "name": name,
        "rank": rank,
        "image": image_url
    }

    data.setdefault("state_toppers", []).append(new_topper)

    with open("data/site_data.json", "w") as f:
        json.dump(data, f, indent=2)

    flash("✅ New State Topper Added", "success")
    return redirect(url_for('admin_dashboard', _anchor='tab-state_toppers'))



@app.route("/admin/delete/state_topper/<int:index>", methods=["POST"])
def delete_state_topper(index):
    with open("data/site_data.json", "r") as f:
        data = json.load(f)

    try:
        image_path = data["state_toppers"][index]["image"].lstrip("/")
        full_image_path = os.path.join(os.getcwd(), image_path)
        if os.path.exists(full_image_path):
            os.remove(full_image_path)

        data["state_toppers"].pop(index)
        with open("data/site_data.json", "w") as f:
            json.dump(data, f, indent=2)

        flash("✅ State Topper Deleted", "success")
    except IndexError:
        flash("❌ Invalid index", "error")
    except Exception as e:
        flash(f"❌ Error deleting image: {e}", "error")

    return redirect(url_for('admin_dashboard'))



@app.route('/admin/update/subject_toppers', methods=['POST'])
def update_subject_toppers():
    try:
        data = load_site_data()
        subject_toppers = {}
        count = int(request.form.get('count', 0))

        for i in range(count):
            year = request.form[f'year_{i}']
            title = request.form[f'title_{i}']
            image = request.form.get(f'image_existing_{i}', '')

            if f'image_{i}' in request.files:
                file = request.files[f'image_{i}']
                if file and file.filename:
                    filename = secure_filename(file.filename)
                    filepath = os.path.join('static/images', filename)
                    file.save(filepath)
                    image = f"/static/images/{filename}"

            subject_toppers[year] = {
                'title': title,
                'image': image
            }

        data['subject_toppers'] = subject_toppers
        save_site_data(data)
        flash('✅ Subject toppers updated successfully!', 'success')

    except Exception as e:
        flash(f'❌ Error updating subject toppers: {str(e)}', 'error')

    return redirect(url_for('admin_dashboard', _anchor='tab-subject_toppers'))


@app.route('/admin/update/subject_toppers_add', methods=['POST'])
def add_subject_topper():
    try:
        data = load_site_data()
        year = request.form['new_year']
        title = request.form['new_title']
        image_url = ""

        if "new_image" in request.files and request.files["new_image"].filename:
            file = request.files["new_image"]
            filename = secure_filename(file.filename)
            file_path = os.path.join("static/images", filename)
            file.save(file_path)
            image_url = f"/static/images/{filename}"

        data.setdefault('subject_toppers', {})[year] = {
            'title': title,
            'image': image_url
        }

        save_site_data(data)
        flash("✅ New subject topper added!", "success")

    except Exception as e:
        flash(f"❌ Error adding subject topper: {str(e)}", "error")

    return redirect(url_for('admin_dashboard', _anchor='tab-subject_toppers'))


@app.route('/admin/delete/subject_topper/<year>', methods=['POST'])
def delete_subject_topper(year):
    try:
        data = load_site_data()
        if year in data.get('subject_toppers', {}):
            del data['subject_toppers'][year]
            save_site_data(data)
            flash(f"✅ Subject topper for {year} deleted", "success")
        else:
            flash("❌ Year not found", "error")

    except Exception as e:
        flash(f"❌ Error deleting subject topper: {str(e)}", "error")

    return redirect(url_for('admin_dashboard', _anchor='tab-subject_toppers'))





@app.route('/admin/update/ad_section', methods=['POST'])
def update_ad_section():
    try:
        data = load_site_data()

        # Handle left image
        if 'left_image' in request.files:
            file = request.files['left_image']
            if file.filename:
                filename = secure_filename(file.filename)
                filepath = os.path.join("static/images", filename)
                file.save(filepath)
                data['ad_section']['left_image'] = f"/static/images/{filename}"

        # Handle right image
        if 'right_image' in request.files:
            file = request.files['right_image']
            if file.filename:
                filename = secure_filename(file.filename)
                filepath = os.path.join("static/images", filename)
                file.save(filepath)
                data['ad_section']['right_image'] = f"/static/images/{filename}"

        save_site_data(data)
        flash('✅ Ad section updated successfully!', 'success')
    except Exception as e:
        flash(f'❌ Error updating ad section: {str(e)}', 'error')

    return redirect(url_for('admin_dashboard', _anchor='tab-ad_section'))


@app.route('/admin/update/faculty_edit', methods=['POST'])
def update_faculty():
    try:
        site_data = load_site_data()
        faculty_id = request.form['id']
        for faculty in site_data['faculties_section']:
            if faculty['id'] == faculty_id:
                faculty['name'] = request.form['name']
                faculty['subject'] = request.form['subject']
                faculty['qualification'] = request.form['qualification']
                if 'image' in request.files:
                    file = request.files['image']
                    if file.filename:
                        filepath = save_uploaded_file(file)
                        if filepath:
                            faculty['image'] = filepath
                break
        save_site_data(site_data)
        flash('Faculty updated successfully!', 'success')
    except Exception as e:
        flash(f'Error updating faculty: {str(e)}', 'error')
    return redirect(url_for('admin_dashboard', _anchor='tab-faculties_section'))

@app.route('/admin/update/faculty_add', methods=['POST'])
def add_faculty():
    try:
        site_data = load_site_data()
        existing_ids = [int(f['id'].split('-')[1]) for f in site_data['faculties_section'] if f['id'].startswith('T-') and f['id'].split('-')[1].isdigit()]
        new_id = f"T-{max(existing_ids, default=0) + 1}"

        image_path = ''
        if 'image' in request.files:
            file = request.files['image']
            if file.filename:
                filepath = save_uploaded_file(file)
                if filepath:
                    image_path = filepath

        new_faculty = {
            'id': new_id,
            'name': request.form['name'],
            'subject': request.form['subject'],
            'qualification': request.form['qualification'],
            'image': image_path
        }

        site_data['faculties_section'].append(new_faculty)
        save_site_data(site_data)
        flash('Faculty added successfully!', 'success')
    except Exception as e:
        flash(f'Error adding faculty: {str(e)}', 'error')
    return redirect(url_for('admin_dashboard', _anchor='tab-faculties_section'))

@app.route('/admin/delete/faculty/<faculty_id>', methods=['POST'])
def delete_faculty(faculty_id):
    try:
        site_data = load_site_data()
        site_data['faculties_section'] = [f for f in site_data['faculties_section'] if f['id'] != faculty_id]
        save_site_data(site_data)
        flash('Faculty deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting faculty: {str(e)}', 'error')
    return redirect(url_for('admin_dashboard', _anchor='tab-faculties_section'))





@app.route('/admin/update/album', methods=['POST'])
def update_album():
    try:
        updated_album = []
        i = 0
        while f'caption_{i}' in request.form:
            album_item = {
                'id': f"A-{i+1}",
                'caption': request.form[f'caption_{i}'],
                'image': data['album'][i]['image'] if i < len(data['album']) else ''
            }
            
            # Handle image upload
            if f'image_{i}' in request.files:
                file = request.files[f'image_{i}']
                if file.filename:
                    filepath = save_uploaded_file(file)
                    if filepath:
                        album_item['image'] = filepath
            
            updated_album.append(album_item)
            i += 1
        
        data['album'] = updated_album
        save_data()
        flash('Album updated successfully!', 'success')
    except Exception as e:
        flash(f'Error updating album: {str(e)}', 'error')
    
    return redirect(url_for('admin_dashboard', _anchor='tab-album'))

@app.route('/admin/update/admission_section', methods=['POST'])
def update_admission_section():
    try:
        data['admission_section']['rules'] = request.form.getlist('rules')
        save_data()
        flash('Admission section updated successfully!', 'success')
    except Exception as e:
        flash(f'Error updating admission section: {str(e)}', 'error')
    
    return redirect(url_for('admin_dashboard', _anchor='tab-admission_section'))

@app.route('/admin/update/hostel_carousel', methods=['POST'])
def update_hostel_carousel():
    try:
        updated_images = []
        i = 0
        while f'image_{i}' in request.files:
            file = request.files[f'image_{i}']
            if file.filename:
                filepath = save_uploaded_file(file)
                if filepath:
                    updated_images.append(filepath)
            i += 1
        
        if updated_images:
            data['hostel_carousel_images'] = updated_images
            save_data()
            flash('Hostel carousel updated successfully!', 'success')
        else:
            flash('No new images were uploaded', 'info')
    except Exception as e:
        flash(f'Error updating hostel carousel: {str(e)}', 'error')
    
    return redirect(url_for('admin_dashboard', _anchor='tab-hostel_carousel_images'))

@app.route('/admin/update/map_section', methods=['POST'])
def update_map_section():
    try:
        data['map_section']['title'] = request.form['title']
        data['map_section']['iframe_src'] = request.form['iframe_src']
        save_data()
        flash('Map section updated successfully!', 'success')
    except Exception as e:
        flash(f'Error updating map section: {str(e)}', 'error')
    
    return redirect(url_for('admin_dashboard', _anchor='tab-map_section'))

@app.route('/admin/update/layout', methods=['POST'])
def update_layout():
    try:
        # Update social links
        data['layout']['footer']['social_links']['facebook'] = request.form['social_facebook']
        data['layout']['footer']['social_links']['twitter'] = request.form['social_twitter']
        data['layout']['footer']['social_links']['instagram'] = request.form['social_instagram']
        
        # Update contact info
        data['layout']['footer']['contact_email'] = request.form['contact_email']
        data['layout']['footer']['contact_phone'] = request.form['contact_phone']
        data['layout']['footer']['contact_address'] = request.form['contact_address']
        
        # Update copyright
        data['layout']['footer']['copyright'] = request.form['copyright']
        
        save_data()
        flash('Layout & footer updated successfully!', 'success')
    except Exception as e:
        flash(f'Error updating layout: {str(e)}', 'error')
    
    return redirect(url_for('admin_dashboard', _anchor='tab-layout'))
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
