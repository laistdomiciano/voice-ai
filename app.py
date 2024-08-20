from flask import Flask, request, send_file, render_template
from gtts import gTTS
from io import BytesIO
import requests

app = Flask(__name__)

def text_to_audio_file(text):
    tts = gTTS(text)
    audio_file = BytesIO()
    tts.write_to_fp(audio_file)
    audio_file.seek(0)
    return audio_file


def ask_question(content):
    url = "https://open-ai21.p.rapidapi.com/conversationpalm2"

    question_content = f"{content}" + '. Please answer back to me in a silly way.And please be as short as possible and as funny as possible'

    payload = {"messages": [
        {
            "role": "user",
            "content": question_content,
        }
    ]}
    headers = {
        "x-rapidapi-key": "29e4910dcbmsh8f620cdeb08c4b4p1bca49jsndd4e2fb86c75",
        "x-rapidapi-host": "open-ai21.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.json())
    return response.json()
# ask_question("how are you?")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/speak', methods=['POST'])
def speak():
    sentence = request.form.get('sentence')
    print(sentence)
    print(type(sentence))

    if not sentence:
        return {"error": "Please provide a sentence"}, 400
    if sentence:
        answer = ask_question(sentence)

    audio_file = text_to_audio_file(answer['BOT'])
    return send_file(audio_file, mimetype='audio/mpeg')


if __name__ == '__main__':
    app.run(debug=True)