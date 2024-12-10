"""
Classifies: CHEBI:33470 heteroaryl group
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_heteroaryl_group(smiles: str):
    """
    Determines if a molecule is a heteroaryl group, defined as a heterocyclyl group derived
    from a heteroarene by removal of a hydrogen atom from any ring atom.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a heteroaryl group, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule has at least one aromatic ring
    aromatic_rings = AllChem.GetAromaticRings(mol)
    if not aromatic_rings:
        return False, "No aromatic rings found"

    # Check if the molecule has at least one heteroatom in an aromatic ring
    heteroatom_rings = []
    for ring in aromatic_rings:
        atoms = [mol.GetAtomWithIdx(idx) for idx in ring]
        if any(atom.GetAtomicNum() != 6 for atom in atoms):
            heteroatom_rings.append(ring)

    if not heteroatom_rings:
        return False, "No aromatic rings with heteroatoms found"

    # Check if the molecule has a radical site
    radical_atom_idx = None
    for atom in mol.GetAtoms():
        if atom.GetNumRadicalElectrons() > 0:
            radical_atom_idx = atom.GetIdx()
            break

    if radical_atom_idx is None:
        return False, "No radical site found"

    # Check if the radical site is in an aromatic ring with heteroatoms
    for ring in heteroatom_rings:
        if radical_atom_idx in ring:
            return True, "Heteroaryl group detected"

    return False, "Radical site is not in a heteroaromatic ring"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33470',
                          'name': 'heteroaryl group',
                          'definition': 'A heterocyclyl group derived from a '
                                        'heteroarene by removal of a hydrogen '
                                        'atom from any ring atom.',
                          'parents': ['CHEBI:33453']},
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
    'error': "module 'rdkit.Chem.AllChem' has no attribute 'GetAromaticRings'",
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