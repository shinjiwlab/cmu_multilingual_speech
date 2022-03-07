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

    if (MkbuildConfig.docs_path / 'index').exists():
        print("cleaning old files...")
        shutil.rmtree(MkbuildConfig.docs_path / 'index')


def write_table(w, lang_lst, relative_path='/cmu_multilingual_speech/lang'):

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
            row.append('[yes]('+relative_path+'/'+lang_id+'/corpus)')
        else:
            row.append('')

        # create recipe
        if lang.recipe is not None:
            row.append('[yes]('+relative_path+'/'+lang_id+'/recipe)')
        else:
            row.append('')
            
        # create model
        if lang.model is not None:
            row.append('[yes]('+relative_path+'/'+lang_id+'/model)')
        else:
            row.append('')
            
        # create inventory
        if lang.model is not None:
            row.append(f'[yes]({MkbuildConfig.github_root}/data/lang/{lang_id}/phoible.txt)')
        else:
            row.append('')
            
        w.write('|' + '|'.join(row) + '|\n')
            

def embed_map(w, langs):

    w.write("""\n\n<div id='map' style='height: 640px'></div>\n<script>var langs = [""")
    for lang in langs:
        if lang.info is not None:
            a = float(lang.info['info']['latitude'])
            b = float(lang.info['info']['longitude'])
            if a is None or np.isnan(a) or b is None or np.isnan(b):
                continue

            w.write("{"+f"""\"type": "Point", "coordinates": [{b}, {a}], "popupContent": "<a href='/cmu_multilingual_speech/lang/{lang.lang_id}'>{lang.lang_id}</a>\""""+"},\n")
    w.write("];\n</script>\n\n")


def build_index(lang_collection):
    w = open(MkbuildConfig.docs_path / 'index.md', 'w')
    w.write("""---\nhide:\n- toc\n- navigation\n---\n""")
    w.write("""# Home \nWelcome to CMU Speech Multilingual DB\nFor full data, visit our [repository](https://github.com/shinjiwlab/cmu_multilingual_speech).\n\n""")
    w.write(f"We attempt to index speech database for **{len(lang_collection)}** languages.")
    w.write("![map](./img/map.png)\n")
    w.close()


def build_lang_index(lang_collection):
    w = open(MkbuildConfig.docs_path / 'lang/index.md', 'w')
    w.write("""---\nhide:\n- toc\n- navigation\n---\n""")
    w.write("""# Language\n""")
    embed_map(w, lang_collection.langs)
    write_table(w, lang_collection.langs, '.')
    w.close()


def build_alphabet_index(lang_collection):

    (MkbuildConfig.docs_path / 'index').mkdir(parents=True, exist_ok=True)

    w = open(MkbuildConfig.docs_path / 'index/index.md', 'w')
    w.write("""---\nhide:\n- toc\n- navigation\n---\n""")
    w.write("""# Language\n""")
    embed_map(w, lang_collection.langs)

    w.write("## Language Index\n\n")
    for i in range(ord('a'), ord('z')+1):
        char = chr(i)
        w.write(f"[Languages ISO Prefix {char.upper()}](/cmu_multilingual_speech/index/{char})\n\n")

    w.close()

    for i in range(ord('a'), ord('z')+1):
        char = chr(i)
        w = open(MkbuildConfig.docs_path / f'index/{char}.md', 'w')
        lang_lst = lang_collection.filter_by_alphabet(char)
        w.write("""---\nhide:\n- toc\n- navigation\n---\n""")
        w.write(f"# Language {char.upper()}\n\n")
        embed_map(w, lang_lst)
        write_table(w, lang_lst)
        w.close()


def write_progressbar(w, lang_collection, lang_lst):

    w.write(f"[={len(lang_lst)*100/len(lang_collection):.2f}% \"{len(lang_lst)*100/len(lang_collection):.2f}% available \"]\n\n")


def build_corpus(lang_collection):

    w = open(MkbuildConfig.docs_path / 'corpus.md', 'w')
    w.write("""---\nhide:\n- toc\n- navigation\n---\n""")
    w.write("""# Corpus\n\n""")
    lang_lst = lang_collection.filter_by_corpus()
    embed_map(w, lang_lst)
    write_progressbar(w, lang_collection, lang_lst)
    write_table(w, lang_lst)
    w.close()


def build_model(lang_collection):

    w = open(MkbuildConfig.docs_path / 'model.md', 'w')
    w.write("""---\nhide:\n- toc\n- navigation\n---\n""")
    w.write("""# Model\n\n""")
    lang_lst = lang_collection.filter_by_model()
    embed_map(w, lang_lst)
    write_progressbar(w, lang_collection, lang_lst)

    write_table(w, lang_lst)
    w.close()


def build_recipe(lang_collection):

    w = open(MkbuildConfig.docs_path / 'recipe.md', 'w')
    w.write("""---\nhide:\n- toc\n- navigation\n---\n""")
    w.write("""# Recipe\n\n""")
    lang_lst = lang_collection.filter_by_recipe()
    embed_map(w, lang_lst)
    write_progressbar(w, lang_collection, lang_lst)
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

    w.write("\n\n")
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
    build_alphabet_index(lang_collection)