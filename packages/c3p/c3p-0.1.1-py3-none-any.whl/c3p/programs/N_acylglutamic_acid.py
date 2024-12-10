"""
Classifies: CHEBI:21658 N-acylglutamic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_N_acylglutamic_acid(smiles: str):
    """
    Determines if a molecule is an N-acylglutamic acid, which is a glutamic acid derivative
    where a hydrogen attached to the nitrogen has been replaced by an acyl group.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an N-acylglutamic acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find glutamic acid substructure
    glutamic_acid_pattern = Chem.MolFromSmarts('NC(CCC(O)=O)C(O)=O')
    matches = mol.GetSubstructMatches(glutamic_acid_pattern)

    if not matches:
        return False, "Glutamic acid substructure not found"

    # Check for acyl group on the nitrogen
    for match in matches:
        n_idx = match[0]
        n_atom = mol.GetAtomWithIdx(n_idx)
        if n_atom.GetAtomicNum() == 7:  # Nitrogen
            n_neighbors = [mol.GetAtomWithIdx(neighbor_idx) for neighbor_idx in n_atom.GetNeighbors()]
            for neighbor in n_neighbors:
                if neighbor.GetIsAromatic() and any(neighbor.GetNeighbors()):
                    return True, "N-acylglutamic acid derivative"

    return False, "Not an N-acylglutamic acid derivative"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:21658',
                          'name': 'N-acylglutamic acid',
                          'definition': 'A glutamic acid derivative that is '
                                        'glutamic acid in which a hydrogen '
                                        'attached to the nitrogen has been '
                                        'replaced by an acyl group.',
                          'parents': ['CHEBI:24315']},
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
    'success': False,
    'best': True,
    'error': 'Python argument types in\n'
             '    Mol.GetAtomWithIdx(Mol, Atom)\n'
             'did not match C++ signature:\n'
             '    GetAtomWithIdx(RDKit::ROMol {lvalue} self, unsigned int idx)',
    'stdout': '',
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0,
    'f1': 0,
    'accuracy': None}