"""
Classifies: CHEBI:23825 dibenzodioxine
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_dibenzodioxine(smiles: str):
    """
    Determines if a molecule belongs to the class of dibenzodioxine (oxanthrene and its derivatives).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule belongs to the class of dibenzodioxine, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Generate the aromatic ring information
    rings = mol.GetRingInfo()

    # Check for exactly 3 aromatic rings
    aromatic_rings = []
    for ring in rings.AtomRings():
        atoms = [mol.GetAtomWithIdx(i) for i in ring]
        if all(atom.GetIsAromatic() for atom in atoms):
            aromatic_rings.append(ring)

    if len(aromatic_rings) != 3:
        return False, "Does not contain exactly 3 aromatic rings"

    # Check if the rings are 6-membered and fused
    ring_sizes = [len(ring) for ring in aromatic_rings]
    if ring_sizes != [6, 6, 6]:
        return False, "Aromatic rings are not all 6-membered"

    ring_atoms = set().union(*aromatic_rings)
    if len(ring_atoms) != len(set(ring_atoms)):
        return False, "Aromatic rings are not fused"

    # Check for the presence of exactly 2 oxygen atoms
    oxygen_atoms = [atom for atom in mol.GetAtoms() if atom.GetSymbol() == 'O']
    if len(oxygen_atoms) != 2:
        return False, "Does not contain exactly 2 oxygen atoms"

    # Check if the oxygen atoms are part of the aromatic system
    oxygen_atom_indices = [atom.GetIdx() for atom in oxygen_atoms]
    if not all(idx in ring_atoms for idx in oxygen_atom_indices):
        return False, "Oxygen atoms are not part of the aromatic system"

    # Check if the oxygen atoms are in different rings
    oxygen_rings = [set(ring) for ring in aromatic_rings if any(idx in ring for idx in oxygen_atom_indices)]
    if len(oxygen_rings) != 2:
        return False, "Oxygen atoms are not in different rings"

    return True, "Molecule belongs to the class of dibenzodioxine (oxanthrene and its derivatives)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23825',
                          'name': 'dibenzodioxine',
                          'definition': 'Oxanthrene (formerly '
                                        'dibenzo[b,e][1,4]dioxine) and its '
                                        'derivatives.',
                          'parents': ['CHEBI:26979', 'CHEBI:27171']},
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
    'num_true_negatives': 183918,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9999945628238518}