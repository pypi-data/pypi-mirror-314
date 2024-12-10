"""
Classifies: CHEBI:26959 thiocarboxylic ester
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_thiocarboxylic_ester(smiles: str):
    """
    Determines if a molecule is a thiocarboxylic ester.

    A thiocarboxylic ester is defined as an ester in which one or both
    oxygens of an ester group have been replaced by divalent sulfur.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a thiocarboxylic ester, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find all ester groups
    ester_smarts = "C(=O)O[C,S]"
    ester_atoms = [mol.GetAtomWithIdx(idx) for idx in mol.GetSubstructMatches(Chem.MolFromSmarts(ester_smarts))]

    if not ester_atoms:
        return False, "No ester groups found"

    # Check if one or both oxygens are replaced by sulfur
    thiocarboxylic_esters = []
    for atom_idx, atom in enumerate(ester_atoms):
        if atom.GetSymbol() == 'S':
            neighbor_atoms = [mol.GetAtomWithIdx(neighbor) for neighbor in atom.GetNeighbors()]
            if any(neighbor.GetSymbol() == 'O' and neighbor.GetFormalCharge() == 0 for neighbor in neighbor_atoms):
                thiocarboxylic_esters.append(atom_idx)

    if not thiocarboxylic_esters:
        return False, "No thiocarboxylic ester groups found"

    # Construct the reason
    reason = "Thiocarboxylic ester group(s) found at atom index(es): " + ", ".join(map(str, thiocarboxylic_esters))
    return True, reason


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26959',
                          'name': 'thiocarboxylic ester',
                          'definition': 'An ester in which one or both oxygens '
                                        'of an ester group have been replaced '
                                        'by divalent sulfur.',
                          'parents': ['CHEBI:33261', 'CHEBI:35701']},
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
    'error': 'Python argument types in\n'
             '    Mol.GetAtomWithIdx(Mol, tuple)\n'
             'did not match C++ signature:\n'
             '    GetAtomWithIdx(RDKit::ROMol {lvalue} self, unsigned int idx)',
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