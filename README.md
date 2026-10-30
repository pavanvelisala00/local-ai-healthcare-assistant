# Local AI Healthcare Assistant with Safety Guardrails

An educational prototype that explores local language-model inference for general healthcare information with basic safety checks around user input and generated responses.

## Features

- Local inference using a GGUF model through `llama-cpp-python`
- Flask web interface and command-line interface
- Basic checks for emergency-related language
- Basic prompt-injection detection
- Selected medication-safety and output checks
- Unit tests for the guardrail functions

## Project structure

```text
.
├── app.py
├── web_app.py
├── guardrails.py
├── model_loader.py
├── requirements.txt
├── models/README.txt
├── templates/index.html
├── static/css/styles.css
├── static/js/app.js
└── tests/test_guardrails.py
```

## Setup

Use Python 3.10 or newer. Create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

Place a compatible GGUF model in the `models/` directory and configure the model path as described in `model_loader.py` and `models/README.txt`. Model weights are intentionally not included in this repository.

Run the command-line application:

```bash
python app.py
```

Run the web application:

```bash
python web_app.py
```

Then open the local address printed by Flask in your browser.

Run tests:

```bash
python -m unittest discover -s tests -v
```

## Safety and limitations

This is a learning prototype, not a medical device and not a substitute for a qualified healthcare professional. It is not clinically validated. Its rule-based checks are limited and can produce false positives or miss harmful content. Emergency warning detection is not comprehensive; seek emergency services for urgent symptoms rather than relying on this application.

Local model inference does not by itself guarantee that the entire setup is offline: installing dependencies and obtaining model weights may require an internet connection. Review the model's licence and terms before downloading or using it.

## Licence

MIT. See [LICENSE](LICENSE).
