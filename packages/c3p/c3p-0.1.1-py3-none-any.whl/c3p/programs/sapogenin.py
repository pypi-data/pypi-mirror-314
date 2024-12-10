"""
Classifies: CHEBI:26606 sapogenin
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors
from rdkit.Chem import AllChem

def is_sapogenin(smiles: str):
    """
    Determines if a molecule is a sapogenin (organic polycyclic compound, aglycon moiety of a saponin).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a sapogenin, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for organic compound
    if not AllChem.GetMolDescriptor(mol, 'isOrganic'):
        return False, "Not an organic compound"

    # Check for polycyclic structure
    num_rings = rdMolDescriptors.CalcNumRings(mol)
    if num_rings < 2:
        return False, "Not a polycyclic compound"

    # Check for steroid or triterpenoid skeleton
    ring_info = mol.GetRingInfo()
    ring_sizes = [len(ring) for ring in ring_info.AtomRings()]

    is_steroid = (
        len(set(ring_sizes)) == 2
        and 6 in ring_sizes
        and 5 in ring_sizes
    )

    is_triterpenoid = (
        len(set(ring_sizes)) == 2
        and 6 in ring_sizes
        and 9 in ring_sizes
    )

    if not (is_steroid or is_triterpenoid):
        return False, "Not a steroid or triterpenoid skeleton"

    return True, "Molecule is a sapogenin"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26606',
                          'name': 'sapogenin',
                          'definition': 'Any organic polycyclic compound that '
                                        'is the aglycon moiety of a saponin; '
                                        'sapogenins may be steroids or '
                                        'triterpenoids.',
                          'parents': ['CHEBI:51958']},
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
    'success': False,
    'best': True,
    'error': "module 'rdkit.Chem.AllChem' has no attribute 'GetMolDescriptor'",
    'stdout': '',
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0,
    'f1': 0,
    'accuracy': None}