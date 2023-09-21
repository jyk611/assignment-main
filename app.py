from flask import Flask, render_template, request, redirect, url_for
from pymysql import connections
import os
import boto3
from config import *
from flask import send_from_directory

app = Flask(__name__)
# Configure the 'templates' folder for HTML templates.
app.template_folder = 'pages'
app.static_folder = 'static'

bucket = custombucket
region = customregion

db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb

)
output = {}
table = 'students'

def getCompFiles(bucket, path):
    contents = []
    folder_prefix = path

    for image in bucket.objects.filter(Prefix=folder_prefix):
        # Extract file name without the folder prefix
        file_name = image.key[len(folder_prefix):]
        contents.append(file_name)

    return contents

@app.route("/", methods=['GET'], endpoint='index')
def index():

    return render_template('index.html')

@app.route('/s3_image/<path:filename>')
def s3_image(filename):
    # Construct the S3 URL for the image using your bucket and path
    s3_url = f'https://{custombucket}.s3.amazonaws.com/Company/{filename}'
    return send_from_directory(s3_url, filename)

@app.route("/job_listing", methods=['GET'])
def job_listing():
    # get approved company name
    return render_template('job_listing.html')

@app.route("/about", methods=['GET'])
def about():
    return render_template('about.html')

@app.route("/blog", methods=['GET'])
def blog():
    return render_template('blog.html')

@app.route("/single_blog", methods=['GET'])
def single_blog():
    return render_template('single_blog.html')

@app.route("/elements", methods=['GET'])
def elements():
    return render_template('elements.html')

@app.route("/job_details", methods=['GET'])
def job_details():
    return render_template('job_details.html')

@app.route("/contact", methods=['GET'])
def contact():
    return render_template('contact.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        gender = request.form['gender']
        email = request.form['email']
        password = request.form['password']
        ic = request.form['ic']
        programmeSelect = request.form['programmeSelect']
        tutorialGrp = request.form['tutorialGrp']
        studentID = request.form['studentID']
        cgpa = request.form['cgpa']
        ucSupervisor = request.form['ucSupervisor']

        ucSupervisor_split = ucSupervisor.split(', ')
        ucSuperName = ucSupervisor_split[0]
        ucSuperEmail = ucSupervisor_split[1]

        # Check if the email is already in the database.
        cursor = db_conn.cursor()
        cursor.execute("SELECT * FROM students WHERE stud_email=%s", (email))
        results = cursor.fetchall()
        cursor.close()

        # If the email is already in the database, return an error message to the user and display it on the register.html page.
        if len(results) > 0:
            return render_template('register.html', email_error="The email is already in use.")

        # Otherwise, check if the IC is already in the database.
        cursor = db_conn.cursor()
        cursor.execute("SELECT * FROM students WHERE ic=%s", (ic))
        results = cursor.fetchall()
        cursor.close()

        # If the IC is already in the database, return an error message to the user and display it on the register.html page.
        if len(results) > 0:
            return render_template('register.html', ic_error="The IC is already in use.")

        # Otherwise, check if the student ID is already in the database.
        cursor = db_conn.cursor()
        cursor.execute(
            "SELECT * FROM students WHERE studentID=%s", (studentID))
        results = cursor.fetchall()
        cursor.close()

        # If the student ID is already in the database, return an error message to the user and display it on the register.html page.
        if len(results) > 0:
            return render_template('register.html', studentID_error="The student ID is already in use.")

        insert_sql = "INSERT INTO students VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor = db_conn.cursor()

        try:
            cursor.execute(insert_sql, (studentID,
                                        firstName,
                                        lastName,
                                        gender,
                                        email,
                                        password,
                                        ic,
                                        programmeSelect,
                                        tutorialGrp,
                                        cgpa,
                                        ucSuperName,
                                        ucSuperEmail
                                        ))
            db_conn.commit()
            cursor.close()
            # Redirect to the homepage after successful registration
            return redirect(url_for('login'))
        except Exception as e:
            cursor.close()
            return str(e)  # Handle any database errors here

    # Fetch data from the database here
    cursor = db_conn.cursor()
    select_sql = "SELECT lectName, lectEmail FROM lecturer"
    cursor.execute(select_sql)
    data = cursor.fetchall()  # Fetch a single row
    print(data)

    return render_template('register.html', list_of_lect=data)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')

        if role == 'Student':
            # Fetch data from the database here
            cursor = db_conn.cursor()
            select_sql = "SELECT stud_email, password, firstName, studentID FROM students WHERE stud_email = %s"
            cursor.execute(select_sql, (email,))
            data = cursor.fetchone()  # Fetch a single row

            if data:
                # Data is found in the database
                stored_password = data[1]
                name = data[2]
                studID = data[3]

                if password == stored_password:
                    # Passwords match, user is authenticated
                    return render_template('index.html', user_login_name=name, studentID=studID, user_authenticated=True)
                else:
                    return render_template('login.html', pwd_error="Incorrect password. Please try again.")
            else:
                return render_template('login.html', email_login_error="Email not found. Please register or try a different email.")
        elif role == 'Company':
            # Fetch data from the database here
            cursor = db_conn.cursor()
            select_sql = "SELECT compEmail, comPassword, compName FROM company WHERE compEmail = %s"
            cursor.execute(select_sql, (email,))
            data = cursor.fetchone()  # Fetch a single row

            if data:
                # Data is found in the database
                stored_password = data[1]
                name = data[2]

                if password == stored_password:
                    # Passwords match, user is authenticated
                    return render_template('companyDashboard.html', user_authenticated=True)
                else:
                    return render_template('login.html', pwd_error="Incorrect password. Please try again.")
            else:
                return render_template('login.html', email_login_error="Email not found. Please register or try a different email.")
        elif role == 'Admin':
            # Fetch data from the database here
            cursor = db_conn.cursor()
            select_sql = "SELECT adminEmail, adminPassword, adminName FROM admin WHERE adminEmail = %s"
            cursor.execute(select_sql, (email,))
            data = cursor.fetchone()  # Fetch a single row

            if data:
                # Data is found in the database
                stored_password = data[1]
                name = data[2]

                if password == stored_password:
                    # Passwords match, user is authenticated
                    return render_template('lectDashboard.html', user_login_name=name, user_authenticated=True)
                else:
                    return render_template('login.html', pwd_error="Incorrect password. Please try again.")
            else:
                return render_template('login.html', email_login_error="Email not found. Please register or try a different email.")
        elif role == 'Lecturer':
            # Fetch data from the database here
            cursor = db_conn.cursor()
            select_sql = "SELECT lectEmail, password, lectID FROM lecturer WHERE lectEmail = %s"
            cursor.execute(select_sql, (email,))
            data = cursor.fetchone()  # Fetch a single row

            if data:
                # Data is found in the database
                stored_password = data[1]
                name = data[2]

                if password == stored_password:
                    # Passwords match, user is authenticated
                    return render_template('index.html', user_login_name=name, studentID=None, user_authenticated=True)
                else:
                    return render_template('login.html', pwd_error="Incorrect password. Please try again.")
            else:
                return render_template('login.html', email_login_error="Email not found. Please register or try a different email.")

    return render_template('login.html')


@app.route("/studentDashboard", methods=['GET'])
def studentDashboard():
    # Retrieve the studentID from the query parameters
    student_id = request.args.get('studentID')

    # Pass the studentID to the studentDashboard.html template
    return render_template('studentDashboard.html', studentID=student_id)

@app.route("/studentProfile", methods=['GET'])
def studentProfile():
    # Retrieve the studentID from the query parameters
    # student_id = request.args.get('studentID')

    # Pass the studentID to the studentDashboard.html template
    return render_template('studentProfile.html')

@app.route("/form", methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        studID = request.form['studentID']

        # put the files into array
        # use the get() method to return None if the field is not present.
        uploaded_files = [' ', ' ', ' ', ' ']
        uploaded_files[0] = request.files.get('acceptanceForm')
        uploaded_files[1] = request.files.get('parentForm')
        uploaded_files[2] = request.files.get('letterForm')
        uploaded_files[3] = request.files.get('hireEvi')

        comp_form = request.form.get('acceptanceFormFileName', None)
        parent_form = request.form.get('parentFormFileName', None)
        letter = request.form.get('letterFormFileName', None)
        hire_evi = request.form.get('hireEviFileName', None)

        # Uplaod image file in S3 
        s3 = boto3.resource('s3')

        # Create a folder or prefix for the files in S3
        # submit form and store into student s3 
        folder_name = 'Student/' + studID + "/" + "Form/"

        # Fetch data from the lecturer database
        cursor = db_conn.cursor()
        select_sql = "SELECT l.lectID \
                      FROM students s\
                      JOIN lecturer l on s.ucSuperEmail = l.lectEmail \
                      WHERE studentID = %s"
        cursor.execute(select_sql, (studID,))
        data = cursor.fetchone()  # Fetch a single row

        lecturerID = data[0]

        # submit form to lecturer
        lect_folder_name = 'Lecturer/' + lecturerID + "/" + studID + "/" + "Form/"

        list_files = []
        form_list = ['_comp_form.', '_parent_form.', '_letter.', '_hire_evi.']
        ctr = 0

        try:
            print("Data inserted in MySQL RDS... uploading image to S3...")

            for file in uploaded_files:
                if file is None:
                    list_files.append('')
                else:
                    list_files.append(file.filename)

                # if not empty
                if file and file is not None:
                    filename = file.filename.split('.')

                    # Construct the key with the folder prefix and file name
                    # student
                    stud_key = folder_name + filename[0] + form_list[ctr] + filename[1]
                    #lecture
                    lect_key = lect_folder_name + filename[0] + form_list[ctr] + filename[1]

                    # Upload the file into the specified folder
                    # to student folder
                    s3.Bucket(custombucket).put_object(Key=stud_key, Body=file)
                    # to lecturer folder
                    s3.Bucket(custombucket).put_object(Key=lect_key, Body=file)

                    # Generate the object URL
                    bucket_location = boto3.client('s3').get_bucket_location(Bucket=custombucket)
                    s3_location = (bucket_location['LocationConstraint'])

                    if s3_location is None:
                        s3_location = ''
                    else:
                        s3_location = '-' + s3_location

                ctr += 1

        except Exception as e:
            return str('bucket', str(e))

        # get the submitted form w/o reupload it into s3
        if comp_form:
            list_files[0] = comp_form

        if parent_form:
            list_files[1] = parent_form

        if letter:
            list_files[2] = letter
        
        if hire_evi:
            list_files[3] = hire_evi

        bucket = s3.Bucket(custombucket)

        return render_template('form.html', my_bucket=bucket, studentID=studID, list_of_files=list_files)

    # Retrieve the studentID from the query parameters
    student_id = request.args.get('studentID')

    return render_template('form.html', studentID=student_id)

def list_files(bucket, path):
    contents = []
    folder_prefix = path

    for object_summary in bucket.objects.filter(Prefix=folder_prefix):
        # Extract file name without the folder prefix
        file_name = object_summary.key[len(folder_prefix):]
        if file_name:
            last_modified = object_summary.last_modified
            size = object_summary.size
            contents.append({
                'file_name': file_name,
                'last_modified': last_modified,
                'size': size
            })

    return contents

@app.route("/report", methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        studID = request.form['studentID']
        reportForm_files = request.files['reportForm']

        # Uplaod image file in S3
        s3 = boto3.resource('s3')

        # Create a folder or prefix for the files in S3
        # to student s3 folder
        folder_name = 'Student/' + studID + "/" + "report/"

        # Fetch data from the lecturer database
        cursor = db_conn.cursor()
        select_sql = "SELECT l.lectID \
                      FROM students s\
                      JOIN lecturer l on s.ucSuperEmail = l.lectEmail \
                      WHERE studentID = %s"
        cursor.execute(select_sql, (studID,))
        data = cursor.fetchone()  # Fetch a single row

        lecturerID = data[0]

        # submit form to lecturer
        lect_folder_name = 'Lecturer/' + lecturerID + "/" + studID + "/" + "report/"

        try:
            print("Data inserted in MySQL RDS... uploading image to S3...")

            filename = reportForm_files.filename.split('.')

            # Construct the key with the folder prefix and file name
            stud_key = folder_name + filename[0] + "_progress_report." + filename[1]
            #lecture
            lect_key = lect_folder_name + filename[0] + "_progress_report." + filename[1]

            # Upload the file into the specified folder
            # to student folder
            s3.Bucket(custombucket).put_object(Key=stud_key, Body=reportForm_files)
            # to lecturer folder
            s3.Bucket(custombucket).put_object(Key=lect_key, Body=reportForm_files)

            # Generate the object URL
            bucket_location = boto3.client(
                's3').get_bucket_location(Bucket=custombucket)
            s3_location = (bucket_location['LocationConstraint'])

            if s3_location is None:
                s3_location = ''
            else:
                s3_location = '-' + s3_location

        except Exception as e:
            return str('bucket', str(e))

        bucket = s3.Bucket(custombucket)
        list_of_files = list_files(bucket, folder_name)

        return render_template('report.html', my_bucket=bucket, studentID=studID, list_of_files=list_of_files)

    # Retrieve the studentID from the query parameters
    studID = request.args.get('studentID')

    folder_name = 'Student/' + studID + "/" + "report/"

    # Uplaod image file in S3
    s3 = boto3.resource('s3')

    bucket = s3.Bucket(custombucket)
    list_of_files = list_files(bucket, folder_name)

    # Sort the list by last modified timestamp in descending order
    list_of_files.sort(key=lambda x: x['last_modified'], reverse=True)

    return render_template('report.html', my_bucket=bucket, studentID=studID, list_of_files=list_of_files)

@app.route("/delete", methods=['POST'])
def delete_file():
    if request.method == 'POST':
        studID = request.form['studentID']
        print(studID)
        # Get the file key to delete from the form data
        file_key = request.form['file_name']

        # Fetch data from the lecturer database
        cursor = db_conn.cursor()
        select_sql = "SELECT l.lectID \
                      FROM students s\
                      JOIN lecturer l on s.ucSuperEmail = l.lectEmail \
                      WHERE studentID = %s"
        cursor.execute(select_sql, (studID,))
        data = cursor.fetchone()  # Fetch a single row

        lecturerID = data[0]
        
        stud_file_key = 'Student/' + studID + "/" + "report/" + file_key
        lect_file_key = 'Lecturer/' + lecturerID + "/" + studID + "/" + file_key

        # Delete the file from S3
        try:
            s3 = boto3.client('s3')
            s3.delete_object(Bucket=custombucket, Key=stud_file_key)
            s3.delete_object(Bucket=custombucket, Key=lect_file_key)
            
            # Uplaod image file in S3
            s3 = boto3.resource('s3')

            folder_name = 'Student/' + studID + "/" + "report/"

            bucket = s3.Bucket(custombucket)
            list_of_files = list_files(bucket, folder_name)

            # Sort the list by last modified timestamp in descending order
            list_of_files.sort(key=lambda x: x['last_modified'], reverse=True)

            return render_template('report.html', my_bucket=bucket, studentID=studID, list_of_files=list_of_files)
        except Exception as e:
            return str(e)

# -------------------------------------------------------------- Student End --------------------------------------------------------------#


# -------------------------------------------------------------- Lecturer START (Kuah Jia Yu) --------------------------------------------------------------#

@app.route("/lectRegister", methods=['GET', 'POST'])
def lectRegister():
    if request.method == 'POST':
        lectName = request.form['lectName']
        lectID = request.form['lectID']
        lectEmail = request.form['lectEmail']
        gender = request.form['gender']
        password = request.form['password']

        insert_sql = "INSERT INTO lecturer VALUES (%s, %s, %s, %s, %s)"
        cursor = db_conn.cursor()

        try:
            cursor.execute(insert_sql, (lectName,
                                        lectID,
                                        lectEmail,
                                        gender,
                                        password
                                        ))
            db_conn.commit()
            cursor.close()
            # Go to the dashboard after successful registration
            return redirect(url_for('login'))
        except Exception as e:
            cursor.close()
            return str(e)  # Handle any database errors here
    return render_template('lectRegister.html')

@app.route("/lectDashboard", methods=['GET'])
def lectDashboard():
    # Retrieve the lecturer's email from the session
    lecturer_email = request.args.get('lectEmail')

    if lecturer_email:
        # Fetch student data based on the lecturer's email
        cursor = db_conn.cursor()
        select_students_sql = "SELECT * \
                                FROM students s\
                                JOIN lecturer l on s.ucSuperEmail = l.lectEmail \
                                WHERE l.lectEmail = %s"
        cursor.execute(select_students_sql, (lecturer_email,))
        student_data = cursor.fetchall()

        return render_template('lectDashboard.html', student_data=student_data)
    else:
        # Redirect to the login page if the lecturer is not authenticated
        return redirect(url_for('login'))

# ------------------------------------------------------------------- Lecturer END -------------------------------------------------------------------#

# ------------------------------------------------------------------- Company START (Wong Kar Yan) -------------------------------------------------------------------#


@app.route("/companyRegister", methods=['GET', 'POST'])
def companyRegister():
    if request.method == 'POST':
        compName = request.form['compName']
        compEmail = request.form['compEmail']
        comPassword = request.form['comPassword']

        # Fetch data from the database here
        cursor = db_conn.cursor()
        select_sql = "SELECT max(compID) FROM company"
        cursor.execute(select_sql)
        data = cursor.fetchone()  # Fetch a single row
        data = str(data[0])

        print(data)
        if data == None:
            compID = 'C' + str(10001)
        else:
            comp_no = int(data[1:]) + 1
            compID = 'C' + str(comp_no)

        # Check if the email is already in the database.
        cursor = db_conn.cursor()
        cursor.execute("SELECT * FROM company WHERE compEmail=%s", (compEmail))
        results = cursor.fetchall()
        cursor.close()

        # If the email is already in the database, return an error message to the user and display it on the register.html page.
        if len(results) > 0:
            return render_template('companyRegister.html', email_error="This company email is already in use.")

        insert_sql = "INSERT INTO company VALUES (%s, %s, %s, %s, %s)"
        cursor = db_conn.cursor()

        try:
            cursor.execute(insert_sql, (compID,
                                        compName,
                                        compEmail,
                                        comPassword,
                                        'pending'
                                        ))
            db_conn.commit()
            cursor.close()
            # Go to the dashboard after successful registration
            return redirect(url_for('login'))
        except Exception as e:
            cursor.close()
            return str(e)  # Handle any database errors here
    return render_template('companyRegister.html')


@app.route("/jobReg", methods=['GET', 'POST'])
def jobReg():
    if request.method == 'POST':
        comp_name = request.form['comp_name']
        job_title = request.form['job_title']
        job_desc = request.form['job_desc']
        job_req = request.form['job_req']
        sal_range = request.form['sal_range']
        contact_person_name = request.form['contact_person_name']
        contact_person_email = request.form['contact_person_email']
        contact_number = request.form['contact_number']
        comp_state = request.form['comp_state']
        companyImage = request.files['companyImage']

        insert_sql = "INSERT INTO jobApply VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor = db_conn.cursor()

        if companyImage.filename == "":
            return "Please select a file"

        cursor.execute(insert_sql, (comp_name, job_title, job_desc, job_req, sal_range,
                       contact_person_name, contact_person_email, contact_number, comp_state))
        db_conn.commit()
        cursor.close()

        # Uplaod image file in S3 #
        comp_image_file_name_in_s3 = "company-" + \
            str(comp_name) + "_image_file"
        s3 = boto3.resource('s3')

        try:
            print("Data inserted in MySQL RDS... uploading image to S3...")
            s3.Bucket(custombucket).put_object(
                Key=comp_image_file_name_in_s3, Body=companyImage)
            bucket_location = boto3.client(
                's3').get_bucket_location(Bucket=custombucket)
            s3_location = (bucket_location['LocationConstraint'])

            if s3_location is None:
                s3_location = ''
            else:
                s3_location = '-' + s3_location

            object_url = "https://s3%7B0%7D.amazonaws.com/%7B1%7D/%7B2%7D".format(
                s3_location,
                custombucket,
                comp_image_file_name_in_s3)
            return redirect(url_for('companyDashboard'))
        except Exception as e:
            cursor.close()
            print(f"Error during database insertion: {e}")
            return str(e)  # Handle any database errors here

    return render_template('jobReg.html')


@app.route("/companyDashboard", methods=['GET'])
def companyDashboard():
    return render_template('companyDashboard.html')

# ------------------------------------------------------------------- Company END -------------------------------------------------------------------#

# Define the route for admin registration
@app.route("/adminRegister", methods=['GET', 'POST'])
def adminRegister():
    if request.method == 'POST':
        adminName = request.form['adminName']
        adminEmail = request.form['adminEmail']
        adminContact = request.form['adminContact']
        password = request.form['password']

        # Fetch data from the database here
        cursor = db_conn.cursor()
        select_sql = "SELECT max(adminID) FROM admin"
        cursor.execute(select_sql)
        data = cursor.fetchone()  # Fetch a single row
        data = data[0]

        print(data)
        if data == None:
            adminID = 'A' + str(10001)
        else:
            admin_no = int(data[1:]) + 1
            adminID = 'A' + str(admin_no)

        insert_sql = "INSERT INTO admin VALUES (%s, %s, %s, %s, %s)"
        cursor = db_conn.cursor()

        try:
            cursor.execute(insert_sql, (adminID, adminName,
                           adminEmail, adminContact, password))
            db_conn.commit()
            cursor.close()
            # Redirect to admin login after successful registration
            return redirect(url_for('login'))
        except Exception as e:
            cursor.close()
            return str(e)  # Handle any database errors here

    return render_template('adminRegister.html')


@app.route('/approve-company', methods=['POST'])
def approve_company():
    data = request.json  # Assuming you send JSON data with company_id

    # Extract company_id from the request
    company_id = data.get('company_id')

    if not company_id:
        return jsonify({"error": "Company ID is missing"}), 400

    try:
        with db_conn.cursor() as cursor:
            # Update the company's status to 'approved' in the database
            update_query = "UPDATE companies SET status = 'approved' WHERE id = %s"
            cursor.execute(update_query, (company_id,))
            db_conn.commit()

            return jsonify({"message": "Company approved successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/reject-company', methods=['POST'])
def reject_company():
    data = request.json  # Assuming you send JSON data with company_id

    # Extract company_id from the request
    company_id = data.get('company_id')

    if not company_id:
        return jsonify({"error": "Company ID is missing"}), 400

    try:
        with db_conn.cursor() as cursor:
            # Update the company's status to 'rejected' in the database
            update_query = "UPDATE companies SET status = 'rejected' WHERE id = %s"
            cursor.execute(update_query, (company_id,))
            db_conn.commit()

            return jsonify({"message": "Company rejected successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
