weight_dict = {
    'ultralight': 100,
    'light': 200,
    'normal': 400,
    'regular': 400,
    'book': 400,
    'medium': 500,
    'roman': 500,
    'semibold': 600,
    'demibold': 600,
    'demi': 600,
    'bold': 700,
    'heavy': 800,
    'extra bold': 800,
    'black': 900,
}

weight_set = set(weight_dict)

font_props_default = {
    'style': 'normal',
    'weight': weight_dict['normal'],
    "size": "scalable",
    "stretch": "normal",
    "variant": "normal",
}

font_extensions = {
    '.vfb', '.pfa', '.fnt', '.sfd', '.vlw', '.jfproj', '.woff', '.pfb', '.otf', '.fot', '.bdf', '.glif', '.woff2',
    '.odttf', '.ttf', '.fon', '.chr', '.pmt', '.fnt', '.ttc', '.amfm', '.bmfc', '.mf', '.pf2', '.compositefont', '.etx',
    '.gxf', '.pfm', '.abf', '.pcf', '.dfont', '.sfp', '.gf', '.mxf', '.ufo', '.tte', '.tfm', '.pfr', '.gdr', '.xfn',
    '.bf', '.vnf', '.afm', '.xft', '.eot', '.txf', '.acfm', '.pk', '.suit', '.ffil', '.nftr', '.t65', '.euf', '.cha',
    '.ytf', '.mcf', '.lwfn', '.f3f', '.fea', '.pft', '.sft'
}
