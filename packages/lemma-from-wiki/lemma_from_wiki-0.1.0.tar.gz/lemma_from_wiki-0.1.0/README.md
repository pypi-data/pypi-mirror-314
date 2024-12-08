# Overview

Gets a wikipedia dump for a language and creates a lemma table from it for use in [vocabsieve](https://github.com/FreeLanguageTools/vocabsieve/).

Project is AGPL3+ licensed as it re-uses code from [gogadget](https://gogadget.jfox.io).

Needs CUDA toolkit installed and an NVIDIA GPU available: <https://developer.nvidia.com/cuda-toolkit-archive>
On Windows, you will need to install Visual Studio first. I also needed to manually add the following to my PATH: `C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.42.34433\bin\Hostx64\x64`

# Running

Assumes `uv` but will work equally well with a pip venv.

No need to download anything apart from this repository. The script will automatically grab the wikipedia articles for your chosen language.

Running:

```sh
git clone https://github.com/jonathanfox5/lemma_from_wiki
cd lemma_from_wiki
uv sync
uv run lemma_from_wiki -l "language code" -n "number of articles to process"
```

Getting help:

```sh
uv run lemma_from_wiki --help
```

Or just :

```sh
uv run lemma_from_wiki
```
