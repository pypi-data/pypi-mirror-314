"""
Classifies: CHEBI:139340 1,3-dihydroimidazole-2-thiones
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_1_3_dihydroimidazole_2_thiones(smiles: str):
    """
    Determines if a molecule is a 1,3-dihydroimidazole-2-thione or its derivative.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a 1,3-dihydroimidazole-2-thione or its derivative, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule contains an imidazole ring
    imidazole_ring = AllChem.FindMolRingOfSize(mol, 5)
    if not imidazole_ring:
        return False, "No imidazole ring found"

    # Check if the imidazole ring contains a sulfur atom
    s_atom_idx = [atom.GetIdx() for atom in mol.GetAtoms() if atom.GetSymbol() == 'S']
    if not any(s_atom_idx in ring for ring in mol.GetRingInfo().AtomRings()):
        return False, "No sulfur atom in the imidazole ring"

    # Check if the sulfur atom is connected to a carbon atom
    s_atom = mol.GetAtomWithIdx(s_atom_idx[0])
    if not any(neighbor.GetSymbol() == 'C' for neighbor in s_atom.GetNeighbors()):
        return False, "Sulfur atom not connected to a carbon atom"

    # Check for substitution
    substituents = []
    for atom in mol.GetAtoms():
        if atom.GetSymbol() != 'C' and atom.GetSymbol() != 'N' and atom.GetSymbol() != 'S':
            substituents.append(atom.GetSymbol())

    if substituents:
        substituents_str = ', '.join(set(substituents))
        return True, f"1,3-dihydroimidazole-2-thione with substituents: {substituents_str}"
    else:
        return True, "Unsubstituted 1,3-dihydroimidazole-2-thione"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:139340',
                          'name': '1,3-dihydroimidazole-2-thiones',
                          'definition': 'A member of the class of imidazoles '
                                        'that is 1,3-dihydroimidazole-2-thione '
                                        'and its derivatives by substitution.',
                          'parents': ['CHEBI:24780', 'CHEBI:51276']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.8,
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
    'error': "module 'rdkit.Chem.AllChem' has no attribute 'FindMolRingOfSize'",
    'stdout': '',
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': None}