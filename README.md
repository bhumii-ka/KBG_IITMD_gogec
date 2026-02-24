# Drug Discovery Pipeline for Disease-Drug Interaction Analysis

A comprehensive machine learning pipeline for identifying potential drug candidates for various diseases by analyzing gene regulation patterns and drug-target binding affinities. This project combines gene expression analysis, deep learning-based binding prediction, and ADMET profiling to rank drugs based on their therapeutic potential.

##  Project Overview

This pipeline integrates three key approaches to identify and rank drug candidates:

1. **Gene Regulation Analysis**: Matches disease gene signatures with drug perturbation profiles
2. **Drug-Target Binding Prediction**: Uses DeepPurpose framework to predict binding affinities
3. **ADMET Profiling**: Evaluates drug-like properties and pharmacokinetic characteristics

### Key Features

- Multi-source drug data integration from SMILES representations
- Disease-specific gene signature analysis
- Deep learning-based binding affinity prediction
- Comprehensive ADMET property calculation
- Dual ranking methodology for drug candidates

##  Pipeline Architecture

```
Disease Signatures + Drug Perturbation Data
    ↓
Gene Regulation Scoring (reg_scores.ipynb)
    ↓
Drug-Target Binding Prediction (binding_score.ipynb)
    ↓
Combined Scoring (final_drug_pred.ipynb)
    ↓
ADMET Profiling (ADMET.ipynb)
    ↓
Ranked Drug Candidates
```

##  Project Structure



## Getting Started

### Prerequisites

```bash
# Core dependencies
python >= 3.10
pandas
numpy
rdkit
torch

# Deep learning framework
DeepPurpose
descriptastorus

# Additional libraries
scikit-learn
matplotlib
```

### Installation

1. Clone the repository
```bash
git clone <repository-url>
cd drug-discovery-pipeline
```

2. Install DeepPurpose and dependencies
```bash
pip install git+https://github.com/bp-kelley/descriptastorus
pip install DeepPurpose
pip install rdkit pandas numpy scikit-learn
```

##  Methodology

### 1. Gene Regulation Scoring (`matching.ipynb`)

**Purpose**: Identifies drugs whose perturbation signatures counter disease gene expression patterns.

**Process**:
- Loads disease signatures with upregulated and downregulated genes
- Loads drug perturbation profiles from large-scale screening datasets
- Computes matching scores by comparing gene regulation directions
- Generates disease-specific drug scoring matrices

**Key Concept**: Drugs that downregulate disease-upregulated genes and upregulate disease-downregulated genes receive favorable scores (negative values indicate therapeutic potential).

**Output**:  Matrix of drugs × diseases with regulation scores

### 2. Drug-Target Binding Prediction (`binding_score.ipynb`)

**Purpose**: Predicts binding affinities between drug compounds and disease-associated protein targets using deep learning.

**Process**:
- Utilizes DeepPurpose framework with pre-trained models
- Encodes drugs as SMILES strings and proteins as amino acid sequences
- Generates drug-gene binding affinity matrix
- Supports multiple encoding methods (Morgan fingerprints, CNN, Transformer, etc.)

**Models Used**:
- Drug encoding: Morgan fingerprints, MPNN, CNN
- Protein encoding: CNN, Transformer, AAC
- Prediction: Pre-trained models from BindingDB and other databases

**Output**: Binding scores for drug-target pairs

### 3. Combined Drug Ranking (`final_drug_pred.ipynb`)

**Purpose**: Integrates gene regulation and binding scores to rank drug candidates for each disease.

**Methodology**:

We present results using **two complementary ranking approaches**:

#### Approach 1: Gene Regulation Score Ranking
- Direct ranking based on gene regulation matching scores
- Lower (more negative) scores indicate stronger therapeutic potential
- Prioritizes drugs that counter disease gene expression patterns

#### Approach 2: Weighted Binding Score Ranking
- Computes: `Score = Σ(binding_score × |gene_regulation_score|)`
- Gene regulation scores act as probabilistic weights
- Weights binding affinities by biological relevance
- Captures both binding strength and regulatory impact

**Process**:
1. Loads binding scores and regulation scores
2. Maps disease-associated genes to drug candidates
3. Computes element-wise product of binding × regulation matrices
4. Aggregates scores per drug for each disease
5. Generates ranked lists for all diseases

**Output**: Disease-specific ranked drug lists 

### 4. SMILES Data Preparation (`DrugDataCSVGenerator.ipynb`)

**Purpose**: Enriches drug dataset with SMILES molecular representations.

**Process**:
- Loads drug perturbation data
- Matches drug names with SMILES from reference database (DP.json)
- Handles case-insensitive matching
- Incorporates manual SMILES for special cases
- Filters out biological drugs without SMILES (antibodies, proteins)

**Output**: Drugs with validated SMILES representations

### 5. ADMET Profiling (`ADMET.ipynb`)

**Purpose**: Evaluates pharmacokinetic, drug-like properties, and toxicological risks of candidates.

**Framework**: Combines RDKit and Mordred descriptors for comprehensive profiling.

**Properties Calculated**:

**Molecular Descriptors** (RDKit):
- Molecular Weight (MW)
- LogP (lipophilicity - Wildman-Crippen method)
- Topological Polar Surface Area (TPSA)
- Hydrogen Bond Donors (HBD) and Acceptors (HBA)
- Rotatable Bonds
- QED Score (Quantitative Estimate of Drug-likeness)

**Advanced Descriptors** (Mordred):
- **SLogP**: Alternative lipophilicity calculation
- **Bases**: Number of basic nitrogen atoms
- **BertzCT**: Molecular complexity index
- **Halogens**: Halogen atom count (F, Cl, Br, I)

**Drug-Likeness Metrics**:
- **Lipinski's Rule of Five Violations**: MW ≤ 500, LogP ≤ 5, HBD ≤ 5, HBA ≤ 10
  - Violation count indicates oral bioavailability issues

**Toxicology Alerts & Risk Assessment**:

1. **PAINS Filters** (Pan Assay Interference Compounds)
   - Detects promiscuous binders and assay interference patterns
   - Binary alert: 0 (Pass) or 1 (PAINS detected)

2. **hERG Cardiotoxicity Risk**
   - Based on: SLogP > 4.5 AND presence of basic nitrogens
   - Output: "High" or "Low" risk
   - Rationale: Lipophilic bases tend to block hERG potassium channels

3. **Hepatotoxicity Risk**
   - Based on: Molecular complexity (BertzCT > 1000) OR Halogens > 3
   - Output: "High" or "Low" risk
   - Rationale: Complex molecules and poly-halogenated compounds linked to liver toxicity

**Risk Interpretation**:
- **PAINS Alert = 1**: Likely assay interference, deprioritize
- **hERG High Risk**: Potential QT prolongation, requires electrophysiology testing
- **Hepato High Risk**: Requires hepatocyte toxicity assays
- **Zero Lipinski Violations**: Favorable oral bioavailability profile

**Output**: Comprehensive property profiles with drug-likeness violations and toxicity risk flags





##  Citation

If you use this pipeline in your research, please cite:

```bibtex
@software{drug_discovery_pipeline,
  title={Drug Discovery Pipeline for Disease-Drug Interaction Analysis},
  author={KBG IIT Mandi},
  year={2026}
}
```

##  Acknowledgments

- **DeepPurpose**: Drug-target interaction prediction framework
- **RDKit**: Cheminformatics toolkit for ADMET calculations
- **Gene Expression Database**: Disease signature sources

##  Contact

For questions and feedback:
- Open an issue on GitHub

---

**Note**: This pipeline is for research purposes only. Drug candidates require extensive experimental validation before clinical consideration.
