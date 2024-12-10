"""
Classifies: CHEBI:140151 cyclosporin A derivative
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_cyclosporin_A_derivative(smiles: str):
    """
    Determines if a molecule is a cyclosporin A derivative.
    A cyclosporin A derivative is defined as any homodetic cyclic peptide whose structure is derived from
    cyclosporin A. The term includes metabolites of cyclosporin A.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a cyclosporin A derivative, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule is cyclic
    if not mol.GetRingInfo().IsCyclic():
        return False, "Molecule is not cyclic"

    # Check if the molecule is a peptide
    if not Descriptors.PeptideFromSmiles(mol):
        return False, "Molecule is not a peptide"

    # Check if the molecule is homodetic (all rings are made up of the same atoms)
    if not AllChem.IsMoleculeHomodetic(mol):
        return False, "Molecule is not homodetic"

    # Check if the molecule is similar to cyclosporin A
    cyclosporin_a = Chem.MolFromSmiles('C1C(NC(=O)C(N2C(=O)[C@@H](NC(=O)[C@H](NC(=O)[C@H](NC(=O)[C@H](NC(=O)[C@H](NC(=O)[C@H](NC(=O)[C@H](NC(=O)[C@H](NC1=O)CC)C(C)C)C(C)C)CC(C)C)CC(O)(C)C)CC(C)C)C(=O)NC(C)C)CC)C(=O)N[C@@H](C)C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@@H](C(=O)N2)C(C)C)CC(C)C)C(C)C)CC)C(C)C')
    if mol.GetMolecularSimilarity(cyclosporin_a) < 0.8:
        return False, "Molecule is not similar enough to cyclosporin A"

    return True, "Molecule is a cyclosporin A derivative"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:140151',
                          'name': 'cyclosporin A derivative',
                          'definition': 'Any homodetic cyclic peptide whose '
                                        'structure is derived from cyclosporin '
                                        'A. The term includes metabolites of '
                                        'cyclosporin A.',
                          'parents': ['CHEBI:24613']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': None,
    'attempt': 0,
    'success': False,
    'best': True,
    'error': "'RingInfo' object has no attribute 'IsCyclic'",
    'stdout': '',
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': None}