"""
Classifies: CHEBI:17950 beta-D-galactosyl-(1->4)-beta-D-glucosyl-(1<->1)-N-acylsphingosine
"""
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def is_beta_D_galactosyl__1__4__beta_D_glucosyl__1___1__N_acylsphingosine(smiles: str):
    """
    Determines if a molecule is a beta-D-galactosyl-(1->4)-beta-D-glucosyl-(1<->1)-N-acylsphingosine,
    which is a diosylceramide having beta-D-galactosyl-(1->4)-beta-D-glucose as the disaccharide component.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a beta-D-galactosyl-(1->4)-beta-D-glucosyl-(1<->1)-N-acylsphingosine, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Find the amide nitrogen atom
    amide_n = None
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'N' and atom.GetTotalNumHs() == 0:
            amide_n = atom
            break
    if amide_n is None:
        return False, "No amide nitrogen found"

    # Check the acyl chain
    acyl_atoms = [amide_n] + list(amide_n.GetNeighbors())
    acyl_chain = Chem.Mol(Chem.PathToSubmol(mol, [a.GetIdx() for a in acyl_atoms]))
    if not is_acyl_chain(acyl_chain):
        return False, "Acyl chain is not long enough or contains unsaturated bonds"

    # Check the sphingosine base
    sphingosine_atoms = [atom for atom in mol.GetAtoms() if atom not in acyl_atoms]
    sphingosine = Chem.Mol(Chem.PathToSubmol(mol, [a.GetIdx() for a in sphingosine_atoms]))
    if not is_sphingosine_base(sphingosine):
        return False, "Sphingosine base is not valid"

    # Check the disaccharide component
    disaccharide = find_disaccharide(sphingosine)
    if disaccharide is None:
        return False, "No valid disaccharide component found"
    if not is_beta_D_galactosyl__1__4__beta_D_glucosyl(disaccharide):
        return False, "Disaccharide component is not beta-D-galactosyl-(1->4)-beta-D-glucosyl"

    return True, "The molecule is a valid beta-D-galactosyl-(1->4)-beta-D-glucosyl-(1<->1)-N-acylsphingosine"

def is_acyl_chain(mol):
    """Checks if the given molecule is a valid acyl chain."""
    # Check if the molecule contains only C and H atoms
    if not all(atom.GetSymbol() in ['C', 'H'] for atom in mol.GetAtoms()):
        return False

    # Check if the chain is linear and fully saturated
    conf = mol.GetConformer()
    for bond in mol.GetBonds():
        if bond.GetBondType() != Chem.BondType.SINGLE:
            return False
        begin = conf.GetAtomPosition(bond.GetBeginAtomIdx())
        end = conf.GetAtomPosition(bond.GetEndAtomIdx())
        if not is_linear(begin, end):
            return False

    return True

def is_linear(p1, p2, tol=0.01):
    """Checks if two points are approximately linear."""
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    dz = p2.z - p1.z
    return abs(dx) < tol or abs(dy) < tol or abs(dz) < tol

def is_sphingosine_base(mol):
    """Checks if the given molecule is a valid sphingosine base."""
    # TODO: Implement this function
    return True

def find_disaccharide(mol):
    """Finds the disaccharide component in the given molecule."""
    # TODO: Implement this function
    return None

def is_beta_D_galactosyl__1__4__beta_D_glucosyl(mol):
    """Checks if the given molecule is beta-D-galactosyl-(1->4)-beta-D-glucosyl."""
    # TODO: Implement this function
    return True


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:17950',
                          'name': 'beta-D-galactosyl-(1->4)-beta-D-glucosyl-(1<->1)-N-acylsphingosine',
                          'definition': 'A diosylceramide having '
                                        'beta-D-galactosyl-(1->4)-beta-D-glucose '
                                        'as the disaccharide component.',
                          'parents': ['CHEBI:63415', 'CHEBI:79208']},
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
    'error': 'Range Error\n'
             '\tidx\n'
             '\tViolation occurred on line 329 in file '
             'Code/GraphMol/ROMol.cpp\n'
             '\tFailed Expression: 58 < 58\n'
             '\tRDKIT: 2024.03.6\n'
             '\tBOOST: 1_85\n',
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