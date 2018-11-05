# DynaST
**Dynamic Scrapping Tool** (DynaST) is a tool created to download and extract information from the iBeetle (https://ibeetle-base.uni-goettingen.de/) database.

## Installation

1. Download the dynast.py Python script

```wget https://raw.githubusercontent.com/tasmonteiro/bioinfoscripts/master/dynast/dynast.py```

2. (Optional) Make it executable without calling Python

```chmod +x dynast.py```

## Usage

1. Right-click the empty space inside the installation folder and open a terminal

2. Running dynast in standart mode will generate all files that you'll need

```python3 dynast.py```

3. But adding flags to the execution command will alter its parameters, allowing for customization

```(python3) dynast.py -v(erbose) -s(crapper-only) -i(nput) INPUT_PATH -o(utput) OUTPUT_PATH -n(ame) OUTPUT_FILE_NAME```

4. You can always check the help (-h) option

```(python3) dynast.py -h(--help)```
