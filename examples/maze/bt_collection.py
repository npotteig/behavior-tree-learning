_bt_1 = ['f(',
            'ReachGoal?',
            's(',
                'CompLkGraph!',
                'f(',
                    'NotReadyForSG?',
                    'GetSubGoal!',
                ')',
                'MoveTo!',
             ')',
         ')']

_bt_2 = ['s(',
            'f(',
                'LkGraph?',
                'CompLkGraph!',
            ')',
            'f(',
                'ReachGoal?',
                'f(',
                    's(',
                        'LkClose?',
                        'GetLk!',
                    ')',
                    's(',
                        'f(',
                            'NotReadyForSG?',
                            'GetSubGoal!',
                        ')',
                        'MoveTo!',
                    ')',
                ')',
            ')',
         ')']

def select_bt(idx: int):
    collection = [_bt_1, _bt_2]
    return collection[idx]