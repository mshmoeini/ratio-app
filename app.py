from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        num1 = float(request.form['num1'])
        num2 = float(request.form['num2'])
        if num2 == 0:
            return "Cannot divide by zero!"
        ratio = num1 / num2
        return f"The ratio is: {ratio:.2f}"
    return '''
        <form method="post">
            Number 1: <input name="num1"><br>
            Number 2: <input name="num2"><br>
            <button type="submit">Calculate Ratio</button>
        </form>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
