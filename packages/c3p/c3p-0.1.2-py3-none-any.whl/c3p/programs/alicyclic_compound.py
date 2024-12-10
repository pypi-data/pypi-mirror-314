"""
Classifies: CHEBI:33654 alicyclic compound
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_alicyclic_compound(smiles: str):
    """
    Determines if a molecule is an alicyclic compound.

    Alicyclic compounds are defined as aliphatic compounds having a carbocyclic ring structure
    which may be saturated or unsaturated, but may not be a benzenoid or other aromatic system.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is an alicyclic compound, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for carbocyclic rings
    ring_info = mol.GetRingInfo()
    carbocyclic_rings = [ring for ring in ring_info.AtomRings() if all(mol.GetAtomWithIdx(atom_idx).GetSymbol() == 'C' for atom_idx in ring)]
    if not carbocyclic_rings:
        return False, "No carbocyclic rings found"

    # Check for aromaticity
    aromatic_rings = [ring for ring in ring_info.AtomRings() if all(mol.GetAtomWithIdx(atom_idx).GetIsAromatic() for atom_idx in ring)]
    if aromatic_rings:
        return False, "Molecule contains aromatic rings"

    # Check for aliphatic substituents
    aliphatic_substituents = []
    for ring in carbocyclic_rings:
        ring_atoms = set(ring)
        for atom_idx in ring_atoms:
            atom = mol.GetAtomWithIdx(atom_idx)
            for neighbor in atom.GetNeighbors():
                if neighbor.GetIdx() not in ring_atoms:
                    aliphatic_substituents.append(neighbor.GetSymbol())

    if aliphatic_substituents:
        return True, f"Alicyclic compound with aliphatic substituents: {', '.join(set(aliphatic_substituents))}"
    else:
        return True, "Unsubstituted alicyclic compound"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33654',
                          'name': 'alicyclic compound',
                          'definition': 'An aliphatic compound having a '
                                        'carbocyclic ring structure which may '
                                        'be saturated or unsaturated, but may '
                                        'not be a benzenoid or other aromatic '
                                        'system.',
                          'parents': ['CHEBI:33598', 'CHEBI:33653']},
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
    'num_true_positives': 26,
    'num_false_positives': 100,
    'num_true_negatives': 720,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.20634920634920634,
    'recall': 0.9629629629629629,
    'f1': 0.3398692810457516,
    'accuracy': 0.8807556080283353}