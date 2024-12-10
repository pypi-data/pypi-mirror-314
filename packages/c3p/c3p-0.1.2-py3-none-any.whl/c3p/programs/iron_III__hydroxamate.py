"""
Classifies: CHEBI:28163 iron(III) hydroxamate
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_iron_III_hydroxamate(smiles: str):
    """
    Determines if a molecule is an iron(III) hydroxamate complex.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an iron(III) hydroxamate, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of iron(III)
    iron_atoms = [atom for atom in mol.GetAtoms() if atom.GetSymbol() == 'Fe' and atom.GetFormalCharge() == 3]
    if not iron_atoms:
        return False, "No iron(III) atom found"

    # Check for the presence of three hydroxamic acid groups
    hydroxamic_acid_count = sum(Chem.MolFromSmarts('C(=O)NO').GetNumAtomsMatchedBySmarts(mol))
    if hydroxamic_acid_count != 3:
        return False, f"Found {hydroxamic_acid_count} hydroxamic acid groups, expected 3"

    # Check if the three hydroxamic acid groups are coordinated to the iron(III)
    iron_atom = iron_atoms[0]
    coordinated_atoms = [atom for atom in iron_atom.GetNeighbors()]
    coordinated_hydroxamic_acids = sum(1 for atom in coordinated_atoms if atom.IsInRingSize(5) and atom.GetSymbol() == 'N')
    if coordinated_hydroxamic_acids != 3:
        return False, f"Found {coordinated_hydroxamic_acids} hydroxamic acid groups coordinated to iron(III), expected 3"

    return True, "Molecule is an iron(III) hydroxamate complex"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:28163',
                          'name': 'iron(III) hydroxamate',
                          'definition': 'A complex between iron(III) and three '
                                        'hydroxamic acid groups, used for iron '
                                        'transport.',
                          'parents': ['CHEBI:5975']},
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
    'error': "name 'is_iron_III__hydroxamate' is not defined",
    'stdout': '',
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0,
    'f1': 0,
    'accuracy': None}