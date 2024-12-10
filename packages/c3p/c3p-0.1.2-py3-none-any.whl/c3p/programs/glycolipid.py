"""
Classifies: CHEBI:33563 glycolipid
"""
from rdkit import Chem

def is_glycolipid(smiles: str):
    """
    Determines if a molecule is a glycolipid based on its SMILES string.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a glycolipid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of a carbohydrate part
    carbohydrate_part = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'O' and atom.GetTotalDegree() == 2:
            neighbors = [mol.GetAtomWithIdx(neighbor.GetIdx()).GetSymbol() for neighbor in atom.GetNeighbors()]
            if 'C' in neighbors and 'C' in neighbors:
                carbohydrate_part = True
                break

    if not carbohydrate_part:
        return False, "No carbohydrate part found"

    # Check for the presence of a lipid part
    lipid_part = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C' and atom.GetTotalDegree() == 4:
            neighbors = [mol.GetAtomWithIdx(neighbor.GetIdx()).GetSymbol() for neighbor in atom.GetNeighbors()]
            if 'C' in neighbors and 'C' in neighbors and 'C' in neighbors and ('O' in neighbors or 'N' in neighbors):
                lipid_part = True
                break

    if not lipid_part:
        return False, "No lipid part found"

    return True, "Molecule contains both carbohydrate and lipid parts"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33563',
                          'name': 'glycolipid',
                          'definition': 'Any member of class of '
                                        '1,2-di-O-acylglycerols joined at '
                                        'oxygen 3 by a glycosidic linkage to a '
                                        'carbohydrate part (usually a mono-, '
                                        'di- or tri-saccharide). Some '
                                        'substances classified as bacterial '
                                        'glycolipids have the sugar part '
                                        'acylated by one or more fatty acids '
                                        'and the glycerol part may be absent.',
                          'parents': ['CHEBI:35740']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': 'Attempt failed: Python argument types in\n'
               '    Mol.GetAtomWithIdx(Mol, Atom)\n'
               'did not match C++ signature:\n'
               '    GetAtomWithIdx(RDKit::ROMol {lvalue} self, unsigned int '
               'idx)',
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 161,
    'num_false_positives': 100,
    'num_true_negatives': 42,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.6168582375478927,
    'recall': 1.0,
    'f1': 0.7630331753554502,
    'accuracy': 0.66996699669967}