"""
Classifies: CHEBI:26254 prenylnaphthoquinone
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_prenylnaphthoquinone(smiles: str):
    """
    Determines if a molecule is a prenylnaphthoquinone (a naphthoquinone substituted at position 2 by a prenyl or polyprenyl group, including compounds functionalized on the prenyl/polyprenyl chain).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a prenylnaphthoquinone, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find the naphthoquinone core
    naphthoquinone_smarts = "[$(O=C1C=CC2=C(C=CC=C2)C=C1[O,$(O=C)])]"
    matches = mol.GetSubstructMatches(Chem.MolFromSmarts(naphthoquinone_smarts))

    if not matches:
        return False, "No naphthoquinone core found"

    # Find the prenyl/polyprenyl group at position 2
    prenyl_smarts = "[$(CC=C(C)CC=C),$(CC=C(C)CCC=C),$(CC=C(C)CCCC=C)]"
    prenyl_pattern = Chem.MolFromSmarts(prenyl_smarts)

    # Find the atoms in the naphthoquinone core
    naphthoquinone_atoms = set([atom.GetIdx() for match in matches for atom in mol.GetAtoms()[match:match+10]])

    # Find atoms in the prenyl/polyprenyl group
    prenyl_atoms = set()
    for match in mol.GetSubstructMatches(prenyl_pattern):
        prenyl_atoms.update(match)

    # Check if the prenyl/polyprenyl group is attached to position 2
    if any(atom.GetIdx() in naphthoquinone_atoms and any(nbr.GetIdx() in prenyl_atoms for nbr in atom.GetNeighbors()) for atom in mol.GetAtoms()):
        return True, "Prenylnaphthoquinone found"
    else:
        return False, "No prenyl/polyprenyl group found at position 2 of the naphthoquinone core"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:26254',
                          'name': 'prenylnaphthoquinone',
                          'definition': 'Any napthoquinone that is substituted '
                                        'at position 2 by a prenyl or '
                                        'polyprenyl group. The term also '
                                        'includes compounds that are '
                                        'functionalised on the prenyl or '
                                        'polyprenyl chain (e.g. by a hydroxy '
                                        'group).',
                          'parents': ['CHEBI:25481', 'CHEBI:26255']},
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
    'num_true_negatives': 183916,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9999945627647254}