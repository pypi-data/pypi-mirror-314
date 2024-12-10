"""
Classifies: CHEBI:146266 pyrimido-indole
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_pyrimido_indole(smiles: str) -> tuple[bool, str]:
    """
    Determines if a molecule is a pyrimido-indole.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a pyrimido-indole, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find all aromatic rings
    aromatic_rings = [list(ring) for ring in AllChem.GetSymmSSSR(mol)]

    # Check for a pyrimidine ring
    pyrimidine_ring = None
    for ring in aromatic_rings:
        if len(ring) == 6:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            n_count = sum(atom.GetAtomicNum() == 7 for atom in atoms)
            if n_count == 2:
                pyrimidine_ring = ring
                break

    if pyrimidine_ring is None:
        return False, "No pyrimidine ring found"

    # Check for an indole ring fused to the pyrimidine ring
    indole_ring = None
    for ring in aromatic_rings:
        if len(ring) == 9:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            n_count = sum(atom.GetAtomicNum() == 7 for atom in atoms)
            if n_count == 2:
                common_atoms = set(pyrimidine_ring) & set(ring)
                if len(common_atoms) == 2:
                    indole_ring = ring
                    break

    if indole_ring is None:
        return False, "No indole ring fused to the pyrimidine ring"

    return True, "The molecule is a pyrimido-indole"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:146266',
                          'name': 'pyrimido-indole',
                          'definition': 'Any organic heterotricyclic compound '
                                        'with a skeleton consisting of a '
                                        'pyrimidine ring fused to an indole.',
                          'parents': ['CHEBI:26979']},
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
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 0,
    'num_false_positives': 1,
    'num_true_negatives': 183920,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.999989125825078}