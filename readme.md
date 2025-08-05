# pkg: pyinstaller --noconfirm --onedir --windowed --add-data "D:/dev_software/Anaconda3/envs/tk-dlp/Lib/site-packages/customtkinter;customtkinter/"  main.py

# mac sign
xattr -dr com.apple.quarantine dist/main.app

# mac test run
cd dist/main.app/Contents/MacOS/
./main