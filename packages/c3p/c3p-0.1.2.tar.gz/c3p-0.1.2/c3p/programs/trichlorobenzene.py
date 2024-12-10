"""
Classifies: CHEBI:27096 trichlorobenzene
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_trichlorobenzene(smiles: str):
    """
    Determines if a molecule is a trichlorobenzene (any member of the class of chlorobenzenes carrying three chloro substituents at unspecified positions).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a trichlorobenzene, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule contains a benzene ring
    aromatic_rings = [ring for ring in mol.GetRingInfo().AtomRings() if all(mol.GetAtomWithIdx(idx).GetIsAromatic() for idx in ring) and len(ring) == 6]
    if not aromatic_rings:
        return False, "No aromatic 6-membered rings found"

    # Check if the benzene ring contains exactly 3 chlorine atoms
    for ring in aromatic_rings:
        atoms = [mol.GetAtomWithIdx(idx) for idx in ring]
        chlorine_count = sum(1 for atom in atoms if atom.GetSymbol() == 'Cl')
        if chlorine_count == 3:
            return True, "Trichlorobenzene found"

    return False, "No trichlorobenzene substructure found"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:27096',
                          'name': 'trichlorobenzene',
                          'definition': 'Any member of the class of '
                                        'chlorobenzenes carrying three chloro '
                                        'substituents at unspecified '
                                        'positions.',
                          'parents': ['CHEBI:23132']},
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
    'num_true_negatives': 183881,
    'num_false_negatives': 5,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999728092405077}