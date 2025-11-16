# Data Files

## gene_network_data.h5

**Size**: 1.97 GB (too large for GitHub)

**Download Link**: [Provide your download link here]

### Description
This HDF5 file contains:
- **TEC Matrix**: Translation Efficiency Covariation correlation matrix (11,088 × 11,088 genes)
- **RNA Matrix**: RNA expression correlation matrix (11,088 × 11,088 genes)

### Usage
After downloading, place the file in this directory:
```
data/gene_network_data.h5
```

Then run the analysis:
```bash
python run_remaining_notebooks.py
```

### Alternative
Pre-computed results are available in:
- `gnn_only_results.json`
- `gnn_vs_traditional_comparison.json`
- `analysis_results/comprehensive_experiments_results.json`
