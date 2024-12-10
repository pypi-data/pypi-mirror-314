"""
Classifies: CHEBI:26948 vitamin B1
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_vitamin_B1(smiles: str):
    """
    Determines if a molecule is a member of the vitamin B1 group.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a vitamin B1, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of a 1,3-thiazolium ring
    ring_info = mol.GetRingInfo()
    thiazolium_ring = False
    for ring in ring_info.AtomRings():
        if len(ring) == 5:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            if len([atom for atom in atoms if atom.GetSymbol() == 'S']) == 1 and \
               len([atom for atom in atoms if atom.GetSymbol() == 'N']) == 1:
                thiazolium_ring = True
                break

    if not thiazolium_ring:
        return False, "No 1,3-thiazolium ring found"

    # Check for positive charge on the nitrogen of the thiazolium ring
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'N' and atom.GetFormalCharge() == 1:
            break
    else:
        return False, "No positively charged nitrogen found in the thiazolium ring"

    # Check for substituents
    substituents = []
    for atom in mol.GetAtoms():
        if atom.GetSymbol() != 'C' and atom.GetSymbol() != 'N' and atom.GetSymbol() != 'S':
            substituents.append(atom.GetSymbol())

    if len(substituents) > 0:
        return True, f"Member of the vitamin B1 group with substituents: {', '.join(set(substituents))}"
    else:
        return True, "Unsubstituted member of the vitamin B1 group"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26948',
                          'name': 'vitamin B1',
                          'definition': 'Any member of the group of '
                                        '1,3-thiazolium cations that exhibit '
                                        'biological activity against vitamin '
                                        'B1 deficiency in animals. Symptoms of '
                                        'vitamin B1 deficiency include '
                                        'constipation, loss of apetite, '
                                        'fatigue, nausea, delirium, blurry '
                                        'vision and muscle weakness. Severe '
                                        'vitamin B1 deficiency can also lead '
                                        'to a disease known as beriberi. '
                                        'Vitamin B1 consists of the vitamer '
                                        'thiamin and its acid, aldehyde and '
                                        'phosphorylated derivatives (and their '
                                        'corresponding ionized, salt and '
                                        'hydrate forms).',
                          'parents': [   'CHEBI:38338',
                                         'CHEBI:63048',
                                         'CHEBI:75769']},
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
    'num_true_positives': 1,
    'num_false_positives': 100,
    'num_true_negatives': 80267,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.009900990099009901,
    'recall': 1.0,
    'f1': 0.0196078431372549,
    'accuracy': 0.9987557236711129}