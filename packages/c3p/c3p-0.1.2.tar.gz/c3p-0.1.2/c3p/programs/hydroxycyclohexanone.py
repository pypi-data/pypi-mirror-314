"""
Classifies: CHEBI:24693 hydroxycyclohexanone
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def is_hydroxycyclohexanone(smiles: str):
    """
    Determines if a molecule is a hydroxycyclohexanone (cyclohexanone with one or more hydroxy substituents).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a hydroxycyclohexanone, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for cyclohexanone ring
    ring_info = mol.GetRingInfo()
    cyclohexanone_ring = None
    for ring in ring_info.AtomRings():
        if len(ring) == 6:
            atoms = [mol.GetAtomWithIdx(idx) for idx in ring]
            if any(atom.GetSymbol() == 'O' and atom.GetFormalCharge() == 0 for atom in atoms) and \
               all(atom.GetHybridization() == Chem.HybridizationType.SP3 for atom in atoms if atom.GetSymbol() == 'C'):
                cyclohexanone_ring = ring
                break

    if cyclohexanone_ring is None:
        return False, "No cyclohexanone ring found"

    # Check for hydroxy substituents
    hydroxy_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'O' and atom.GetFormalCharge() == 0 and atom.GetIdx() not in cyclohexanone_ring)

    if hydroxy_count > 0:
        return True, f"Hydroxycyclohexanone with {hydroxy_count} hydroxy substituent(s)"
    else:
        return False, "No hydroxy substituents found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24693',
                          'name': 'hydroxycyclohexanone',
                          'definition': 'Any member of the class of '
                                        'cyclohexanones carrying one or more '
                                        'hydroxy substituents.',
                          'parents': ['CHEBI:23482']},
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
    'num_false_positives': 100,
    'num_true_negatives': 450,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.8166969147005445}