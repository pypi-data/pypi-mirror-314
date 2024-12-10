"""
Classifies: CHEBI:27267 valine derivative
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Fragments import fr_val

def is_valine_derivative(smiles: str):
    """
    Determines if a molecule is a valine derivative.

    A valine derivative is defined as an amino acid derivative resulting from reaction
    of valine at the amino group or the carboxy group, or from the replacement of any
    hydrogen of valine by a heteroatom. The definition normally excludes peptides
    containing valine residues.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a valine derivative, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule contains a valine substructure
    valine_pattern = Chem.MolFromSmarts('C(C(C)C)[C@H](C(=O)O)N')
    if mol.HasSubstructMatch(valine_pattern):
        # Check for modifications to the amino or carboxy groups
        modified_amino_group = False
        modified_carboxy_group = False
        for atom in mol.GetAtoms():
            if atom.GetSymbol() == 'N' and atom.GetDegree() > 3:
                modified_amino_group = True
            elif atom.GetSymbol() == 'O' and atom.GetDegree() > 1:
                modified_carboxy_group = True

        if modified_amino_group or modified_carboxy_group:
            modification_details = []
            if modified_amino_group:
                modification_details.append("amino group modified")
            if modified_carboxy_group:
                modification_details.append("carboxy group modified")
            return True, "Valine derivative with " + ", ".join(modification_details)
        else:
            return False, "Unmodified valine"

    # Check for hydrogen replacements with heteroatoms
    hydrogen_replacement = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() != 'C' and atom.GetSymbol() != 'H' and atom.GetSymbol() != 'O' and atom.GetSymbol() != 'N':
            hydrogen_replacement = True
            break

    if hydrogen_replacement:
        return True, "Valine derivative with hydrogen replacement by heteroatom"

    # Check for peptides containing valine residues
    valine_residue_pattern = Chem.MolFromSmarts('C(C(C)C)[C@H](C(=O)N)')
    if mol.HasSubstructMatch(valine_residue_pattern):
        return False, "Peptide containing valine residue"

    return False, "Not a valine derivative"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:27267',
                          'name': 'valine derivative',
                          'definition': 'An amino acid derivative resulting '
                                        'from reaction of valine at the amino '
                                        'group or the carboxy group, or from '
                                        'the replacement of any hydrogen of '
                                        'valine  by a heteroatom. The '
                                        'definition normally excludes peptides '
                                        'containing valine  residues.',
                          'parents': ['CHEBI:83821']},
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
    'error': "cannot import name 'fr_val' from 'rdkit.Chem.Fragments' "
             '(/Users/cjm/Library/Caches/pypoetry/virtualenvs/c3p-93U7KWO_-py3.11/lib/python3.11/site-packages/rdkit/Chem/Fragments.py)',
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