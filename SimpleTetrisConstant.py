MINO = ['X', 'T', 'S', 'Z', 'L', 'J', 'O', 'I']

MINO_DICT = {'T' : 1,
             'S' : 2,
             'Z' : 3,
             'L' : 4,
             'J' : 5,
             'O' : 6,
             'I' : 7,}

IMAGE_MINO = ['',
              './Sprite/TMino.png',
              './Sprite/SMino.png',
              './Sprite/ZMino.png',
              './Sprite/LMino.png',
              './Sprite/JMino.png',
              './Sprite/OMino.png',
              './Sprite/IMino.png',]

IMAGE_NEXT_MINO = ['',
              './Sprite/NextTMino.png',
              './Sprite/NextSMino.png',
              './Sprite/NextZMino.png',
              './Sprite/NextLMino.png',
              './Sprite/NextJMino.png',
              './Sprite/NextOMino.png',
              './Sprite/NextIMino.png',]

IMAGE_BLOCK = ['',
               './Sprite/TBlock.png',
               './Sprite/SBlock.png',
               './Sprite/ZBlock.png',
               './Sprite/LBlock.png',
               './Sprite/JBlock.png',
               './Sprite/OBlock.png',
               './Sprite/IBlock.png',]

IMAGE_SHADOW = ['',
                './Sprite/TMino_shadow.png',
                './Sprite/SMino_shadow.png',
                './Sprite/ZMino_shadow.png',
                './Sprite/LMino_shadow.png',
                './Sprite/JMino_shadow.png',
                './Sprite/OMino_shadow.png',
                './Sprite/IMino_shadow.png',]

IMAGE_MENU = './Sprite/Menu.png'

IMAGE_BUTTON = ['./Sprite/SinglePlayButtonOn.png',
                './Sprite/SinglePlayButtonDown.png',
                './Sprite/MultiPlayButtonOn.png',
                './Sprite/MultiPlayButtonDown.png',
                './Sprite/ExitButtonOn.png',
                './Sprite/ExitButtonDown.png']

IMAGE_CLEAR = ['./Sprite/ClearSingle.png',
               './Sprite/ClearSingleTspin.png',
               './Sprite/ClearSingleBTBTspin.png',
               './Sprite/ClearDouble.png',
               './Sprite/ClearDoubleTspin.png',
               './Sprite/ClearDoubleBTBTspin.png',
               './Sprite/ClearTriple.png',
               './Sprite/ClearTripleTspin.png',
               './Sprite/ClearTripleBTBTspin.png',
               './Sprite/ClearTetris.png',
               './Sprite/ClearTetrisBTB.png',]

BACKGROUND = './Sprite/Background.png'
MINO_STATE = {'T' : [((-1,  0), ( 0, -1), ( 0,  0), ( 0,  1)),
                     ((-1,  0), ( 0,  0), ( 0,  1), ( 1,  0)),
                     (( 0, -1), ( 0,  0), ( 0,  1), ( 1,  0)),
                     ((-1,  0), ( 0, -1), ( 0,  0), ( 1,  0))],
              'S' : [((-1,  0), (-1,  1), ( 0, -1), ( 0,  0)),
                     ((-1,  0), ( 0,  0), ( 0,  1), ( 1,  1)),
                     (( 0,  0), ( 0,  1), ( 1, -1), ( 1,  0)),
                     ((-1, -1), ( 0, -1), ( 0,  0), ( 1,  0))],
              'Z' : [((-1, -1), (-1,  0), ( 0,  0), ( 0,  1)),
                     ((-1,  1), ( 0,  0), ( 0,  1), ( 1,  0)),
                     (( 0, -1), ( 0,  0), ( 1,  0), ( 1,  1)),
                     ((-1,  0), ( 0, -1), ( 0,  0), ( 1, -1))],
              'L' : [((-1,  1), ( 0, -1), ( 0,  0), ( 0,  1)),
                     ((-1,  0), ( 0,  0), ( 1,  0), ( 1,  1)),
                     (( 0, -1), ( 0,  0), ( 0,  1), ( 1, -1)),
                     ((-1, -1), (-1,  0), ( 0,  0), ( 1,  0))],
              'J' : [((-1, -1), ( 0, -1), ( 0,  0), ( 0,  1)),
                     ((-1,  0), (-1,  1), ( 0,  0), ( 1,  0)),
                     (( 0, -1), ( 0,  0), ( 0,  1), ( 1,  1)),
                     ((-1,  0), ( 0,  0), ( 1,  0), ( 1, -1))],
              'O' : [((-1,  0), (-1,  1), ( 0,  0), ( 0,  1)),
                     ((-1,  0), (-1,  1), ( 0,  0), ( 0,  1)),
                     ((-1,  0), (-1,  1), ( 0,  0), ( 0,  1)),
                     ((-1,  0), (-1,  1), ( 0,  0), ( 0,  1))],
              'I' : [(( 0, -1), ( 0,  0), ( 0,  1), ( 0,  2)),
                     ((-1,  1), ( 0,  1), ( 1,  1), ( 2,  1)),
                     (( 1, -1), ( 1,  0), ( 1,  1), ( 1,  2)),
                     ((-1,  0), ( 0,  0), ( 1,  0), ( 2,  0))],}
WALL_KICK = {'X' : [[(), ((0, 0), (0, -1), (-1, -1), (2, 0), (2, -1)), (), ((0, 0), (0, 1), (-1, 1), (2, 0), (2, 1))],
                    [((0, 0), (0, 1), (1, 1), (-2, 0), (-2, 1)), (), ((0, 0), (0, 1), (1, 1), (-2, 0), (-2, 1)), ()],
                    [(), ((0, 0), (0, -1), (-1, -1), (2, 0), (2, -1)), (), ((0, 0), (0, 1), (-1, 1), (2, 0), (2, 1))],
                    [((0, 0), (0, -1), (1, -1), (-2, 0), (-2, -1)), (), ((0, 0), (0, -1), (1, -1), (-2, 0), (-2, -1)), ()]],
             'I' : [[(), ((0, 0), (0, -2), (0, 1), (1, -2), (-2, 1)), (), ((0, 0), (0, -1), (0, 2), (-2, -1), (1, 2))],
                    [((0, 0), (0, 2), (0, -1), (1, -2), (2, -1)), (), ((0,0), (0, -1), (0, 2), (-2, 1), (1, 2)), ()],
                    [(), ((0,0), (0, 1), (0, -2), (-2, -1), (1, -2)), (), ((0, 0), (0, 2), (0, -1), (1, -2), (2, -1))],
                    [((0,0), (0, 1), (0, -2), (-2, -1), (1, -2)), (), ((0, 0), (0, -2), (0, 1), (1, -2), (-2, 1)), ()]]}
SHADOW_ROTATION = {0 : (  0, (0, 0)),
                   1 : (270, (0, 1)),
                   2 : (180, (1, 0)),
                   3 : ( 90, (0, 0))}
SHADOW_ROTATION_I = {0 : (  0, (1, 0)),
                     1 : (270, (0, 2)),
                     2 : (180, (2, 0)),
                     3 : ( 90, (0, 1))}
DELAY_V = 4
DELAY_FIRST = 8