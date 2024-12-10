"""
Classifies: CHEBI:142118 imidazobenzodiazepine
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_imidazobenzodiazepine(smiles: str):
    """
    Determines if a molecule is an imidazobenzodiazepine.
    Imidazobenzodiazepines are defined as any organic heterotricyclic compound that is any
    benzodiazepine which is ortho-fused with an imidazole.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an imidazobenzodiazepine, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Generate the ring information
    rings = mol.GetRingInfo().AtomRings()

    # Check for at least three rings
    if len(rings) < 3:
        return False, "Not a heterotricyclic compound"

    # Check for benzodiazepine substructure
    benzodiazepine_pattern = Chem.MolFromSmarts("C1=C2N=CN=C2C(=C3C=CC=CC3=N1)C4=NCC=N4")
    if not mol.HasSubstructMatch(benzodiazepine_pattern):
        return False, "Not a benzodiazepine"

    # Check for imidazole substructure
    imidazole_pattern = Chem.MolFromSmarts("N1C=NC=N1")
    if not mol.HasSubstructMatch(imidazole_pattern):
        return False, "No imidazole substructure found"

    # Check if imidazole and benzodiazepine are fused
    for ring1 in rings:
        for ring2 in rings:
            if len(set(ring1) & set(ring2)) >= 2:
                atoms1 = [mol.GetAtomWithIdx(idx) for idx in ring1]
                atoms2 = [mol.GetAtomWithIdx(idx) for idx in ring2]
                if benzodiazepine_pattern.HasSubstructMatch(mol, atomsToUse=atoms1) and \
                   imidazole_pattern.HasSubstructMatch(mol, atomsToUse=atoms2):
                    return True, "Imidazobenzodiazepine"

    return False, "Not an imidazobenzodiazepine"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:142118',
                          'name': 'imidazobenzodiazepine',
                          'definition': 'Any organic heterotricyclic compound '
                                        'that is any benzodiazepine which is '
                                        'ortho-fused with a imidazole.',
                          'parents': ['CHEBI:22720', 'CHEBI:26979']},
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
    'num_false_positives': 0,
    'num_true_negatives': 183925,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999945630307842}