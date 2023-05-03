from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    daily_expense = request.form['expense']
    # Do something with the daily_expense, e.g., store in a database, process, etc.
    print(f"Daily expense: {daily_expense}")
    return "Form submitted successfully!"

if __name__ == '__main__':
    app.run(debug=True, port=5001)
