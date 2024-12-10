"""
Classifies: CHEBI:131862 HPODE(1-)
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_HPODE_1__(smiles: str):
    """
    Determines if a molecule is a HPODE(1-) anion.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a HPODE(1-) anion, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of 18 carbon atoms
    if mol.GetNumHeavyAtoms() != 18:
        return False, "The molecule does not contain 18 heavy atoms"

    # Check for the presence of 2 double bonds
    bond_types = [bond.GetBondType() for bond in mol.GetBonds()]
    if bond_types.count(Chem.BondType.DOUBLE) != 2:
        return False, "The molecule does not contain 2 double bonds"

    # Check for the presence of a carboxylate group
    carboxylate_found = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'O' and atom.GetFormalCharge() == -1:
            neighbors = [mol.GetAtomWithIdx(neighbor.GetIdx()) for neighbor in atom.GetNeighbors()]
            if len(neighbors) == 1 and neighbors[0].GetSymbol() == 'C' and neighbors[0].GetFormalCharge() == 0:
                carboxylate_found = True
                break

    if not carboxylate_found:
        return False, "The molecule does not contain a carboxylate group"

    # Check for the presence of a hydroperoxy group
    hydroperoxy_found = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'O' and atom.GetFormalCharge() == 0:
            neighbors = [mol.GetAtomWithIdx(neighbor.GetIdx()) for neighbor in atom.GetNeighbors()]
            if len(neighbors) == 2 and neighbors[0].GetSymbol() == 'O' and neighbors[1].GetSymbol() == 'C':
                hydroperoxy_found = True
                break

    if not hydroperoxy_found:
        return False, "The molecule does not contain a hydroperoxy group"

    return True, "The molecule is a HPODE(1-) anion"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:131862',
                          'name': 'HPODE(1-)',
                          'definition': 'An octadecanoid anion anion obtained '
                                        'by the deprotonation of the carboxy '
                                        'group of any '
                                        'hydroperoxyoctadecadienoic acid.',
                          'parents': ['CHEBI:131860', 'CHEBI:134019']},
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
    'num_true_negatives': 183924,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999945630012234}