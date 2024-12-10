"""
Classifies: CHEBI:137001 C-terminal alpha-amino-acid amide residue
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_C_terminal_alpha_amino_acid_amide_residue(smiles):
    """
    Determines if a molecule is a C-terminal alpha-amino-acid amide residue.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a C-terminal alpha-amino-acid amide residue, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find the amide nitrogen atom
    amide_nitrogen = [atom for atom in mol.GetAtoms() if atom.GetSymbol() == 'N' and atom.GetIsAromatic() == False and atom.GetFormalCharge() == 0 and atom.GetImplicitValence() == 3]

    if not amide_nitrogen:
        return False, "No amide nitrogen atom found"

    # Check if the amide nitrogen is connected to a carbonyl carbon
    carbonyl_carbon = None
    for neighbor in amide_nitrogen[0].GetNeighbors():
        if neighbor.GetSymbol() == 'C' and neighbor.GetImplicitValence() == 3:
            carbonyl_carbon = neighbor
            break

    if carbonyl_carbon is None:
        return False, "Amide nitrogen not connected to a carbonyl carbon"

    # Check if the carbonyl carbon is connected to an oxygen atom
    carbonyl_oxygen = None
    for neighbor in carbonyl_carbon.GetNeighbors():
        if neighbor.GetSymbol() == 'O':
            carbonyl_oxygen = neighbor
            break

    if carbonyl_oxygen is None:
        return False, "Carbonyl carbon not connected to an oxygen atom"

    # Check if the carbonyl carbon is connected to a chiral carbon
    chiral_carbon = None
    for neighbor in carbonyl_carbon.GetNeighbors():
        if neighbor.GetSymbol() == 'C' and neighbor.GetChiralTag() != 0:
            chiral_carbon = neighbor
            break

    if chiral_carbon is None:
        return False, "No chiral carbon atom found"

    # Check if the chiral carbon is connected to an alkylamino group
    alkylamino_group = False
    for neighbor in chiral_carbon.GetNeighbors():
        if neighbor.GetSymbol() == 'N' and neighbor.GetIsAromatic() == False and neighbor.GetFormalCharge() == 0:
            alkylamino_group = True
            break

    if not alkylamino_group:
        return False, "No alkylamino group found"

    return True, "Molecule is a C-terminal alpha-amino-acid amide residue"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:137001',
                          'name': 'C-terminal alpha-amino-acid amide residue',
                          'definition': 'An alkylamino group derived from any '
                                        'alpha-amino-acid amide.',
                          'parents': ['CHEBI:22332']},
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
    'num_true_negatives': 183920,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.999994562882977}