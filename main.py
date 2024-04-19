import requests
from gtts import gTTS
import os

# Import genai library for Gemine API
import genai

# Function to recognize speech using Google Cloud Speech-to-Text API
def recognize_speech():
    GOOGLE_SPEECH_API_KEY = "YOUR_GOOGLE_SPEECH_API_KEY"
    url = f"https://speech.googleapis.com/v1/speech:recognize?key={GOOGLE_SPEECH_API_KEY}"

    with open("audio.wav", "rb") as audio_file:
        audio_content = audio_file.read()

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "config": {
            "encoding": "LINEAR16",
            "sampleRateHertz": 16000,
            "languageCode": "en-US"
        },
        "audio": {
            "content": audio_content
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        if 'results' in result:
            if result['results']:
                return result['results'][0]['alternatives'][0]['transcript']
    else:
        print("Error occurred while recognizing speech:", response.text)
        return None

# Function to send text to Google Gemini API
def send_to_gemine(text):
    api_key = "AIzaSyCtg69viYMbLFgTlkq-rwSSubOviPF4J-0"
    genai.configure(api_key=api_key)
    
    # Add text in front of the speech
    text_with_intro = "You are Jarvis from Iron Man and your responses should be familiar to its talking style. " + text
    
    try:
        response = genai.language.analyze_content(text_with_intro)
        return response['text']
    except Exception as e:
        print("Error occurred while sending text to Gemine API:", e)
        return None

# Function to convert text to speech and play it
def speak_text(text):
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save("output.mp3")
    os.system("mpg123 output.mp3")
    os.remove("output.mp3")

# Main function
def main():
    while True:
        input("Press Enter to start recording...")
        os.system("arecord -D plughw:1,0 -f cd -c1 -r 16000 -d 5 -t wav -q -vv -V mono audio.wav")
        print("Recording finished.")
        speech_text = recognize_speech()
        if speech_text:
            print("You said:", speech_text)
            gemine_response = send_to_gemine(speech_text)
            if gemine_response:
                print("Gemine API Response:", gemine_response)
                speak_text(gemine_response)

if __name__ == "__main__":
    main()
        elapsed_time = time.time() - recording_start_time

        # Wait for silence if recording duration hasn't been reached yet
        if elapsed_time < recording_duration:
            silence_timer = 0
            while silence_timer < silence_threshold:
                time.sleep(0.1)
                silence_timer += 0.1
                if not recognize_speech("audio.wav"):
                    break

if __name__ == "__main__":
    main()
