"""
Classifies: CHEBI:20012 3-enoyl-CoA
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_3_enoyl_CoA(smiles: str):
    """
    Determines if a molecule is a 3-enoyl-CoA derivative.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a 3-enoyl-CoA derivative, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of the CoA moiety
    coa_pattern = Chem.MolFromSmarts('C(=O)NCCC(=O)NCCC(=O)O[C@H]1[C@H](O)[C@@H](OP(=O)(O)O)O[C@H](n2cnc3c(N)ncnc23)[C@@H]1OP(=O)(O)O')
    if not mol.HasSubstructMatch(coa_pattern):
        return False, "CoA moiety not found"

    # Check for the presence of a C=C double bond
    double_bond_pattern = Chem.MolFromSmarts('C=C')
    if not mol.HasSubstructMatch(double_bond_pattern):
        return False, "No C=C double bond found"

    # Check if the C=C double bond is beta to the thioester linkage
    thioester_pattern = Chem.MolFromSmarts('C(=O)S')
    for match in mol.GetSubstructMatches(thioester_pattern):
        atom_idx = match[0]
        atom = mol.GetAtomWithIdx(atom_idx)
        for neighbor in atom.GetNeighbors():
            if neighbor.GetSymbol() == 'C':
                if neighbor.GetDegree() == 3:
                    double_bond_atom = None
                    for neighbor_of_neighbor in neighbor.GetNeighbors():
                        if neighbor_of_neighbor.GetSymbol() == 'C' and neighbor_of_neighbor.GetDegree() == 2:
                            double_bond_atom = neighbor_of_neighbor
                            break
                    if double_bond_atom is not None:
                        return True, "Molecule is a 3-enoyl-CoA derivative"

    return False, "C=C double bond not beta to the thioester linkage"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:20012',
                          'name': '3-enoyl-CoA',
                          'definition': 'Generic name for any derivative of '
                                        'coenzyme A in which the thiol group '
                                        'is in thioester linkage with an acyl '
                                        'group containing a C=C double bond '
                                        'beta to the thioester linkage.',
                          'parents': ['CHEBI:51006']},
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
    'num_false_positives': 0,
    'num_true_negatives': 183921,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.999994562912539}