"""
Classifies: CHEBI:172368 brominated flame retardant
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors

def is_brominated_flame_retardant(smiles: str):
    """
    Determines if a molecule is a brominated flame retardant.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a brominated flame retardant, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule contains bromine
    if 'Br' not in Chem.MolToSmiles(mol):
        return False, "Molecule does not contain bromine"

    # Check for presence of aromatic rings
    rings = mol.GetRingInfo().AtomRings()
    aromatic_rings = [ring for ring in rings if all(mol.GetAtomWithIdx(idx).GetIsAromatic() for idx in ring)]

    # Check if the molecule has an aromatic ring and a bromine substituent
    has_bromine_substituent = False
    for ring in aromatic_rings:
        for idx in ring:
            atom = mol.GetAtomWithIdx(idx)
            for neighbor in atom.GetNeighbors():
                if neighbor.GetSymbol() == 'Br' and neighbor.GetIdx() not in ring:
                    has_bromine_substituent = True
                    break

    if has_bromine_substituent:
        return True, "Molecule is a brominated flame retardant"
    else:
        return False, "Molecule does not meet the criteria for a brominated flame retardant"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:172368',
                          'name': 'brominated flame retardant',
                          'definition': 'Any organobromine compound that is '
                                        'used as a flame retardant. These '
                                        'chemicals are widely incorporated as '
                                        'additives in consumer products such '
                                        'as electronics, vehicles, '
                                        'polyurethane foams etc, to make them '
                                        'less flammable.',
                          'parents': ['CHEBI:37141']},
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
    'num_true_positives': 1,
    'num_false_positives': 100,
    'num_true_negatives': 13089,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.009900990099009901,
    'recall': 1.0,
    'f1': 0.0196078431372549,
    'accuracy': 0.9924184988627748}