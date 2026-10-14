#!/usr/bin/env bash
# Usage : ./run_benchmark.sh /chemin/vers/base_kraken2
set -euo pipefail
DB="${1:?Indique le chemin de la base Kraken2}"
mkdir -p results && cd results

# 1. Simulation des reads Illumina (vérité connue)
iss generate --genomes ../data/genomes.fasta --abundance_file ../data/abundances.txt \
  --model novaseq --n_reads 2000000 --output mock

# 2. Kraken2 à plusieurs seuils de confiance
for c in 0.0 0.05 0.1 0.2 0.5; do
  kraken2 --db "$DB" --paired --confidence "$c" --threads 4 \
    --report "report_c${c}.txt" --output "out_c${c}.txt" \
    mock_R1.fastq mock_R2.fastq
done

# 3. Métriques
python ../analyse.py --truth ../data/truth.csv --reports "report_c*.txt" --min-reads 10 --out results.csv
