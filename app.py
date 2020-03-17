from flask import Flask, request, jsonify
import werkzeug
from subprocess import call


app = Flask(__name__)


def execute_openface_script():
    # can also suppress outputs here, this could improve performance
    call(['./../build/bin/FeatureExtraction', '-fdir', './../build/bin/uploaded', '-out_dir', './out'])


def read_output():
    with open("out/uploaded.csv") as f:
        result = []
        lis = [line.split() for line in f]
        for i, x in enumerate(lis):
            result.append(x[1:10]) # these are from confidence to eye gaze angle

        return jsonify(faces=result)


@app.route('/predict', methods=['POST'])
def get_prediction():
    read_and_save_file('file1')
    read_and_save_file('file2')
    execute_openface_script()
    return read_output()


def read_and_save_file(file_key):
    imagefile = request.files[file_key]
    filename = werkzeug.utils.secure_filename(imagefile.filename)
    print('Received image File name : ' + imagefile.filename)
    imagefile.save('../build/bin/uploaded/' + filename)  # save file to uploaded folder


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='80')