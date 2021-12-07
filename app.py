from flask import Flask, render_template, abort, jsonify, request, url_for, redirect
from model import db, save_db

app = Flask(__name__)

@app.route("/")
def welcome():
    return render_template("welcome.html", cards=db)


@app.route("/card/<int:index>")
def card(index):
    try:
        card = db[index]
        return render_template("card.html", card=card, index=index, max_index=len(db)-1)
    except IndexError:
        return abort(404)


@app.route('/add_card', methods=['GET', 'POST'])
def add_card():
    if request.method == 'POST':
        # add the card
        question = request.form.get('question')
        answer = request.form.get('answer')
        if question and answer:
            card = {
                'question': question,
                'answer': answer
            }
            db.append(card)
            save_db()
            return redirect(url_for('card', index=len(db)-1))
        else:
            return render_template('add_card.html')
    else:
        return render_template('add_card.html')


@app.route('/remove_card/<int:index>', methods=['GET', 'POST'])
def remove_card(index):
    print(request.method)
    if request.method == 'POST':
        del(db[index])
        save_db()
        return redirect(url_for('welcome'))
    else:
        card = db[index]
        return render_template('remove_card.html', card=card)

@app.route('/api/card/<int:index>')
def api_card_detail(index):
    try:
        return db[index]
    except IndexError:
        abort(404)

@app.route('/api/card/all')
def api_card_list():
    return jsonify(db)