"""
Classifies: CHEBI:33658 arene
"""
from rdkit import Chem
from rdkit.Chem import AllChem

def is_arene(smiles: str):
    """
    Determines if a molecule is an arene (any monocyclic or polycyclic aromatic hydrocarbon).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is an arene, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Generate the aromatic ring information
    rings = mol.GetRingInfo()

    # Check for at least one aromatic ring
    aromatic_rings = []
    for ring in rings.AtomRings():
        atoms = [mol.GetAtomWithIdx(i) for i in ring]
        if all(atom.GetIsAromatic() for atom in atoms):
            aromatic_rings.append(ring)

    if not aromatic_rings:
        return False, "No aromatic rings found"

    # Check if all atoms in the aromatic rings are carbon or hydrogen
    for ring in aromatic_rings:
        atoms = [mol.GetAtomWithIdx(i) for i in ring]
        if not all(atom.GetSymbol() in ['C', 'H'] for atom in atoms):
            return False, "Ring contains non-carbon and non-hydrogen atoms"

    # Check if there are no non-aromatic substituents attached to the aromatic rings
    ring_atoms = set().union(*aromatic_rings)
    non_aromatic_substituents = []
    for atom in mol.GetAtoms():
        if atom.GetIdx() in ring_atoms:
            continue
        neighbors = atom.GetNeighbors()
        if any(neighbor.GetIdx() in ring_atoms for neighbor in neighbors):
            symbol = atom.GetSymbol()
            if symbol not in ['C', 'H']:
                non_aromatic_substituents.append(symbol)

    if non_aromatic_substituents:
        return False, f"Molecule contains non-aromatic substituents ({', '.join(set(non_aromatic_substituents))}) attached to the aromatic rings"

    if len(aromatic_rings) == 1:
        return True, "Monocyclic arene"
    else:
        return True, "Polycyclic arene"


__metadata__ = {   'chemical_class': {   'id': 'CHEBI:33658',
                          'name': 'arene',
                          'definition': 'Any monocyclic or polycyclic aromatic '
                                        'hydrocarbon.',
                          'parents': ['CHEBI:33659', 'CHEBI:33663']},
    'config': {   'llm_model_name': 'claude-3-sonnet',
                  'f1_threshold': 0.0,
                  'max_attempts': 5,
                  'max_negative_to_test': None,
                  'max_positive_in_prompt': 50,
                  'max_negative_in_prompt': 20,
                  'max_instances_in_prompt': 100,
                  'test_proportion': 0.1},
    'message': '\n'
               'Attempt failed: F1 score of 0.12162162162162163 is too low.\n'
               'True positives: '
               "[('c1cc2cc3ccc4cc5ccc6cc7ccc8cc9ccc%10cc%11ccc%12cc1c1cc%12c%11cc%10c9cc8c7cc6c5cc4c3cc21', "
               "'Polycyclic arene'), "
               "('c1ccc-2c(c1)-c1ccccc1-c1ccccc1-c1ccccc-21', 'Polycyclic "
               "arene'), ('Cc1cccc(C)c1', 'Monocyclic arene'), "
               "('c1ccc2c(c1)cc1ccc3cc4ccccc4c4ccc2c1c34', 'Polycyclic "
               "arene'), ('c1ccc2ccccc2c1', 'Polycyclic arene'), "
               "('c1ccc2cc3ccccc3cc2c1', 'Polycyclic arene'), "
               "('Oc1c(O)c2c3ccccc3cc3ccc4cccc1c4c23', 'Polycyclic arene'), "
               "('Cc1ccc(C)cc1', 'Monocyclic arene'), "
               "('Oc1cc2ccc3cc4ccccc4c4ccc(c1)c2c34', 'Polycyclic arene')]\n"
               "False positives: [('Clc1ccc(cc1)-c1c(Cl)cc(Cl)cc1Cl', "
               "'Polycyclic arene'), "
               "('C12=C3C4=C5C6=C7C=8C(*)=C5C(=C(*)C4=C(C1=C(*)C9=C%10C2=C%11C%12=C3C6=C%13C%14=C7C=%15C=%16C%17=C%14C%18=C%19C%20=C%21C(=C%22C(C(*)=C%21C(*)=C(C%20=C(C%18=C(*)C%17=C(*)C%23=C(C(=C(C(C%16%23)=C(C%15C8*)*)*)*)*)*)*)=C(C=%24C(=C%11%22)C%10=C%25C(=C9*)C(*)=C(C(=C%25C%24*)*)*)*)C%12=C%19%13)*)*', "
               "'Polycyclic arene'), ('N(c1ccccc1)c1cccc2ccccc12', 'Polycyclic "
               "arene'), ('[Cl-].[I+]1c2ccccc2-c2ccccc12', 'Polycyclic "
               "arene'), ('FC1=CC=C(OC=2C=C(N)C=CC2)C=C1', 'Polycyclic "
               "arene'), ('Oc1ccc(Br)cc1O', 'Monocyclic arene'), "
               "('Nc1ccc(Cl)cc1', 'Monocyclic arene'), "
               "('Oc1c2ccccc2c(O)c2ccccc12', 'Polycyclic arene'), "
               "('Cc1cc(C)c(N)c(C)c1', 'Monocyclic arene'), "
               "('Oc1cc(Cl)c(cc1Cl)-c1cc(Cl)c(Cl)cc1Cl', 'Polycyclic arene'), "
               "('C=12C=C(C3=CC=CC=4C3=C2C(C=CC1)=CC4)*', 'Polycyclic arene'), "
               "('C=1C=C(C=CC1O)Br', 'Monocyclic arene'), "
               "('NC=1C=2C(C(N)=CC1)=CC=CC2', 'Polycyclic arene'), "
               "('C1=CC#CC=C1', 'Monocyclic arene'), ('Clc1ccccc1', "
               "'Monocyclic arene'), "
               "('C=1C=CC=C2C3=CC=C4C=C(C=CC4=C3C=CC21)O', 'Polycyclic "
               "arene'), ('C1=CC=CC2=C1NC=3C=CC=CC3N2', 'Polycyclic arene'), "
               "('c1ccc(cc1)-c1ccc(cc1)-c1ccc(cc1)-c1ccccc1', 'Polycyclic "
               "arene'), ('C12=C(C=CC=C1C=C(C(=C2)C)C)C', 'Polycyclic arene'), "
               "('Nc1cccc(O)c1', 'Monocyclic arene'), "
               "('C1=C(C=CC(C2=CC=CC=C2)=C1)O', 'Polycyclic arene'), "
               "('NC1=CC=C(C2=CC(=CC(=C2)C3=CC=C(N)C=C3)C4=CC=C(N)C=C4)C=C1', "
               "'Polycyclic arene'), ('Nc1ccc(O)c(O)c1', 'Monocyclic arene'), "
               "('Nc1c(Cl)cccc1Cl', 'Monocyclic arene'), "
               "('C1=CC(=CC=C1CC2=CC=C(C=C2)O)O', 'Polycyclic arene'), "
               "('C1=C(C=C(C=C1O)Cl)Cl', 'Monocyclic arene'), "
               "('C(c1ccccc1)c1ccccc1', 'Polycyclic arene'), "
               "('c1ccc(cc1)-c1ccccc1', 'Polycyclic arene'), "
               "('Clc1cc2Oc3c(Oc2c(Cl)c1Cl)cc(Cl)c(Cl)c3Cl', 'Polycyclic "
               "arene'), "
               "('O=C1C2=C(O)C3=C(C(=O)C4=C3C=CC=C4O)C=C2C(=O)C=5C1=C(O)C=CC5', "
               "'Polycyclic arene'), ('BrC1=C(F)C=C(F)C(F)=C1', 'Monocyclic "
               "arene'), ('C=1C=CC=C2C3=CC=C4C=CC=C(C4=C3C=CC21)O', "
               "'Polycyclic arene'), ('Cc1cc(Cl)ccc1N', 'Monocyclic arene'), "
               "('Clc1cccc(c1)-c1ccccc1', 'Polycyclic arene'), "
               "('O(C=1C(=CC(=CC1Br)Br)Br)C=2C=CC(=CC2Br)Br', 'Polycyclic "
               "arene'), ('Nc1ccccc1O', 'Monocyclic arene'), "
               "('Clc1c(Cl)c(Cl)c2Oc3ccccc3Oc2c1Cl', 'Polycyclic arene'), "
               "('Oc1ccc(c(Cl)c1)-c1c(Cl)cc(Cl)cc1Cl', 'Polycyclic arene'), "
               "('[B]c1cccc2ccccc12', 'Polycyclic arene'), "
               "('BrC1=C(OC2=C(Br)C(=C(Br)C(=C2)O)C)C(Br)=C(C)C(=C1O)Br', "
               "'Polycyclic arene'), ('Nc1ccc(N)cc1', 'Monocyclic arene'), "
               "('C=1(C(=CC=CC1)Cl)C=2C(=C(C=CC2)O)O', 'Polycyclic arene'), "
               "('Oc1ccc(cc1)-c1ccc(Cl)cc1', 'Polycyclic arene'), "
               "('Nc1cc(N)cc(N)c1', 'Monocyclic arene'), "
               "('Oc1cc2ccc3cccc4ccc(c1)c2c34', 'Polycyclic arene'), "
               "('Clc1ccc(Cl)c(Cl)c1', 'Monocyclic arene'), "
               "('Brc1cc(Br)c(Oc2c(Br)cc(Br)c(Br)c2Br)cc1Br', 'Polycyclic "
               "arene'), ('Clc1cc2Oc3cc(Cl)c(Cl)cc3Oc2cc1Cl', 'Polycyclic "
               "arene'), "
               "('Oc1cc(O)cc(Oc2c(O)cc(O)c3Oc4c(Oc23)c(O)cc(O)c4-c2c(O)cc(O)c3Oc4c(Oc5cc(O)cc(O)c5)c(O)cc(O)c4Oc23)c1', "
               "'Polycyclic arene'), ('C=1(C=CC(=CC1)*)C', 'Monocyclic "
               "arene'), ('c1ccc(cc1)[As+](c1ccccc1)(c1ccccc1)c1ccccc1', "
               "'Polycyclic arene'), ('Oc1ccc(Oc2ccccc2)cc1', 'Polycyclic "
               "arene'), ('C=1C(=CC2=C(C1)C=C(C=C2)O)Br', 'Polycyclic arene'), "
               "('C=1(C(=C(C(=C(C1*)*)O)*)*)[O]', 'Monocyclic arene'), "
               "('C1(C2=CC=C(C=C2)*)=CC=CC=C1', 'Polycyclic arene'), "
               "('ClC1=C(O)C=C(O)C=C1O', 'Monocyclic arene'), "
               "('C1c2ccccc2-c2ccc3ccccc3c12', 'Polycyclic arene'), "
               "('c1ccc(cc1)[P+](c1ccccc1)(c1ccccc1)c1ccccc1', 'Polycyclic "
               "arene'), ('O(C=1C=CC=CC1Br)C=2C(=CC(=CC2)Br)Br', 'Polycyclic "
               "arene'), ('Clc1ccc(Cl)c(c1)-c1cc(Cl)ccc1Cl', 'Polycyclic "
               "arene'), ('Oc1cccc(I)c1', 'Monocyclic arene'), "
               "('Cc1cc(O)c2c3c1c1c(C)cc(O)c4c1c1c5c(c(O)cc(O)c5c4=O)c4c(O)cc(O)c(c4c31)c2=O', "
               "'Polycyclic arene'), ('Oc1cc2ccccc2c2ccccc12', 'Polycyclic "
               "arene'), ('Oc1cc(O)cc(c1)-c1ccccc1', 'Polycyclic arene'), "
               "('O=C1C2=C(O)C=3C=4C(=C5C(O)=CC(=C6C5=C(C4C2=CC(=C1)C)C=7C(C(=O)C=C(C7)C)=C6O)O)C(O)=CC3O', "
               "'Polycyclic arene'), ('Oc1cc(O)cc(O)c1', 'Monocyclic arene'), "
               "('Cc1cc(O)ccc1N', 'Monocyclic arene'), "
               "('Oc1c2ccccc2cc2ccccc12', 'Polycyclic arene'), "
               "('Nc1ccc(N)c(N)c1', 'Monocyclic arene'), "
               "('O(C=1C=C(C(=CC1Br)Br)Br)C=2C=CC(=CC2Br)Br', 'Polycyclic "
               "arene'), ('[O]C1=CC=C([*])C=C1', 'Monocyclic arene'), "
               "('Cc1ccccc1O', 'Monocyclic arene'), "
               "('C=1C=CC=C2C3=CC=C4C(=CC=CC4=C3C=CC21)O', 'Polycyclic "
               "arene'), ('C=1C=C(C=CC1O)F', 'Monocyclic arene'), "
               "('Cc1cc(C)c2Cc3c(C)cc(C)c(Cc4c(C)cc(C)c(Cc5c(C)cc(C)c(Cc1c2C)c5C)c4C)c3C', "
               "'Polycyclic arene'), ('C=1(C(=CC=CC1)N)C=2C(=C(C=CC2)O)O', "
               "'Polycyclic arene'), ('Nc1ccc(cc1)-c1ccccc1N', 'Polycyclic "
               "arene'), "
               "('ClC1=C(OC2=C(Cl)C=C(Cl)C=C2)C(O)=CC(=C1C3=C(O)C(Cl)=CC(=C3)Cl)Cl', "
               "'Polycyclic arene'), "
               "('Clc1cc(cc(Cl)c1Cl)-c1cc(Cl)c(Cl)c(Cl)c1', 'Polycyclic "
               "arene'), ('Oc1c(Cl)cc(Cl)c(Cl)c1Cc1c(O)c(Cl)cc(Cl)c1Cl', "
               "'Polycyclic arene'), ('Oc1cc2ccccc2cc1O', 'Polycyclic arene'), "
               "('Clc1ccccc1Cl', 'Monocyclic arene'), ('C=1(C=CC=CC1*)*', "
               "'Monocyclic arene'), "
               "('C12=C3C(=CC=C1C=CC4=C2C=CC(=C4)O)C=CC=C3', 'Polycyclic "
               "arene'), ('Oc1cccc(c1)-c1cc(Cl)c(Cl)c(Cl)c1Cl', 'Polycyclic "
               "arene'), ('Oc1c(Br)cc(Br)cc1-c1cc(Br)cc(Br)c1O', 'Polycyclic "
               "arene'), ('Oc1ccc(c(Cl)c1)-c1ccccc1', 'Polycyclic arene'), "
               "('Nc1cccc(N)c1N', 'Monocyclic arene'), "
               "('Oc1c(Cl)cc(cc1Cl)-c1cc(Cl)ccc1Cl', 'Polycyclic arene'), "
               "('Oc1c(O)c2cccc3ccc4cccc1c4c23', 'Polycyclic arene'), "
               "('Fc1ccccc1', 'Monocyclic arene'), ('Oc1ccc(Cl)cc1Cl', "
               "'Monocyclic arene'), ('Oc1ccc2cc3ccccc3cc2c1O', 'Polycyclic "
               "arene'), "
               "('Clc1c(Cl)c(Cl)c(c(Cl)c1Cl)-c1c(Cl)c(Cl)c(Cl)c(Cl)c1Cl', "
               "'Polycyclic arene'), "
               "('BrC1=C(OC2=C(Br)C=C(Br)C=C2)C(O)=CC=C1OC3=C(Br)C=C(OC4=CC(Br)=C(O)C=C4)C=C3OC5=C(Br)C=C(Br)C=C5', "
               "'Polycyclic arene'), ('C1=CC=C2C(=C1)CC=3C=CC(=CC32)O', "
               "'Polycyclic arene'), ('Oc1cc(Br)c(Br)c(Br)c1Oc1ccc(Br)cc1Br', "
               "'Polycyclic arene'), ('Cc1cc(O)c(O)c(Oc2cc(C)cc(O)c2O)c1', "
               "'Polycyclic arene'), ('C=1(C(=CC(=CC1Cl)O)Cl)[O-]', "
               "'Monocyclic arene'), "
               "('CC1=CC2=C(C3=C(C2=O)C(=O)C2=C(O)C=CC=C2C3=O)C(O)=C1', "
               "'Polycyclic arene')]\n"
               "False negatives: [('CC1=C(C=C(C=C1)NCCC(=O)C2=CC=CS2)C', 'Ring "
               "contains non-carbon and non-hydrogen atoms'), "
               "('O[C@H]1C[C@](CCC1)(C2=C(O)C=C(C(CCCCCCCO)(C)C)C=C2)[H]', "
               "'Molecule contains non-aromatic substituents attached to the "
               "aromatic rings'), "
               "('CCCCCCCCCCCCCC(=O)N[C@@H](C)[C@@H](C1=CC=CC=C1)O', 'Molecule "
               'contains non-aromatic substituents attached to the aromatic '
               "rings'), ('CC1=CC=C(CO)C(C)=C1', 'Molecule contains "
               "non-aromatic substituents attached to the aromatic rings'), "
               "('CCOC(=O)C(Cl)Cc1ccc(OCC(C)(C)c2ccccc2)cc1', 'Molecule "
               'contains non-aromatic substituents attached to the aromatic '
               "rings'), ('CCCCC1=CC(C)=C(NC(C)=O)C=C1', 'Molecule contains "
               "non-aromatic substituents attached to the aromatic rings'), "
               "('C=Cc1cccc2ccccc12', 'Molecule contains non-aromatic "
               "substituents attached to the aromatic rings'), "
               "('O1[C@]2(O)[C@@]3([C@@]([C@H]([C@](C2=O)(C=C3[C@]4(OC=5C(C(=O)C4)=C(O)C=C(O)C5)[H])[H])C6=CC(OC)=C(O)C=C6)(C1)[H])[H]', "
               "'Molecule contains non-aromatic substituents attached to the "
               "aromatic rings'), "
               "('CC(C)(C)C1=CC(=CC(=C1O)C(C)(C)C)CC(C)(C)CO', 'Molecule "
               'contains non-aromatic substituents attached to the aromatic '
               "rings'), ('OC(CC1=CC=CC=C1)(C)C=O', 'Molecule contains "
               "non-aromatic substituents attached to the aromatic rings'), "
               "('P(OC(CC1=CC=CC=C1)C)(OCC2=CC=CC=C2)(OCC3=CC=CC=C3)=O', "
               "'Molecule contains non-aromatic substituents attached to the "
               "aromatic rings'), ('CC(C)(c1ccc(O)cc1)C1=CC(=O)C(=O)C=C1', "
               "'Molecule contains non-aromatic substituents attached to the "
               "aromatic rings'), "
               "('S1C=C(C(=O)C(=CNC2=CC=C(C(C)(C)C)C=C2)C#N)C=C1', 'Ring "
               "contains non-carbon and non-hydrogen atoms'), "
               "('C(CC=1C(=C(C(=CC1C)C)C)C)C(C)C', 'Molecule contains "
               "non-aromatic substituents attached to the aromatic rings'), "
               "('C(=CCN[C@H]([C@H](O)C1=CC=CC=C1)C)(C=2C=CSC2)C=3C=CSC3', "
               "'Ring contains non-carbon and non-hydrogen atoms'), "
               "('CC(C)(C)C1=CC(=CC(=C1O)C(C)(C)C)CN(CCO)CCO', 'Molecule "
               'contains non-aromatic substituents attached to the aromatic '
               "rings'), ('OC(C(C)C=O)C1=CC=CC=C1', 'Molecule contains "
               "non-aromatic substituents attached to the aromatic rings'), "
               "('OC1=C(C(O)=CC(=C1)C[C@@H](O)C)C', 'Molecule contains "
               "non-aromatic substituents attached to the aromatic rings'), "
               "('OC(C(NC(=O)CCC/C=C\\\\C/C=C\\\\C/C=C\\\\C/C=C\\\\CCCCC)C)C1=CC=CC=C1', "
               "'Molecule contains non-aromatic substituents attached to the "
               "aromatic rings'), "
               "('O=C(O)C1=CC(=CC(=C1)C(C#N)(C)C)C(C#N)(C)C', 'Molecule "
               'contains non-aromatic substituents attached to the aromatic '
               "rings'), ('OC1=CC=C(C(C)(C)C)C=C1C(C)(C)C', 'Molecule contains "
               "non-aromatic substituents attached to the aromatic rings'), "
               "('CCCC(=O)CNC(=O)Oc1cc(C)cc(c1)C(C)C', 'Molecule contains "
               "non-aromatic substituents attached to the aromatic rings'), "
               "('C(CC)(C=1N=C(ON1)CCN(CC)CC)C2=CC=CC=C2', 'Ring contains "
               "non-carbon and non-hydrogen atoms'), "
               "('O=C1C(OC2=C(C(O)=CC(=C2)C)C)=C(C(=O)C(=C1C)O)C', 'Molecule "
               'contains non-aromatic substituents attached to the aromatic '
               "rings'), "
               "('CC(C)(C)C1=CC=C(C=C1)C2=CC(=C(S2)C(=O)OC)NC(=O)CSCC(=O)O', "
               "'Ring contains non-carbon and non-hydrogen atoms'), "
               "('O[C@@H]([C@@H](N)C)C1=CC=C(O)C=C1', 'Molecule contains "
               "non-aromatic substituents attached to the aromatic rings'), "
               "('O(C(CC1=CC=CC=C1)(C)C)C(=O)CCC', 'Molecule contains "
               "non-aromatic substituents attached to the aromatic rings'), "
               "('OC1=CC(N)=C(C)C(=C1)C(C(O)C)C', 'Molecule contains "
               "non-aromatic substituents attached to the aromatic rings'), "
               "('CCC(=NNC(=S)NC1=CC=CC(=C1)C)C2=CC=CC=C2', 'Molecule contains "
               "non-aromatic substituents attached to the aromatic rings'), "
               "('O1[C@H](CN(CC(CC2=CC=C(C(C)(C)C)C=C2)C)C[C@H]1C)C', "
               "'Molecule contains non-aromatic substituents attached to the "
               "aromatic rings')]",
    'attempt': 4,
    'success': True,
    'best': True,
    'error': '',
    'stdout': None,
    'num_true_positives': 18,
    'num_false_positives': 100,
    'num_true_negatives': 2481,
    'num_false_negatives': 21,
    'num_negatives': None,
    'precision': 0.15254237288135594,
    'recall': 0.46153846153846156,
    'f1': 0.22929936305732485,
    'accuracy': 0.9538167938931298}