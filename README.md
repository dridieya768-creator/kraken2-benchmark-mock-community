# Kraken2 benchmark on a simulated mock community

How precise is Kraken2 at classifying Illumina reads taxonomically, and down to what abundance can it
detect a species? This repository measures **false positives**, **recall** and the **limit of detection**
as a function of the `--confidence` threshold.

**Key result:** `[TO FILL: one sentence with your main finding and its number, e.g. best F1 at --confidence X, lowest abundance detected]`

## Method

1. **Mock community**: 7 bacterial species with abundances from 50% down to 0.01%, including two close
   species (*Escherichia coli*, *Shigella flexneri*) and a negative control absent from the mixture
   (*Vibrio cholerae*). Ground truth: `data/truth.csv`.
2. **Simulation**: Illumina paired-end reads (NovaSeq model, 2 M reads) generated with
   [InSilicoSeq](https://github.com/HadrienG/InSilicoSeq).
3. **Classification**: Kraken2 with the database `[TO FILL: database name and version]`,
   `--confidence` = 0, 0.05, 0.1, 0.2, 0.5.
4. **Evaluation**: `analyse.py` compares the species detected (at least `--min-reads` reads,
   default `[TO FILL: value]`) with the ground truth.

## Installation

```bash
mamba env create -f environment.yml
conda activate k2bench
```

## Usage

Put the community genomes in `data/genomes.fasta` (identifiers must match `data/abundances.txt`), then:

```bash
./run_benchmark.sh /path/to/kraken2_database
pytest            # unit tests for the metric functions
```

## Results

`[TO FILL: results from results/results.csv: precision/recall curve across --confidence, true vs estimated abundance, list of false positives]`

| `--confidence` | Precision | Recall | F1 | False positives | Limit of detection |
|---|---|---|---|---|---|
| 0.0 | | | | | |
| 0.05 | | | | | |
| 0.1 | | | | | |
| 0.2 | | | | | |
| 0.5 | | | | | |

*Limit of detection = lowest true abundance at which the species is still detected.*

## Limitations

- Simulated data: no real contamination or library-preparation bias.
- Results depend on the reference database and on the `--min-reads` parameter.
- Single simulation replicate `[TO FILL: update if you run several]`.

## Next steps

Abundance correction with Bracken, comparison with Kaiju / MetaPhlAn, a Snakemake pipeline.

## License

MIT
