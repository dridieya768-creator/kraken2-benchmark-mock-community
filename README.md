# Benchmark de Kraken2 sur une communauté mock simulée

Quelle est la précision de Kraken2 pour la classification taxonomique de reads Illumina,
et jusqu'à quelle abondance détecte-t-il une espèce ? Ce dépôt mesure les **faux positifs**,
le **rappel** et la **limite de détection** en fonction du seuil `--confidence`.

## Méthode
1. **Communauté mock** : 7 espèces bactériennes à abondances de 50 % à 0,01 %, dont deux espèces
   proches (*Escherichia coli*, *Shigella flexneri*), plus un contrôle négatif absent du mélange
   (*Vibrio cholerae*). Vérité terrain : `data/truth.csv`.
2. **Simulation** : reads Illumina paired-end (modèle NovaSeq, 2 M reads) avec [InSilicoSeq](https://github.com/HadrienG/InSilicoSeq).
3. **Classification** : Kraken2 avec la base `[À COMPLÉTER : nom et version de la base]`,
   seuils `--confidence` = 0, 0.05, 0.1, 0.2, 0.5.
4. **Évaluation** : `analyse.py` compare les espèces détectées (≥ `--min-reads` reads) à la vérité.

## Installation
```bash
mamba env create -f environment.yml
conda activate k2bench
```

## Utilisation
Place les génomes de la communauté dans `data/genomes.fasta` (identifiants cohérents avec
`data/abundances.txt`), puis :
```bash
./run_benchmark.sh /chemin/vers/base_kraken2
pytest            # tests unitaires des fonctions de calcul
```

## Résultats
> À COMPLÉTER avec tes vrais chiffres : tableau `results/results.csv`, courbe précision/rappel
> selon `--confidence`, abondance réelle vs estimée, liste des faux positifs.

| --confidence | Précision | Rappel | F1 | Limite de détection |
|---|---|---|---|---|
| 0.0 | | | | |
| 0.1 | | | | |
| 0.5 | | | | |

## Limites
- Données simulées : pas de contaminations ni de biais de préparation réels.
- Résultats dépendants de la base de référence et du paramètre `--min-reads`.
- Une seule réplique de simulation `[À COMPLÉTER si tu en fais plusieurs]`.

## Pistes
Correction d'abondance avec Bracken, comparaison avec Kaiju / MetaPhlAn, pipeline Snakemake.

## Licence
MIT
