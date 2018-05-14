# DeepSpeech German
This repository contains scripts used to test deepspeech (https://github.com/mozilla/DeepSpeech) with a "small" set of german speech (~60h). This is just for prototyping. The results, on speech that is noisy or very dissimilar to the training data, are really bad.

## Used data

### Language  model
For the language model a text corpus is used, also provided by the people of the " German speech data corpus"
(https://www.inf.uni-hamburg.de/en/inst/ab/lt/resources/data/acoustic-models.html).

### Speech data

* https://www.inf.uni-hamburg.de/en/inst/ab/lt/resources/data/acoustic-models.html
* http://www.repository.voxforge1.org/downloads/de/Trunk/Audio/Main/16kHz_16bit/

## Training

First the following path have to be defined:

* **tuda_corpus_path**: Path where the German Distant Speech Corpus is stored.
* **voxforge_corpus_path**: Path where the Voxforge German Speech data is stored.
* **text_corpus_path**: Path where the text corpus is stored.
* **exp_path**: A directory where all output files are written to.
* **kenlm_bin**: Path to the kenLM tool
* **deepspeech**: Path to the cloned DeepSpeech repository

The commands are expected to be executed from the path where this repository is cloned. Take a look at `run_all.sh` as an example for executing all the commands.

### Install Python Requirements
```
pip install -r requirements.txt
```

### Download the data
1. Download the text corpus from http://ltdata1.informatik.uni-hamburg.de/kaldi_tuda_de/German_sentences_8mil_filtered_maryfied.txt.gz and store it to `text_corpus_path`.
2. Download the German Distant Speech Corpus (TUDA) from http://www.repository.voxforge1.org/downloads/de/german-speechdata-package-v2.tar.gz and store it to `tuda_corpus_path`.
3. Download the Voxforge German Speech data (via pingu python library):
```python
from pingu.corpus import io

dl = io.VoxforgeDownloader(lang='de')
dl.download(voxforge_corpus_path)
```

### Build LM 
```
# First the text is normalized and cleaned.
./prepare_text.py $text_corpus_path $exp_path/clean_vocab.txt

# KenLM is used to build the LM
$kenlm_bin/lmplz --text $exp_path/clean_vocab.txt --arpa $exp_path/words.arpa --o 3
$kenlm_bin/build_binary -T -s $exp_path/words.arpa $exp_path/lm.binary
```

### Build trie
```
# The deepspeech tools are used to create the trie
$deepspeech/native_client/generate_trie data/alphabet.txt $exp_path/lm.binary $exp_path/clean_vocab.txt $exp_path/trie
```

### Prepare audio data
```
# prepare_data.py creates the csv files defining the audio data used for training
./prepare_data.py $tuda_corpus_path $voxforge_corpus_path $exp_path/data
```

### Run training
```
./run_training.sh $deepspeech $(realpath data/alphabet.txt) $exp_path
```

## Results

```
I Test of Epoch 29 - WER: 0.809315, loss: 122.42175595, mean edit distance: 0.326160
I --------------------------------------------------------------------------------
I WER: 0.250000, loss: 1.636255, mean edit distance: 0.043478
I  - src: "ich möchte bitte kochen"
I  - res: "ich möchte bitte kocen"
I --------------------------------------------------------------------------------
I WER: 0.250000, loss: 1.869046, mean edit distance: 0.043478
I  - src: "ich werde sie ausmachen"
I  - res: "ich werde sie ausmache"
I --------------------------------------------------------------------------------
I WER: 0.250000, loss: 2.086848, mean edit distance: 0.043478
I  - src: "ich werde sie ausmachen"
I  - res: "ich werde sie ausmochen"
I --------------------------------------------------------------------------------
I WER: 0.250000, loss: 2.458537, mean edit distance: 0.043478
I  - src: "ich möchte etwas kochen"
I  - res: "ich möchte etwas krochen"
I --------------------------------------------------------------------------------
I WER: 0.250000, loss: 2.557195, mean edit distance: 0.043478
I  - src: "ich möchte etwas kochen"
I  - res: "ich möchte etwas krochen"
I --------------------------------------------------------------------------------
I WER: 0.333333, loss: 0.520140, mean edit distance: 0.058824
I  - src: "ich möchte kochen"
I  - res: "ich möchte krochen"
I --------------------------------------------------------------------------------
I WER: 0.333333, loss: 2.551879, mean edit distance: 0.230769
I  - src: "miss die zeit"
I  - res: "ist die zeit "
I --------------------------------------------------------------------------------
I WER: 0.500000, loss: 1.450505, mean edit distance: 0.076923
I  - src: "ich möchte häppchen machen"
I  - res: "ich möchte häpchenmachen"
I --------------------------------------------------------------------------------
I WER: 1.000000, loss: 0.757631, mean edit distance: 1.000000
I  - src: "gut"
I  - res: ""
I --------------------------------------------------------------------------------
I WER: 1.000000, loss: 2.250979, mean edit distance: 1.000000
I  - src: "gern"
I  - res: "die "
```
