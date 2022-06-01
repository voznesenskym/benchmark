import subprocess
import sys
import os
import tarfile
from pathlib import Path


def pip_install_requirements():
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', '-r', 'requirements.txt'])

def spacy_download(language):
    subprocess.check_call([sys.executable, '-m', 'spacy', 'download', language])

def preprocess():
    current_dir = Path(os.path.dirname(os.path.realpath(__file__)))
    data_dir = os.path.join(current_dir.parent.parent, "data")
    decompress_dir = os.path.join(data_dir, ".data")
    multi30k_data_dir = os.path.join(current_dir.parent.parent, "data", ".data", "multi30k")
    for tarball in filter(lambda x: x.endswith(".tar.gz"), os.listdir(data_dir)):
        tarball_path = os.path.join(data_dir, tarball)
        tar = tarfile.open(tarball_path)
        tar.extractall(path=decompress_dir)
        tar.close()
    root = os.path.join(str(Path(__file__).parent), ".data")
    os.makedirs(root, exist_ok=True)
    subprocess.check_call([sys.executable, 'preprocess.py', '-lang_src', 'de', '-lang_trg', 'en', '-share_vocab',
                           '-save_data', os.path.join(root, 'm30k_deen_shr.pkl'), '-data_path', multi30k_data_dir])
if __name__ == '__main__':
    pip_install_requirements()
    spacy_download('en')
    spacy_download('de')
    # Preprocessed pkl is larger than 100MB so we cannot skip preprocess
    preprocess()

