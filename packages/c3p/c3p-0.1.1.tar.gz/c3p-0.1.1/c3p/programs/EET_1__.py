"""
Classifies: CHEBI:131865 EET(1-)
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_EET_1__(smiles: str):
    """
    Determines if a molecule is an EET(1-) anion, which is an icosanoid anion obtained by the deprotonation of the carboxy group of any epoxyicosatrienoic acid.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an EET(1-) anion, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for exactly 20 carbon atoms
    if Descriptors.NumDescriptors[mol] != 20:
        return False, "Molecule does not contain 20 carbon atoms"

    # Check for exactly 3 double bonds
    if Descriptors.NumHDoubleAcceptors(mol) != 3:
        return False, "Molecule does not contain 3 double bonds"

    # Check for exactly 1 epoxide ring
    rings = mol.GetRingInfo().AtomRings()
    epoxide_rings = [ring for ring in rings if len(ring) == 3 and sum(mol.GetAtomWithIdx(idx).GetAtomicNum() == 8 for idx in ring) == 1]
    if len(epoxide_rings) != 1:
        return False, "Molecule does not contain exactly 1 epoxide ring"

    # Check for exactly 1 carboxylate anion
    carboxylate_anions = [atom for atom in mol.GetAtoms() if atom.GetFormalCharge() == -1 and atom.GetSymbol() == 'O' and atom.GetTotalNumHs() == 1]
    if len(carboxylate_anions) != 1:
        return False, "Molecule does not contain exactly 1 carboxylate anion"

    return True, "Molecule is an EET(1-) anion"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:131865',
                          'name': 'EET(1-)',
                          'definition': 'An icosanoid anion obtained by the '
                                        'deprotonation of the carboxy group of '
                                        'any epoxyicosatrienoic acid.',
                          'parents': [   'CHEBI:190711',
                                         'CHEBI:57560',
                                         'CHEBI:62937']},
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
    'success': False,
    'best': True,
    'error': "module 'rdkit.Chem.Descriptors' has no attribute "
             "'NumDescriptors'",
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