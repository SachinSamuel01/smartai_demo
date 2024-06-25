import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from lib.rag2 import create_vec_db 
from lib.rag2 import get_response
from werkzeug.utils import secure_filename
import shutil

app = Flask(__name__)
CORS(app)

# Configurations for file uploads
app.config['UPLOAD_FOLDER'] = 'uploads/'

global_vector_db = None
user_prompt = None
global_prompt = None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf'}

def delete_all_content(folder_path):
    # List all files and directories in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            # Check if it is a file and remove it
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)
            # Check if it is a directory and remove it recursively
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

@app.route("/create", methods=['POST'])
def create_bot():
    print("Called")
    try:
        delete_all_content('./uploads')
        delete_all_content('./db')
        global global_vector_db, user_prompt, global_prompt
        prompt = request.form['prompt']
        user_prompt = request.form['prompt']
        print(user_prompt, flush=True)
        files = request.files.getlist('documents')  # Get the files list
        documents = []
        for file in files:
            print(file, flush=True)
            if file and allowed_file(file.filename):
                #print(file.filename, file.read())
                filename = secure_filename(file.filename)
                if not os.path.exists(f'uploads/'):
                    os.makedirs(f'uploads/')
                if not os.path.exists(f'db/'):
                    os.makedirs(f'db/')
                file.seek(0)
                file.save(os.path.join(f'uploads/', filename))
                documents.append(filename)
        print(documents)
        
        files=[os.path.join('uploads',x) for x in os.listdir('uploads')]
        print(files, flush=True)
        global_vector_db, global_prompt = create_vec_db(user_prompt, files)
        
        print(global_vector_db, global_prompt)
        
        return jsonify({'Created': True}), 200
    except Exception as e:
        
        return jsonify({'error': str(e)}), 500



@app.route('/chat',methods=['POST'])
def get_responce_from_llm():
    query = request.form['query']
    response = get_response(global_prompt, global_vector_db, query)
    print(response)
    return jsonify({'response': response}), 200

@app.route('/test',methods=['GET'])
def test_endpoint():
    return jsonify({'response': "Success"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)