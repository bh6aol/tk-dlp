#!/bin/bash

# 1. curr dir
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

# 2. main script
MAIN_FILE="main.py"

# 3. conda evn
CONDA_ENV_NAME="tk-dlp"

# 4. activate conda env
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate "$CONDA_ENV_NAME"

# 5. customtkinter path
CUSTOMTKINTER_PATH="$(python -c 'import customtkinter, os; print(os.path.dirname(customtkinter.__file__))')"

# 6. cmd
BUILD_CMD=(
  pyinstaller
  --noconfirm
  --onedir
  --windowed
  --add-data "config.ini:."
  --add-data "language:language"
  --add-data "image:image"
  --add-data "$CUSTOMTKINTER_PATH:customtkinter"
  "$MAIN_FILE"
)

# 7. run
echo "🔧 build cmd:"
echo "${BUILD_CMD[@]}"
"${BUILD_CMD[@]}"

# 8. done
echo "✅ Pkg done."
