"""
Classifies: CHEBI:132310 S-acyl-4'-phosphopantetheine
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_S_acyl_4__phosphopantetheine(smiles: str):
    """
    Determines if a molecule is an S-acyl-4'-phosphopantetheine.

    S-acyl-4'-phosphopantetheine is defined as a thioester obtained by formal condensation
    of the thiol group of D-pantetheine 4'-phosphate with the carboxy group of any carboxylic acid.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is an S-acyl-4'-phosphopantetheine, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of the D-pantetheine 4'-phosphate substructure
    pantetheine_smarts = 'C(NC(CCNC(=O)[C@@H](C(COP(O)(=O)O)(C)C)O)=O)CSC'
    pantetheine_match = mol.GetSubstructMatches(Chem.MolFromSmarts(pantetheine_smarts))

    if not pantetheine_match:
        return False, "D-pantetheine 4'-phosphate substructure not found"

    # Check for the presence of a thioester bond (S-C(=O)-C)
    thioester_smarts = 'S-C(=O)-C'
    thioester_match = mol.GetSubstructMatches(Chem.MolFromSmarts(thioester_smarts))

    if not thioester_match:
        return False, "Thioester bond not found"

    # Check if the thioester bond is connected to the D-pantetheine 4'-phosphate substructure
    for idx in pantetheine_match[0]:
        atom = mol.GetAtomWithIdx(idx)
        if atom.GetSymbol() == 'S':
            for neighbor in atom.GetNeighbors():
                if neighbor.GetSymbol() == 'C' and neighbor.GetDegree() == 3:
                    for nbr_neighbor in neighbor.GetNeighbors():
                        if nbr_neighbor.GetSymbol() == 'O' and nbr_neighbor.GetDegree() == 1:
                            return True, "S-acyl-4'-phosphopantetheine structure found"

    return False, "S-acyl-4'-phosphopantetheine structure not found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:132310',
                          'name': "S-acyl-4'-phosphopantetheine",
                          'definition': 'A thioester obtained by formal '
                                        'condensation of the thiol group of '
                                        "D-pantetheine 4'-phosphate with the "
                                        'carboxy group of any carboxylic acid.',
                          'parents': ['CHEBI:26073', 'CHEBI:51277']},
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
    'num_true_positives': 1,
    'num_false_positives': 100,
    'num_true_negatives': 8901,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.009900990099009901,
    'recall': 1.0,
    'f1': 0.0196078431372549,
    'accuracy': 0.9888913574761165}