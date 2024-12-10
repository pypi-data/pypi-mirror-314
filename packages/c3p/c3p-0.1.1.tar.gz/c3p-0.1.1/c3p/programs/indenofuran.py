"""
Classifies: CHEBI:149453 indenofuran
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_indenofuran(smiles: str):
    """
    Determines if a molecule is an indenofuran (an organic heterotricyclic compound whose skeleton consists of an indene fused to a furan ring).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an indenofuran, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Get the ring information
    rings = mol.GetRingInfo()

    # Check for exactly three rings
    if len(rings.AtomRings()) != 3:
        return False, "Molecule does not have exactly three rings"

    # Check if the rings are fused
    fused_rings = []
    for ring1_idx, ring1 in enumerate(rings.AtomRings()):
        for ring2_idx, ring2 in enumerate(rings.AtomRings()):
            if ring2_idx > ring1_idx:
                common_atoms = set(ring1) & set(ring2)
                if len(common_atoms) > 1:
                    fused_rings.append((ring1, ring2))

    if len(fused_rings) != 2:
        return False, "Molecule does not have two fused rings"

    # Check if one of the rings is a 5-membered ring (furan)
    has_furan = False
    for ring in rings.AtomRings():
        if len(ring) == 5:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            if any(atom.GetSymbol() == 'O' for atom in atoms):
                has_furan = True
                break

    if not has_furan:
        return False, "Molecule does not contain a furan ring"

    # Check if the other ring is an indene
    has_indene = False
    for ring1, ring2 in fused_rings:
        if len(ring1) == 6 and len(ring2) == 6:
            atoms1 = [mol.GetAtomWithIdx(i) for i in ring1]
            atoms2 = [mol.GetAtomWithIdx(i) for i in ring2]
            if all(atom.GetSymbol() == 'C' for atom in atoms1 + atoms2):
                has_indene = True
                break

    if not has_indene:
        return False, "Molecule does not contain an indene ring"

    return True, "Molecule is an indenofuran"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:149453',
                          'name': 'indenofuran',
                          'definition': 'Any organic heterotricyclic compound '
                                        'whose skeleton consists of an indene '
                                        'fused to a furan ring.',
                          'parents': ['CHEBI:26979']},
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
    'num_false_positives': 100,
    'num_true_negatives': 44053,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9977125515242107}