### Instructions to install the snakefile environment in this project

```bash
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh
```

After processing the installation of miniforge, you must restart your terminal, and proceed with the installation of snakefile:

```bash
conda activate base
mamba create -c bioconda -c conda-forge -n snakemake snakemake-minimal
```

Finally, after installing snakefile, you can get into the proper environment with:

```bash
mamba activate snakemake
```