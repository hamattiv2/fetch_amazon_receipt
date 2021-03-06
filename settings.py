import configparser

conf = configparser.ConfigParser()
conf.read('settings.ini')

user_id = conf['info']['USER_ID']
password = conf['info']['PASSWORD']
download_path = conf['info']['DOWNLOAD_PATH']
save_path = conf['info']['SAVE_PATH']
collect_year = conf['info']['COLLECT_YEAR']