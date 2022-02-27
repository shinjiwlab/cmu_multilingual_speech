from pathlib import Path
import shutil
import os
from config import MkbuildConfig
from lang import read_all_lang
from utils import copy_file_with_header
import numpy as np

def clean_docs():
    
    if (MkbuildConfig.docs_path / 'lang').exists():
        print("cleaning old files...")
        shutil.rmtree(MkbuildConfig.docs_path / 'lang')


def write_table(w, lang_lst):

    w.write("| Language Id | Language Name | Corpus | Recipe | Model | Inventory |\n|-|-|-|-|-|-|\n")

    for lang in lang_lst:
        lang_id = lang.lang_id

        row = []
        row.append(f'[{lang_id}]({MkbuildConfig.github_root}/data/lang/{lang_id})')

        # create name
        name = ''
        if lang.info is not None:
            name = lang.info['info']['name']

        row.append(name)

        # create corpus
        if lang.corpus is not None:
            row.append('[yes](./lang/'+lang_id+'/corpus.md)')
        else:
            row.append('')

        # create recipe
        if lang.recipe is not None:
            row.append('[yes](./lang/'+lang_id+'/recipe.md)')
        else:
            row.append('')
            
        # create model
        if lang.model is not None:
            row.append('[yes](./lang/'+lang_id+'/model.md)')
        else:
            row.append('')
            
        # create inventory
        if lang.model is not None:
            row.append(f'[yes]({MkbuildConfig.github_root}/data/lang/{lang_id}/phoible.txt)')
        else:
            row.append('')
            
        w.write('|' + '|'.join(row) + '|\n')
            


    # for lang_dir in lang_lst:
    #     lang_id = lang_dir.stem
    #
    #     lst = []
    #
    #     lst.append(f'[{lang_id}]({MkbuildConfig.github_root}/data/lang/{lang_id})')
    #     readme = lang_dir /'README.md'
    #
    #     if not readme.exists():
    #         continue
    #
    #     r = open(readme, 'r')
    #     for line in r:
    #         if not line.startswith('| name'):
    #             continue
    #         lang_name = line.strip().split('|')[2]
    #         lst.append(lang_name)
    #         break
    #
    #     if (lang_dir / 'corpus.md').exists():
    #         lst.append('[yes](./lang/'+lang_id+'/corpus.md)')
    #     else:
    #         lst.append('')
    #
    #     if (lang_dir / 'recipe.md').exists():
    #         lst.append('[yes](./lang/'+lang_id+'/recipe.md)')
    #     else:
    #         lst.append('')
    #
    #     if (lang_dir / 'model.md').exists():
    #         lst.append('[yes](./lang/'+lang_id+'/model.md)')
    #     else:
    #         lst.append('')
    #
    #     if (lang_dir / 'phoible.txt').exists():
    #         lst.append(f'[yes]({MkbuildConfig.github_root}/data/lang/{lang_id}/phoible.txt)')
    #     else:
    #         lst.append('')
    #
    #     w.write('|' + '|'.join(lst) + '|\n')


def write_langs():

    """
    var langs = [{
    "type": "Point",
    "coordinates": [0, 0],
    "popupContent": "<a href='https://www.google.com'>hello</a>"
}, {
    "type": "Point",
    "coordinates": [30, 30],
    "popupContent": "world"
}];
    """


def embed_map(w, langs):

    w.write("""\n\n<div id='map' style='height: 500px'></div>\n<script>var langs = [""")
    for lang in langs:
        if lang.info is not None:
            a = float(lang.info['info']['latitude'])
            b = float(lang.info['info']['longitude'])
            if a is None or np.isnan(a) or b is None or np.isnan(b):
                continue

            w.write("{"+f"""\"type": "Point", "coordinates": [{b}, {a}], "popupContent": "<a href='/lang/{lang.lang_id}'>{lang.lang_id}</a>\""""+"},\n")
    w.write("];\n</script>\n\n")


def build_index(lang_collection):
    w = open(MkbuildConfig.docs_path / 'index.md', 'w')
    w.write("""---\nhide:\n- toc\n- navigation\n---\n""")
    w.write("""# Home \nWelcome to CMU Speech Multilingual DB\nFor full data, visit our repository.\n\n""")
    w.write("![map](./img/map.png)\n")
    w.close()


def build_lang_index(lang_collection):
    w = open(MkbuildConfig.docs_path / 'lang/index.md', 'w')
    w.write("""---\nhide:\n- toc\n- navigation\n---\n""")
    w.write("""# Language\n""")
    embed_map(w, lang_collection.langs)
    write_table(w, lang_collection.langs)
    w.close()


def build_corpus(lang_collection):

    w = open(MkbuildConfig.docs_path / 'corpus.md', 'w')
    w.write("""---\nhide:\n- toc\n- navigation\n---\n""")
    w.write("""# Corpus\n\n""")
    lang_lst = lang_collection.filter_by_corpus()
    embed_map(w, lang_lst)
    write_table(w, lang_lst)
    w.close()


def build_model(lang_collection):

    w = open(MkbuildConfig.docs_path / 'model.md', 'w')
    w.write("""---\nhide:\n- toc\n- navigation\n---\n""")
    w.write("""# Model\n\n""")
    lang_lst = lang_collection.filter_by_model()
    embed_map(w, lang_lst)
    write_table(w, lang_lst)
    w.close()


def build_recipe(lang_collection):

    w = open(MkbuildConfig.docs_path / 'recipe.md', 'w')
    w.write("""---\nhide:\n- toc\n- navigation\n---\n""")
    w.write("""# Model\n\n""")
    lang_lst = lang_collection.filter_by_recipe()
    embed_map(w, lang_lst)
    write_table(w, lang_lst)
    w.close()


def build_individual_lang(source_lang_dir, target_lang_dir, lang):

    if target_lang_dir.exists():
        return

    target_lang_dir.mkdir(parents=True, exist_ok=True)
    w = open(target_lang_dir / 'index.md', 'w')
    w.write("""---\nhide:\n- toc\n- navigation\n---\n""")

    w = open(target_lang_dir / 'index.md', 'w')
    lang_id = lang.lang_id

    w.write('# '+lang_id+'\n')

    if (source_lang_dir / 'README.md').exists():
        r = open(source_lang_dir / 'README.md', 'r')
        w.write(r.read())
        r.close()

    write_table(w, [lang])

    w.close()


def build_language(lang_collection):

    # clean previous builds
    if Path(MkbuildConfig.docs_path / 'lang').exists():
        shutil.rmtree(MkbuildConfig.docs_path / 'lang')

    (MkbuildConfig.docs_path / 'lang').mkdir(exist_ok=True, parents=True)

    w = open(MkbuildConfig.docs_path / 'lang/index.md', 'w')
    w.write("""---\nhide:\n- toc\n- navigation\n---\n""")

    w.write("""# Language\n""")
    w.close()

    data_dir = MkbuildConfig.data_path / 'lang'
    target_dir = MkbuildConfig.docs_path / 'lang'

    for lang in lang_collection.langs:
        lang_id = lang.lang_id
        source_lang_dir = data_dir / lang_id
        target_lang_dir = target_dir / lang_id

        if lang.corpus is not None:
            build_individual_lang(source_lang_dir, target_lang_dir, lang)
            copy_file_with_header(source_lang_dir / 'corpus.md', target_lang_dir / 'corpus.md')

        if lang.recipe is not None:
            build_individual_lang(source_lang_dir, target_lang_dir, lang)
            copy_file_with_header(source_lang_dir / 'recipe.md', target_lang_dir / 'recipe.md')

        if lang.model is not None:
            build_individual_lang(source_lang_dir, target_lang_dir, lang)
            copy_file_with_header(source_lang_dir / 'model.md', target_lang_dir / 'model.md')


if __name__ == '__main__':

    print("loading all data")
    lang_collection = read_all_lang()

    print("Building...")
    build_index(lang_collection)
    build_corpus(lang_collection)
    build_model(lang_collection)
    build_recipe(lang_collection)
    build_language(lang_collection)
    build_lang_index(lang_collection)