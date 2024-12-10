"""
Classifies: CHEBI:25185 menaquinones
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_menaquinones(smiles: str):
    """
    Determines if a molecule is a menaquinone (any prenylnaphthoquinone having a prenyl or polyprenyl group
    at position 3 and a methyl group at position 2 on the naphthoquinone ring).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a menaquinone, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule is a naphthoquinone
    is_naphthoquinone = False
    for ring in mol.GetRingInfo().AtomRings():
        if len(ring) == 10:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            if all(atom.GetSymbol() == 'C' for atom in atoms) and sum(atom.GetIsAromatic() for atom in atoms) == 6:
                is_naphthoquinone = True
                break

    if not is_naphthoquinone:
        return False, "Not a naphthoquinone"

    # Check for prenyl/polyprenyl group at position 3
    position_3 = None
    for atom in atoms:
        if sum(bond.GetIsAromatic() for bond in atom.GetBonds()) == 2:
            position_3 = atom.GetIdx()
            break

    if position_3 is None:
        return False, "Could not identify position 3"

    atom_3 = mol.GetAtomWithIdx(position_3)
    neighbors_3 = [mol.GetAtomWithIdx(neighbor.GetIdx()) for neighbor in atom_3.GetNeighbors()]
    prenyl_group = False
    for neighbor in neighbors_3:
        if neighbor.GetSymbol() == 'C' and not neighbor.GetIsAromatic():
            prenyl_group = True
            break

    if not prenyl_group:
        return False, "No prenyl/polyprenyl group at position 3"

    # Check for methyl group at position 2
    position_2 = None
    for atom in atoms:
        if sum(bond.GetIsAromatic() for bond in atom.GetBonds()) == 2:
            position_2 = atom.GetIdx()
            break

    if position_2 is None:
        return False, "Could not identify position 2"

    atom_2 = mol.GetAtomWithIdx(position_2)
    neighbors_2 = [mol.GetAtomWithIdx(neighbor.GetIdx()) for neighbor in atom_2.GetNeighbors()]
    methyl_group = False
    for neighbor in neighbors_2:
        if neighbor.GetSymbol() == 'C' and neighbor.GetDegree() == 1:
            methyl_group = True
            break

    if not methyl_group:
        return False, "No methyl group at position 2"

    return True, "Molecule is a menaquinone"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:25185',
                          'name': 'menaquinones',
                          'definition': 'Any prenylnaphthoquinone having a '
                                        'prenyl or polyprenyl group at '
                                        'position 3 and a methyl group at '
                                        'position 2 on the naphthoquinone '
                                        'ring.',
                          'parents': ['CHEBI:26254']},
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
    'num_true_negatives': 183917,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9999945627942888}