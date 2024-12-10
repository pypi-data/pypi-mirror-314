"""
Classifies: CHEBI:27162 tryptamines
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_tryptamine(smiles: str):
    """
    Determines if a molecule is a tryptamine or its substitution derivative.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a tryptamine or its substitution derivative, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule contains an indole ring
    indole_ring = AllChem.FindMolChiralUnspecifiedSubstructure(mol, Chem.MolFromSmiles('c1ccc2[nH]ccc2c1'), useChirality=False)
    if not indole_ring:
        return False, "No indole ring found"

    # Check if the molecule contains an ethylamine side chain attached to the indole ring
    ethylamine_sidechain = AllChem.FindMolChiralUnspecifiedSubstructure(mol, Chem.MolFromSmiles('CCN'), useChirality=False)
    if not ethylamine_sidechain:
        return False, "No ethylamine side chain found"

    # Check the attachment point of the ethylamine side chain to the indole ring
    for bond in mol.GetBonds():
        if bond.GetBeginAtomIdx() in ethylamine_sidechain and bond.GetEndAtomIdx() in indole_ring:
            begin_atom = mol.GetAtomWithIdx(bond.GetBeginAtomIdx())
            end_atom = mol.GetAtomWithIdx(bond.GetEndAtomIdx())
            if begin_atom.GetSymbol() == 'N' and end_atom.GetIsAromatic():
                substituents = []
                for neighbor in end_atom.GetNeighbors():
                    if neighbor.GetIsAromatic() and neighbor.GetIdx() != bond.GetEndAtomIdx():
                        substituents.append(neighbor.GetSymbol())
                if substituents:
                    return True, f"Tryptamine with substituents on the indole ring: {', '.join(substituents)}"
                else:
                    return True, "Unsubstituted tryptamine"

    return False, "Not a tryptamine or substitution derivative"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:27162',
                          'name': 'tryptamines',
                          'definition': 'Tryptamine and its substitution '
                                        'derivatives.',
                          'parents': ['CHEBI:24828']},
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
    'error': "name 'is_tryptamines' is not defined",
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