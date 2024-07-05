import pyaudio
import wave
import subprocess
import datetime
import threading
from pynput import keyboard
from openai import OpenAI
import dotenv
dotenv.load_dotenv()

client = OpenAI()

# Audio recording parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
STOP_RECORDING = False

def list_audio_devices():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    num_devices = info.get('deviceCount')
    devices = []

    for i in range(0, num_devices):
        device_info = p.get_device_info_by_host_api_device_index(0, i)
        devices.append(device_info)
        print(f"{i}: {device_info.get('name')}")

    p.terminate()
    return devices

def get_timestamped_filename():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"output_{timestamp}.wav"

def record_audio(device_index, filename):
    global STOP_RECORDING
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True, input_device_index=device_index,
                        frames_per_buffer=CHUNK)
    print("Recording... Press 'ESC' to stop.")

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)

        while not STOP_RECORDING:
            data = stream.read(CHUNK)
            wf.writeframes(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()
    print(f"Finished recording. File saved as {filename}")
    return filename

def on_press(key):
    global STOP_RECORDING
    try:
        if key == keyboard.Key.esc:
            STOP_RECORDING = True
            return False  # Stop listener
    except AttributeError:
        pass

def listen_for_keypress():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

def convert_audio_to_text(filename):
    command = f"./whisper.cpp/main --model ./models/ggml-medium.en.bin {filename} --output-txt"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
    # read in the output file - it is the filename + ".txt"
    with open(f"{filename}.txt", "r", encoding='utf8') as f:
        return f.read()

def summarize_text(text):
    prompt = f"""The following is a transcript from a meeting. Turn this into some useful notes that I can use to refresh my memory before the next meeting.
    
{text}
"""
    print(prompt)
    messages = [
      { 'role': 'user', 'content': prompt}
    ]
    # get OpenAI to summarize the transcript in a funny whitty way
    
    chat_completion = client.chat.completions.create(model="gpt-4o",
    messages=messages)
    return chat_completion.choices[0].message.content

def main():
    global STOP_RECORDING
    STOP_RECORDING = False
    
    devices = list_audio_devices()
    device_index = int(input("Select the device index to use for recording: "))

    filename = get_timestamped_filename()

    record_thread = threading.Thread(target=record_audio, args=(device_index, filename))
    keypress_thread = threading.Thread(target=listen_for_keypress)

    record_thread.start()
    keypress_thread.start()

    record_thread.join()
    keypress_thread.join()

    text = convert_audio_to_text(filename)
    print(f"Transcribed Text: {text}")
    summary = summarize_text(text)
    print(f"Meeting Summary:\n\n {summary}")

if __name__ == "__main__":
    main()
