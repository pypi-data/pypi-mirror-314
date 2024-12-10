"""
Classifies: CHEBI:24335 glutathione conjugate
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_glutathione_conjugate(smiles: str):
    """
    Determines if a molecule is a glutathione conjugate.

    A glutathione conjugate is defined as any bioconjugate in which glutathione is one of the components.

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if the molecule is a glutathione conjugate, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Define the SMARTS pattern for glutathione
    glutathione_pattern = Chem.MolFromSmarts('C(N)C(=O)NCC(=O)O')

    # Check if glutathione is present as a substructure
    match = mol.GetSubstructMatches(glutathione_pattern)
    if match:
        return True, "Molecule is a glutathione conjugate"

    # Check for common glutathione conjugation sites
    for atom in mol.GetAtoms():
        if atom.GetSymbol() == 'S' and atom.GetDegree() == 2:
            neighbor1 = atom.GetNeighbors()[0]
            neighbor2 = atom.GetNeighbors()[1]
            if neighbor1.GetSymbol() == 'C' and neighbor2.GetSymbol() == 'C':
                if neighbor1.GetDegree() == 3 and neighbor2.GetDegree() == 3:
                    if any(neighbor.GetSmarts() == '[NX3H2]' for neighbor in neighbor1.GetNeighbors()) and \
                       any(neighbor.GetSmarts() == '[CX3](=O)[NX3H2]' for neighbor in neighbor2.GetNeighbors()):
                        return True, "Molecule is a glutathione conjugate"

    return False, "Molecule is not a glutathione conjugate"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:24335',
                          'name': 'glutathione conjugate',
                          'definition': 'Any bioconjugate in which glutathione '
                                        'is one of the components',
                          'parents': ['CHEBI:24337', 'CHEBI:64985']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0 is too low.\n'
               'True positives: []\n'
               'False positives: '
               "[('BrC1=C(O)C(Br)=CC(=C1)/C=C/C=C/C=C/C=C/C=C/C(=O)N[C@@H]2C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(N[C@H](C(O[C@@H]2C)=O)[C@@H](CC)C)=O)CC(=O)N)CC(=O)N)C(C)C', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@@H](CC=1C=2C(NC1)=CC=CC2)C(O)=O)[C@@H](NC(=O)[C@@H](N)CCCCN)CC(=O)N', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@@H](CC(=O)N)C(=O)N[C@@H](CCC(=O)N)C(O)=O)[C@@H](N)CC=1C=2C(NC1)=CC=CC2', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@@H](CCCCN)C(O)=O)[C@@H](NC(=O)[C@@H](N)[C@H](O)C)CC(=O)N', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(NCC(O)=O)[C@@H](NC(=O)CN)CC(=O)N', 'Molecule is a "
               "glutathione conjugate'), "
               "('BrC1=C(O)C=CC(=C1)/C=C/C=C/C=C/C=C/C(=O)N[C@@H]2C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(N[C@H](C(O[C@@H]2C)=O)C(C)C)=O)CC(=O)N)CC(=O)N)C(C)C', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@@H](CCC(O)=O)C(O)=O)[C@@H](NC(=O)[C@@H](N)C)CC(=O)N', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C1O[C@@H]([C@H](NC(=O)CC(O)CCCCCCCCCCCCCCN=C(N)N)C(=O)N[C@@H](C(=O)N[C@@H]([C@H](CC)C)C(N[C@@H](C(N[C@@H](C(N[C@@H]1C)=O)CC(=O)N)=O)[C@H](O)C)=O)CC(C)C)C', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@@H](CC(=O)N)C(=O)N[C@@H](CC1=CC=CC=C1)C(O)=O)[C@@H](N)C(C)C', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@@H](CC(=O)N)C(=O)NCC(O)=O)[C@@H](N)[C@H](CC)C', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@@H](CO)C(O)=O)[C@@H](NC(=O)CN)CC(=O)N', 'Molecule is "
               "a glutathione conjugate'), "
               "('O=C1OC[C@@H](NC(=O)C[C@H](O)[C@@H](N)CCCCNC(=O)C2=C(O)C(O)=CC=C2)C(=O)N[C@@H](CCCN(O)C=O)C(N[C@@H](C(N[C@H]1CCCN(O)C=O)=O)CC(=O)N)=O', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@@H](CC(=O)N)C(=O)NCC(O)=O)[C@@H](N)C(C)C', 'Molecule "
               "is a glutathione conjugate'), "
               "('O=C1O[C@@H]([C@H](NC(=O)CC(O)CCCCCCCCCCCCN=C(N)N)C(=O)N[C@@H](C(=O)N[C@@H]([C@H](CC)C)C(N[C@@H](C(N[C@@H](C(N[C@@H]1C)=O)CC(=O)N)=O)[C@H](O)C)=O)[C@@H](CC)C)C', "
               "'Molecule is a glutathione conjugate'), "
               "('S(CC[C@H](N)C(=O)N[C@@H](CC(=O)N)C(=O)N[C@@H]([C@H](O)C)C(O)=O)C', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@@H](CC=1C=2C(NC1)=CC=CC2)C(O)=O)[C@@H](NC(=O)[C@@H](N)CO)CC(=O)N', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@@H](CC(=O)N)C(=O)NCC(O)=O)[C@@H](N)CCC(=O)N', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@@H](CC(=O)N)C(=O)N[C@@H](CC(O)=O)C(O)=O)[C@@H](N)CCCCN', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@@H](CC=1C=2C(NC1)=CC=CC2)C(O)=O)[C@@H](NC(=O)[C@@H](N)CCC(=O)N)CC(=O)N', "
               "'Molecule is a glutathione conjugate'), "
               "('SC[C@H](NC(=O)[C@@H](NC(=O)[C@@H](N)CCCCN)CC(=O)N)C(O)=O', "
               "'Molecule is a glutathione conjugate'), "
               "('C([C@@H](N)CC=1C=CC=CC1)(=O)NCC(=O)NCC(=O)N[C@H](C(=O)N[C@H](C(=O)NCC(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(N[C@H](C(=O)N[C@H](C(N[C@H](C(N[C@H](C(=O)N[C@H](C(=O)N[C@H](C(=O)O)CCC(=O)N)CC(=O)N)C)=O)CC(C)C)=O)CCCCN)CCCNC(=N)N)=O)C)CO)CCCCN)CCCNC(=N)N)C)[C@@H](C)O)CC=2C=CC=CC2', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@@H](CC(=O)N)C(=O)NCC(O)=O)[C@@H](N)CC1=CC=C(O)C=C1', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@@H](CC(=O)N)C(=O)N[C@@H](CC1=CC=CC=C1)C(O)=O)[C@@H](N)CC=2C=3C(NC2)=CC=CC3', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@@H](CC(=O)N)C(=O)N[C@@H](CC(=O)N)C(O)=O)[C@@H](N)CC=1C=2C(NC1)=CC=CC2', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@@H](CC(=O)N)C(=O)N[C@@H](CC(=O)N)C(O)=O)[C@@H](N)CCCCN', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@@H](CC1=CC=C(O)C=C1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(O)=O)CC(=O)N', "
               "'Molecule is a glutathione conjugate'), "
               "('S(CC[C@H](NC(=O)[C@@H](NC(=O)[C@H]1NCCC1)CC(=O)N)C(O)=O)C', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@@H](CC(=O)N)C(=O)N[C@@H](C)C(O)=O)[C@@H](N)CCCN=C(N)N', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@@H](CC(=O)N)C(=O)NCC(O)=O)[C@@H](N)CCCCN', 'Molecule "
               "is a glutathione conjugate'), "
               "('SC[C@H](N)C(=O)N[C@H](C(=O)N[C@@H]([C@H](O)C)C(O)=O)CC(=O)N', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@@H](CCCCN)C(O)=O)[C@@H](NC(=O)[C@@H](N)CCCN=C(N)N)CC(=O)N', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@@H](CC(=O)N)C(=O)N[C@@H](CC1=CC=C(O)C=C1)C(O)=O)[C@H]2NCCC2', "
               "'Molecule is a glutathione conjugate'), "
               "('SC[C@H](N)C(=O)N[C@H](C(=O)N[C@@H](CCCCN)C(O)=O)CC(=O)N', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@@H](CC(C)C)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC=1C=2C(NC1)=CC=CC2)CC(=O)N', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@@H](CCCN=C(N)N)C(O)=O)[C@@H](NC(=O)[C@@H](N)CCC(O)=O)CC(=O)N', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@@H](CC(=O)N)C(O)=O)[C@@H](NC(=O)CN)CC(=O)N', "
               "'Molecule is a glutathione conjugate'), "
               "('S(CC[C@H](N)C(=O)N[C@@H](CC(=O)N)C(=O)N[C@@H](CC(=O)N)C(O)=O)C', "
               "'Molecule is a glutathione conjugate'), "
               "('CSCC[C@H](NC(=O)[C@H](CC(C)C)NC(=O)[C@H](Cc1c[nH]c2ccccc12)NC(=O)[C@H](CCC(N)=O)NC(=O)[C@@H](NC(=O)[C@H](Cc1ccccc1)NC(=O)[C@H](CC(O)=O)NC(=O)[C@H](CCC(N)=O)NC(=O)[C@H](C)NC(=O)[C@H](CCCNC(N)=N)NC(=O)[C@H](CCCNC(N)=N)NC(=O)[C@H](CO)NC(=O)[C@H](CC(O)=O)NC(=O)[C@H](CC(C)C)NC(=O)[C@H](Cc1ccc(O)cc1)NC(=O)[C@H](CCCCN)NC(=O)[C@H](CO)NC(=O)[C@H](Cc1ccc(O)cc1)NC(=O)[C@H](CC(O)=O)NC(=O)[C@H](CO)NC(=O)[C@@H](NC(=O)[C@H](Cc1ccccc1)NC(=O)[C@@H](NC(=O)CNC(=O)[C@H](CCC(N)=O)NC(=O)[C@H](CO)NC(=O)[C@@H](N)Cc1cnc[nH]1)[C@@H](C)O)[C@@H](C)O)C(C)C)C(=O)N[C@@H](CC(N)=O)C(=O)N[C@@H]([C@@H](C)O)C(O)=O', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@@H](CC(C)C)C(O)=O)[C@@H](NC(=O)CN)CC(=O)N', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N1[C@H](CCC1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CCCN=C(N)N)CC(=O)N', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@@H](CCCCN)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC1=CC=CC=C1)CC(=O)N', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@@H](CC(=O)N)C(=O)N[C@@H](CC1=CC=CC=C1)C(O)=O)[C@@H](N)[C@H](CC)C', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@@H](CC(C)C)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC=1NC=NC1)CC(=O)N', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@@H](CC(=O)N)C(=O)N[C@@H](CCC(=O)N)C(O)=O)[C@@H](N)CC(C)C', "
               "'Molecule is a glutathione conjugate'), "
               "('SC[C@H](N)C(=O)N[C@H](C(=O)N[C@@H](CCC(O)=O)C(O)=O)CC(=O)N', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@@H](CC(=O)N)C(=O)N[C@@H](CO)C(O)=O)[C@@H](N)[C@H](CC)C', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@@H](CC1=CC=C(O)C=C1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC2=CC=CC=C2)CC(=O)N', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@@H](CC(=O)N)C(=O)N[C@@H](CCC(O)=O)C(O)=O)[C@@H](N)CC(C)C', "
               "'Molecule is a glutathione conjugate'), "
               "('CC(C)[C@H](NC(=O)[C@@H](N)CC(N)=O)C(O)=O', 'Molecule is a "
               "glutathione conjugate'), "
               "('O=C(N[C@@H](CC(=O)N)C(O)=O)[C@@H](NC(=O)[C@@H](N)CO)CC(=O)N', "
               "'Molecule is a glutathione conjugate'), "
               "('N[C@@H](CC(N)=O)C(=O)N[C@@H](CC(N)=O)C(O)=O', 'Molecule is a "
               "glutathione conjugate'), "
               "('O=C1O[C@@H]([C@H](NC(=O)/C=C/C=C/C=C/C=C/C=C/C2=CC=C(O)C=C2)C(=O)N[C@H](C(=O)N[C@H](C(N[C@H](C(N[C@H]1C(C)C)=O)CC(=O)N)=O)CC(=O)N)C(C)C)C', "
               "'Molecule is a glutathione conjugate'), "
               "('N[C@@H](CC(N)=O)C(=O)N[C@@H](Cc1ccc(O)cc1)C(O)=O', 'Molecule "
               "is a glutathione conjugate'), "
               "('O=C(N[C@@H](CCCCN)C(O)=O)[C@@H](NC(=O)[C@@H](N)CCC(=O)N)CC(=O)N', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@@H]([C@H](CC)C)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC=1C=2C(NC1)=CC=CC2)CC(=O)N', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@H](C(=O)N[C@@H](C(C)C)C(O)=O)CC(=O)N)[C@@H](N)CC(C)C', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@@H](C(C)C)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(O)=O)CC(=O)N', "
               "'Molecule is a glutathione conjugate'), "
               "('S(CC[C@H](NC(=O)[C@@H](NC(=O)[C@@H](N)CC1=CC=C(O)C=C1)CC(=O)N)C(O)=O)C', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C1O[C@@H]([C@H](NC(=O)/C=C/C=C/C=C/C=C/C2=CC=C(O)C=C2)C(=O)N[C@H](C(=O)N[C@H](C(N[C@H](C(N[C@H]1CC(C)C)=O)CC(=O)N)=O)CC(=O)N)C(C)C)C', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@@H](CC(=O)N)C(=O)NCC(O)=O)[C@@H](N)CC(C)C', "
               "'Molecule is a glutathione conjugate'), "
               "('BrC1=C(O)C(Br)=CC(=C1)/C=C/C=C/C=C/C=C/C(=O)N[C@H]2C(=O)N[C@@H](C(=O)N[C@H](C(=O)N[C@@H](C(N[C@@H](C(O[C@@H]2C)=O)CC(C)C)=O)CC(=O)N)CC(=O)N)[C@H](CC)C', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(NCCCC[C@H](N)[C@@H](O)CC(=O)N[C@@H](C(=O)N[C@H](C(=O)N[C@@H](C(=O)N[C@H](C(=O)OC)CCCN(O)C=O)CC(=O)N)CCCN(O)C=O)CO)C1=C(O)C(O)=CC=C1', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@@H](CC1=CC=CC=C1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC2=CC=C(O)C=C2)CC(=O)N', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@@H](CC(C)C)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(=O)N)CC(=O)N', "
               "'Molecule is a glutathione conjugate'), "
               "('O[C@@H]([C@H](N)C(=O)N[C@@H](CC(=O)N)C(=O)N[C@@H](C)C(O)=O)C', "
               "'Molecule is a glutathione conjugate'), "
               "('S(CC[C@H](N)C(=O)N[C@@H](CC(=O)N)C(=O)N[C@@H](CC1=CC=CC=C1)C(O)=O)C', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N1[C@H](CCC1)C(O)=O)[C@@H](NC(=O)[C@@H](N)[C@H](O)C)CC(=O)N', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@@H](CC(=O)N)C(=O)N[C@@H](CCC(=O)N)C(O)=O)[C@H]1NCCC1', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C1O[C@@H]([C@H](NC(=O)CC(O)CCCCCCCCCCCCN=C(N)N)C(=O)N[C@@H](C(=O)N[C@@H](C(C)C)C(N[C@@H](C(N[C@@H](C(N[C@@H]1C)=O)CC(=O)N)=O)[C@H](O)C)=O)[C@H](CC)C)C', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@@H](CCC(=O)N)C(O)=O)[C@@H](NC(=O)[C@@H](N)CO)CC(=O)N', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@@H](CC(=O)N)C(=O)N[C@@H](CO)C(O)=O)[C@@H](N)CC1=CC=CC=C1', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@@H](CC(O)=O)C(O)=O)[C@@H](NC(=O)[C@@H](N)CCC(O)=O)CC(=O)N', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@H](C(=O)N[C@@H]([C@H](CC)C)C(O)=O)CC(=O)N)[C@@H](N)[C@H](CC)C', "
               "'Molecule is a glutathione conjugate'), "
               "('C[C@H](N)C(=O)N[C@@H](Cc1c[nH]c2ccccc12)C(=O)N[C@@H](CC(N)=O)C(=O)N[C@@H](CC(O)=O)C(O)=O', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@@H](C)C(O)=O)[C@@H](N)CC(=O)N', 'Molecule is a "
               "glutathione conjugate'), "
               "('O[C@@H]([C@H](N)C(=O)N[C@@H](CC(=O)N)C(=O)N[C@@H](CO)C(O)=O)C', "
               "'Molecule is a glutathione conjugate'), "
               "('O[C@@H]([C@H](NC(=O)[C@@H](NC(=O)[C@@H](N)CCC(O)=O)CC(=O)N)C(O)=O)C', "
               "'Molecule is a glutathione conjugate'), "
               "('SC[C@H](N)C(=O)N[C@@H](CC(=O)N)C(=O)N[C@@H](C)C(O)=O', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@@H](CC(=O)N)C(=O)N[C@@H](C)C(O)=O)[C@H]1NCCC1', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@@H](CCCN=C(N)N)C(O)=O)[C@@H](NC(=O)CN)CC(=O)N', "
               "'Molecule is a glutathione conjugate'), "
               "('S(CC[C@H](NC(=O)[C@@H](NC(=O)[C@@H](N)CC(=O)N)CC(=O)N)C(O)=O)C', "
               "'Molecule is a glutathione conjugate'), "
               "('S(CC[C@H](N)C(=O)N[C@@H](CC(=O)N)C(=O)N[C@@H](CCC(=O)N)C(O)=O)C', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@@H](CC(=O)N)C(=O)N[C@@H](CC(=O)N)C(O)=O)[C@@H](N)CCCN=C(N)N', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(NCC(O)=O)[C@@H](NC(=O)[C@@H](N)CO)CC(=O)N', 'Molecule is "
               "a glutathione conjugate'), "
               "('SC[C@H](N)C(=O)N[C@H](C(=O)N[C@@H](CC(C)C)C(O)=O)CC(=O)N', "
               "'Molecule is a glutathione conjugate'), "
               "('S(CCC(NC(=O)C(N)CC(=O)N)C(=O)NC(CC(=O)N)C(=O)NC(CC=1NC=NC1)C(O)=O)C', "
               "'Molecule is a glutathione conjugate'), "
               "('C[C@H](N)C(=O)N[C@@H](CC(N)=O)C(=O)N[C@@H](CC(N)=O)C(=O)N1CCC[C@H]1C(O)=O', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@@H](CC(O)=O)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(=O)N)CC(=O)N', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@@H](CCC(=O)N)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC1=CC=CC=C1)CC(=O)N', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@@H](CC1=CC=CC=C1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CCC(O)=O)CC(=O)N', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@@H]([C@H](CC)C)C(O)=O)[C@@H](NC(=O)[C@@H](N)CCCN=C(N)N)CC(=O)N', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C1O[C@@H]([C@H](NC(=O)/C=C/C=C/C=C/C=C/C=C/C2=CC=C(O)C=C2)C(=O)N[C@H](C(=O)N[C@H](C(N[C@H](C(N[C@H]1[C@@H](CC)C)=O)CC(=O)N)=O)CC(=O)N)C(C)C)C', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@@H](C(C)C)C(=O)N[C@@H](CC(=O)N)C(=O)N[C@@H](CC1=CC=CC=C1)C(O)=O)[C@H]2NCCC2', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C1O[C@@H]([C@H](NC(=O)CC(O)CCCCCCCCCCCCN=C(N)N)C(=O)N[C@@H](C(=O)N[C@@H]([C@H](CC)C)C(N[C@@H](C(N[C@@H](C(N[C@@H]1C)=O)CC(=O)N)=O)C(O)C)=O)C(C)C)C', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@H](C(=O)N[C@@H](C(C)C)C(O)=O)CC(=O)N)[C@H]1NCCC1', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@@H]([C@H](CC)C)C(O)=O)[C@@H](NC(=O)[C@@H](N)CCC(O)=O)CC(=O)N', "
               "'Molecule is a glutathione conjugate'), "
               "('SC[C@H](N)C(=O)N[C@H](C(=O)N[C@@H](C(C)C)C(O)=O)CC(=O)N', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N1[C@H](CCC1)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(C)C)CC(=O)N', "
               "'Molecule is a glutathione conjugate'), "
               "('S(CC[C@H](N)C(=O)N[C@H](C(=O)N1[C@H](CCC1)C(O)=O)CC(=O)N)C', "
               "'Molecule is a glutathione conjugate'), "
               "('O=C(N[C@@H](C)C(O)=O)[C@@H](NC(=O)[C@@H](N)CC(=O)N)CC(=O)N', "
               "'Molecule is a glutathione conjugate')]\n"
               'False negatives: '
               "[('C(\\\\CC=CC=CC=C[C@@H]([C@@H](C/C=C\\\\CC)O)SC[C@H](NC(CC[C@H](N)C(=O)O)=O)C(=O)NCC(=O)O)=C\\\\C/C=C\\\\CCC(O)=O', "
               "'Molecule is not a glutathione conjugate')]",
    'attempt': 3,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 1,
    'num_false_positives': 100,
    'num_true_negatives': 1244,
    'num_false_negatives': 0,
    'num_negatives': None,
    'precision': 0.009900990099009901,
    'recall': 1.0,
    'f1': 0.0196078431372549,
    'accuracy': 0.9256505576208178}