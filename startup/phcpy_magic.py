from __future__ import print_function
from IPython.core.magic import register_line_cell_magic

@register_line_cell_magic
def phcpy(line, cell=None):
    "Solve a system of polynomials formatted for phcpy."
    # TODO: progress bar

    from phcpy.solver import solve
    from phcpy.solutions import strsol2dict

    if cell is None:
        with open(line, 'r') as poly:
            sys = ' '.join([f.rstrip() for f in poly])
    else:
        # jupyter uses unix newlines
        sys = ' '.join([f.rstrip() for f in cell.split('\n')]) 
                # cell.replace('\n',' ').lstrip()
        
    # discard equation count (and undeterminate count) if present
    while sys.split(' ')[0].isdigit():
        sys = sys.split(' ', 1)[1]
        
    # convert to list with delimiters intact
    sys = [f+';' for f in sys.split(';')[:-1]]
    # for l in sys: print(l)
        
    ret = solve(sys)
    return [strsol2dict(s) for s in ret]

del phcpy # for automagic to work
