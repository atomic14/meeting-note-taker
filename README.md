# Cloning

Make sure to clone recursively to get the whisper.cpp submodule

```bash
git clone --recursive git@github.com:atomic14/meeting-note-taker.git
```

# Build whisper.cpp

```bash
cd whisper.cpp
make clean
WHISPER_COREML=1 make -j
```

# Download the whisper model

```bash
cd whisper.cpp
bash ./models/download-ggml-model.sh  medium.en
```

# Setup the python app

```bash
python -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file with the following content:

```
OPENAI_API_KEY=<<YOUR OPENAI API KEY>>
```

# Running

```bash
python note-taker.py
```