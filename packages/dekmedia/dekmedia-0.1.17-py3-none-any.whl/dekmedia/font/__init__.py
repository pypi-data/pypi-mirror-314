import re
from matplotlib import font_manager


def is_font_family(s):
    return re.fullmatch(r'^[ 0-9a-zA-Z_-]+$', s)


def find_font_path(font_name):
    try:
        return font_manager.findfont(font_manager.FontProperties(family=font_name), fallback_to_default=False)
    except ValueError:
        return None


def get_font_source(name):
    if name is None:
        name = 'SimSun'
    if isinstance(name, str):
        if is_font_family(name):
            font_path = find_font_path(name)
        else:
            font_path = name
        with open(font_path, 'rb') as f:
            return f.read()
    elif isinstance(name, bytes):
        return name
    else:
        return name.getvalue()


all_fonts_ext = {
    '.vfb', '.pfa', '.fnt', '.sfd', '.vlw', '.jfproj', '.woff', '.pfb', '.otf', '.fot', '.bdf', '.glif', '.woff2',
    '.odttf', '.ttf', '.fon', '.chr', '.pmt', '.fnt', '.ttc', '.amfm', '.bmfc', '.mf', '.pf2', '.compositefont', '.etx',
    '.gxf', '.pfm', '.abf', '.pcf', '.dfont', '.sfp', '.gf', '.mxf', '.ufo', '.tte', '.tfm', '.pfr', '.gdr', '.xfn',
    '.bf', '.vnf', '.afm', '.xft', '.eot', '.txf', '.acfm', '.pk', '.suit', '.ffil', '.nftr', '.t65', '.euf', '.cha',
    '.ytf', '.mcf', '.lwfn', '.f3f', '.fea', '.pft', '.sft'
}
