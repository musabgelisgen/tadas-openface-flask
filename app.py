from flask import Flask, request, jsonify
import werkzeug
from subprocess import call
import os, shutil


app = Flask(__name__)


def execute_openface_script():
    # can also suppress outputs here, this could improve performance
    call(['./../bin/FeatureExtraction', '-fdir', './../bin/uploaded', '-out_dir', './out'])


def read_output(gaze_offset, pose_offset):
    with open("out/uploaded.csv") as f:
        result = []
        lis = [line.split() for line in f]
        confidence = 0
        gaze_angle_x = 0
        gaze_angle_y = 0
        pose_Rx = 0
        pose_Ry = 0
        blink = 0
        driver_attention = False

        for i, x in enumerate(lis):
            confidence = x[3]
            gaze_angle_x = x[11]
            pose_Ry = x[297]
            gaze_angle_y = x[12]
            pose_Rx = x[296]
            blink = x[713]

            # arr = x
            # arr = x[3:4] + x[11:13] + x[296:298] + x[713:714]
            arr = x[3:4] + x[11:13] + x[296:298]
            result.append(arr)  # confidence, eye-gaze-angle, head-pose-angle

        confidence = confidence[0:len(confidence)-1]
        is_confident = float(confidence) > 0.5

        gaze_angle_x = gaze_angle_x[0:len(gaze_angle_x)-1]
        gaze_angle_x = float(gaze_angle_x) - float(gaze_offset)
        pose_Ry = pose_Ry[0:len(pose_Ry)-1]
        pose_Ry = float(pose_Ry) - float(pose_offset)

        if is_confident:
            eyes_on_the_road = True
            head_on_the_road = True
            if 0.15 < gaze_angle_x or gaze_angle_x < -0.2:
                eyes_on_the_road = False

            if 0.35 < pose_Ry or pose_Ry < -0.35:
                head_on_the_road = False

            if eyes_on_the_road and head_on_the_road:
                driver_attention = True

        return jsonify(driver_attention=driver_attention, is_confident=is_confident, result=result, gaze_angle=gaze_angle_x, pose=pose_Ry)


@app.route('/predict', methods=['POST'])
def get_prediction():
    cleanse_uploaded_directory()

    gaze_offset = request.form['gaze_offset']
    pose_offset = request.form['pose_offset']

    for key in request.files:
        read_and_save_file(key)
 
    execute_openface_script()
    return read_output(gaze_offset, pose_offset)


@app.route('/calibrate', methods=['POST'])
def calibrate():
    cleanse_uploaded_directory()

    for key in request.files:
        read_and_save_file(key)

    execute_openface_script()
    return read_output(0, 0)


def cleanse_uploaded_directory():
    folder = '../bin/uploaded'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def read_and_save_file(file_key):
    imagefile = request.files[file_key]
    filename = werkzeug.utils.secure_filename(imagefile.filename)
    print('Received image File name : ' + imagefile.filename)
    imagefile.save('../bin/uploaded/' + filename)  # save file to uploaded folder


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='8000')