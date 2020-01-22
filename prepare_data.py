import os
import sys
import click

import audiomate
from audiomate.corpus import io

@click.command()
@click.argument('source-path', type=click.Path(exists=True))
@click.argument('target-path', type=click.Path())
def run(source_path, target_path):
    print('Load corpus')
    corpus = audiomate.Corpus.load(source_path)

    print('Save in deepspeech format')
    deepspeech_writer = io.MozillaDeepSpeechWriter()
    deepspeech_writer.save(corpus, target_path)


if __name__ == '__main__':
    run()
