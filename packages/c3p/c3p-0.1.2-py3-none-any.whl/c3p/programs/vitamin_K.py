"""
Classifies: CHEBI:28384 vitamin K
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_vitamin_K(smiles: str):
    """
    Determines if a molecule is a vitamin K compound.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a vitamin K compound, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of a 2-methyl-1,4-naphthoquinone core
    naphthoquinone_core = Chem.MolFromSmiles('O=C1C2=C(C(=O)C=C1C)C=CC=C2C')
    if not mol.HasSubstructMatch(naphthoquinone_core):
        return False, "Missing 2-methyl-1,4-naphthoquinone core"

    # Check for the presence of a side chain
    side_chain = mol.GetSubstructMatches(Chem.MolFromSmarts('C([C])(C)CCCCCC'))
    if not side_chain:
        return False, "Missing side chain"

    # Count the double bonds in the side chain
    side_chain_bonds = [mol.GetBondBetweenAtoms(side_chain[0][i], side_chain[0][i+1]).GetBondType()
                        for i in range(len(side_chain[0])-1)]
    double_bonds = sum(bond == Chem.BondType.DOUBLE for bond in side_chain_bonds)

    if double_bonds == 0:
        return True, "Vitamin K1 (Phylloquinone)"
    elif double_bonds > 0:
        return True, f"Vitamin K2 (Menaquinone) with {double_bonds} double bond(s) in the side chain"
    else:
        return False, "Unknown vitamin K compound"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:28384',
                          'name': 'vitamin K',
                          'definition': 'Any member of a group of fat-soluble '
                                        '2-methyl-1,4-napthoquinones that '
                                        'exhibit biological activity against '
                                        'vitamin K deficiency. Vitamin K is '
                                        'required for the synthesis of '
                                        'prothrombin and certain other blood '
                                        'coagulation factors.',
                          'parents': ['CHEBI:132142']},
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
    'error': "'NoneType' object has no attribute 'GetBondType'",
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