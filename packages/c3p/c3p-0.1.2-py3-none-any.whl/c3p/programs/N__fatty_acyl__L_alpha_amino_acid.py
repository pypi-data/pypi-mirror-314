"""
Classifies: CHEBI:137550 N-(fatty acyl)-L-alpha-amino acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors

def is_N__fatty_acyl__L_alpha_amino_acid(smiles: str):
    """
    Determines if a molecule is an N-(fatty acyl)-L-alpha-amino acid.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an N-(fatty acyl)-L-alpha-amino acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule contains a carboxylic acid group
    carboxyl_present = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'O' and atom.GetFormalCharge() == -1:
            carboxyl_present = True
            break

    if not carboxyl_present:
        return False, "No carboxylic acid group found"

    # Check if the molecule contains an amide group
    amide_present = False
    for bond in mol.GetBonds():
        if bond.GetBondType() == Chem.BondType.AMIDE:
            amide_present = True
            break

    if not amide_present:
        return False, "No amide group found"

    # Check if the molecule contains a fatty acid chain
    fatty_acid_chain = False
    chain_length = 0
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'C' and atom.GetDegree() == 2:
            chain_length += 1
        else:
            if chain_length >= 6:
                fatty_acid_chain = True
                break
            chain_length = 0

    if not fatty_acid_chain:
        return False, "No fatty acid chain found"

    # Check if the molecule contains an L-alpha-amino acid
    l_alpha_amino_acid = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'N' and atom.GetDegree() == 3:
            neighbors = [mol.GetAtomWithIdx(n).GetSymbol() for n in atom.GetNeighbors()]
            if 'C' in neighbors and 'H' in neighbors:
                for neighbor in atom.GetNeighbors():
                    if mol.GetAtomWithIdx(neighbor).GetSymbol() == 'C':
                        chiral_tag = mol.GetAtomWithIdx(neighbor).GetChiralTag()
                        if chiral_tag == Chem.ChiralType.CHI_TETRAHEDRAL_CW:
                            l_alpha_amino_acid = True
                            break

    if not l_alpha_amino_acid:
        return False, "No L-alpha-amino acid found"

    return True, "This molecule is an N-(fatty acyl)-L-alpha-amino acid"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:137550',
                          'name': 'N-(fatty acyl)-L-alpha-amino acid',
                          'definition': 'An N-acyl-L-alpha-amino acid '
                                        'resulting from the formal '
                                        'condensation of the carboxy group of '
                                        'any fatty acid with the amino group '
                                        'of any L-amino acid.',
                          'parents': ['CHEBI:29348', 'CHEBI:48927']},
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
    'error': "type object 'BondType' has no attribute 'AMIDE'",
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