from flask import Flask, request, jsonify, render_template
app = Flask(__name__)

@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html')



@app.route('/', methods = ['POST'])
def indexLogic():
    return (jsonify({
        'success': 1,
        'message': 'Available time fetched successfully',
        'data' : 'resp',
        'status': 200
    }))
if __name__ == "__main__":
    app.run(debug=True)