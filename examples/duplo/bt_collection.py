_bt_1 = ['s(',
             'apply force 0!',
             'apply force 0!',
             'apply force 0!',
         ')']

_bt_2 = ['f(',
             '0 at pos (0.0, 0.05, 0.0)?',
             's(',
                 'pick 1!',
                 'place on 0!',
                 'pick 2!',
                 'place on 1!',
             ')',
         ')']

_bt_3 = ['s(',
            'f(',
                '0 at pos (0.0, 0.05, 0.0)?',
                's(', 'f(', 'picked 0?', 'pick 0!', ')', 'place at (0.0, 0.05, 0.0)!', ')',
            ')',
            'f(',
                '1 at pos (0.0, 0.05, 0.0192)?',
                's(',
                    'f(', '1 on 0?', 's(', 'f(', 'picked 1?', 'pick 1!', ')', 'place on 0!', ')', ')',
                    'apply force 1!',
                ')',
            ')',
            'f(',
                '2 at pos (0.0, 0.05, 0.0384)?',
                's(',
                    'f(', '2 on 1?', 's(', 'f(', 'picked 2?', 'pick 2!', ')', 'place on 1!', ')', ')',
                    'apply force 2!',
                ')',
            ')',
         ')']

_bt_croissant = ['s(', 'f(', '0 at pos (0.0, 0.0, 0.0)?', \
                           's(', 'f(', 'picked 0?', 'pick 0!', ')', 'place at (0.0, 0.0, 0.0)!', ')', ')', \
                     'f(', '1 at pos (0.0, 0.0, 0.0192)?', \
                           's(', 'f(', '1 on 0?', 's(', 'f(', 'picked 1?', 'pick 1!', ')', 'place on 0!', ')', ')', \
                                 'apply force 1!', ')', ')', \
                     'f(', '2 at pos (0.016, -0.032, 0.0)?', \
                           's(', 'f(', 'picked 2?', 'pick 2!', ')', 'place at (0.016, -0.032, 0.0)!', ')', ')', \
                     'f(', '3 at pos (0.016, 0.032, 0.0)?', \
                           's(', 'f(', 'picked 3?', 'pick 3!', ')', 'place at (0.016, 0.032, 0.0)!', ')', ')', ')']

solve_cro = ['s(', 'f(', '0 at pos (0.0, 0.0, 0.0)?', 'place at (0.0, 0.0, 0.0)!', 'pick 0!', ')', 'f(', '2 at pos (0.016, -0.032, 0.0)?', 's(', 'f(', '3 at pos (0.016, 0.032, 0.0)?', 'pick 3!', ')', 'pick 2!', 'place at (0.016, -0.032, 0.0)!', ')', 'place at (0.016, 0.032, 0.0)!', ')', 'f(', '1 on 0?', 's(', 'pick 1!', 'place on 0!', ')', ')', 'apply force 1!', ')']



def select_bt(idx: int):
    collection = [_bt_1, _bt_2, _bt_3, _bt_croissant, solve_cro]
    return collection[idx]
