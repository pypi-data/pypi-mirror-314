### TVSM Extractor

Tooling for reading [this dataset](https://zenodo.org/records/7025971).

### Usage

Run from within a parent directory of unzipped TVSM datasets.
Files are output to "TVSM-extractor-audio" and "TVSM-extractor-images".

### Test data

All samples by default

```
tvsm-extractor
```

### Specific language

```
tvsm-extractor --language en
```

### Specific language and genre

```
tvsm-extractor --language en --genre Thrillers
```

## Specific file/files

```
tvsm-extractor test 3235
```

### Cue sheet training data

Note, the speech timings are very noisy.

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
