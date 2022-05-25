WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 720

BLOCK_MAP = [
    '666666666666',
    '455444744544',
    '333333333333',
    '222222222222',
    '111111111111',
    '            ',
    '            ',
    '            ',
    '            ']

GAP_SIZE = 10
BLOCK_HEIGHT = WINDOW_HEIGHT / len(BLOCK_MAP) - GAP_SIZE
BLOCK_WIDTH = WINDOW_WIDTH / len(BLOCK_MAP[0]) - GAP_SIZE
TOP_OFFSET = WINDOW_HEIGHT // 20
COLOR_TEXT = (255, 127, 0)
UPGRADES = ['speed_slow', 'speed_fast', 'extra_heart', 'size_small', 'size_big']
