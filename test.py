from encrypt_upload import encrypt_and_upload
from decrypt_download import download_and_decrypt
import time
import vlc
if __name__ == '__main__':
    timestamped = 'Thomas_S._Wootton_High_School*240048000934' + str(time.time()) + '.mp4'
    encrypt_and_upload('Thomas_S._Wootton_High_School*240048000934.mp4', timestamped)

