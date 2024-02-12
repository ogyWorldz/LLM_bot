from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    video_url = data['videoUrl']
    query = data['query']
    answer = video_url + ' cool ' + query
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)


# video_url = "https://www.youtube.com/watch?v=YHy4gqTyrX4"
# query = "question"
# answer = video_url + ' ' + query
# print(answer)
