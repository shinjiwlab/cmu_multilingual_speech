from pathlib import Path

class MkbuildConfig:
    
    root_path = Path(__file__).parent.parent
    data_path = root_path / 'data'
    docs_path = root_path / 'docs'
    github_root = "https://github.com/xinjli/cmu_multilingual_speech/tree/main"