import os
import tempfile
import zipfile

from midi_inverter import midi_inverter
from werkzeug.utils import secure_filename
from flask import Flask, request, render_template, send_file, flash, url_for, redirect
app = Flask(__name__)
app.secret_key = 'Z$\x82l\xd7\x8fc?F\xaa\x1b\xc2U\x86\x9e)\xaa\x04#K\x94y\xb4\xf8'

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/invert', methods=['GET', 'POST'])
def invert():
    error = None
    if request.method == 'POST':
        f = request.files['midi_file']
        invert_drums = request.form.get('invertDrums')
        try:
            inverted_midi = midi_inverter.invert_midi(f, invert_drums)
        except IOError:
            flash('Invalid midi file - file could be corrupt, or simply not a midi file.')
            return redirect(url_for('index'))
        inverted_filename = os.path.splitext(secure_filename(f.filename))
        inverted_filename = inverted_filename[0] + "--inverted" + (inverted_filename[1] or '.mid')
        return send_file(inverted_midi, mimetype="audio/midi", as_attachment=True, attachment_filename=inverted_filename)

@app.route('/invert_bulk', methods=['POST'])
def bulk_invert():
    files = request.files.getlist('midi_files[]')
    invert_drums = request.form.get('invertDrums')
    response_file = tempfile.NamedTemporaryFile()
    zip = zipfile.ZipFile(response_file, mode='w')
    for f in files:
        try:
            inverted_midi = midi_inverter.invert_midi(f, invert_drums)
        except IOError:
            continue
        inverted_filename = os.path.splitext(secure_filename(f.filename))
        inverted_filename = inverted_filename[0] + "--inverted" + (inverted_filename[1] or '.mid')
        zip.writestr(inverted_filename, inverted_midi.read())
    zip.close()
    return send_file(
        zip.filename,
        mimetype="zip",
        as_attachment=True,
        attachment_filename='bulk_inverted_midis.zip'
    )

