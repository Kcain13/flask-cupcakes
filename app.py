"""Flask app for Cupcakes"""

from flask import Flask, request, jsonify, render_template

from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLAlCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "Yankee-Candle"

connect_db(app)


@app.route("/")
def root():
    '''Render Homepage'''

    return render_template("index.html")


@app.route("/api/cupcakes")
def list_cupcakes():
    '''Return all cupcakes in the system'''

    cupcakes = [cupcake.to_dict() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)


@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    '''add cupcake into the system'''

    data = request.json

    cupcake = Cupcake(
        flavor=data['flavor'],
        rating=data['rating'],
        size=data['size'],
        image=data['image'] or None
    )

    db.session.add(cupcake)
    db.session.commit()

    # POST requests should return HTTP status of 201 CREATED
    return (jsonify(cupcake=cupcake.todict()), 201)


@app.route("/api/cupcakes/<int:cucpake_id>")
def get_cupcake(cupcake_id):
    '''return data on specific cupcake'''

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.todict())


@app.route("/api/cupcakes/<int:cupcake_id>", methods=['PATCH'])
def update_cupcake(cupcake_id):
    '''update cupcake from data in request'''

    data = request.json

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = data['flavor']
    cupcake.rating = data['rating']
    cupcake.size = data['size']
    cupcake.image = data['image']

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.todict())


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def remove_cupcake(cupcake_id):
    '''delete cupcake and return confirmation message'''

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")
