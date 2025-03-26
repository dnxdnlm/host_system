import logging


def set_logger(log_file, log_level='info'):
    log_level_dict = {
        'info': logging.INFO,
        'debug': logging.DEBUG,
        'warn': logging.WARN,
        'error': logging.ERROR
    }
    assert log_level in log_level_dict.keys()
    logger = logging.getLogger()  # 不加名称设置root logger
    logger.setLevel(log_level_dict[log_level])
    formatter = logging.Formatter(
        '%(asctime)s.%(msecs)03d %(levelname)s %(filename)s:%(lineno)d %(process)d: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')

    # 使用FileHandler输出到文件
    fh = logging.FileHandler(log_file)
    fh.setLevel(log_level_dict[log_level])
    fh.setFormatter(formatter)

    # 使用StreamHandler输出到屏幕
    ch = logging.StreamHandler()
    ch.setLevel(log_level_dict[log_level])
    ch.setFormatter(formatter)

    # 添加两个Handler
    logger.addHandler(ch)
    logger.addHandler(fh)


log_info = logging.info
log_warn = logging.warn
log_error = logging.error
log_debug = logging.debug
