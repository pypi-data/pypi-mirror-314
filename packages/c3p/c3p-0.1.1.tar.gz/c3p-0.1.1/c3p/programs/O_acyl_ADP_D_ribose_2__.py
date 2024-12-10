"""
Classifies: CHEBI:138087 O-acyl-ADP-D-ribose(2-)
"""
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors
from rdkit.Chem.rdqueries import AtomNumEqualsQueryAtom, BondBetweenAtomQuery, DescriptorQuery

def is_O_acyl_ADP_D_ribose_2__(smiles: str):
    """
    Determines if a molecule is an O-acyl-ADP-D-ribose(2-).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an O-acyl-ADP-D-ribose(2-), False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check for two deprotonated phosphate groups
    deprotonated_phosphates = sum(atom.GetFormalCharge() == -1 and atom.GetSymbol() == 'O'
                                  for atom in mol.GetAtoms())
    if deprotonated_phosphates != 2:
        return False, "Does not contain two deprotonated phosphate groups"

    # Check for ADP-D-ribose substructure
    adp_ribose_query = Chem.MolFromSmarts('C1OC(COP(=O)(O)[O-])C(O)C1COP(=O)(O)[O-]')
    if not mol.HasSubstructMatch(adp_ribose_query):
        return False, "Does not contain ADP-D-ribose substructure"

    # Check for acyl group
    acyl_query = BondBetweenAtomQuery(DescriptorQuery('Atom.IsCarboxyl'), DescriptorQuery('Atom.IsOxygen'))
    if not mol.HasSubstructMatch(acyl_query):
        return False, "Does not contain an acyl group"

    return True, "Molecule is an O-acyl-ADP-D-ribose(2-)"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:138087',
                          'name': 'O-acyl-ADP-D-ribose(2-)',
                          'definition': 'A nucleotide-sugar oxoanion obtained '
                                        'by deprotonation of the phosphate OH '
                                        'groups of any O-acyl-ADP-D-ribose; '
                                        'major species at pH 7.3.',
                          'parents': ['CHEBI:59737']},
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
    'error': "cannot import name 'BondBetweenAtomQuery' from "
             "'rdkit.Chem.rdqueries' "
             '(/Users/cjm/Library/Caches/pypoetry/virtualenvs/c3p-93U7KWO_-py3.11/lib/python3.11/site-packages/rdkit/Chem/rdqueries.so)',
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