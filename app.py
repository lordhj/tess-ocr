import cv2
import pytesseract
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'static/images'


from flask import *
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def read_text(name):
    img = cv2.imread("static/images/"+name)
    # pytesseract path
    config = ('-l eng --oem 1 --psm 3')

    pytesseract.pytesseract.tesseract_cmd = "module/Tesseract-OCR/tesseract.exe"
    text = pytesseract.image_to_string(img, config=config)
    # print results
    text = text.split('\n')
    text=[segment for segment in text if segment!=""]
    text = ("\n".join(text)).strip()
    return text

@app.route('/')
def main():
    return render_template("index.html")


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':

        # Get the list of files from webpage
        files = request.files.getlist("file")
        count=0
        # Iterate for each file in the files List, and Save them
        if len(files)>5:
            return "<h1>Only 5 files allowed at max1</h1>"
            #USER WILL BE RETURNED WITH THE ERROR MESSAGE

        #For storing original names
        names=[]
        data=[]
        for file in files:
            count+=1
            filename = secure_filename(file.filename)
            names.append(filename)
            name="file"+str(count)+".png"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], name))
            data.append(read_text(name))

        return render_template("results.html", names=names, data=data, count=count)



if __name__ == '__main__':
    app.run(debug=False)