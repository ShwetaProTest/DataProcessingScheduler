# Installation

To install the dependencies, run the following (you'll need at least Python 3.7):

```
pip install pandas azure-storage-blob
```

TODO: Can we improve these installation instructions?

# Usage

## Merge

To generate the merged schedule dataset provide the keyword `merge`:

```
python schedule_data_processing/app.py merge
```

The output will be saved as 

## Processing

To look up an individual flight record provide the keyword `lookup` 
followed by the flight number, e.g.:

```
python schedule_data_processing/app.py lookup ZG2362
```

To look up more than one flight record (the output JSON strings will be separated 
by newlines), provide a list of flights separated by commas, e.g.

```
python schedule_data_processing/app.py lookup ZG2361,ZG2362
```

TODO: Can we find a way to make these commands more user friendly, 
      e.g. `schedule_data lookup ZG2362`?