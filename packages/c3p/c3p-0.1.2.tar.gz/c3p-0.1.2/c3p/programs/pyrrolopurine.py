"""
Classifies: CHEBI:136861 pyrrolopurine
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdchem

def is_pyrrolopurine(smiles: str):
    """
    Determines if a molecule is a pyrrolopurine.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a pyrrolopurine, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Get the ring information
    rings = mol.GetRingInfo()
    rings = rings.AtomRings()

    # Check for the presence of a pyrrole and purine ring
    pyrrole_ring = None
    purine_ring = None

    for ring in rings:
        is_pyrrole = False
        is_purine = False

        if len(ring) == 5:
            # Check for pyrrole ring
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            symbols = [atom.GetSymbol() for atom in atoms]
            if 'N' in symbols and symbols.count('C') == 4:
                is_pyrrole = True
                pyrrole_ring = ring

        elif len(ring) == 6:
            # Check for purine ring
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            symbols = [atom.GetSymbol() for atom in atoms]
            if symbols.count('N') == 3 and symbols.count('C') == 3:
                is_purine = True
                purine_ring = ring

        if is_pyrrole and is_purine:
            break

    if pyrrole_ring is None or purine_ring is None:
        return False, "Missing pyrrole or purine ring"

    # Check if the pyrrole and purine rings are fused
    pyrrole_atoms = set(pyrrole_ring)
    purine_atoms = set(purine_ring)
    shared_atoms = pyrrole_atoms.intersection(purine_atoms)

    if len(shared_atoms) == 2:
        return True, "Molecule is a pyrrolopurine"
    else:
        return False, "Pyrrole and purine rings are not fused"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:136861',
                          'name': 'pyrrolopurine',
                          'definition': 'Any organic heterotricyclic compound '
                                        'with a skeleton consisting of a '
                                        'pyrrole ring fused to a purine ring '
                                        'system.',
                          'parents': ['CHEBI:26979', 'CHEBI:38101']},
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
    'num_false_positives': 35,
    'num_true_negatives': 183888,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9998042669798395}