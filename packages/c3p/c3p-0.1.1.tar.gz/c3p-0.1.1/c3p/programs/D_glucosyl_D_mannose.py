"""
Classifies: CHEBI:21010 D-glucosyl-D-mannose
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_D_glucosyl_D_mannose(smiles: str):
    """
    Determines if a molecule is a D-glucosyl-D-mannose, i.e., a glycosylmannose with both components having D-configuration.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a D-glucosyl-D-mannose, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Get the ring atoms and their configurations
    ring_atoms = mol.GetRingInfo().AtomRings()
    ring_configurations = []
    for ring in ring_atoms:
        ring_conf = []
        for atom_idx in ring:
            atom = mol.GetAtomWithIdx(atom_idx)
            if atom.HasProp('_CIPCode'):
                cip_code = atom.GetProp('_CIPCode')
                if cip_code == 'R':
                    ring_conf.append('D')
                elif cip_code == 'S':
                    ring_conf.append('L')
                else:
                    ring_conf.append(None)
            else:
                ring_conf.append(None)
        ring_configurations.append(ring_conf)

    # Check if there are two rings, one with all 'D' configurations and one with at least one 'D' configuration
    has_d_glucose = False
    has_d_mannose = False
    for conf in ring_configurations:
        if all(c == 'D' for c in conf):
            has_d_glucose = True
        elif any(c == 'D' for c in conf):
            has_d_mannose = True

    if has_d_glucose and has_d_mannose:
        return True, "Molecule is a D-glucosyl-D-mannose"
    else:
        return False, "Molecule is not a D-glucosyl-D-mannose"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:21010',
                          'name': 'D-glucosyl-D-mannose',
                          'definition': 'A glycosylmannose with both '
                                        'components having D-configuration.',
                          'parents': ['CHEBI:35318']},
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
    'num_false_positives': 26,
    'num_true_negatives': 183893,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9998531970421922}