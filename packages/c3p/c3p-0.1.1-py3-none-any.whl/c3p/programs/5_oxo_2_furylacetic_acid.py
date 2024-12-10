"""
Classifies: CHEBI:23730 5-oxo-2-furylacetic acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_5_oxo_2_furylacetic_acid(smiles: str):
    """
    Determines if a molecule is a 5-oxo-2-furylacetic acid.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a 5-oxo-2-furylacetic acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of a 5-membered ring
    rings = mol.GetRingInfo().AtomRings()
    if not any(len(ring) == 5 for ring in rings):
        return False, "No 5-membered ring found"

    # Find the 5-membered ring containing an oxygen atom
    furan_ring = None
    for ring in rings:
        if len(ring) == 5:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            if any(atom.GetSymbol() == 'O' for atom in atoms):
                furan_ring = ring
                break

    if furan_ring is None:
        return False, "No 5-membered ring with oxygen found"

    # Check if the ring is aromatic and unsaturated
    furan_atoms = [mol.GetAtomWithIdx(i) for i in furan_ring]
    if not all(atom.GetIsAromatic() for atom in furan_atoms):
        return False, "5-membered ring is not aromatic"

    # Check for the presence of a carboxylic acid group
    carboxyl_group = None
    for atom in furan_atoms:
        for neighbor in atom.GetNeighbors():
            if neighbor.GetSymbol() == 'C':
                for neighbor_2 in neighbor.GetNeighbors():
                    if neighbor_2.GetSymbol() == 'O' and neighbor_2.GetFormalCharge() == 0:
                        for neighbor_3 in neighbor_2.GetNeighbors():
                            if neighbor_3.GetSymbol() == 'O' and neighbor_3.GetFormalCharge() == -1:
                                carboxyl_group = (neighbor.GetIdx(), neighbor_2.GetIdx(), neighbor_3.GetIdx())
                                break

    if carboxyl_group is None:
        return False, "No carboxylic acid group found"

    # Check for the presence of an oxo group at position 5 of the furan ring
    oxo_group = None
    for atom_idx in furan_ring:
        atom = mol.GetAtomWithIdx(atom_idx)
        if atom.GetSymbol() == 'O' and atom.GetFormalCharge() == 0:
            oxo_group = atom_idx

    if oxo_group is None:
        return False, "No oxo group found at position 5 of the furan ring"

    return True, "Molecule is a 5-oxo-2-furylacetic acid"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23730',
                          'name': '5-oxo-2-furylacetic acid',
                          'definition': 'An oxo monocarboxylic acid that is '
                                        '2,5-dihydrofuran-2-ylacetic acid '
                                        'substituted by an oxo group at '
                                        'position 5.',
                          'parents': ['CHEBI:35871', 'CHEBI:50523']},
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
    'num_true_negatives': 183921,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.999994562912539}