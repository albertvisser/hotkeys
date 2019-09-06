"""HotKeys gtkaccel plugin - code for wrting to descriptions file
"""
import os
import csv
import shutil


def read_data(outfile, desc):
    try:
        _in = open(outfile)
    except FileNotFoundError:
        return '{} not found'.format(outfile), {}
    else:
        with _in:
            rdr = csv.reader(_in)
            for line in rdr:
                if line:
                    key, oms = line
                    ## print(key, oms)
                    if oms:
                        desc[int(key)] = oms
    return '', desc


def write_data(outfile, new_values):
    if os.path.exists(outfile):
        shutil.copyfile(outfile, outfile + '~')
    with open(outfile, 'w') as _out:
        writer = csv.writer(_out)
        for key, value in new_values.items():
            if value:
                writer.writerow((key, value))

