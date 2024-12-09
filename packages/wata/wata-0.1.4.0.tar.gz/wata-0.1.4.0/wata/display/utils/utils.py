


def wataprint(content,type):
    color_map = {
        "r": "\x1b[31m{}\x1b[0m",
        "rr": "\x1b[1;31m{}\x1b[0m",
        "r_": "\x1b[4;31m{}\x1b[0m",
        "rr_": "\x1b[1;4;31m{}\x1b[0m",
        "rx": "\x1b[3;31m{}\x1b[0m",
        "rx_": "\x1b[3;4;31m{}\x1b[0m",
        "rrx": "\x1b[1;3;31m{}\x1b[0m",
        "rrx_": "\x1b[1;3;4;31m{}\x1b[0m",
        
        "g": "\x1b[32m{}\x1b[0m",
        "gg": "\x1b[1;32m{}\x1b[0m",
        "g_": "\x1b[4;32m{}\x1b[0m",
        "gg_": "\x1b[1;4;32m{}\x1b[0m",
        
        "y": "\x1b[33m{}\x1b[0m",
        "yy": "\x1b[1;33m{}\x1b[0m",
        "y_": "\x1b[4;33m{}\x1b[0m",
        "yy_": "\x1b[1;4;33m{}\x1b[0m",
        
        "p": "\x1b[35m{}\x1b[0m",
        "pp": "\x1b[1;35m{}\x1b[0m",
        "p_": "\x1b[4;35m{}\x1b[0m",
        "pp_": "\x1b[1;4;35m{}\x1b[0m",
        
        "b": "\x1b[36m{}\x1b[0m",
        "bb": "\x1b[1;36m{}\x1b[0m",
        "b_": "\x1b[4;36m{}\x1b[0m",
        "bb_": "\x1b[1;4;36m{}\x1b[0m",
    }
    print(color_map[type].format(content))