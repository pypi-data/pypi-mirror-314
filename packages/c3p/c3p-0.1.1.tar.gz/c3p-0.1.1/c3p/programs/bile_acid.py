"""
Classifies: CHEBI:3098 bile acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors

def is_bile_acid(smiles: str):
    """
    Determines if a molecule is a bile acid.

    Bile acids are defined as hydroxy-5beta-cholanic acids occurring in bile, where they are present as the
    sodium salts of their amides with glycine or taurine. In mammals, bile acids almost invariably have
    a 5beta-configuration.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a bile acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the 5beta-cholanic acid scaffold
    ring_info = mol.GetRingInfo()
    cholanic_rings = []
    for ring in ring_info.AtomRings():
        if len(ring) == 17:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            is_cholanic = all(atom.GetSymbol() == 'C' for atom in atoms)
            if is_cholanic:
                cholanic_rings.append(ring)

    if not cholanic_rings:
        return False, "No cholanic acid scaffold found"

    # Check for hydroxy groups
    hydroxy_count = Chem.Crippen.MolLogP(mol) < 4.0  # Empirical threshold based on logP
    if not hydroxy_count:
        return False, "No hydroxy groups found"

    # Check for 5beta-configuration
    ring_atoms = set(cholanic_rings[0])
    ring_atoms_sorted = sorted(ring_atoms, key=lambda x: mol.GetAtomWithIdx(x).GetDegree(), reverse=True)
    ring_atom_idx = ring_atoms_sorted[4]  # 5th highest degree atom is the ring junction
    ring_atom = mol.GetAtomWithIdx(ring_atom_idx)

    if ring_atom.GetHybridization() != Chem.HybridizationType.SP3:
        return False, "Ring junction atom is not sp3 hybridized"

    ring_atom_neighbors = [mol.GetAtomWithIdx(neighbor_idx) for neighbor_idx in ring_atom.GetNeighbors()]
    hydrogens = [neighbor for neighbor in ring_atom_neighbors if neighbor.GetSymbol() == 'H']

    if len(hydrogens) != 1:
        return False, "Ring junction atom does not have a single hydrogen"

    if hydrogens[0].GetIsotope():  # Check for deuterium
        return False, "Ring junction hydrogen is deuterated"

    return True, "Molecule is a bile acid"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:3098',
                          'name': 'bile acid',
                          'definition': 'Any member of a group of '
                                        'hydroxy-5beta-cholanic acids occuring '
                                        'in bile, where they are present as '
                                        'the sodium salts of their amides with '
                                        'glycine or taurine. In mammals bile '
                                        'acids almost invariably have '
                                        '5beta-configuration.',
                          'parents': ['CHEBI:138366', 'CHEBI:24663']},
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
    'error': 'Python argument types in\n'
             '    Mol.GetAtomWithIdx(Mol, Atom)\n'
             'did not match C++ signature:\n'
             '    GetAtomWithIdx(RDKit::ROMol {lvalue} self, unsigned int idx)',
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