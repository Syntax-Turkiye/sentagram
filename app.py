from flask import Flask, request, render_template, jsonify
import sentagram_script  # Model dosyamızı içeri aktarıyoruz

app = Flask(__name__)

# Anasayfa rotası
@app.route('/')
def index():
    return render_template('index.html')

# Cümleyi ögelerine ayırma rotası
@app.route('/process', methods=['POST'])
def process():
    sentence = request.form['sentence']
    result = sentagram_script.process_sentence(sentence)  # Modeli kullanarak sonucu alıyoruz
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
