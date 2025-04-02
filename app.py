from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ''
    if request.method == 'POST':
        try:
            num1 = float(request.form['num1'])
            num2 = float(request.form['num2'])
            if num1 == 0:
                result = "Cannot calculate percentage. Number 1 must not be zero."
            else:
                percentage = (num2 / num1) * 100
                result = f"📊 Number 2 is {percentage:.2f}% of Number 1."
        except:
            result = "⚠️ Please enter valid numbers."

    return f'''
        <html>
        <head>
            <title>Ratio App v3</title>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
        </head>
        <body class="container mt-5">
            <h2 class="mb-4">💡 Ratio App - Version 3</h2>
            <form method="POST" class="mb-3">
                <div class="mb-3">
                    <label>Number 1</label>
                    <input type="number" step="any" name="num1" class="form-control" required>
                </div>
                <div class="mb-3">
                    <label>Number 2</label>
                    <input type="number" step="any" name="num2" class="form-control" required>
                </div>
                <button type="submit" class="btn btn-primary">Calculate</button>
            </form>
            <h4>{result}</h4>
        </body>
        </html>
    '''
