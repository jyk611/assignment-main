from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

# Configure the 'templates' folder for HTML templates.
app.template_folder = 'pages'
app.static_folder = 'static'

@app.route("/", methods=['GET'], endpoint='index')
def index():
    return render_template('index.html')

@app.route("/job_listing", methods=['GET'])
def job_listing():
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

        return redirect(url_for('login'))  # Redirect to the homepage after successful registration
    
    return render_template('register.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return render_template('index.html', user_authenticated=True)

    return render_template('login.html')

@app.route("/studentDashboard", methods=['GET'])
def studentDashboard():
    return render_template('studentDashboard.html')

@app.route("/form", methods=['GET', 'POST'])
def form():
            
    return render_template('form.html')

@app.route("/report", methods=['GET'])
def report():
    return render_template('report.html')

# -------------------------------------------------------------- Lecturer START (Kuah Jia Yu) --------------------------------------------------------------#
    
@app.route("/lectRegister", methods=['GET', 'POST'])
def lectRegister():
    return render_template('lectRegister.html')
    
@app.route("/lectLogin", methods=['GET', 'POST'])
def lectLogin():
    if request.method == 'POST':
        return render_template('index.html', user_authenticated=True)
    return render_template('lectLogin.html', lecturer=data)
    
@app.route("/lectDashboard", methods=['GET'])
def lectDashboard():
    return render_template('lectDashboard.html')
    
# ------------------------------------------------------------------- Lecturer END -------------------------------------------------------------------#

# ------------------------------------------------------------------- Company START (Wong Kar Yan) -------------------------------------------------------------------#
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

        # if companyImage.filename == "":
        #     return "Please select a file"
 
        cursor.execute(insert_sql, (comp_name, job_title, job_desc, job_req, sal_range, contact_person_name, contact_person_email, contact_number, comp_state))
        db_conn.commit()
        cursor.close()

        return redirect(url_for('companyDashboard'))
        # # Uplaod image file in S3 #
        # comp_image_file_name_in_s3 = "company-" + str(comp_name) + "_image_file"
        # s3 = boto3.resource('s3')
        
        # try:
        #     print("Data inserted in MySQL RDS... uploading image to S3...")
        #     s3.Bucket(custombucket).put_object(Key=comp_image_file_name_in_s3, Body=companyImage)
        #     bucket_location = boto3.client('s3').get_bucket_location(Bucket=custombucket)
        #     s3_location = (bucket_location['LocationConstraint'])

        #     if s3_location is None:
        #         s3_location = ''
        #     else:
        #         s3_location = '-' + s3_location

        #     object_url = "https://s3%7B0%7D.amazonaws.com/%7B1%7D/%7B2%7D".format(
        #         s3_location,
        #         custombucket,
        #         comp_image_file_name_in_s3)
        #     return redirect(url_for('companyDashboard'))
        # except Exception as e:
        #     cursor.close()
        #     print(f"Error during database insertion: {e}")
        #     return str(e)  # Handle any database errors here

    return render_template('jobReg.html')

@app.route("/companyDashboard", methods=['GET'])
def companyDashboard():
    return render_template('companyDashboard.html')

# ------------------------------------------------------------------- Company END -------------------------------------------------------------------#

if __name__ == '__main__':
    app.run(debug=True)
