from flask import Flask, render_template, send_from_directory
import os
app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1

assets_folder = os.path.join(app.root_path, 'public')

@app.route('/<path:filename>')
def assets(filename):
  return send_from_directory(assets_folder, filename)

@app.route('/')
def hello_world():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')