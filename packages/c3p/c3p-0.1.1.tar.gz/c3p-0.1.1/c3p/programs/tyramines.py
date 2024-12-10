"""
Classifies: CHEBI:27175 tyramines
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_tyramines(smiles: str):
    """
    Determines if a molecule is a tyramine (aralkylamino compound containing a tyramine skeleton).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a tyramine, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of the tyramine substructure
    tyramine_substructure = Chem.MolFromSmarts('c1ccc(cc1)CCNC')
    matches = mol.GetSubstructMatches(tyramine_substructure)

    if not matches:
        return False, "Tyramine substructure not found"

    # Check if the matched substructure is aromatic and connected to an amino group
    for match in matches:
        atoms = [mol.GetAtomWithIdx(idx) for idx in match]
        aromatic_atoms = [atom for atom in atoms[:4] if atom.GetIsAromatic()]
        if len(aromatic_atoms) == 4:
            amino_group = atoms[-1].GetNeighbors()
            if any(atom.GetSymbol() == 'N' and atom.GetTotalNumHs() < 2 for atom in amino_group):
                return True, "Tyramine substructure found"

    return False, "Tyramine substructure not correctly substituted"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:27175',
                          'name': 'tyramines',
                          'definition': 'Aralkylamino compounds which contain '
                                        'a tyramine skeleton.',
                          'parents': ['CHEBI:33853', 'CHEBI:64365']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'True positives: []\n'
               'False positives: []\n'
               "False negatives: [('C1=CC(=CC=C1O)CCNC(CCCCC)=O', 'Tyramine "
               "substructure not correctly substituted')]",
    'attempt': 2,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1,
    'num_false_positives': 100,
    'num_true_negatives': 1187,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.009900990099009901,
    'recall': 1.0,
    'f1': 0.0196078431372549,
    'accuracy': 0.922360248447205}