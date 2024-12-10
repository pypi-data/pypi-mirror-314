"""
Classifies: CHEBI:26912 oxolanes
"""
from rdkit import Chem

def is_oxolanes(smiles: str):
    """
    Determines if a molecule contains an oxolane (tetrahydrofuran) skeleton.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule contains an oxolane skeleton, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    rings = mol.GetRingInfo().AtomRings()
    for ring in rings:
        atoms = [mol.GetAtomWithIdx(idx) for idx in ring]
        if len(ring) == 5:  # oxolane ring size
            oxolane_ring = True
            for atom in atoms:
                if atom.GetAtomicNum() != 8 and atom.GetAtomicNum() != 6:  # not oxygen or carbon
                    oxolane_ring = False
                    break
            if oxolane_ring:
                bond_types = [mol.GetBondBetweenAtoms(atoms[i].GetIdx(), atoms[(i+1)%5].GetIdx()).GetBondType()
                              for i in range(5)]
                if sum(bond_types) == sum([Chem.rdchem.BondType.SINGLE] * 5):  # all single bonds
                    return True, "Molecule contains an oxolane (tetrahydrofuran) skeleton"

    return False, "Molecule does not contain an oxolane skeleton"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26912',
                          'name': 'oxolanes',
                          'definition': 'Any oxacycle having an oxolane '
                                        '(tetrahydrofuran) skeleton.',
                          'parents': ['CHEBI:25693', 'CHEBI:38104']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': "Attempt failed: name 'is_oxolanes' is not defined",
    'attempt': 2,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 85,
    'num_false_positives': 100,
    'num_true_negatives': 705,
    'num_false_negatives': 5,
    'num_negatives': None,
    'precision': 0.4594594594594595,
    'recall': 0.9444444444444444,
    'f1': 0.6181818181818182,
    'accuracy': 0.88268156424581}