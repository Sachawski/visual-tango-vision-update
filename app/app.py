from flask import Flask, render_template, request,redirect,url_for
import os
from src.angle_calculation import process_image
from werkzeug.utils import secure_filename
import ast
from src.angle_classification import frobenius, angle_classification
from src.tomatrix import pose_to_matrix
from src.pose import Pose
from src.animation_creation import animation_creation
from datetime import datetime
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

UPLOAD_FOLDER = 'static/temp'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def generate_unique_filename(filename,id):
    base_filename, file_extension = os.path.splitext(filename)
    
    if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'],f"{base_filename}_{id}{file_extension}")):
        return f"{base_filename}_{id}{file_extension}"
    else :
        return "ERROR"

def generate_unique_identifier():
    return datetime.now().strftime('%Y%m%d%H%M%S%f')
    
def delete_temp():
    folder_path = 'static/temp/'
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Erreur lors de la suppression du fichier {file_path}: {e}")

scheduler = BackgroundScheduler()
scheduler.add_job(func=delete_temp, trigger="interval", hours=12)
scheduler.start()

atexit.register(lambda: scheduler.shutdown())

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r   

@app.route('/')
def index():
    identifier = generate_unique_identifier()
    return render_template('index.html',id=identifier)

@app.route('/visualtango', methods=['POST'])
def visualtango(): 
    with open("static/temp/save.txt", "wb") as output_file:
            output_file.write(bytearray("",'utf-8'))
    return render_template('visualtango.html')

@app.route('/classification', methods=['POST'])
def classification():
    if request.method == 'POST' and 'input_file1' in request.files:
        file = request.files['input_file1']
        if file.filename == '':
        # Gérer le cas où aucun fichier n'est sélectionné
            return render_template('index.html')
        
        poses=[]
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #all_poses={}
        #nompose = "Test" # Get corresponding pose name.
        all_poses = process_image(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print(f'all_poses:{all_poses}')
        os.remove(f'{UPLOAD_FOLDER}/{file.filename}')
        #s = angle_classification(poses,all_poses)
        
        with open("static/output/angle_for_classification.txt", 'r') as file:
            angle_for_classification = file.read()
            angle_for_classification = ast.literal_eval(angle_for_classification)
            file.close()
        for frame,value in all_poses.items() :
            L=[(i,frobenius(pose_to_matrix(all_poses[frame]),pose_to_matrix(angle_for_classification[i]))) for i in angle_for_classification.keys()]
            # Code pour exécuter le programme Python avec le fichier d'entrée
            # Enregistrer le fichier de sortie
            s=""
            L.sort(key=lambda x: x[1])
            for item in L:
                s+=f'{item[0]}: {item[1]}\n'
            poses.append(eval(L[0][0]))
        
        to_save = ""
        for pose in poses:
            
            #Order in the saved file for 1 pose :
            #Direction
            #Height
            #Name
            #Rotation
            #Slider
            #Weighted leg
            
            to_save += str(pose._d)
            to_save += str(pose.get_height_ind)
            to_save += str(pose.get_name_ind)
            to_save += str(pose.get_angle_ind)
            to_save += str(pose.get_slider_ind) 
            to_save += str(pose.get_leg_ind)

        data = bytearray(to_save,'utf-8')
        print(data)

        with open("static/temp/save.txt", "wb") as output_file:
            output_file.write(data)


        return render_template('visualtango.html', token=s)
	
    return render_template('index.html')


@app.route('/modelisation/<id>', methods=['POST'])
def modelisation(id):
    if request.method == 'POST' and 'input_file2' in request.files:
        file = request.files['input_file2']
        if file.filename =='':
            return render_template('index.html')
        
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    filename_animation = generate_unique_filename("AnimationFile.txt",id)
    with open(f"static/temp/{filename_animation}","w") as f:
        f.writelines(["%s\n" % item for item in animation_creation(os.path.join(app.config['UPLOAD_FOLDER'],filename))])
    os.remove(f'{UPLOAD_FOLDER}/{file.filename}')
    
    return render_template('modelisation.html',id=id)
    
        



if __name__ == '__main__':
    app.run(debug=True)
    
