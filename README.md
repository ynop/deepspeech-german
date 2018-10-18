# DeepSpeech German
This repository contains scripts used to test deepspeech (https://github.com/mozilla/DeepSpeech) (v0.2.0-alpha.8).
This is just for prototyping.
The results, on speech that is noisy or very dissimilar to the training data, are really bad.

## Used data

### Language  model
For the language model a text corpus is used, also provided by the people of the " German speech data corpus"
(https://www.inf.uni-hamburg.de/en/inst/ab/lt/resources/data/acoustic-models.html).

### Speech data

* https://www.inf.uni-hamburg.de/en/inst/ab/lt/resources/data/acoustic-models.html (~30h)
* http://www.repository.voxforge1.org/downloads/de/Trunk/Audio/Main/16kHz_16bit/ (~50h)
* https://nats.gitlab.io/swc/ (~150h)

## Training

First the following path have to be defined:

* **tuda_corpus_path**: Path where the German Distant Speech Corpus is stored.
* **voxforge_corpus_path**: Path where the Voxforge German Speech data is stored.
* **swc_corpus_path**: Path where the Spoken Wikipedia Corpus is stored.
* **text_corpus_path**: Path where the text corpus is stored.
* **exp_path**: A directory where all output files are written to.
* **kenlm_bin**: Path to the kenLM tool
* **deepspeech**: Path to the cloned DeepSpeech repository

The commands are expected to be executed from the path where this repository is cloned. Take a look at `run_all.sh` as an example for executing all the commands.

### Install Python Requirements
```
pip install -r requirements.txt
```

For requirements regarding DeepSpeech checkout their repository.
For the native-client with gpu use:

```
python3 util/taskcluster.py --target native_client --branch "v0.2.0-alpha.8" --arch gpu
```

### Download the data
1. Download the text corpus from http://ltdata1.informatik.uni-hamburg.de/kaldi_tuda_de/German_sentences_8mil_filtered_maryfied.txt.gz and store it to `text_corpus_path`.
2. Download the German Distant Speech Corpus (TUDA) from http://www.repository.voxforge1.org/downloads/de/german-speechdata-package-v2.tar.gz and store it to `tuda_corpus_path`.
3. Download the Spoken Wikipedia Corpus (SWC) from https://nats.gitlab.io/swc/ and prepare
   it according to https://audiomate.readthedocs.io/en/latest/documentation/indirect_support.html.
4. Download the Voxforge German Speech data (via pingu python library):

```python
from audiomate.corpus import io

dl = io.VoxforgeDownloader(lang='de')
dl.download(voxforge_corpus_path)
```

### Prepare audio data
```
# prepare_data.py creates the csv files defining the audio data used for training
./prepare_data.py $tuda_corpus_path $voxforge_corpus_path $exp_path/data
```

### Build LM
```
# First the text is normalized and cleaned.
./prepare_vocab.py $text_corpus_path $exp_path/clean_vocab.txt

# KenLM is used to build the LM
$kenlm_bin/lmplz --text $exp_path/clean_vocab.txt --arpa $exp_path/words.arpa --o 3
$kenlm_bin/build_binary -T -s $exp_path/words.arpa $exp_path/lm.binary
```

### Build trie
```
# The deepspeech tools are used to create the trie
$deepspeech/native_client/generate_trie data/alphabet.txt $exp_path/lm.binary $exp_path/clean_vocab.txt $exp_path/trie
```

### Run training
```
./run_training.sh $deepspeech $(realpath data/alphabet.txt) $exp_path
```

## Results

```
I Test of Epoch 19 - WER: 0.667205, loss: 69.56213065852289, mean edit distance: 0.287312
I --------------------------------------------------------------------------------
I WER: 0.333333, loss: 0.544307, mean edit distance: 0.200000
I  - src: "p c b"
I  - res: "p c "
I --------------------------------------------------------------------------------
I WER: 0.500000, loss: 0.533773, mean edit distance: 0.142857
I  - src: "oder bundesrat"
I  - res: "der bundesrat "
I --------------------------------------------------------------------------------
I WER: 1.000000, loss: 0.102555, mean edit distance: 0.125000
I  - src: "handlung"
I  - res: "handlunge"
I --------------------------------------------------------------------------------
I WER: 1.000000, loss: 0.152456, mean edit distance: 0.500000
I  - src: "erde"
I  - res: "er "
I --------------------------------------------------------------------------------
I WER: 1.000000, loss: 0.152456, mean edit distance: 0.500000
I  - src: "erde"
I  - res: "er "
I --------------------------------------------------------------------------------
I WER: 1.000000, loss: 0.555418, mean edit distance: 0.500000
I  - src: "form"
I  - res: "vor "
I --------------------------------------------------------------------------------
I WER: 1.000000, loss: 0.714687, mean edit distance: 0.250000
I  - src: "werk"
I  - res: "wer "
I --------------------------------------------------------------------------------
I WER: 1.000000, loss: 0.851070, mean edit distance: 0.200000
I  - src: "texte"
I  - res: "text "
I --------------------------------------------------------------------------------
I WER: 1.000000, loss: 0.912912, mean edit distance: 0.600000
I  - src: "misst"
I  - res: "mit "
I --------------------------------------------------------------------------------
I WER: 2.000000, loss: 0.898193, mean edit distance: 0.250000
I  - src: "beilagen"
I  - res: "bei lagen "
I --------------------------------------------------------------------------------
```

