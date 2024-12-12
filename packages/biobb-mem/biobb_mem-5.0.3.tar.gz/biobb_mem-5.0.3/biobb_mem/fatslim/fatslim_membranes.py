#!/usr/bin/env python3

"""Module containing the FATSLiM Membranes class and the command line interface."""
import argparse
from pathlib import PurePath
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import settings
from biobb_common.tools.file_utils import launchlogger
from biobb_common.tools import file_utils as fu
import MDAnalysis as mda
from MDAnalysis.transformations.boxdimensions import set_dimensions
import shutil


class FatslimMembranes(BiobbObject):
    """
    | biobb_mem FatslimMembranes
    | Wrapper of the `FATSLiM membranes <https://pythonhosted.org/fatslim/documentation/leaflets.html>`_ module for leaflet and membrane identification.
    | FATSLiM is designed to provide efficient and robust analysis of physical parameters from MD trajectories, with a focus on processing large trajectory files quickly.

    Args:
        input_top_path (str): Path to the input topology file. File type: input. `Sample file <https://github.com/bioexcel/biobb_mem/raw/main/biobb_mem/test/data/A01JD/A01JD.pdb>`_. Accepted formats: tpr (edam:format_2333), gro (edam:format_2033), g96 (edam:format_2033), pdb (edam:format_1476), brk (edam:format_2033), ent (edam:format_1476).
        input_traj_path (str) (Optional): Path to the GROMACS trajectory file. File type: input. `Sample file <https://github.com/bioexcel/biobb_mem/raw/main/biobb_mem/test/data/A01JD/A01JD.xtc>`_. Accepted formats: xtc (edam:format_3875), trr (edam:format_3910), cpt (edam:format_2333), gro (edam:format_2033), g96 (edam:format_2033), pdb (edam:format_1476), tng (edam:format_3876).
        output_ndx_path (str): Path to the output index NDX file. File type: output. `Sample file <https://github.com/bioexcel/biobb_mem/raw/main/biobb_mem/test/data/A01JD/A01JD.ndx>`_. Accepted formats: ndx (edam:format_2033).
        properties (dic - Python dictionary object containing the tool parameters, not input/output files):
            * **selection** (*str*) - ("resname DPPC and element P") Molecules used in the identification using MDAnalysis `selection language <https://docs.mdanalysis.org/stable/documentation_pages/selections.html>`_.
            * **cutoff** (*float*) - (2) Cutoff distance (in nm) to be used when leaflet identification is performed.
            * **begin_frame** (*int*) - (-1) First frame index to be used for analysis.
            * **end_frame** (*int*) - (-1) Last frame index to be used for analysis.
            * **ignore_no_box** (*bool*) - (False) Ignore the absence of box information in the topology. If the topology does not contain box information, the box will be set to the minimum and maximum positions of the atoms.
            * **binary_path** (*str*) - ("fatslim") Path to the fatslim executable binary.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **sandbox_path** (*str*) - ("./") [WF property] Parent path to the sandbox directory.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_mem.fatslim.fatslim_membranes import fatslim_membranes
            prop = {
                'selection': '(resname DPPC and name P8)',
                'cutoff': 2.2
            }
            fatslim_membranes(input_top_path='/path/to/myTopology.tpr',
                              input_traj_path='/path/to/myTrajectory.xtc',
                              output_ndx_path='/path/to/newIndex.ndx',
                              properties=prop)

    Info:
        * wrapped_software:
            * name: FATSLiM
            * version: 0.2.2
            * license: GNU
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl

    """

    def __init__(self, input_top_path, output_ndx_path, input_traj_path=None, properties=None, **kwargs) -> None:
        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)
        self.locals_var_dict = locals().copy()

        # Input/Output files
        self.io_dict = {
            "in": {"input_top_path": input_top_path,
                   "input_traj_path": input_traj_path},
            "out": {"output_ndx_path": output_ndx_path}
        }

        # Properties specific for BB
        self.selection = properties.get('selection', "resname DPPC or resname POPC) and element P")
        self.cutoff = properties.get('cutoff', 2.2)
        self.begin_frame = properties.get('begin_frame', -1)
        self.end_frame = properties.get('end_frame', -1)
        self.ignore_no_box = properties.get('ignore_no_box', False)
        self.binary_path = properties.get('binary_path', 'fatslim')
        self.properties = properties

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`FatslimMembranes <fatslim.fatslim_membranes.FatslimMembranes>` fatslim.fatslim_membranes.FatslimMembranes object."""

        # Setup Biobb
        if self.check_restart():
            return 0
        self.stage_files()

        # Create index file using MDAnalysis
        u = mda.Universe(topology=self.stage_io_dict["in"]["input_top_path"],
                         coordinates=self.stage_io_dict["in"].get("input_traj_path"))
        if u.dimensions is None:
            if self.ignore_no_box:
                print('Warning: trajectory probably has no box variable. Setting dimensions ussing the minimum and maximum positions of the atoms.')
                # Calculate the dimensions of the box
                positions = u.atoms.positions
                box_dimensions = positions.max(axis=0) - positions.min(axis=0)
                u.trajectory.add_transformations(set_dimensions([*box_dimensions, 90, 90, 90]))
            else:
                raise ValueError('The trajectory does not contain box information. Please set the ignore_no_box property to True to ignore this error.')

        # Build the index to select the atoms from the membrane
        self.tmp_ndx = str(PurePath(fu.create_unique_dir()).joinpath('headgroups.ndx'))
        with mda.selections.gromacs.SelectionWriter(self.tmp_ndx, mode='w') as ndx:
            ndx.write(u.select_atoms(self.selection), name='headgroups')

        if self.stage_io_dict["in"]["input_top_path"].endswith('gro'):
            self.cfg = self.stage_io_dict["in"]["input_top_path"]
            self.cmd = []
        else:
            # Convert topology .gro and add box dimensions if not available in the topology
            self.cfg = str(PurePath(fu.create_unique_dir()).joinpath('output.gro'))
            self.tmp_files.extend([PurePath(self.cfg).parent])
            self.cmd = ['gmx', 'editconf',
                        '-f', self.stage_io_dict["in"]["input_top_path"],
                        '-o', self.cfg,
                        '-box', ' '.join(map(str, u.dimensions[:3])), ';',
                        ]
        self.tmp_out = str(PurePath(fu.create_unique_dir()).joinpath('output.ndx'))

        # Build command
        self.cmd.extend([
            self.binary_path, "membranes",
            "-n", self.tmp_ndx,
            "-c", self.cfg,
            "--output-index", self.tmp_out,
            "--cutoff", str(self.cutoff),
            "--begin-frame", str(self.begin_frame),
            "--end-frame", str(self.end_frame)
        ])

        # Run Biobb block
        self.run_biobb()
        shutil.move(self.tmp_out[:-4]+'_0000.ndx', self.stage_io_dict["out"]["output_ndx_path"])
        # Copy files to host
        self.copy_to_host()

        # Remove temporary files
        self.tmp_files.extend([
            self.stage_io_dict.get("unique_dir"),
            PurePath(self.tmp_ndx).parent,
            PurePath(self.tmp_out).parent
        ])
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)

        return self.return_code


def fatslim_membranes(input_top_path: str, output_ndx_path: str, input_traj_path: str = None, properties: dict = None, **kwargs) -> int:
    """Execute the :class:`FatslimMembranes <fatslim.fatslim_membranes.FatslimMembranes>` class and
    execute the :meth:`launch() <fatslim.fatslim_membranes.FatslimMembranes.launch>` method."""

    return FatslimMembranes(input_top_path=input_top_path,
                            input_traj_path=input_traj_path,
                            output_ndx_path=output_ndx_path,
                            properties=properties, **kwargs).launch()


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description="Calculates the density along an axis of a given cpptraj compatible trajectory.", formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    # Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_top_path', required=True, help='Path to the input structure or topology file. Accepted formats: ent, gro, pdb, tpr.')
    required_args.add_argument('--output_ndx_path', required=True, help='Path to the GROMACS index file. Accepted formats: ndx')
    parser.add_argument('--input_traj_path', required=False, help='Path to the input trajectory to be processed. Accepted formats: gro, pdb, tng, trr, xtc.')

    args = parser.parse_args()
    args.config = args.config or "{}"
    properties = settings.ConfReader(config=args.config).get_prop_dic()

    # Specific call of each building block
    fatslim_membranes(input_top_path=args.input_top_path,
                      output_ndx_path=args.output_ndx_path,
                      properties=properties)


def parse_index(ndx):
    """
    Parses a GROMACS index file (.ndx) to extract leaflet groups.

    Args:
        ndx (str): Path to the GROMACS index file (.ndx).
    Returns:
        dict: A dictionary where keys are group names and values are lists of integers representing atom indices.
    """

    # Read the leaflet.ndx file
    with open(ndx, 'r') as file:
        leaflet_data = file.readlines()

    # Initialize dictionaries to store leaflet groups
    leaflet_groups = {}
    current_group = None

    # Parse the leaflet.ndx file
    for line in leaflet_data:
        line = line.strip()
        if line.startswith('[') and line.endswith(']'):
            current_group = line[1:-1].strip()
            leaflet_groups[current_group] = []
        elif current_group is not None:
            leaflet_groups[current_group].extend(map(int, line.split()))
    return leaflet_groups


def display_fatslim(input_top_path: str, lipid_sel: str, input_traj_path: str = None, output_ndx_path="leaflets.ndx", leaflets=True,
                    colors=['blue', 'cyan', 'yellow', 'orange', 'purple', 'magenta'], non_mem_color='red'):
    """
    Visualize the leaflets of a membrane using NGLView. The lipids in the membrane are colored according to their leaflet. The ones not in the membrane are colored in red.

    Args:
        input_top_path (str): Path to the input topology file.
        input_traj_path (str, optional): Path to the input trajectory file. Default is None.
        output_ndx_path (str, optional): Path to the output index file containing leaflet information. Default is "leaflets.ndx".
        leaflets (bool, optional): If True, visualize individual leaflets. If False, visualize entire membranes. Default is True.
        colors (list of str, optional): List of colors to use for visualizing the leaflets or membranes. Default is ['blue', 'cyan', 'yellow', 'orange', 'purple', 'magenta'].
        non_mem_color (str, optional): Color to use for visualizing lipids not in the membrane. Default is 'red'.
    Returns:
        nglview.NGLWidget: An NGLView widget displaying the membrane leaflets.
    """
    try:
        import nglview as nv
        import numpy as np
    except ImportError:
        raise ImportError('Please install the nglview package to visualize the membrane/s.')

    u = mda.Universe(topology=input_top_path,
                     coordinates=input_traj_path)
    # Visualize the system with NGLView
    view = nv.show_mdanalysis(u)
    view.clear_representations()

    leaflet_groups = parse_index(output_ndx_path)
    n_mems = len(leaflet_groups.keys())//2

    non_mem_resn = set(u.select_atoms(lipid_sel).residues.resnums)
    for n in range(n_mems):
        # Convert atoms list to resnums (nglview uses cannot use resindex)
        top_resn = u.atoms[np.array(leaflet_groups[f'membrane_{n+1}_leaflet_1'])-1].residues.resnums
        bot_resn = u.atoms[np.array(leaflet_groups[f'membrane_{n+1}_leaflet_2'])-1].residues.resnums
        non_mem_resn -= set(top_resn)
        non_mem_resn -= set(bot_resn)
        if leaflets:
            view.add_point(selection=", ".join(map(str, top_resn)), color=colors[n*2])              # lipids in top leaflet
            view.add_point(selection=", ".join(map(str, bot_resn)), color=colors[n*2+1])            # lipids in bot leaflet
        else:
            mem_resn = np.concatenate((top_resn, bot_resn))
            view.add_point(selection=", ".join(map(str, mem_resn)), color=colors[n*2])              # lipids in membrane
    if len(non_mem_resn) > 0:
        view.add_point(selection=", ".join(map(str, non_mem_resn)), color=non_mem_color)   # lipids without membrane
    return view


if __name__ == '__main__':
    main()
