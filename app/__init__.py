from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home_page():
    return render_template('home.html')

@app.route("/about")
def about_page():
    return render_template('about.html')

@app.route("/card_types")
def card_types_page():
    return render_template('card_types.html')

@app.route("/cards")
def cards_page():
    return render_template('cards.html')

@app.route("/subtypes")
def subtypes_page():
    return render_template('subtypes.html')

@app.route("/families")
def families_page():
    return render_template('families.html')

if __name__ == "__main__":
    app.run()

