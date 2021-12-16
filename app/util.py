def format_duration(timeStart, timeEnd):
    minutes, seconds = divmod(timeEnd - timeStart, 60)
    return '%02d:%02d' % (minutes, seconds)