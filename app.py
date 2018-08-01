#!/usr/bin/env python3

import flask_sqlalchemy
import io
import os

from flask import Flask, jsonify, send_file, request
from PIL import Image, ImageDraw

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'sqlite:////tmp/test.db')

db = flask_sqlalchemy.SQLAlchemy(app)

PORT = os.environ.get('PORT', 5000)


class Counter(db.Model):
    host = db.Column(db.String(128), primary_key=True)
    value = db.Column(db.Integer, default=0, nullable=False)


@app.route('/')
def index():
    host = request.args.get('host')

    if not host:
        return jsonify(error='which host?')

    counter = Counter.query.get(host)

    if not counter:
        counter = Counter(host=host, value=0)
        db.session.add(counter)

    counter.value += 1
    db.session.commit()

    out = io.BytesIO()
    img = Image.new('RGB', (45, 20))

    draw = ImageDraw.Draw(img)
    draw.text((5, 5), str(counter.value).zfill(6), fill=(255, 0, 0))

    img.save(out, format='JPEG')
    out.seek(0)

    return send_file(out, mimetype='image/jpeg')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True)
