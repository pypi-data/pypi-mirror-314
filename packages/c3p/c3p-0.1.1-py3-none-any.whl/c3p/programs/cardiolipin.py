"""
Classifies: CHEBI:28494 cardiolipin
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_cardiolipin(smiles: str):
    """
    Determines if a molecule is a cardiolipin (a phosphatidylglycerol composed of two molecules of phosphatidic acid covalently linked to a molecule of glycerol).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a cardiolipin, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Count the number of phosphorus atoms
    p_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'P')
    if p_count != 2:
        return False, "Molecule does not contain exactly 2 phosphorus atoms"

    # Find the glycerol component
    glycerol_atoms = []
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C' and atom.GetDegree() == 3 and sum(1 for neighbor in atom.GetNeighbors() if neighbor.GetSymbol() == 'O') == 3:
            glycerol_atoms.append(atom.GetIdx())

    if len(glycerol_atoms) != 1:
        return False, "Unable to identify the glycerol component"

    glycerol_atom = glycerol_atoms[0]

    # Find the phosphatidic acid components
    phosphatidic_acid_components = []
    for p_atom in mol.GetAtoms():
        if p_atom.GetSymbol() == 'P':
            for neighbor in p_atom.GetNeighbors():
                if neighbor.GetSymbol() == 'O' and neighbor.GetDegree() == 1:
                    continue
                if neighbor.GetSymbol() == 'C':
                    phosphatidic_acid_components.append(neighbor.GetIdx())

    if len(phosphatidic_acid_components) != 4:
        return False, "Unable to identify the phosphatidic acid components"

    # Check if the phosphatidic acid components are linked to the glycerol component
    for component in phosphatidic_acid_components:
        if not any(mol.GetBondBetweenAtoms(component, atom).GetBondType() == Chem.BondType.SINGLE for atom in glycerol_atoms):
            return False, "Phosphatidic acid components are not linked to the glycerol component"

    return True, "Molecule is a cardiolipin"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:28494',
                          'name': 'cardiolipin',
                          'definition': 'A phosphatidylglycerol composed of '
                                        'two molecules of phosphatidic acid '
                                        'covalently linked to a molecule of '
                                        'glycerol.',
                          'parents': ['CHEBI:166988', 'CHEBI:17517']},
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
    'num_true_negatives': 183899,
    'num_false_negatives': 4,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.999978249403218}