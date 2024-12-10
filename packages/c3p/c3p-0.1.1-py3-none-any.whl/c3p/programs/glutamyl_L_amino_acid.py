"""
Classifies: CHEBI:24323 glutamyl-L-amino acid
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_glutamyl_L_amino_acid(smiles: str):
    """
    Determines if a molecule is a glutamyl-L-amino acid, i.e., a dipeptide in which one of the amino acid residues is glutamine.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a glutamyl-L-amino acid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Check if the molecule contains a glutamine residue
    has_glutamine = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'N' and atom.GetTotalNumHs() == 2:
            has_glutamine = True
            break

    if not has_glutamine:
        return False, "No glutamine residue found"

    # Check if the molecule contains another amino acid residue
    has_amino_acid = False
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'N' and atom.GetTotalNumHs() == 2 and atom.GetDegree() == 3:
            has_amino_acid = True
            break

    if not has_amino_acid:
        return False, "No other amino acid residue found"

    # Check if the glutamine and amino acid residues are connected by a peptide bond
    peptide_bond = False
    for bond in mol.GetBonds():
        if bond.GetBondType() == Chem.BondType.AMIDE:
            atoms = [mol.GetAtomWithIdx(bond.GetBeginAtomIdx()), mol.GetAtomWithIdx(bond.GetEndAtomIdx())]
            if any(atom.GetSymbol() == 'N' and atom.GetTotalNumHs() == 2 for atom in atoms):
                peptide_bond = True
                break

    if not peptide_bond:
        return False, "No peptide bond found between glutamine and amino acid residues"

    # Check if the amino acid residue is L-configured
    l_configured = False
    for atom in mol.GetAtoms():
        if atom.GetChiralTag() == Chem.ChiralType.CHI_TETRAHEDRAL_CW:
            l_configured = True
            break

    if not l_configured:
        return False, "Amino acid residue is not L-configured"

    return True, "Molecule is a glutamyl-L-amino acid"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24323',
                          'name': 'glutamyl-L-amino acid',
                          'definition': 'A dipeptide in which one of the amino '
                                        'acid residues is glutamine.',
                          'parents': ['CHEBI:46761']},
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
    'num_false_positives': 0,
    'num_true_negatives': 183924,
    'num_false_negatives': 1,
    'num_negatives': None,
    'precision': 0.0,
    'recall': 0.0,
    'f1': 0,
    'accuracy': 0.9999945630012234}