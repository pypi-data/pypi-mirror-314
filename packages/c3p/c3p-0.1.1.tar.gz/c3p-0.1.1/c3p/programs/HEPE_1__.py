"""
Classifies: CHEBI:131874 HEPE(1-)
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_HEPE_1__(smiles: str):
    """
    Determines if a molecule is a HEPE(1-) (an unsaturated fatty acid anion arising from deprotonation of the carboxylic acid function of any hydroxyicosapentaenoic acid).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a HEPE(1-), False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for 20 heavy atoms (carbon, oxygen, and hydrogen)
    if Descriptors.HeavyAtomCount(mol) != 20:
        return False, "Incorrect number of heavy atoms"

    # Check for 5 double bonds
    if Descriptors.NumHeteroatomicDoubleBonds(mol) != 5:
        return False, "Incorrect number of double bonds"

    # Check for 1 oxygen atom
    if Descriptors.NHOHCount(mol) != 1:
        return False, "Incorrect number of oxygen atoms"

    # Check for 1 carboxylate anion group
    carboxylate_found = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'O' and atom.GetFormalCharge() == -1:
            neighbors = [mol.GetAtomWithIdx(n).GetSymbol() for n in atom.GetNeighbors()]
            if 'C' in neighbors and 'O' in neighbors:
                carboxylate_found = True
                break

    if not carboxylate_found:
        return False, "No carboxylate anion group found"

    # Check for 1 hydroxyl group
    hydroxyl_found = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'O' and atom.GetFormalCharge() == 0:
            neighbors = [mol.GetAtomWithIdx(n).GetSymbol() for n in atom.GetNeighbors()]
            if 'C' in neighbors and 'H' in neighbors:
                hydroxyl_found = True
                break

    if not hydroxyl_found:
        return False, "No hydroxyl group found"

    return True, "Molecule is a HEPE(1-)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:131874',
                          'name': 'HEPE(1-)',
                          'definition': 'An unsaturated fatty acid anion '
                                        'arising from deprotonation of the '
                                        'carboxylic acid function of any '
                                        'hydroxyicosapentaenoic acid (HEPE).',
                          'parents': ['CHEBI:131871', 'CHEBI:62937']},
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
    'error': "module 'rdkit.Chem.Descriptors' has no attribute "
             "'NumHeteroatomicDoubleBonds'",
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