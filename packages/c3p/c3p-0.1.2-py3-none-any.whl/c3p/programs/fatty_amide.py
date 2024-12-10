"""
Classifies: CHEBI:29348 fatty amide
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_fatty_amide(smiles: str):
    """
    Determines if a molecule is a fatty amide (a monocarboxylic acid amide derived from a fatty acid).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a fatty amide, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for amide functional group
    amide_atoms = [atom.GetIdx() for atom in mol.GetAtoms() if atom.GetSymbol() == 'N' and atom.GetTotalNumHs() == 0]
    for atom_idx in amide_atoms:
        atom = mol.GetAtomWithIdx(atom_idx)
        neighbors = [mol.GetAtomWithIdx(n.GetIdx()) for n in atom.GetNeighbors()]
        if len(neighbors) == 2 and neighbors[0].GetSymbol() == 'C' and neighbors[1].GetSymbol() == 'C':
            if neighbors[0].GetDegree() == 3 and neighbors[1].GetDegree() == 2:
                amide_carbonyl = neighbors[1]
                amide_carbon = neighbors[0]
            elif neighbors[1].GetDegree() == 3 and neighbors[0].GetDegree() == 2:
                amide_carbonyl = neighbors[0]
                amide_carbon = neighbors[1]
            else:
                continue

            # Check if amide is derived from a fatty acid
            fatty_acid_chain = []
            next_atom = amide_carbon
            while next_atom.GetDegree() == 2:
                fatty_acid_chain.append(next_atom.GetIdx())
                neighbors = [mol.GetAtomWithIdx(n.GetIdx()) for n in next_atom.GetNeighbors()]
                next_atom = neighbors[0] if neighbors[0].GetIdx() != fatty_acid_chain[-2] else neighbors[1]

            if len(fatty_acid_chain) >= 6:
                return True, f"Fatty amide derived from a {len(fatty_acid_chain) + 1}-carbon fatty acid"

    return False, "Not a fatty amide"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:29348',
                          'name': 'fatty amide',
                          'definition': 'A monocarboxylic acid amide derived '
                                        'from a fatty acid.',
                          'parents': ['CHEBI:29347', 'CHEBI:61697']},
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
    'num_true_negatives': 183550,
    'num_false_negatives': 39,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9997875689719973}