import logging
import os
import threading

from flask import Blueprint, jsonify, request, send_from_directory

from file_orchestrator import FileConsumer, FileProducer, Orchestrator

log = logging.getLogger()
log.setLevel(logging.INFO)

FILES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'files'))

api: Blueprint = Blueprint('api', __name__)


@api.route('/upload', methods=['POST'])
def upload():
    try:
        file = request.files.get('file')

        file_orchestrator: Orchestrator = Orchestrator(file=file)
        process_complete: bool = file_orchestrator.orchestrate()
        
    except Exception as e:
        log.error(e)
        return jsonify(message='Something went wrong'), 500
    
    return jsonify(message='file uploaded successfully'), 200


@api.route('/download/<filename>', methods=['GET'])
def download(filename: str):
    try:
        send_from_directory(directory=FILES_DIR,
                            path=filename,
                            as_attachment=True)
    except Exception as e:
        log.error(e)
        return jsonify(message='Something went wrong'), 500
    
    return jsonify(message='file downloaded successfully'), 200


@api.route('/delete/<filename>', methods=['DELETE'])
def delete(filename: str):
    try:
        os.remove(f'{FILES_DIR}/{filename}')
    
    except Exception as e:
        log.error(e)
        return jsonify(message='Something went wrong'), 500
    
    return jsonify(message='file deleted successfully'), 200