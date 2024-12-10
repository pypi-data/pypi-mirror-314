"""
Classifies: CHEBI:17021 S-substituted glutathione
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_S_substituted_glutathione(smiles: str):
    """
    Determines if a molecule is an S-substituted glutathione, which is a glutathione derivative
    where the hydrogen of the thiol has been replaced by any other group.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is an S-substituted glutathione, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Get the SMARTS pattern for glutathione
    glutathione_smarts = "[NX3H2,NX4H3+]-[C@@H](C(=O)N[C@@H](C(=O)O)CS[#6])-C(=O)O"

    # Match the SMARTS pattern against the molecule
    matches = mol.GetSubstructMatches(Chem.MolFromSmarts(glutathione_smarts))

    if not matches:
        return False, "Molecule does not contain the glutathione substructure"

    # Check if the sulfur atom has a non-hydrogen substituent
    for match in matches:
        s_atom_idx = match[-1]
        s_atom = mol.GetAtomWithIdx(s_atom_idx)
        for neighbor_atom in s_atom.GetNeighbors():
            if neighbor_atom.GetSymbol() != "H":
                return True, "Molecule is an S-substituted glutathione"

    return False, "Molecule is glutathione or a non-S-substituted glutathione derivative"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:17021',
                          'name': 'S-substituted glutathione',
                          'definition': 'A glutathione derivative that is '
                                        'glutathione in which the hydrogen of '
                                        'the thiol has been replaced by any '
                                        'other group.',
                          'parents': ['CHEBI:24337']},
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
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 183917,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999945627942888}