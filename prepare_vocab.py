import click
import audiomate


@click.command()
@click.argument('target-path', type=click.Path())
@click.option('--text-path', '-t', multiple=True)
@click.option('--corpus-path', '-c', multiple=True)
def run(target_path, text_path, corpus_path):
    all_sentences = set()

    for path in text_path:
        print(' - Load sentences text-file {}'.format(path))
        with open(path, 'r') as text_path:
            for line in text_path.readlines():
                all_sentences.add(line.strip())

    for path in corpus_path:
        print(' - Load sentences corpus {}'.format(path))
        corpus = audiomate.Corpus.load(path)

        for utterance in corpus.utterances.values():
            ll = utterance.label_lists[audiomate.corpus.LL_WORD_TRANSCRIPT]
            all_sentences.append(ll.join().strip())

    print(' - Save all sentences: {}'.format(len(all_sentences)))
    with open(target_path, 'w') as f:
        f.write('\n'.join(all_sentences))


if __name__ == '__main__':
    run()
