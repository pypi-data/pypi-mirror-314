"""
Classifies: CHEBI:24407 glycosyl glycoside
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_glycosyl_glycoside(smiles: str):
    """
    Determines if a molecule is a glycosyl glycoside (a disaccharide connected by a glycosidic linkage between anomeric centres).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a glycosyl glycoside, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find all rings in the molecule
    rings = mol.GetRingInfo().AtomRings()

    # Check for at least two rings (monosaccharides)
    if len(rings) < 2:
        return False, "Less than two monosaccharide units found"

    # Check each pair of rings for a glycosidic linkage
    for i in range(len(rings)):
        for j in range(i+1, len(rings)):
            ring1 = set(rings[i])
            ring2 = set(rings[j])

            # Find atoms that connect the two rings
            link_atoms = ring1.intersection(ring2)

            # Check if there is exactly one linking atom
            if len(link_atoms) == 1:
                link_atom_idx = list(link_atoms)[0]
                link_atom = mol.GetAtomWithIdx(link_atom_idx)

                # Check if the linking atom is an oxygen (glycosidic linkage)
                if link_atom.GetSymbol() == 'O':
                    # Check if the linking atom is an anomeric carbon
                    anomeric_carbon1 = None
                    anomeric_carbon2 = None

                    for neighbor_idx in link_atom.GetNeighbors():
                        neighbor = mol.GetAtomWithIdx(neighbor_idx)
                        if neighbor_idx in ring1 and neighbor.GetHybridization() == Chem.HybridizationState.SP2:
                            anomeric_carbon1 = neighbor_idx
                        if neighbor_idx in ring2 and neighbor.GetHybridization() == Chem.HybridizationState.SP2:
                            anomeric_carbon2 = neighbor_idx

                    if anomeric_carbon1 is not None and anomeric_carbon2 is not None:
                        return True, "Glycosyl glycoside found"

    return False, "No glycosidic linkage between anomeric centres found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24407',
                          'name': 'glycosyl glycoside',
                          'definition': 'Any disaccharide in which the two '
                                        'monosaccharide components are '
                                        'connected by a glycosidic linkage '
                                        'between their anomeric centres.',
                          'parents': ['CHEBI:36233']},
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
    'num_true_negatives': 183916,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9999945627647254}