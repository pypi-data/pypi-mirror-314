"""
Classifies: CHEBI:28892 ganglioside
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_ganglioside(smiles: str):
    """
    Determines if a molecule is a ganglioside, defined as a glycosphingolipid
    (ceramide and oligosaccharide) with one or more sialic acids linked on the sugar chain.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a ganglioside, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for ceramide
    ceramide_atoms = []
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'N' and atom.GetIsAromatic() == False:
            ceramide_atoms.append(atom.GetIdx())

    if len(ceramide_atoms) != 1:
        return False, "No ceramide found"

    # Check for oligosaccharide
    oligosaccharide_atoms = []
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'O' and atom.GetIsAromatic() == False and len(atom.GetNeighbors()) > 1:
            oligosaccharide_atoms.append(atom.GetIdx())

    if len(oligosaccharide_atoms) < 3:
        return False, "No oligosaccharide found"

    # Check for sialic acid
    sialic_acid_found = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C' and atom.GetIsAromatic() == False:
            env = Chem.FindAtomEnvironmentOfRadiusN(mol, atom.GetIdx(), 4)
            if env and 'N' in env and 'O=C-O-C' in ''.join(sorted(env.replace('C', ''))):
                sialic_acid_found = True
                break

    if not sialic_acid_found:
        return False, "No sialic acid found"

    return True, "Ganglioside identified"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:28892',
                          'name': 'ganglioside',
                          'definition': 'A molecule composed of a '
                                        'glycosphingolipid (ceramide and '
                                        'oligosaccharide) with one or more '
                                        'sialic acids linked on the sugar '
                                        'chain.',
                          'parents': [   'CHEBI:17761',
                                         'CHEBI:231691',
                                         'CHEBI:36526']},
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
    'num_true_negatives': 183643,
    'num_false_negatives': 29,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9998421098479899}