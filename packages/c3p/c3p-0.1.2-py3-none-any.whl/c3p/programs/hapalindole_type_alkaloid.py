"""
Classifies: CHEBI:141616 hapalindole-type alkaloid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdMolDescriptors
from typing import Tuple

def is_hapalindole_type_alkaloid(smiles: str) -> Tuple[bool, str]:
    """
    Determines if a molecule is a hapalindole-type alkaloid.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a hapalindole-type alkaloid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for the presence of an indole ring
    indole_ring = None
    for ring in mol.GetRingInfo().AtomRings():
        atoms = [mol.GetAtomWithIdx(i) for i in ring]
        if len(ring) == 9 and all(atom.GetSymbol() == 'C' or atom.GetSymbol() == 'N' for atom in atoms):
            indole_ring = ring
            break
    if indole_ring is None:
        return False, "No indole ring found"

    # Check for the presence of an isonitrile group
    isonitrile_atom = None
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C' and sum(1 for neighbor in atom.GetNeighbors() if neighbor.GetSymbol() == 'N' and neighbor.GetIsotope() == 0 and neighbor.GetTotalNumHs() == 0) == 1:
            isonitrile_atom = atom.GetIdx()
            break
    if isonitrile_atom is None:
        return False, "No isonitrile group found"

    # Check for the carbon-carbon motif (C10-C11) connecting the indole and isonitrile groups
    c10_atom = None
    c11_atom = None
    for bond in mol.GetBonds():
        atom1 = mol.GetAtomWithIdx(bond.GetBeginAtomIdx())
        atom2 = mol.GetAtomWithIdx(bond.GetEndAtomIdx())
        if atom1.GetIdx() in indole_ring and atom2.GetIdx() == isonitrile_atom:
            c10_atom = atom1.GetIdx()
            c11_atom = atom2.GetIdx()
        elif atom2.GetIdx() in indole_ring and atom1.GetIdx() == isonitrile_atom:
            c10_atom = atom2.GetIdx()
            c11_atom = atom1.GetIdx()
    if c10_atom is None or c11_atom is None:
        return False, "No carbon-carbon motif connecting indole and isonitrile groups found"

    # Check for the presence of a monoterpene unit
    monoterpene_atoms = set()
    for atom in mol.GetAtoms():
        if atom.GetIdx() != isonitrile_atom and atom.GetIdx() not in indole_ring:
            monoterpene_atoms.add(atom.GetIdx())
    if len(monoterpene_atoms) < 5:
        return False, "No monoterpene unit found"

    return True, "Molecule is a hapalindole-type alkaloid"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:141616',
                          'name': 'hapalindole-type alkaloid',
                          'definition': 'Any member of a structurally diverse '
                                        'group of hybrid isoprenoid-indole '
                                        'alkaloids, produced solely by members '
                                        'of the Subsection V cyanobacterial '
                                        'strains. The major classes of '
                                        'hapalindole-type molecules include '
                                        'hapalindoles, fischerindoles, '
                                        'welwitindolinones and ambiguines that '
                                        'share a common molecular feature '
                                        'where an indole and an isonitrile '
                                        'group are connected by a '
                                        'carbon-carbon motif (C10-C11) that is '
                                        'appended with a monoterpene unit. '
                                        'Fusion of the exomethylene carbon '
                                        'C-16 with indole backbones in the '
                                        'tricyclic hapalindoles provides '
                                        'tetracyclic hapalindoles and '
                                        'fischerindoles that, on '
                                        'rearrangement, can also lead to the '
                                        'bridged tetracyclic '
                                        'welwitindolinones. Decoration of '
                                        'tetracyclic hapalindoles with a '
                                        'tert-prenyl group at C-2 of the '
                                        'indole ring results in ambiguines, of '
                                        'which many have a fused pentacyclic '
                                        '6-6-6-5-7 or 6-6-6-5-6 ring system.',
                          'parents': ['CHEBI:38958']},
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
    'num_false_positives': 73,
    'num_true_negatives': 183852,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9995976642780249}