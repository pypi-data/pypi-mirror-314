"""
Classifies: CHEBI:18100 multi-methyl-branched fatty acyl-CoA
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_multi_methyl_branched_fatty_acyl_CoA(smiles: str):
    """
    Determines if a molecule is a multi-methyl-branched fatty acyl-CoA.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a multi-methyl-branched fatty acyl-CoA, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of a coenzyme A substructure
    coenzyme_a_smarts = 'C(C(=O)NCCS)(C(=O)NCCC(=O)NCCC(=O)O)O'
    coenzyme_a_pattern = Chem.MolFromSmarts(coenzyme_a_smarts)
    matches = mol.GetSubstructMatches(coenzyme_a_pattern)
    if not matches:
        return False, "Coenzyme A substructure not found"

    # Find the carbon atom connected to the coenzyme A substructure
    for idx in matches[0]:
        atom = mol.GetAtomWithIdx(idx)
        if atom.GetSymbol() == 'C' and atom.GetDegree() == 2:
            acyl_carbon = atom
            break
    else:
        return False, "Cannot identify the acyl carbon atom"

    # Check if the fatty acid chain is branched and contains multiple methyl groups
    chain = []
    current_atom = acyl_carbon
    while current_atom.GetDegree() > 1:
        neighbors = [n for n in current_atom.GetNeighbors() if n.GetIdx() != acyl_carbon.GetIdx()]
        if len(neighbors) != 1:
            return False, "Branched fatty acid chain not found"
        current_atom = neighbors[0]
        chain.append(current_atom)

    methyl_count = sum(1 for atom in chain if atom.GetSymbol() == 'C' and len([n for n in atom.GetNeighbors() if n.GetSymbol() == 'C']) == 3)
    if methyl_count < 2:
        return False, "Fatty acid chain does not contain multiple methyl branches"

    return True, "Multi-methyl-branched fatty acyl-CoA detected"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:18100',
                          'name': 'multi-methyl-branched fatty acyl-CoA',
                          'definition': 'A branched-chain fatty acyl-CoA that '
                                        'results from the formal condensation '
                                        'of the thiol group of coenzyme A with '
                                        'the carboxy group of any '
                                        'multi-methyl-branched fatty acid.',
                          'parents': ['CHEBI:25271']},
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
    'num_true_negatives': 183921,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.999994562912539}