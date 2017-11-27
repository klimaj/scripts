import pyrosetta

pyrosetta.init('-ignore_waters 0 -extra_res_fa NAD.fa.params')
ligand_params = pyrosetta.Vector1(['NAD.fa.params'])
pose = pyrosetta.rosetta.core.pose.Pose()
res_set = pose.conformation().modifiable_residue_type_set_for_conf()
res_set.read_files_for_base_residue_types( ligand_params )
pose.conformation().reset_residue_type_set_for_conf( res_set )
pose = pyrosetta.pose_from_file(filename='pdbfile.pdb')

obj = pyrosetta.rosetta.protocols.rosetta_scripts.XmlObjects.create_from_string("""
<RESIDUE_SELECTORS>
    <ResiduePDBInfoHasLabel name="context" property="CONTEXT" />
    <Index name="ligand2" resnums="1" />
    <Chain name="chA" chains="A"/>
    <ResidueName name="ligand" residue_name3="NAD" />
    <And name="context_ligand" selectors="ligand,context" />
    <Neighborhood name="CN01" selector="ligand" distance="10.0" include_focus_in_subset="0" atom_names_for_distance_measure="N6" />
</RESIDUE_SELECTORS>
""")

obj2 = pyrosetta.rosetta.protocols.rosetta_scripts.XmlObjects.create_from_string(""" 
<ROSETTASCRIPTS>
    <RESIDUE_SELECTORS>
        <ResiduePDBInfoHasLabel name="context" property="CONTEXT"/>
        <Index name="ligand2" resnums="1"/>
        <Chain chains="A" name="chA"/>
        <ResidueName name="ligand" residue_name3="NAD"/>
        <And name="context_ligand" selectors="ligand,context"/>
    <Neighborhood atom_names_for_distance_measure="N6" distance="10.0" include_focus_in_subset="0" name="CN01" selector="ligand"/>
</RESIDUE_SELECTORS>
<TASKOPERATIONS>
    <OperateOnResidueSubset name="prevent_repacking" selector="CN01" >
        <PreventRepackingRLT/>
    </OperateOnResidueSubset>
</TASKOPERATIONS>
<MOVERS>
    <FastDesign name="fd" task_operations="prevent_repacking"/>
</MOVERS>
<PROTOCOLS>
    <Add mover="fd" />
</PROTOCOLS>
</ROSETTASCRIPTS>
""")

n = obj.get_residue_selector("context_ligand")
resi = list(pyrosetta.rosetta.core.select.get_residues_from_subset(n.apply(pose)))
print('Done!')
