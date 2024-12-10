"""
Classifies: CHEBI:27933 beta-lactam antibiotic
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_beta_lactam_antibiotic(smiles: str):
    """
    Determines if a molecule is a beta-lactam antibiotic.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a beta-lactam antibiotic, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for beta-lactam ring
    beta_lactam_ring = False
    for ring in mol.GetRingInfo().AtomRings():
        if len(ring) == 4:
            atoms = [mol.GetAtomWithIdx(idx) for idx in ring]
            if any(atom.GetSymbol() == 'N' for atom in atoms) and any(atom.GetSymbol() == 'O' for atom in atoms):
                beta_lactam_ring = True
                break

    if not beta_lactam_ring:
        return False, "No beta-lactam ring found"

    # Check for nitrogen in the molecule
    if not any(atom.GetSymbol() == 'N' for atom in mol.GetAtoms()):
        return False, "No nitrogen atoms found"

    # Check if the molecule is an antibiotic
    # (This is a simplified check based on the presence of specific functional groups)
    antibiotic_groups = ['C(=O)N', 'C(=O)O', 'S=O', 'N=O', 'C#N']
    has_antibiotic_group = False
    for group in antibiotic_groups:
        if mol.HasSubstructMatch(Chem.MolFromSmarts(group)):
            has_antibiotic_group = True
            break

    if not has_antibiotic_group:
        return False, "No antibiotic functional groups found"

    return True, "Molecule is a beta-lactam antibiotic"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:27933',
                          'name': 'beta-lactam antibiotic',
                          'definition': 'An organonitrogen heterocyclic '
                                        'antibiotic that contains a '
                                        'beta-lactam ring.',
                          'parents': ['CHEBI:25558', 'CHEBI:35627']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': None,
    'attempt': 0,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 183607,
    'num_false_negatives': 32,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.999825745075937}