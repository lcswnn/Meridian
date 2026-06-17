from flask import Flask, render_template
from fetch_ozone import get_ozone_data

app = Flask(__name__)

@app.route('/')
def home():
    ozone = get_ozone_data()
    return render_template('main.html', ozone=ozone)

if __name__ == '__main__':
    app.run(debug=True)