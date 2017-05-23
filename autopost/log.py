# -*- coding: utf-8 -*-


import logging
import settings
import main


logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

formatter = logging.Formatter('%(asctime)s:  %(levelname)s: '
                              '%(name)s: %(message)s')

console = logging.StreamHandler()
console.setFormatter(formatter)

filehandler = logging.FileHandler(settings.logs_path)
filehandler.setFormatter(formatter)

# copy_filehandler = logging.Filehandler(settings.copy_logs_path)
# copy_filehandler.setFormatter(formatter)

logger.addHandler(console)
logger.addHandler(filehandler)
# logger.addHandler(copy_filehandler)


if __name__ == '__main__':
    main.bot.polling(none_stop=True, interval=0)
    logger.warning('error!')
