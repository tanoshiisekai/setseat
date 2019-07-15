from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///seats.db'
db = SQLAlchemy(app)


class Seat(db.Model):
    seatid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True)
    choose1 = db.Column(db.String(5))
    choose2 = db.Column(db.String(5))
    choose3 = db.Column(db.String(5))
    choose4 = db.Column(db.String(5))
    choose5 = db.Column(db.String(5))

    def __init__(self, username, choose1, choose2, choose3, choose4, choose5):
        self.username = username
        self.choose1 = choose1
        self.choose2 = choose2
        self.choose3 = choose3
        self.choose4 = choose4
        self.choose5 = choose5
    
    def convertintodict(self):
        return {
            "username": self.username,
            "choose1": self.choose1,
            "choose2": self.choose2,
            "choose3": self.choose3,
            "choose4": self.choose4,
            "choose5": self.choose5
        }

@app.route("/summary")
def summary():
    lines = len(Seat.query.all())
    return render_template("summary.html", lines=lines)

@app.route("/getsummary")
def getsummary():
    datas=Seat.query.all()
    datas = [x.convertintodict() for x in datas]
    return jsonify(datas)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/getseat')
def getseat():
    username = request.args.get("username")
    return render_template("finished.html", username=username)

@app.route("/result")
def result():
    choosestr = request.args.get("choosestr")
    username = request.args.get("username")
    chooselist = choosestr.strip().split("^")
    chooselist = [x for x in chooselist if len(x) > 0]
    person = Seat(username, chooselist[0], chooselist[1], chooselist[2], chooselist[3], chooselist[4])
    if Seat.query.filter_by(username=username).first():
        info = "你已经提交过信息了……每人只有一次提交机会，不要重复提交……"
    else:
        db.session.add(person)
        db.session.commit()
        info = "你的信息已经提交，谢谢……"
    return render_template("result.html", info=info)

if __name__ == '__main__':
    db.create_all()
    app.run(host="192.168.2.110", port=9010, debug=True)
