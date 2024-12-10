"""
Classifies: CHEBI:17593 maltooligosaccharide
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import MolFromSmiles, MolToSmiles

def is_maltooligosaccharide(smiles: str):
    """
    Determines if a molecule is a maltooligosaccharide.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a maltooligosaccharide, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule is a saccharide
    if not Chem.MolToSmiles(mol).endswith("C1C(C(C(C(O1)O)O)O)O"):
        return False, "Not a saccharide"

    # Check if the molecule contains only glucose units
    glucose_smiles = "OC[C@H]1O[C@H](O)[C@@H](O)[C@H](O)[C@@H]1O"
    glucose_mol = Chem.MolFromSmiles(glucose_smiles)
    fragments = Chem.GetMolFrags(mol)
    for frag in fragments:
        frag_mol = Chem.MolFragmentToSmiles(mol, frag)
        if frag_mol != glucose_smiles:
            return False, "Contains non-glucose units"

    # Check if the glucose units are linked via alpha-D-1,4 bonds
    bonds = mol.GetBonds()
    for bond in bonds:
        if bond.GetBondType() == Chem.BondType.SINGLE:
            begin_atom = mol.GetAtomWithIdx(bond.GetBeginAtomIdx())
            end_atom = mol.GetAtomWithIdx(bond.GetEndAtomIdx())
            if begin_atom.GetSymbol() == "O" and end_atom.GetSymbol() == "C":
                begin_atom_env = Chem.FindAtomEnvironmentOfRadiusN(mol, begin_atom.GetIdx(), 3)
                end_atom_env = Chem.FindAtomEnvironmentOfRadiusN(mol, end_atom.GetIdx(), 3)
                if not (begin_atom_env.startswith("O1CC") and end_atom_env.startswith("C1OC")):
                    return False, "Glucose units not linked via alpha-D-1,4 bonds"

    # If all checks pass, the molecule is a maltooligosaccharide
    return True, "Maltooligosaccharide"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:17593',
                          'name': 'maltooligosaccharide',
                          'definition': 'A glucooligosaccharide derived from '
                                        'glucose monomers linked via '
                                        'alpha-D-1,4 bonds as in maltose.  The '
                                        'term is commonly applied to the '
                                        'series of linear oligosaccharides '
                                        'composed of two, three, four, five '
                                        'and six such units of glucose.',
                          'parents': ['CHEBI:24268']},
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
    'num_true_negatives': 183917,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0.0,
    'accuracy': 0.9999945627942888}