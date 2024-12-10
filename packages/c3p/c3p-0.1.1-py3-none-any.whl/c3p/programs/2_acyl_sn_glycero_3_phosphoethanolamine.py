"""
Classifies: CHEBI:28936 2-acyl-sn-glycero-3-phosphoethanolamine
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_2_acyl_sn_glycero_3_phosphoethanolamine(smiles: str):
    """
    Determines if a molecule is a 2-acyl-sn-glycero-3-phosphoethanolamine.

    A 2-acyl-sn-glycero-3-phosphoethanolamine is a lysophosphatidylethanolamine
    obtained by selective hydrolysis of the 1-acyl substituent of any 1,2-diacyl-sn-glycero-3-phosphoethanolamine.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a 2-acyl-sn-glycero-3-phosphoethanolamine, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find all phosphorus atoms
    phosphorus_atoms = [atom.GetIdx() for atom in mol.GetAtoms() if atom.GetSymbol() == 'P']

    if len(phosphorus_atoms) != 1:
        return False, "The molecule does not contain exactly one phosphorus atom"

    p_atom_idx = phosphorus_atoms[0]
    p_atom = mol.GetAtomWithIdx(p_atom_idx)

    # Check if the phosphorus atom has four neighbors
    if p_atom.GetDegree() != 4:
        return False, "The phosphorus atom does not have four neighbors"

    # Check if one neighbor is a doubly bonded oxygen (phosphate group)
    has_phosphate_group = False
    for neighbor_idx in p_atom.GetNeighbors():
        neighbor_atom = mol.GetAtomWithIdx(neighbor_idx)
        if neighbor_atom.GetSymbol() == 'O' and mol.GetBondBetweenAtoms(p_atom_idx, neighbor_idx).GetBondType() == Chem.BondType.DOUBLE:
            has_phosphate_group = True
            break

    if not has_phosphate_group:
        return False, "The molecule does not have a phosphate group"

    # Check if one neighbor is an ethanolamine group
    has_ethanolamine_group = False
    for neighbor_idx in p_atom.GetNeighbors():
        neighbor_atom = mol.GetAtomWithIdx(neighbor_idx)
        if neighbor_atom.GetSymbol() == 'O':
            # Follow the chain to find an ethanolamine group
            chain = Chem.FindAllPathsOfLengthN(mol, neighbor_idx, 3)
            if chain:
                chain_atoms = [mol.GetAtomWithIdx(atom_idx) for atom_idx in chain[0]]
                if all(atom.GetSymbol() in ['C', 'N'] for atom in chain_atoms):
                    has_ethanolamine_group = True
                    break

    if not has_ethanolamine_group:
        return False, "The molecule does not have an ethanolamine group"

    # Check if one neighbor is a glycerol group
    has_glycerol_group = False
    for neighbor_idx in p_atom.GetNeighbors():
        neighbor_atom = mol.GetAtomWithIdx(neighbor_idx)
        if neighbor_atom.GetSymbol() == 'O':
            # Follow the chain to find a glycerol group
            chain = Chem.FindAllPathsOfLengthN(mol, neighbor_idx, 3)
            if chain:
                chain_atoms = [mol.GetAtomWithIdx(atom_idx) for atom_idx in chain[0]]
                if all(atom.GetSymbol() in ['C', 'O'] for atom in chain_atoms):
                    has_glycerol_group = True
                    break

    if not has_glycerol_group:
        return False, "The molecule does not have a glycerol group"

    # Check if the remaining neighbor is an acyl group
    has_acyl_group = False
    for neighbor_idx in p_atom.GetNeighbors():
        neighbor_atom = mol.GetAtomWithIdx(neighbor_idx)
        if neighbor_atom.GetSymbol() == 'C':
            has_acyl_group = True
            break

    if not has_acyl_group:
        return False, "The molecule does not have an acyl group"

    return True, "The molecule is a 2-acyl-sn-glycero-3-phosphoethanolamine"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:28936',
                          'name': '2-acyl-sn-glycero-3-phosphoethanolamine',
                          'definition': 'A lysophosphatidylethanolamine '
                                        'obtained by selective hydrolysis of '
                                        'the 1-acyl substituent of any '
                                        '1,2-diacyl-sn-glycero-3-phosphoethanolamine.',
                          'parents': ['CHEBI:64574']},
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
    'error': 'Python argument types in\n'
             '    Mol.GetAtomWithIdx(Mol, Atom)\n'
             'did not match C++ signature:\n'
             '    GetAtomWithIdx(RDKit::ROMol {lvalue} self, unsigned int idx)',
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