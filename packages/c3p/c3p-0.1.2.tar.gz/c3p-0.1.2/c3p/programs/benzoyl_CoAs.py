"""
Classifies: CHEBI:22736 benzoyl-CoAs
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_benzoyl_CoAs(smiles: str):
    """
    Determines if a molecule is a benzoyl-CoA, defined as any aroyl-CoA in which the aroyl group is specified as benzoyl or its substituted derivative.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a benzoyl-CoA, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of a CoA moiety
    coa_pattern = Chem.MolFromSmarts('C(=O)NCCC(=O)NCCSCCNC(=O)CCNC(=O)C')
    if not mol.HasSubstructMatch(coa_pattern):
        return False, "CoA moiety not found"

    # Find the benzoyl group
    benzoyl_pattern = Chem.MolFromSmarts('C(=O)C1=CC=CC=C1')
    benzoyl_match = mol.GetSubstructMatches(benzoyl_pattern)

    if not benzoyl_match:
        return False, "Benzoyl group not found"

    # Check for substitutions on the benzoyl group
    benzoyl_ring = Chem.GetMolFrags(mol)[benzoyl_match[0]]
    substituents = []
    for atom in benzoyl_ring:
        if mol.GetAtomWithIdx(atom).GetSymbol() != 'C' and mol.GetAtomWithIdx(atom).GetSymbol() != 'H':
            substituents.append(mol.GetAtomWithIdx(atom).GetSymbol())

    if len(substituents) > 0:
        return True, f"Substituted benzoyl-CoA with substituents: {', '.join(set(substituents))}"
    else:
        return True, "Unsubstituted benzoyl-CoA"

# Example usage
smiles = "[C@@H]1(N2C3=C(C(=NC=N3)N)N=C2)O[C@H](COP(OP(OCC([C@H](C(NCCC(NCCSC(=O)C=4C=CC(=C(C4)OC)O)=O)=O)O)(C)C)(=O)O)(=O)O)[C@H]([C@H]1O)OP(O)(O)=O"
result, reason = is_benzoyl_CoAs(smiles)
print(result, reason)


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22736',
                          'name': 'benzoyl-CoAs',
                          'definition': 'Any  aroyl-CoA in which the  aroyl '
                                        'group is specified as benzoyl or its '
                                        'substituted derivative.',
                          'parents': ['CHEBI:61940']},
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
    'num_true_negatives': 183924,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9999945630012234}