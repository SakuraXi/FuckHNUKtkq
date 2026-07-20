pyinstaller --noconfirm -F --noconsole --clean ^
  --add-data "templates;templates" ^
  --collect-all mitmproxy ^
  --collect-all cryptography ^
  --collect-all certifi ^
  --icon=640.ico ^
  fuckHNU.py