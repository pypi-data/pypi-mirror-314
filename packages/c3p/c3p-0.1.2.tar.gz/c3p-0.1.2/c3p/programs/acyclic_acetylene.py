"""
Classifies: CHEBI:33650 acyclic acetylene
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors

def is_acyclic_acetylene(smiles: str):
    """
    Determines if a molecule is an acyclic acetylene (acyclic hydrocarbon with one or more carbon-carbon triple bonds).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an acyclic acetylene, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for rings
    if mol.GetRingInfo().NumRings() > 0:
        return False, "Molecule contains rings"

    # Check for triple bonds
    triple_bonds = [bond for bond in mol.GetBonds() if bond.GetBondType() == Chem.BondType.TRIPLE]
    if not triple_bonds:
        return False, "No triple bonds found"

    # Check if all atoms are carbon or hydrogen
    atoms = [atom.GetSymbol() for atom in mol.GetAtoms()]
    if not all(atom in ['C', 'H'] for atom in atoms):
        return False, "Molecule contains atoms other than carbon and hydrogen"

    # Check for linear acyclic acetylenes
    linear_smiles = Chem.MolToSmiles(mol, isomericSmiles=True)
    if linear_smiles.count('#') == 1 and linear_smiles.count('C') > 2:
        return True, "Linear acyclic acetylene"

    # Check for branched acyclic acetylenes
    if linear_smiles.count('#') > 1:
        return True, "Branched acyclic acetylene"

    return False, "Not an acyclic acetylene"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33650',
                          'name': 'acyclic acetylene',
                          'definition': 'Acyclic (branched or unbranched) '
                                        'hydrocarbons having one or more '
                                        'carbon-carbon triple bonds.',
                          'parents': ['CHEBI:33644']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.10526315789473684 is too low.\n'
               "True positives: [('CCCCC#C', 'Acyclic acetylene')]\n"
               "False positives: [('C(CCC=C)C/C=C\\\\C#CC#C\\\\C=C\\\\C', "
               "'Acyclic acetylene'), ('C(CCCC)CCCC#CCC', 'Acyclic "
               "acetylene'), ('C(CC)CC#CC#CC#CC#CC', 'Acyclic acetylene'), "
               "('C(CC/C=C/CC#CC#C/C=C\\\\C)CCC=C', 'Acyclic acetylene'), "
               "('[C+]#[C-]', 'Acyclic acetylene'), "
               "('C(CCCCCCCC)CCCCCCCC#CCC', 'Acyclic acetylene'), ('[C]#[C-]', "
               "'Acyclic acetylene'), ('C(CCCCC#CC/C=C\\\\CCCCC)CCCC', "
               "'Acyclic acetylene'), "
               "('CC\\\\C=C\\\\C=C\\\\C#CC#C\\\\C=C\\\\C', 'Acyclic "
               "acetylene'), ('CC=CC#CC#CC#CC=CC=C', 'Acyclic acetylene'), "
               "('C(CCCCCCC)CCCCCCC#CCCCC', 'Acyclic acetylene'), "
               "('C(CCC=C)C/C=C/C=C/C#CC#CC#CC', 'Acyclic acetylene'), "
               "('[C]#C', 'Acyclic acetylene'), ('C#[C-]', 'Acyclic "
               "acetylene'), ('[C]#[C+]', 'Acyclic acetylene'), "
               "('C(=C\\\\C=C)/C=C/C#CC#C\\\\C=C\\\\C', 'Acyclic acetylene'), "
               "('[C-]#[C-]', 'Acyclic acetylene')]\n"
               'False negatives: []',
    'attempt': 4,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1,
    'num_false_positives': 11,
    'num_true_negatives': 183906,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.08333333333333333,
    'recall': 1.0,
    'f1': 0.15384615384615385,
    'accuracy': 0.9999401907371763}