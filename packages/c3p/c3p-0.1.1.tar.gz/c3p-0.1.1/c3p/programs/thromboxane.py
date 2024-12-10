"""
Classifies: CHEBI:26995 thromboxane
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_thromboxane(smiles: str):
    """
    Determines if a molecule is a thromboxane, a class of oxygenated oxane derivatives that stimulate
    platelet aggregation and blood vessel constriction.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a thromboxane, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of an oxane ring
    ring_info = mol.GetRingInfo()
    oxane_ring = False
    for ring in ring_info.AtomRings():
        if len(ring) == 6:
            atoms = [mol.GetAtomWithIdx(idx) for idx in ring]
            oxane_atoms = [atom.GetSymbol() for atom in atoms]
            if set(oxane_atoms) == {'C', 'O'}:
                oxane_ring = True
                break

    if not oxane_ring:
        return False, "No oxane ring found"

    # Check for oxygenated substituents
    oxygenated = any(atom.GetSymbol() == 'O' for atom in mol.GetAtoms())
    if not oxygenated:
        return False, "No oxygenated substituents found"

    # Check for the presence of a carboxylate group
    carboxylate = any(atom.GetSymbol() == 'O' and atom.GetFormalCharge() == -1 for atom in mol.GetAtoms())
    if not carboxylate:
        return False, "No carboxylate group found"

    # If all conditions are met, classify as a thromboxane
    return True, "Molecule is a thromboxane"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26995',
                          'name': 'thromboxane',
                          'definition': 'A class of oxygenated oxane '
                                        'derivatives, originally derived from '
                                        'prostaglandin precursors in '
                                        'platelets, that stimulate aggregation '
                                        'of platelets and constriction of '
                                        'blood vessels.',
                          'parents': ['CHEBI:26347']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.8,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': "Attempt failed: module 'rdkit.Chem.AllChem' has no attribute "
               "'IsCyclic'",
    'attempt': 2,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1,
    'num_false_positives': 100,
    'num_true_negatives': 6683,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.009900990099009901,
    'recall': 0.5,
    'f1': 0.019417475728155338,
    'accuracy': 0.9851142225497421}