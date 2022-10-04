You can use the GPU with:
1. Change medium in `model = whisper.load_model("medium")` to your favorite model like `large `in setup.py.
2. Change `medium` and `cpu` in `model = whisper.load_model("medium", device="cpu")` to your favorite model like `large` and `cuda` in main.py.