## Overview

Gets a wikipedia dump for a language and creates a lemma table from it for use in [vocabsieve](https://github.com/FreeLanguageTools/vocabsieve/). Uses `spacy` as the lemmatiser but also provides results from `simplemma` for comparison.

Project is AGPL3+ licensed as it re-uses code from [gogadget](https://gogadget.jfox.io).

Needs CUDA toolkit installed and an NVIDIA GPU available: <https://developer.nvidia.com/cuda-toolkit-archive>

On Windows, you will need to install Visual Studio first. I also needed to manually add the following to my PATH: `C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.42.34433\bin\Hostx64\x64`

## Running

Installation instructions assume the use of [uv](https://docs.astral.sh/uv/) to automatically deal with package isolation but will work equally well with a pip venv (if you prefer).

No need to download any extra files. The script will automatically grab the wikipedia articles for your chosen language.

**Install from Pypi**

```sh
uv tool install lemma-from-wiki
```

**Standard analysis**

```sh
lemmafromwiki -l "language code" -n "number of articles to process"
```

**Return only differences from `simplemma`**

```sh
lemmafromwiki -l "language code" -n "number of articles to process" --diff
```

**Getting help**

```sh
lemmafromwiki --help
```

**Getting help (short version)**

```sh
lemmafromwiki
```
