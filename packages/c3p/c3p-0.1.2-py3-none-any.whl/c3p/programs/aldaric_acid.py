"""
Classifies: CHEBI:22290 aldaric acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_aldaric_acid(smiles: str):
    """
    Determines if a molecule is an aldaric acid.
    Aldaric acids are dicarboxylic acids formed from aldoses by replacement
    of both terminal groups (CHO and CH2OH) by carboxy groups.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an aldaric acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Count the number of carboxylic acid groups (-C(=O)O-) in the molecule
    carboxyl_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'O' and atom.GetFormalCharge() == 0 and sum(mol.GetAtomWithIdx(n.GetIdx()).GetFormalCharge() for n in atom.GetNeighbors()) == 0)

    # Aldaric acids should have exactly two carboxylic acid groups
    if carboxyl_count != 2:
        return False, f"Molecule does not have exactly two carboxylic acid groups (found {carboxyl_count})"

    # Count the number of alcohol groups (-OH) in the molecule
    alcohol_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == 'O' and atom.GetFormalCharge() == 0 and sum(mol.GetAtomWithIdx(n.GetIdx()).GetFormalCharge() for n in atom.GetNeighbors()) == 0 and len(atom.GetNeighbors()) == 1)

    # Aldaric acids should not have any alcohol groups
    if alcohol_count > 0:
        return False, "Molecule contains alcohol groups"

    # Aldaric acids should be acyclic
    if any(len(ring) > 0 for ring in mol.GetRingInfo().AtomRings()):
        return False, "Molecule contains rings"

    return True, "Molecule is an aldaric acid"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:22290',
                          'name': 'aldaric acid',
                          'definition': 'Dicarboxylic acids formed from '
                                        'aldoses by replacement of both '
                                        'terminal groups (CHO and CH2OH) by '
                                        'carboxy groups.',
                          'parents': ['CHEBI:33720', 'CHEBI:35692']},
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
    'num_false_positives': 71,
    'num_true_negatives': 183848,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.999608525445846}