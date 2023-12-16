from flask import Flask, jsonify, request, Blueprint
import os
import zipfile

upload = Blueprint('upload', __name__)

@upload.route('/upload', methods=['POST'])
def upload_file():
    # Gelen dosyayı kontrol et
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    # Dosya adı ve uzantısını kontrol et
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Sadece zip dosyalarını kabul et
    if file and file.filename.endswith('.zip'):
        # Dosyayı geçici bir klasöre kaydet
        upload_folder = 'uploads'
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, file.filename)
        file.save(file_path)

        # Zip dosyasını çıkart
        extract_folder = 'extracted'
        os.makedirs(extract_folder, exist_ok=True)
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_folder)

        # Dosya işlemleri tamamlandıktan sonra orijinal zip dosyasını silebilirsiniz
        os.remove(file_path)

        return jsonify({'message': 'File uploaded and extracted successfully'})
    else:
        return jsonify({'error': 'Invalid file format'})