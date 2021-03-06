# settings.iniの準備
[info]
USER_ID = xxxxx@example.com
PASSWORD = password
<!-- PROFILE_PATH = "C:/Users/mako/AppData/Local/Google/Chrome/User" -->
DOWNLOAD_PATH = download_path
SAVE_PATH = save_path
COLLECT_YEAR = 2020

# requirements.txtの編集
chromeのバージョンによっては動作しなくなることがあるため、
以下から自身のChromeのバージョンに合った、chromedriver-binaryを用意する。
https://pypi.org/project/chromedriver-binary/#history