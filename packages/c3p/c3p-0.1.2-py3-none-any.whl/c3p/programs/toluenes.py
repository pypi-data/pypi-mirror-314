"""
Classifies: CHEBI:27024 toluenes
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_toluene(smiles: str) -> tuple[bool, str]:
    """
    Determines if a molecule is a toluene (a substituted benzene with one and only one methyl group).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a toluene, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Generate the aromatic ring information
    rings = mol.GetRingInfo()

    # Check for at least one 6-membered ring
    if not any(len(ring) == 6 for ring in rings.AtomRings()):
        return False, "No 6-membered rings found"

    # Find all aromatic 6-membered rings
    aromatic_rings = []
    for ring in rings.AtomRings():
        if len(ring) == 6:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            if all(atom.GetIsAromatic() for atom in atoms):
                aromatic_rings.append(ring)

    if not aromatic_rings:
        return False, "No aromatic 6-membered rings found"

    # Check if all carbons in the aromatic ring are carbon
    for ring in aromatic_rings:
        atoms = [mol.GetAtomWithIdx(i) for i in ring]
        if not all(atom.GetSymbol() == 'C' for atom in atoms):
            return False, "Ring contains non-carbon atoms"

    # Check for exactly one methyl substituent
    ring_atoms = set(aromatic_rings[0])
    methyl_count = 0

    for atom_idx in ring_atoms:
        atom = mol.GetAtomWithIdx(atom_idx)
        for neighbor in atom.GetNeighbors():
            if neighbor.GetIdx() not in ring_atoms:
                if neighbor.GetSymbol() == 'C' and neighbor.GetDegree() == 4:
                    methyl_count += 1

    if methyl_count != 1:
        return False, "Number of methyl groups is not equal to 1"

    return True, "Toluene (substituted benzene with one methyl group)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:27024',
                          'name': 'toluenes',
                          'definition': 'Any member of the class of benzenes '
                                        'that is a substituted benzene in '
                                        'which the substituents include one '
                                        '(and only one) methyl group.',
                          'parents': ['CHEBI:22712']},
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
    'num_true_negatives': 183703,
    'num_false_negatives': 23,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9998748135810935}