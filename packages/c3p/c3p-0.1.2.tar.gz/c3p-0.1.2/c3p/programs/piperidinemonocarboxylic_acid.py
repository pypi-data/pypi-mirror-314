"""
Classifies: CHEBI:26148 piperidinemonocarboxylic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_piperidinemonocarboxylic_acid(smiles: str):
    """
    Determines if a molecule is a piperidinemonocarboxylic acid (piperidine with one carboxy substituent).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a piperidinemonocarboxylic acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for a piperidine ring
    rings = mol.GetRingInfo().AtomRings()
    piperidine_ring = next((ring for ring in rings if len(ring) == 6), None)
    if piperidine_ring is None:
        return False, "No piperidine ring found"

    # Check if the ring contains one nitrogen atom
    ring_atoms = [mol.GetAtomWithIdx(idx) for idx in piperidine_ring]
    nitrogen_count = sum(atom.GetSymbol() == 'N' for atom in ring_atoms)
    if nitrogen_count != 1:
        return False, "Piperidine ring does not contain exactly one nitrogen atom"

    # Check for one carboxy substituent
    carboxy_count = sum(atom.GetSymbol() == 'C' and atom.GetTotalNumHs() == 0 and len(atom.GetNeighbors()) == 3 for atom in mol.GetAtoms())
    if carboxy_count != 1:
        return False, "Molecule does not contain exactly one carboxy group"

    # Check if the carboxy group is attached to the piperidine ring
    carboxy_atom = next(atom for atom in mol.GetAtoms() if atom.GetSymbol() == 'C' and atom.GetTotalNumHs() == 0 and len(atom.GetNeighbors()) == 3)
    is_attached_to_ring = any(neighbor.GetIdx() in piperidine_ring for neighbor in carboxy_atom.GetNeighbors())
    if not is_attached_to_ring:
        return False, "Carboxy group is not attached to the piperidine ring"

    return True, "Molecule is a piperidinemonocarboxylic acid"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26148',
                          'name': 'piperidinemonocarboxylic acid',
                          'definition': 'Any member of the class of '
                                        'piperidines in which one of the '
                                        'carbons of the piperidine ring is '
                                        'substituted by a carboxy group.',
                          'parents': ['CHEBI:25384', 'CHEBI:26151']},
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
    'num_true_negatives': 68268,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.009900990099009901,
    'recall': 1.0,
    'f1': 0.0196078431372549,
    'accuracy': 0.998537348798432}