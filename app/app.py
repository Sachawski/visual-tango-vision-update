from flask import Flask, render_template, request
import os
from processing_logic.src.angle_calculation_wdisplay import process_image
from werkzeug.utils import secure_filename
import ast
from processing_logic.src.position_classification import frobenius
from processing_logic.src.tomatrix import pose_to_matrix
from processing_logic.src.pose import Pose
from processing_logic.src.animation_creation import animation_creation

app = Flask(__name__)

UPLOAD_FOLDER = 'static/temp'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/classification', methods=['POST'])
def classification():
    if request.method == 'POST' and 'input_file' in request.files:
        file = request.files['input_file']
        if file.filename == '':
        # Gérer le cas où aucun fichier n'est sélectionné
            return render_template('index.html')
        
        poses=[]
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        all_poses={}
        nompose = "Test" # Get corresponding pose name.
        all_poses = process_image(os.path.join(app.config['UPLOAD_FOLDER'], filename), all_poses, nompose)
        os.remove(f'{UPLOAD_FOLDER}/{file.filename}')
        with open("output/angle_for_classification.txt", 'r') as file:
            angle_for_classification = file.read()
            angle_for_classification = ast.literal_eval(angle_for_classification)
            file.close()
        for key,value in all_poses.items() :
            L=[(i,frobenius(pose_to_matrix(all_poses["Test"]),pose_to_matrix(angle_for_classification[i]))) for i in angle_for_classification.keys()]
            # Code pour exécuter le programme Python avec le fichier d'entrée
            # Enregistrer le fichier de sortie
            s=""
            L.sort(key=lambda x: x[1])
            print(L)
            for item in L:
                s+=f'{item[0]}: {item[1]}\n'
            print(L[0][0])
            poses.append(eval(L[0][0]))
        
        to_save = ""
        for pose in poses:
            """
            Order in the save file for 1 pose :
            Direction
            Height
            Name
            Rotation
            Slider
            Weighted leg
            """
            to_save += str(pose._d)
            to_save += str(pose.get_height_ind)
            to_save += str(pose.get_name_ind)
            to_save += str(pose.get_angle_ind)
            to_save += str(pose.get_slider_ind) 
            to_save += str(pose.get_leg_ind)

        print(to_save)
        data = bytearray(to_save,'utf-8')
        print(data)

        with open("static/save.txt", "wb") as output_file:
            output_file.write(data)


        return render_template('classification.html', zeub=s)

    return render_template('index.html')

@app.route('/modelisation', methods=['POST'])
def modelisation():
    if request.method == 'POST' and 'input_file' in request.files:
        file = request.files['input_file']
        if file.filename == '':
        # Gérer le cas où aucun fichier n'est sélectionné
            return render_template('index.html')
        
        poses=[]
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    with open("static/AnimationFile.txt","w") as f:
        f.writelines(["%s\n" % item for item in animation_creation(os.path.join(app.config['UPLOAD_FOLDER'],filename))])
    os.remove(f'{UPLOAD_FOLDER}/{file.filename}')
    
    return render_template('modelisation.html')



if __name__ == '__main__':
    app.run()
