import os, sys
import random
from replit import db
from flask import Flask, render_template, request, redirect, url_for, abort
import json
import re

app = Flask(  # Create a flask app
	__name__,
	template_folder='templates',  # Name of html file folder
	static_folder='static'  # Name of directory for static files
)

# UPLOAD_FOLDER = '/path/to/the/uploads'
# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

@app.route('/')  # What happens when the user visits the site
def base_page():
	return render_template(
		'base.html',  # Template file path, starting from the templates folder. 
	)

#Allow website to have get post.
@app.route('/upload')
def upload_page():
	return render_template('upload.html',)

# Upload file using get post
@app.route('/upload', methods = ['POST'])
def upload_file():
  uploaded_file = request.files['file_name']
  if uploaded_file.filename != '':
    uploaded_file.save(os.path.join("uploads", uploaded_file.filename))
    file_uploaded_read_text(uploaded_file.filename)
    
    return render_template('uploadpass.html',)
  else:
    return render_template('uploadfail.html',)
  return render_template('upload.html',)


@app.route('/uploadpass')  # When successful upload
def uploadpass():
  return render_template('uploadpass.html')


@app.route('/uploadfail')  # When upload failed
def uploadfail():
	return render_template('uploadfail.html')


@app.route('/database')  # Html page that shows database
def showDatabaseTable():
  headings = ("Phone ID","Time Stamp","Phone Model","Contact Details","Battery","Ram Usage","Location")
  data = db.values()
  return render_template('database.html',headings=headings, data=data)

def file_uploaded_read_text(filename):
  lines = ""
  filepath = "uploads/" +filename
  with open(filepath) as f:
    lines = f.readlines()

  lines = lines[0]
  parsed_data = cleanup_data(lines)
  parsed_data 
  add_data(parsed_data, filename)
  return

def cleanup_data(lines):
  cleaned_data = lines.split("<<<")
  cleaned_data_string = ''.join(cleaned_data)

  #grab timestamp:
  try: 
    timestamp = re.search(r'DATETIME:.(.*?) PHONE>>>', cleaned_data_string).group(1)
  except:
    timestamp = ""

  output = []
  clean_up_output = []
  for items in cleaned_data:
    output += re.findall('>>> .*$', items)
  for output_items in output:
    clean_up_output.insert(len(clean_up_output),output_items.replace('>>> ', ''))
  return clean_up_output

def add_data(lines, filename):
  temp_list = lines
  insert_id = filename
  safety_string = filename
  temp_list.insert(0,safety_string)

  if insert_id in db:
    # Updating
    db[insert_id] = temp_list
    print("Phone data already exists in database.")
  else:
    db[insert_id] = temp_list
  return


if __name__ == "__main__":  # Makes sure this is the main process
	app.run( # Starts the site
		host='0.0.0.0',  # EStablishes the host, required for repl to detect the site
		port=random.randint(2000, 9000)  # Randomly select the port the machine hosts on.
	)