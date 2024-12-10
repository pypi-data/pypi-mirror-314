"""
Classifies: CHEBI:33447 phospho sugar
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors

def is_phospho_sugar(smiles: str):
    """
    Determines if a molecule is a phospho sugar, defined as any monosaccharide
    containing an alcoholic hydroxy group esterified with phosphoric acid.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a phospho sugar, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule contains a phosphate group
    has_phosphate = any(atom.GetSymbol() == 'P' and
                        sum(bond.GetBondTypeAsDouble() for bond in atom.GetBonds()) == 5 for atom in mol.GetAtoms())
    if not has_phosphate:
        return False, "Molecule does not contain a phosphate group"

    # Check if the molecule is a monosaccharide
    ring_info = mol.GetRingInfo()
    ring_sizes = [len(ring) for ring in ring_info.AtomRings()]
    has_furanose_or_pyranose = (5 in ring_sizes) or (6 in ring_sizes)
    if not has_furanose_or_pyranose:
        return False, "Molecule is not a monosaccharide"

    # Check if the phosphate group is esterified to an alcoholic hydroxy group
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'P':
            for neighbor in atom.GetNeighbors():
                if neighbor.GetSymbol() == 'O' and neighbor.GetTotalNumHs() == 1:
                    return True, "Molecule is a phospho sugar"

    return False, "Phosphate group is not esterified to an alcoholic hydroxy group"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33447',
                          'name': 'phospho sugar',
                          'definition': 'Any monosaccharide containing an '
                                        'alcoholic hydroxy group esterified '
                                        'with phosphoric acid.',
                          'parents': ['CHEBI:26816', 'CHEBI:63367']},
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
    'num_true_positives': 42,
    'num_false_positives': 100,
    'num_true_negatives': 5077,
    'num_false_negatives': 18,
    'num_negatives': None,
    'precision': 0.29577464788732394,
    'recall': 0.7,
    'f1': 0.41584158415841577,
    'accuracy': 0.9774680160397174}