"""
Classifies: CHEBI:23000 caprolactams
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_caprolactams(smiles: str):
    """
    Determines if a molecule is a caprolactam (a lactam with a 7-membered ring containing an amide bond).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a caprolactam, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Generate the ring information
    rings = mol.GetRingInfo()

    # Check for at least one 7-membered ring
    if not any(len(ring) == 7 for ring in rings.AtomRings()):
        return False, "No 7-membered rings found"

    # Find all 7-membered rings
    seven_rings = []
    for ring in rings.AtomRings():
        if len(ring) == 7:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            seven_rings.append(ring)

    if not seven_rings:
        return False, "No 7-membered rings found"

    # Check if any 7-membered ring contains an amide bond
    for ring in seven_rings:
        atoms = [mol.GetAtomWithIdx(i) for i in ring]
        atom_symbols = [atom.GetSymbol() for atom in atoms]
        atom_types = [atom.GetHybridization() for atom in atoms]

        if 'N' in atom_symbols and 'C' in atom_symbols and Chem.rdchem.BondType.DOUBLE in [mol.GetBondBetweenAtoms(atoms[i].GetIdx(), atoms[i+1].GetIdx()).GetBondType() for i in range(len(atoms)-1)]:
            if Chem.rdchem.HybridizationType.SP2 in atom_types and Chem.rdchem.HybridizationType.SP2 in atom_types:
                return True, "Molecule is a caprolactam"

    return False, "Molecule is not a caprolactam"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:23000',
                          'name': 'caprolactams',
                          'definition': 'A lactam in which the amide bond is '
                                        'contained within a seven-membered '
                                        'ring, which includes the amide '
                                        'nitrogen and the carbonyl carbon.',
                          'parents': ['CHEBI:24995']},
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
    'num_false_positives': 100,
    'num_true_negatives': 69084,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9985401459854014}