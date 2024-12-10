### TVSM Extractor

Tooling for reading [this dataset](https://zenodo.org/records/7025971).

### Usage

Run from within a parent directory of unzipped TVSM datasets.
Files are output to "TVSM-extractor-audio" and "TVSM-extractor-images".

### Test data

All English documentaries by default

```
tvsm-extractor
```

## Specific file/files

```
tvsm-extractor test 3235
```

### Cue sheet training data

All English documentaries by default

```
tvsm-extractor cuesheet
```


### Pseudo training data

This project has not been tested on `TVSM-pseudo`.


### Dev

```
hatch build
hatch publish
```
