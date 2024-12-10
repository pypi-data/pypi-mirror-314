"""
Classifies: CHEBI:33245 organic fundamental parent
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_organic_fundamental_parent(smiles: str):
    """
    Determines if a molecule is an organic fundamental parent based on the definition:
    'An organic fundamental parent is a structure used as a basis for substitutive names in organic nomenclature,
    containing, in addition to one or more hydrogen atoms, a single atom of an element, a number of atoms
    (alike or different) linked together to form an unbranched chain, a monocyclic or polycyclic ring system,
    or a ring assembly or ring/chain system.'

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an organic fundamental parent, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for organic compound
    if not Descriptors.MolWt(mol) > 1.008:
        return False, "Molecule is not organic"

    # Check for single element or chain/ring system
    ring_info = mol.GetRingInfo()
    rings = ring_info.AtomRings()
    if not rings:
        # Check for unbranched chain
        atom_pairs = Chem.FindAllPathsOfLengthN(mol, 2, useBonds=True)
        if len(atom_pairs) == mol.GetNumAtoms() - 1:
            return True, "Unbranched chain"
        else:
            return False, "Neither a chain nor a ring system"
    else:
        # Check for monocyclic or polycyclic ring system
        if len(rings) == 1:
            return True, "Monocyclic ring system"
        else:
            # Check for ring assembly or ring/chain system
            is_ring_assembly = True
            for ring in rings:
                ring_atoms = set(ring)
                for atom_idx in ring_atoms:
                    atom = mol.GetAtomWithIdx(atom_idx)
                    for neighbor in atom.GetNeighbors():
                        if neighbor.GetIdx() not in ring_atoms:
                            is_ring_assembly = False
                            break
                if not is_ring_assembly:
                    break
            if is_ring_assembly:
                return True, "Ring assembly"
            else:
                return True, "Ring/chain system"

    return False, "Unable to classify"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33245',
                          'name': 'organic fundamental parent',
                          'definition': 'An organic fundamental parent is a '
                                        'structure used as a basis for '
                                        'substitutive names in organic '
                                        'nomenclature, containing, in addition '
                                        'to one or more hydrogen atoms, a '
                                        'single atom of an element, a number '
                                        'of atoms (alike or different) linked '
                                        'together to form an unbranched chain, '
                                        'a monocyclic or polycyclic ring '
                                        'system, or a ring assembly or '
                                        'ring/chain system.',
                          'parents': ['CHEBI:37175', 'CHEBI:50860']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': 'Attempt failed: Python argument types in\n'
               '    rdkit.Chem.rdmolops.FindAllPathsOfLengthN(Mol, int)\n'
               'did not match C++ signature:\n'
               '    FindAllPathsOfLengthN(RDKit::ROMol mol, unsigned int '
               'length, bool useBonds=True, bool useHs=False, int '
               'rootedAtAtom=-1, bool onlyShortestPaths=False)',
    'attempt': 1,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 148,
    'num_false_positives': 100,
    'num_true_negatives': 13,
    'num_false_negatives': 41,
    'num_negatives': None,
    'precision': 0.5967741935483871,
    'recall': 0.783068783068783,
    'f1': 0.677345537757437,
    'accuracy': 0.5331125827814569}