#!/bin/zsh
set -u

SCRIPT_DIR="${0:A:h}"
URL="http://127.0.0.1:8765/"
LOG_FILE="/tmp/personal-ai-ui.log"

cd "$SCRIPT_DIR" || {
  echo "Could not find the Personal AI folder:"
  echo "$SCRIPT_DIR"
  read -k 1 "?Press any key to close..."
  exit 1
}

if ! /usr/bin/curl -fsS "$URL" >/dev/null 2>&1; then
  if [[ -x ".venv/bin/python" ]]; then
    PYTHON=".venv/bin/python"
  elif command -v python3 >/dev/null 2>&1; then
    PYTHON="$(command -v python3)"
  else
    PYTHON="$(command -v python)"
  fi

  if ! "$PYTHON" -c "import fastapi, uvicorn" >/dev/null 2>&1; then
    echo "Installing the website's requirements (first time only)..."
    "$PYTHON" -m pip install -r ui/requirements.txt || {
      echo "Could not install requirements. Try running this in Terminal:"
      echo "  pip3 install -r ui/requirements.txt"
      read -k 1 "?Press any key to close..."
      exit 1
    }
  fi

  echo "Starting Personal AI..."
  nohup "$PYTHON" ui/server.py >> "$LOG_FILE" 2>&1 &

  for _ in {1..30}; do
    if /usr/bin/curl -fsS "$URL" >/dev/null 2>&1; then
      break
    fi
    sleep 0.5
  done
fi

if /usr/bin/curl -fsS "$URL" >/dev/null 2>&1; then
  echo "Opening Personal AI..."
  /usr/bin/open "$URL"
  exit 0
fi

echo "Personal AI did not start."
echo "Log file: $LOG_FILE"
read -k 1 "?Press any key to close..."
exit 1
