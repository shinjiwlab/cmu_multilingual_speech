from pathlib import Path
from config import MkbuildConfig
from utils import read_markdown

def read_lang(lang_id):

    lang_dir = MkbuildConfig.data_path / 'lang' / lang_id

    info = None
    if (lang_dir / 'README.md').exists():
        info = read_markdown(lang_dir / 'README.md')

    corpus = None
    if (lang_dir / 'corpus.md').exists():
        corpus = read_markdown(lang_dir / 'corpus.md')

    recipe= None
    if (lang_dir / 'recipe.md').exists():
        recipe = read_markdown(lang_dir / 'recipe.md')

    model = None
    if (lang_dir / 'model.md').exists():
        model = read_markdown(lang_dir / 'model.md')

    inventory = None
    if (lang_dir / 'phoible.txt').exists():
        inventory = open(lang_dir / 'phoible.txt').read()

    return Language(lang_id, info, corpus, recipe, model, inventory)


def read_all_lang():

    langs = []
    for lang_dir in (MkbuildConfig.data_path / 'lang').glob('*'):
        lang_id = lang_dir.stem
        lang = read_lang(lang_id)

        langs.append(lang)

    return LanguageCollection(langs)


class LanguageCollection:

    def __init__(self, langs):
        self.langs = sorted(langs, key=lambda lang: lang.lang_id) 
        
    def __len__(self):
        return len(self.langs)
        
    def filter_by_corpus(self):
        return list(filter(lambda lang: lang.corpus is not None, self.langs))

    def filter_by_recipe(self):
        return list(filter(lambda lang: lang.recipe is not None, self.langs))

    def filter_by_model(self):
        return list(filter(lambda lang: lang.model is not None, self.langs))

    def filter_by_alphabet(self, char):
        return list(filter(lambda lang: lang.lang_id.startswith(char), self.langs))


class Language:

    def __init__(self, lang_id, info, corpus, recipe, model, inventory):
        self.lang_id = lang_id
        self.info = info
        self.corpus = corpus
        self.recipe = recipe
        self.model = model
        self.inventory = inventory