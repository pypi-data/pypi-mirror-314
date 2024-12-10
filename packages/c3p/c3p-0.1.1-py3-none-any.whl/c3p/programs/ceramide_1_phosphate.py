"""
Classifies: CHEBI:13956 ceramide 1-phosphate
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_ceramide_1_phosphate(smiles: str):
    """
    Determines if a molecule is a ceramide 1-phosphate.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a ceramide 1-phosphate, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of a phosphate group
    has_phosphate = any(atom.GetSymbol() == 'P' and atom.GetTotalDegree() == 4 for atom in mol.GetAtoms())
    if not has_phosphate:
        return False, "No phosphate group found"

    # Check for the presence of an amide group
    has_amide = any(bond.GetBondType() == Chem.BondType.AMIDE for bond in mol.GetBonds())
    if not has_amide:
        return False, "No amide group found"

    # Check if the phosphate group is attached to the C1 position of the sphingoid base
    sphingoid_base_atoms = []
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C' and atom.GetTotalDegree() == 3 and atom.GetHybridization() == Chem.HybridizationType.SP2:
            neighbors = [mol.GetAtomWithIdx(nbr_idx) for nbr_idx in atom.GetNeighbors()]
            if any(nbr.GetSymbol() == 'N' for nbr in neighbors) and any(nbr.GetSymbol() == 'O' for nbr in neighbors):
                sphingoid_base_atoms.append(atom)

    if not sphingoid_base_atoms:
        return False, "No sphingoid base found"

    c1_atom = None
    for atom in sphingoid_base_atoms:
        neighbors = [mol.GetAtomWithIdx(nbr_idx) for nbr_idx in atom.GetNeighbors()]
        for nbr in neighbors:
            if nbr.GetSymbol() == 'O' and nbr.GetTotalDegree() == 2 and nbr.IsInRing():
                c1_atom = atom
                break

    if c1_atom is None:
        return False, "Phosphate group not attached to C1 position"

    c1_neighbors = [mol.GetAtomWithIdx(nbr_idx) for nbr_idx in c1_atom.GetNeighbors()]
    has_phosphate_at_c1 = any(nbr.GetSymbol() == 'P' for nbr in c1_neighbors)

    if has_phosphate_at_c1:
        return True, "Molecule is a ceramide 1-phosphate"
    else:
        return False, "Phosphate group not attached to C1 position"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:13956',
                          'name': 'ceramide 1-phosphate',
                          'definition': 'A phosphosphingolipid consisting of '
                                        'any ceramide phosphorylated at '
                                        'position 1',
                          'parents': ['CHEBI:17761', 'CHEBI:35786']},
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
    'success': False,
    'best': True,
    'error': "type object 'BondType' has no attribute 'AMIDE'",
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