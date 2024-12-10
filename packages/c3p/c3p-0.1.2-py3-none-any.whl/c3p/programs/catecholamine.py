"""
Classifies: CHEBI:33567 catecholamine
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_catecholamine(smiles: str):
    """
    Determines if a molecule is a catecholamine (4-(2-Aminoethyl)pyrocatechol and derivatives).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a catecholamine, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for a benzene ring
    ring_info = mol.GetRingInfo()
    aromatic_rings = []
    for ring in ring_info.AtomRings():
        if len(ring) == 6:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            if all(atom.GetIsAromatic() for atom in atoms):
                aromatic_rings.append(ring)

    if not aromatic_rings:
        return False, "No aromatic 6-membered rings found"

    # Check if the ring is substituted with two hydroxyl groups and an aminoethyl group
    ring_atoms = set(aromatic_rings[0])
    substituents = []
    has_aminoethyl = False
    has_two_hydroxyls = False

    for atom_idx in ring_atoms:
        atom = mol.GetAtomWithIdx(atom_idx)
        neighbors = [mol.GetAtomWithIdx(n.GetIdx()) for n in atom.GetNeighbors() if n.GetIdx() not in ring_atoms]

        for neighbor in neighbors:
            symbol = neighbor.GetSymbol()
            if symbol == 'O' and neighbor.IsInRingSize(5):
                substituents.append('OH')
            elif symbol == 'N' and neighbor.IsInRingSize(5):
                has_aminoethyl = True
                substituents.append('Aminoethyl')

    if len(substituents) == 2:
        has_two_hydroxyls = 'OH' in substituents and substituents.count('OH') == 2

    if has_aminoethyl and has_two_hydroxyls:
        return True, f"Catecholamine with substituents: {', '.join(set(substituents))}"
    else:
        return False, "Not a catecholamine"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33567',
                          'name': 'catecholamine',
                          'definition': '4-(2-Aminoethyl)pyrocatechol '
                                        '[4-(2-aminoethyl)benzene-1,2-diol] '
                                        'and derivatives formed by '
                                        'substitution.',
                          'parents': [   'CHEBI:25375',
                                         'CHEBI:33566',
                                         'CHEBI:64365']},
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
    'num_true_negatives': 183901,
    'num_false_negatives': 3,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9999836871411171}