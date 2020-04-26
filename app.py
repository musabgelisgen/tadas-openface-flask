from flask import Flask, request, jsonify
import werkzeug
from subprocess import call
import os, shutil


app = Flask(__name__)


def execute_openface_script():
    # can also suppress outputs here, this could improve performance
    call(['./../bin/FeatureExtraction', '-fdir', './../bin/uploaded', '-out_dir', './out'])


def read_output():
    with open("out/uploaded.csv") as f:
        result = []
        lis = [line.split() for line in f]
        for i, x in enumerate(lis):
            result.append(x[1:10])  # these are from confidence to eye gaze angle

        return jsonify(faces=result)


@app.route('/predict', methods=['POST'])
def get_prediction():
    cleanse_uploaded_directory()

    for key in request.files:
        read_and_save_file(key)

    execute_openface_script()
    return read_output()


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