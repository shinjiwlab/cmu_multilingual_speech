import pandas as pd


def read_markdown(file_path):

    df = pd.read_table(file_path, sep="|", header=0, index_col=1, skipinitialspace=True, skiprows=1).dropna(axis=1, how='all')

    df.columns = df.columns.str.strip()
    df.index = df.index.str.strip()
    return df

def read_geo(lang):
    return [float(lang.info['info']['latitude']),  float(lang.info['info']['longitude'])]


def copy_file_with_header(source, target):

    w = open(target, 'w')
    r = open(source, 'r')
    w.write("""---\nhide:\n- toc\n- navigation\n---\n""")
    w.write(r.read())
    w.close()
    r.close()
