"""
Classifies: CHEBI:23468 cyclohexadienecarboxylic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_cyclohexadienecarboxylic_acid(smiles: str):
    """
    Determines if a molecule is a cyclohexadienecarboxylic acid (Any cyclohexadiene substituted by a carboxylic group at unspecified position).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a cyclohexadienecarboxylic acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of a carboxyl group
    carboxyl_present = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C':
            for neighbor in atom.GetNeighbors():
                if neighbor.GetSymbol() == 'O' and neighbor.GetDegree() == 1:
                    for neighbor_neighbor in neighbor.GetNeighbors():
                        if neighbor_neighbor.GetSymbol() == 'O' and neighbor_neighbor.GetDegree() == 1:
                            carboxyl_present = True
                            break

    if not carboxyl_present:
        return False, "No carboxyl group found"

    # Check for a cyclohexadiene ring
    ring_info = mol.GetRingInfo()
    cyclohexadiene_ring = False
    for ring in ring_info.AtomRings():
        if len(ring) == 6:
            atoms = [mol.GetAtomWithIdx(idx) for idx in ring]
            if len([atom for atom in atoms if atom.GetIsAromatic()]) == 2 and len([atom for atom in atoms if atom.GetSymbol() == 'C']) == 6:
                cyclohexadiene_ring = True
                break

    if cyclohexadiene_ring:
        return True, "Molecule is a cyclohexadienecarboxylic acid"
    else:
        return False, "No cyclohexadiene ring found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23468',
                          'name': 'cyclohexadienecarboxylic acid',
                          'definition': 'Any cyclohexadiene substituted by a '
                                        'carboxylic group at unspecified '
                                        'position.',
                          'parents': ['CHEBI:25384', 'CHEBI:37613']},
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
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 183916,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9999945627647254}