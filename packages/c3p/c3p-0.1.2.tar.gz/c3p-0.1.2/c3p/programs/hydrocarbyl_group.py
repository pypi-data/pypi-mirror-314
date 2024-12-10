"""
Classifies: CHEBI:33248 hydrocarbyl group
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors


def is_hydrocarbyl_group(smiles: str):
    """
    Determines if a molecule is a hydrocarbyl group (a univalent group formed by removing a hydrogen atom
    from a hydrocarbon).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a hydrocarbyl group, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule contains only C and H atoms
    atoms = mol.GetAtoms()
    if not all(atom.GetSymbol() in ['C', 'H'] for atom in atoms):
        return False, "Molecule contains atoms other than C and H"

    # Check if there is only one radical site (*)
    radical_sites = [atom.GetNumRadicalElectrons() for atom in atoms]
    if sum(radical_sites) != 1:
        return False, "Molecule does not have exactly one radical site"

    # Check if the molecule is acyclic
    rings = mol.GetRingInfo()
    if rings.NumRings() > 0:
        return False, "Molecule contains rings"

    # Check if the molecule is a hydrocarbon
    hydrogen_deficit = rdMolDescriptors.CalcHydrogenDeficitBondsNumber(mol)
    if hydrogen_deficit > 0:
        return False, "Molecule contains unsaturated bonds or rings"

    return True, "Molecule is a hydrocarbyl group"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33248',
                          'name': 'hydrocarbyl group',
                          'definition': 'A univalent group formed by removing '
                                        'a hydrogen atom from a hydrocarbon.',
                          'parents': ['CHEBI:33249']},
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
    'error': "module 'rdkit.Chem.rdMolDescriptors' has no attribute "
             "'CalcHydrogenDeficitBondsNumber'",
    'stdout': '',
    'num_true_positives': 0,
    'num_false_positives': 0,
    'num_true_negatives': 0,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0,
    'f1': 0,
    'accuracy': None}