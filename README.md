# Cloning

Make sure to clone recursively to get the whisper.cpp submodule

```bash
git clone --recursive git@github.com:atomic14/meeting-note-taker.git
```

# Setup the python app

```bash
brew install portaudio
python -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
```

# Build whisper.cpp

```bash
cd whisper.cpp
make clean
WHISPER_COREML=1 make -j
```

# Download the whisper model

- To ensure `coremltools` operates correctly, please confirm that [Xcode](https://developer.apple.com/xcode/) is installed and execute `xcode-select --install` to install the command-line tools.

```bash
cd whisper.cpp
bash ./models/download-ggml-model.sh  medium.en
./models/generate-coreml-model.sh medium.en
```

# Running

Create a `.env` file with the following content:

```
OPENAI_API_KEY=<<YOUR OPENAI API KEY>>
```

```bash
. ./venv/bin/activate
python note-taker.py
```