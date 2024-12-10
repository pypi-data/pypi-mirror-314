"""
Classifies: CHEBI:133558 hydroperoxyoctadecatrienoate
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_hydroperoxyoctadecatrienoate(smiles: str):
    """
    Determines if a molecule is a hydroperoxyoctadecatrienoate (An octadecanoid anion that is octadecatrienoate
    containing a hydroperoxy substituent attached to its carbon chain).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a hydroperoxyoctadecatrienoate, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of 18 carbon atoms
    if mol.GetNumAtoms() != 18:
        return False, "Not an octadecanoid"

    # Check for the presence of a carboxylate group (-COO-)
    carboxylate_found = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'O' and atom.GetFormalCharge() == -1:
            for neighbor in atom.GetNeighbors():
                if neighbor.GetSymbol() == 'C' and neighbor.GetDegree() == 3:
                    carboxylate_found = True
                    break
    if not carboxylate_found:
        return False, "No carboxylate group found"

    # Check for the presence of a hydroperoxy group (-OOH)
    hydroperoxy_found = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'O' and atom.GetDegree() == 2:
            neighbors = [neighbor.GetSymbol() for neighbor in atom.GetNeighbors()]
            if 'O' in neighbors and 'C' in neighbors:
                hydroperoxy_found = True
                break
    if not hydroperoxy_found:
        return False, "No hydroperoxy group found"

    # Check for the presence of three double bonds
    double_bonds = Descriptors.Descriptors.BondCountDescriptors.NumAromaticRings(mol)
    if double_bonds != 3:
        return False, "Not an octadecatrienoate"

    return True, "Molecule is a hydroperoxyoctadecatrienoate"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:133558',
                          'name': 'hydroperoxyoctadecatrienoate',
                          'definition': 'An octadecanoid anion that is '
                                        'octadecatrienoate containing a '
                                        'hydroperoxy substituent attached to '
                                        'its carbon chain.',
                          'parents': [   'CHEBI:131860',
                                         'CHEBI:134019',
                                         'CHEBI:57560']},
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
    'error': "module 'rdkit.Chem.Descriptors' has no attribute 'Descriptors'",
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