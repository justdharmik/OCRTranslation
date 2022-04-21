#--Importing Packages

# !apt install tesseract-ocr
# !pip install pytesseract

from PIL import Image
import pytesseract
from flask import Flask, render_template, request
import os
from deep_translator import GoogleTranslator

#--Text Extraction Functionbutton

def getText(filename):
    scan_source_lang = request.form['p_source_lang']

    if scan_source_lang == "eng":
        source_lang = "en"
    elif scan_source_lang == "hin":
        source_lang = "hi"
    elif scan_source_lang == "mar":
        source_lang = "mr"
    elif scan_source_lang == "guj":
        source_lang = "gu"
    elif scan_source_lang == "fra":
        source_lang = "fr"

    target_lang = request.form['t_target_lang']
    
    text = pytesseract.image_to_string(Image.open(filename), lang = scan_source_lang)
    text = text.replace(text[-1], "")
    transText = GoogleTranslator(source = source_lang, target = target_lang).translate(text)
    finalVal = [text, transText]

    return finalVal  


#--Flask App Config

app = Flask(__name__, static_url_path='', static_folder='/root/Desktop/JS Things/Text Extraction Translation 1.1/templates')
extensions = ['png', 'jpg', 'jpeg']
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions

#--Path For Image Storage

path = os.getcwd()
# path += "/templates"
UPLOAD_FOLDER = os.path.join(path, 'uploads/')
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#--Flash Web Interface Config
msg = ''

@app.route('/', methods = ['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('home.html', msg = 'No File Selected')
        file = request.files['file']

        if file.filename == '':
                    return render_template('home.html', msg = 'No File')

        if file and allowed_file(file.filename):
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
                    values = getText(file)
                    extracted = values[0]
                    translations = values[1]
                    return render_template('results.html', 
                                            msg = "OCR Complete!",
                                            extracted = extracted,
                                            translations = translations,
                                            img_src = UPLOAD_FOLDER + file.filename)
        
    else:
        return render_template('home.html')


if __name__ == '__main__':
    # app.debug = True
    app.run(debug=False,host="0.0.0.0")
