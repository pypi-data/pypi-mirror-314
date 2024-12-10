"""
Classifies: CHEBI:22565 ansamycin
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_ansamycin(smiles: str):
    """
    Determines if a molecule is an ansamycin.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an ansamycin, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for macrocyclic lactam ring
    ring_info = mol.GetRingInfo()
    macrocycle_rings = [ring for ring in ring_info.AtomRings() if len(ring) >= 10]
    lactam_rings = []
    for ring in macrocycle_rings:
        atoms = [mol.GetAtomWithIdx(i) for i in ring]
        if any(atom.GetSymbol() == 'N' and not atom.GetIsAromatic() for atom in atoms):
            lactam_rings.append(ring)

    if not lactam_rings:
        return False, "No macrocyclic lactam ring found"

    # Check for aromatic/quinonoid moiety bridged by aliphatic chain
    aromatic_rings = []
    quinonoid_rings = []
    bridging_chain = False

    for ring in ring_info.AtomRings():
        atoms = [mol.GetAtomWithIdx(i) for i in ring]
        if len(ring) == 6:
            if all(atom.GetIsAromatic() for atom in atoms):
                aromatic_rings.append(ring)
            elif all(atom.GetSymbol() in ['C', 'O'] for atom in atoms):
                double_bonds = sum(mol.GetBondBetweenAtoms(i, j).GetBondType() == Chem.BondType.DOUBLE for i, j in zip(ring, ring[1:] + ring[:1]))
                if double_bonds == 2:
                    quinonoid_rings.append(ring)
        elif len(ring) > 6:
            bridging_chain = True

    if not (aromatic_rings or quinonoid_rings) or not bridging_chain:
        return False, "No aromatic/quinonoid moiety bridged by aliphatic chain found"

    return True, "Molecule is an ansamycin"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22565',
                          'name': 'ansamycin',
                          'definition': 'A class of macrocyclic lactams that '
                                        'consist of an aromatic (phenyl or '
                                        'naphthyl) or quinonoid (benzoquinone '
                                        'or naphthoquinone) moiety that is '
                                        'bridged by an aliphatic chain.',
                          'parents': [   'CHEBI:24995',
                                         'CHEBI:26188',
                                         'CHEBI:51026']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': 'Attempt failed: can only concatenate tuple (not "list") to '
               'tuple',
    'attempt': 2,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1,
    'num_false_positives': 100,
    'num_true_negatives': 1552,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.009900990099009901,
    'recall': 1.0,
    'f1': 0.0196078431372549,
    'accuracy': 0.9395039322444041}