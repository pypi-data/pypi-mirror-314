import numpy as np
import json
import os, sys, glob
from math import ceil
from typing import (List, Union, Optional)
# import time
# os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# from pwdata.image import Image
# from pwdata.movement import MOVEMENT
# from pwdata.outcar import OUTCAR
# from pwdata.poscar import POSCAR
# from pwdata.atomconfig import CONFIG
# from pwdata.dump import DUMP
# from pwdata.lammpsdata import LMP
# from pwdata.cp2kdata import CP2KMD, CP2KSCF
# from pwdata.deepmd import DPNPY, DPRAW
# from pwdata.pwmlff import PWNPY
# from pwdata.meta import META
# from pwdata.movement_saver import save_to_movement
# from pwdata.extendedxyz import EXTXYZ, save_to_extxyz
# from pwdata.datasets_saver import save_to_dataset, get_pw, save_to_raw, save_to_npy
# from pwdata.build.write_struc import write_config, write_vasp, write_lammps
import argparse
from pwdata.convert_files import do_scale_cell, do_super_cell, do_perturb, do_convert_config, do_convert_images, do_count_images
from pwdata.utils.constant import FORMAT, get_atomic_name_from_number
from pwdata.check_envs import print_cmd

# from pwdata.open_data.meta_data import get_meta_data

# class Save_Data(object):
#     def __init__(self, data_path, datasets_path = "./PWdata", train_data_path = "train", valid_data_path = "valid", 
#                  train_ratio = None, random = True, seed = 2024, format = None, retain_raw = False, atom_names:list[str] = None) -> None:
#         if format.lower() == "pwmat/config":
#             self.image_data = CONFIG(data_path)
#         elif format.lower() == "vasp/poscar":
#             self.image_data = POSCAR(data_path)
#         elif format.lower() == "lammps/dump":
#             self.image_data = DUMP(data_path, atom_names)
#         elif format.lower() == "lammps/lmp":
#             self.image_data = LMP(data_path)
#         else:
#             assert train_ratio is not None, "train_ratio must be set when format is not config or poscar (inference)"
#             self.data_name = os.path.basename(data_path)
#             self.labels_path = os.path.join(datasets_path, self.data_name)
#             if os.path.exists(datasets_path) is False:
#                 os.makedirs(datasets_path, exist_ok=True)
#             if not os.path.exists(self.labels_path):
#                 os.makedirs(self.labels_path, exist_ok=True)
#             if len(glob.glob(os.path.join(self.labels_path, train_data_path, "*.npy"))) > 0:
#                 print("Data %s has been processed!" % self.data_name)
#                 return
#             if format.lower() == "pwmat/movement":
#                 self.image_data = MOVEMENT(data_path)
#             elif format.lower() == "vasp/outcar":
#                 self.image_data = OUTCAR(data_path)
#             elif format.lower() == "extxyz":
#                 self.image_data = EXTXYZ(data_path)
#             elif format.lower() == "vasp/xml":
#                 pass
#             elif format.lower() == 'cp2k/md':
#                 self.image_data = CP2KMD(data_path)
#             elif format.lower() == 'cp2k/scf':
#                 self.image_data = CP2KSCF(data_path)
#             elif format.lower() == 'deepmd/npy':
#                 self.image_data = DPNPY(data_path)
#             elif format.lower() == 'deepmd/raw':
#                 self.image_data = DPRAW(data_path)
#             elif format.lower() == 'pwmlff/npy':
#                 self.image_data = PWNPY(data_path)
#         self.lattice, self.position, self.energies, self.ei, self.forces, self.virials, self.atom_type, self.atom_types_image, self.image_nums = get_pw(self.image_data.get())

#         if train_ratio is not None:  # inference 时不存数据
#             self.train_ratio = train_ratio        
#             self.split_and_save_data(seed, random, self.labels_path, train_data_path, valid_data_path, retain_raw)
    
#     def split_and_save_data(self, seed, random, labels_path, train_path, val_path, retain_raw):
#         if seed:
#             np.random.seed(seed)
#         indices = np.arange(self.image_nums)    # 0, 1, 2, ..., image_nums-1
#         if random:
#             np.random.shuffle(indices)              # shuffle the indices
#         train_size = ceil(self.image_nums * self.train_ratio)
#         train_indices = indices[:train_size]
#         val_indices = indices[train_size:]
#         # image_nums = [self.image_nums]
#         atom_types_image = self.atom_types_image.reshape(1, -1)

#         train_data = [self.lattice[train_indices], self.position[train_indices], self.energies[train_indices], 
#                       self.forces[train_indices], atom_types_image, self.atom_type,
#                       self.ei[train_indices]]
#         val_data = [self.lattice[val_indices], self.position[val_indices], self.energies[val_indices], 
#                     self.forces[val_indices], atom_types_image, self.atom_type,
#                     self.ei[val_indices]]

#         if len(self.virials) != 0:
#             train_data.append(self.virials[train_indices])
#             val_data.append(self.virials[val_indices])
#         else:
#             train_data.append([])
#             val_data.append([])

#         if self.train_ratio == 1.0 or len(val_indices) == 0:
#             labels_path = os.path.join(labels_path, train_path)
#             if not os.path.exists(labels_path):
#                 os.makedirs(labels_path)
#             if retain_raw:
#                 save_to_raw(train_data, train_path)
#             save_to_npy(train_data, labels_path)
#         else:
#             train_path = os.path.join(labels_path, train_path) 
#             val_path = os.path.join(labels_path, val_path)
#             if not os.path.exists(train_path):
#                 os.makedirs(train_path)
#             if not os.path.exists(val_path):
#                 os.makedirs(val_path)
#             if retain_raw:
#                 save_to_raw(train_data, train_path)
#                 save_to_raw(val_data, val_path)
#             save_to_npy(train_data, train_path)
#             save_to_npy(val_data, val_path)
                
                
# class Config(object):
#     def __init__(self, format: str, data_path: str, pbc = None, atom_names = None, index = ':', **kwargs):
#         self.format = format
#         self.data_path = data_path
#         self.pbc = pbc
#         self.atom_names = atom_names
#         self.index = index
#         self.kwargs = kwargs
#         self.images = self._read()

#     def _read(self):
#         return Config.read(self.format, self.data_path, self.pbc, self.atom_names, self.index, **self.kwargs)
    
#     def append(self, images_obj):
#         if not hasattr(self, 'images'):
#             self.images = []
#         if not isinstance(self.images, list):
#             self.images = [self.images]
#         if not isinstance(images_obj.images, list):
#             images_obj.images = [images_obj.images]
#         self.images += images_obj.images
        
#     @staticmethod
#     def read(format: str, data_path: str, pbc = None, atom_names = None, index = ':', **kwargs):
#         """ Read the data from the input file. 
#             index: int, slice or str
#             The last configuration will be returned by default.  Examples:

#             * ``index=0``: first configuration
#             * ``index=-2``: second to last
#             * ``index=':'`` or ``index=slice(None)``: all
#             * ``index='-3:'`` or ``index=slice(-3, None)``: three last
#             * ``index='::2'`` or ``index=slice(0, None, 2)``: even
#             * ``index='1::2'`` or ``index=slice(1, None, 2)``: odd

#             kwargs: dict
#             Additional keyword arguments for reading the input file.
#             unit: str, optional. for lammps, the unit of the input file. Default is 'metal'.
#             style: str, optional. for lammps, the style of the input file. Default is 'atomic'.
#             sort_by_id: bool, optional. for lammps, whether to sort the atoms by id. Default is True.

#         """
#         if isinstance(index, str):
#             try:
#                 index = string2index(index)
#             except ValueError:
#                 pass

#         if format.lower() == "pwmat/config":
#             image = CONFIG(data_path, pbc).image_list[0]
#         elif format.lower() == "vasp/poscar":
#             image = POSCAR(data_path, pbc).image_list[0]
#         elif format.lower() == "lammps/dump":
#             assert atom_names is not None, "atom_names must be set when format is dump"
#             image = DUMP(data_path, atom_names).image_list[index]
#         elif format.lower() == "lammps/lmp":
#             image = LMP(data_path, atom_names, **kwargs).image_list[0]
#         elif format.lower() == "pwmat/movement":
#             image = MOVEMENT(data_path).image_list[index]
#         elif format.lower() == "vasp/outcar":
#             image = OUTCAR(data_path).image_list[index]
#         elif format.lower() == "extxyz":
#             image = EXTXYZ(data_path, index).image_list[index]
#         elif format.lower() == "vasp/xml":
#             image = None
#         elif format.lower() == 'cp2k/md':
#             image = CP2KMD(data_path).image_list[index]
#         elif format.lower() == 'cp2k/scf':
#             image = CP2KSCF(data_path).image_list[0]
#         elif format.lower() == 'deepmd/npy':
#             image = DPNPY(data_path).image_list[index]
#         elif format.lower() == 'deepmd/raw':
#             image = DPRAW(data_path).image_list[index]
#         elif format.lower() == 'pwmlff/npy':
#             image = PWNPY(data_path).image_list[index]
#         elif format.lower() == 'meta':
#             image = META(data_path, atom_names, **kwargs).image_list[index]
#         else:
#             raise Exception("Error! The format of the input file is not supported!")
#         return image
    
#     def to(self, output_path, save_format = None, **kwargs):
#         """
#         Write all images (>= 1) object to a new file.

#         Note: Set sort to False for CP2K, because data from CP2K is already sorted!!!. It will result in a wrong order if sort again.

#         Args:
#         output_path (str): Required. The path to save the file.
#         save_format (str): Required. The format of the file. Default is None.

#         Kwargs:

#         Additional keyword arguments for image or multi_image format. (e.g. 'pwmat/config', 'vasp/poscar', 'lammps/lmp', 'pwmat/movement', 'extxyz')

#             * data_name (str): Save name of the configuration file.
#             * sort (bool): Whether to sort the atoms by atomic number. Default is False.
#             * wrap (bool): Whether to wrap the atoms into the simulation box (for pbc). Default is False.
#             * direct (bool): The coordinates of the atoms are in fractional coordinates or cartesian coordinates. (0 0 0) -> (1 1 1)


#         Additional keyword arguments for 'pwmlff/npy' format.

#             * data_name (str): Save name of the dataset folder.
#             * train_ratio (float): Required. The ratio of the training dataset. Default is None. 
#             * train_data_path (str): Save path of the training dataset. Default is "train". ("./output_path/train")
#             * valid_data_path (str): Save path of the validation dataset. Default is "valid". ("./output_path/valid")
#             * random (bool): Whether to shuffle the raw data and then split the data into the training and validation datasets. Default is True.
#             * seed (int): Random seed. Default is 2024.
#             * retain_raw (bool): Whether to retain the raw data. Default is False.

#         """
#         assert save_format is not None, "output file format is not specified"
#         if not os.path.exists(output_path):
#             os.makedirs(output_path)

#         images = self if isinstance(self, Image) else self.images
            
#         if isinstance(images, list):
#             self.multi_to(images, output_path, save_format, **kwargs)
#         else:
#             self.write_image(images, output_path, save_format, **kwargs)
        
#     def multi_to(self, images, output_path, save_format, **kwargs):
#         """
#         Write multiple images to new files.
#         """
#         if save_format.lower() in ['pwmat/config', 'vasp/poscar', 'lammps/lmp']:
#             data_name = kwargs['data_name']
#             for i, image in enumerate(images):
#                 kwargs['data_name'] = data_name + "_{0}".format(i)
#                 self.write_image(image, output_path, save_format, **kwargs)
#         else:
#             self.write_image(images, output_path, save_format, **kwargs)

#     def write_image(self, image, output_path, save_format, **kwargs):
#         if save_format.lower() == 'pwmat/config':
#             write_config(image, output_path, **kwargs)
#         elif save_format.lower() == 'vasp/poscar':
#             write_vasp(image, output_path, **kwargs)
#         elif save_format.lower() == "lammps/lmp":
#             write_lammps(image, output_path, **kwargs)
#         elif save_format.lower() == "pwmat/movement":
#             save_to_movement(image, output_path, **kwargs)
#         elif save_format.lower() == "extxyz":
#             save_to_extxyz(image, output_path, **kwargs)
#         elif save_format.lower() == "pwmlff/npy":
#             save_to_dataset(image, datasets_path=output_path, **kwargs)
#         else:
#             raise RuntimeError('Unknown file format')

def string2index(string: str) -> Union[int, slice, str]:
    """Convert index string to either int or slice"""
    if ':' not in string:
        # may contain database accessor
        try:
            return int(string)
        except ValueError:
            return string
    i: List[Optional[int]] = []
    for s in string.split(':'):
        if s == '':
            i.append(None)
        else:
            i.append(int(s))
    i += (3 - len(i)) * [None]
    return slice(*i)

"""
pwdata convert -i dirs -f extxyz -s dir 
"""
def main(cmd_list:list=None):
    if cmd_list is None:
        cmd_list = sys.argv
    if len(cmd_list) == 2 and '.json' in cmd_list[1].lower():
        json_dict = json.load(open(cmd_list[1]))
        format = json_dict['format']  if 'format' in json_dict.keys() else None
        save_format = json_dict['save_format']  if 'save_format' in json_dict.keys() else None
        raw_files = json_dict['raw_files']
        if not isinstance(raw_files, list):
            raw_files = [raw_files]
        train_valid_ratio = json_dict['train_valid_ratio'] if 'train_valid_ratio' in json_dict.keys() else 1.0
        shuffle =  json_dict['valid_shuffle'] if 'valid_shuffle' in json_dict.keys() else False
        save_dir = json_dict['trainSetDir'] if 'trainSetDir' in json_dict.keys() else 'PWdata'
        cmd_list = ['pwdata', 'convert_configs']
        cmd_list.append('-i')
        cmd_list.extend(raw_files)
        if format is not None:
            cmd_list.extend(['-f', format])
        cmd_list.extend(['-s', save_dir])
        if save_format is not None:
            cmd_list.extend(['-o', save_format])
        else:
            cmd_list.extend(['-o', 'pwmlff/npy'])
        cmd_list.extend(['-p', '{}'.format(train_valid_ratio)])
        if shuffle:
            cmd_list.append('-r')
    if len(cmd_list) == 1 or "-h".upper() == cmd_list[1].upper() or \
        "help".upper() == cmd_list[1].upper() or "-help".upper() == cmd_list[1].upper() or "--help".upper() == cmd_list[1].upper():
        print_cmd()
    elif "scale_cell".upper() == cmd_list[1].upper() or "scale".upper() == cmd_list[1].upper():
        run_scale_cell(cmd_list[2:])
    elif "super_cell".upper() == cmd_list[1].upper() or "super".upper() == cmd_list[1].upper():
        run_super_cell(cmd_list[2:])
    elif "perturb".upper() == cmd_list[1].upper():
        run_pertub(cmd_list[2:])
    elif "convert_config".upper() == cmd_list[1].upper() or "cvt_config".upper() == cmd_list[1].upper():
        run_convert_config(cmd_list[2:])
    elif "convert_configs".upper() == cmd_list[1].upper() or "cvt_configs".upper() == cmd_list[1].upper():
        run_convert_configs(cmd_list[2:])
    elif "count".upper() == cmd_list[1].upper() or "count_configs".upper() == cmd_list[1].upper():
        if '.json' in cmd_list[2].lower():
            json_dict = json.load(open(cmd_list[2]))
            format = json_dict['format']  if 'format' in json_dict.keys() else None
            input = json_dict['datapath'] if 'datapath' in json_dict.keys() else None
            if input is None:
                input = json_dict['raw_files'] if 'raw_files' in json_dict.keys() else None
            cmd_list = ["-i"]
            cmd_list.extend(input)
            if format is not None:
                cmd_list.extend(['-f', format])
            count_configs(cmd_list) # pwdata count extract.json
        else:
            count_configs(cmd_list[2:]) # pwdata count -i inputs -f pwmat/config
            
    else:
        print("\n\nERROR! Input cannot be recognized!\n\n\n")
        print_cmd()

def run_scale_cell(cmd_list:list[str]):
    parser = argparse.ArgumentParser(description='This command is used to scaled the structural lattice.')
    parser.add_argument('-r', '--scale_factor', type=float, required=True, nargs='+', help="floating point number list in (0.0, 1.0), the scaling factor of the unit cell.")
    parser.add_argument('-i', '--input',         type=str, required=True, help='The input file path')
    parser.add_argument('-f', '--input_format',  type=str, required=False, default=None, help="The input file format, the supported format as ['pwmat/config','vasp/poscar', 'lammps/lmp', 'cp2k/scf']")
    parser.add_argument('-s', '--savename',      type=str, required=False, default=None, help="The output file name, and the input scale factor parameter will be used as a prefix, such as '0.99_atom.config'. If not provided, the 'atom.config' for pwmat/config, 'POSCAR' for vasp/poscar, 'lammps.lmp' for lammps/lmp will be used. ")
    parser.add_argument('-o', '--output_format', type=str, required=False, default=None, help="the output file format, only support the format ['pwmat/config','vasp/poscar', 'lammps/lmp']. If not provided, the input format be used. Note: that outputting 'cp2k/scf' format is not supported, the output format will be adjusted to 'pwmat/config' with the output file name 'atom.config'")
    parser.add_argument('-c', '--cartesian', action='store_true', help="if '-c' is set, the cartesian coordinates will be used, otherwise the fractional coordinates will be used. Note: 'pwmlff/npy' only support the fractional, 'extxyz' only support the cartesian!")
    parser.add_argument('-t', '--atom_types',    type=str, required=False, nargs='+', help="the atom type list of 'lammps/lmp' or 'lammps/dump' input file, the order is same as input file", default=None)
    args = parser.parse_args(cmd_list)
    # FORMAT.check_format(args.input_format, FORMAT.support_config_format)
    # if args.savename is None:
    #     args.savename = FORMAT.get_filename_by_format(args.input_format)
    # if args.output_format is None:
    #     if args.input_format == FORMAT.cp2k_scf:
    #         args.output_format = FORMAT.pwmat_config
    #         args.savename = FORMAT.pwmat_config_name
    #         print("Warning: The input format is 'cp2k/scf', the output automatically adjust to to atom.config with format pwmat/config\n")
    #     args.output_format = args.input_format
    # else:
    #     FORMAT.check_format(args.output_format, [FORMAT.pwmat_config, FORMAT.vasp_poscar, FORMAT.lammps_lmp])
    for factor in args.scale_factor:
        assert factor > 0.0 and factor <= 1.0, "The scale factor must be 0 < scale_factor < 1.0"
    do_scale_cell(args.input, args.input_format, args.atom_types, args.savename, args.output_format, args.scale_factor, args.cartesian is False)
    print("scaled the config done!")

def run_super_cell(cmd_list:list[str]):
    parser = argparse.ArgumentParser(description='Construct a supercell based on the input original structure and supercell matrix!')
    parser.add_argument('-m', '--supercell_matrix', nargs='+', type=int, help="Supercell matrix, 3 or 9 values, for example, '2 0 0 0 2 0 0 0 2' or '2 2 2' represents that the supercell is 2x2x2", required=True)
    parser.add_argument('-i', '--input',         type=str, required=True, help='The input file path')
    parser.add_argument('-f', '--input_format',  type=str, required=False, default=None, help="The input file format, the supported format as ['pwmat/config','vasp/poscar', 'lammps/lmp', 'cp2k/scf']")
    parser.add_argument('-s', '--savename',      type=str, required=False, default=None, help="The output file name, if not provided, the 'atom.config' for pwmat/config, 'POSCAR' for vasp/poscar, 'lammps.lmp' for lammps/lmp will be used")
    parser.add_argument('-o', '--output_format', type=str, required=False, default=None, help="the output file format, only support the format ['pwmat/config','vasp/poscar', 'lammps/lmp'], if not provided, the input format be used. \nNote: that outputting cp2k/scf format is not supported. In this case, the default will be adjusted to pwmat atom.config")
    parser.add_argument('-c', '--cartesian', action='store_true', help="if '-c' is set, the cartesian coordinates will be used, otherwise the fractional coordinates will be used.")
    parser.add_argument('-p', '--periodicity', nargs='+', type=int, required=False, help="'-p 1 1 1' indicates that the system is periodic in the x, y, and z directions. The default value is [1,1,1]", default=[1,1,1])
    parser.add_argument('-l', '--tolerance', type=float, required=False, help="Tolerance of fractional coordinates. The default is 1e-5. Prevent slight negative coordinates from being mapped into the simulation box.", default=1e-5)
    parser.add_argument('-t', '--atom_types',    type=str, required=False, nargs='+', help="the atom type list of 'lammps/lmp' or 'lammps/dump' input file, the order is same as input file", default=None)
    args = parser.parse_args(cmd_list)
    # FORMAT.check_format(args.input_format, FORMAT.support_config_format)
    # if args.savename is None:
    #     args.savename = FORMAT.get_filename_by_format(args.input_format)
    # if args.output_format is None:
    #     if args.input_format == FORMAT.cp2k_scf:
    #         args.output_format = FORMAT.pwmat_config
    #         args.savename = FORMAT.pwmat_config_name
    #         print("Warning: The input format is 'cp2k/scf', the output automatically adjust to to atom.config with format pwmat/config\n")
    #     args.output_format = args.input_format
    # else:
    #     FORMAT.check_format(args.output_format, [FORMAT.pwmat_config, FORMAT.vasp_poscar, FORMAT.lammps_lmp])
    assert len(args.supercell_matrix) == 3 or len(args.supercell_matrix) == 9, "The supercell matrix must be 3 or 9 values"
    if len(args.supercell_matrix) == 3:
        args.supercell_matrix = np.diag(args.supercell_matrix)

    do_super_cell(args.input, args.input_format, args.atom_types, args.savename, args.output_format, args.supercell_matrix, args.cartesian is False, pbc=args.periodicity, tol=args.tolerance)
    print("supercell the config done!")


def run_pertub(cmd_list:list[str]):
    parser = argparse.ArgumentParser(description='Disturb the atomic positions and unit cells of the structure!')
    parser.add_argument('-d', '--atom_pert_distance', type=float, default=0, help="The relative movement distance of the atom from its original position. Perturbation is the distance measured in angstroms. For example, 0.01 represents an atomic movement distance of 0.01 angstroms.")
    parser.add_argument('-e', '--cell_pert_fraction', type=float, default=0, help="The degree of deformation of the unit cell. Add randomly sampled values from a uniform distribution within the range of [-cell_pert_fraction, cell_pert_fraction] to each of the 9 lattice values. \nFor example, 0.03, indicating that the degree of deformation of the unit cell is 3% relative to the original unit cell.")
    parser.add_argument('-n', '--pert_num',      type=int, help="The number of generated perturbation structures.", required=True)
    parser.add_argument('-i', '--input',         type=str, required=True, help='The input file path')
    parser.add_argument('-f', '--input_format',  type=str, required=False, default=None, help="The input file format, the supported format as 'pwmat/config','vasp/poscar', 'lammps/lmp', 'cp2k/scf'")
    parser.add_argument('-s', '--savename',      type=str, required=False, default='./pertub', help="The storage path of the structure output after perturbation, the default is './pertub'")
    parser.add_argument('-o', '--output_format', type=str, required=False, default=None, help="the output file format, only support the format ['pwmat/config','vasp/poscar', 'lammps/lmp'], if not provided, the input format be used. \nNote: that outputting cp2k/scf format is not supported. In this case, the default will be adjusted to pwmat atom.config")
    parser.add_argument('-c', '--cartesian', action='store_true', help="if '-d' is set, the cartesian coordinates will be used, otherwise the fractional coordinates will be used.")
    parser.add_argument('-t', '--atom_types',    type=str, required=False, nargs='+', help="the atom type list of 'lammps/lmp' or 'lammps/dump' input file, the order is same as input file", default=None)
    
    args = parser.parse_args(cmd_list)
    # FORMAT.check_format(args.input_format, FORMAT.support_config_format)
    # if args.savename is None:
    #     args.savename = FORMAT.get_filename_by_format(args.input_format)
    # if args.output_format is None:
    #     if args.input_format == FORMAT.cp2k_scf:
    #         args.output_format = FORMAT.pwmat_config
    #         args.savename = FORMAT.pwmat_config_name
    #         print("Warning: The input format is 'cp2k/scf', the output automatically adjust to to atom.config with format pwmat/config\n")
    #     args.output_format = args.input_format
    # else:
    #     FORMAT.check_format(args.output_format, [FORMAT.pwmat_config, FORMAT.vasp_poscar, FORMAT.lammps_lmp])
    perturb_files, perturbed_structs = do_perturb(args.input, 
                args.input_format, 
                args.atom_types, 
                args.savename, 
                FORMAT.get_filename_by_format(args.output_format),
                args.output_format, 
                args.cell_pert_fraction, 
                args.atom_pert_distance,
                args.pert_num,
                args.cartesian is False
                )
    print("pertub the config done!")

def run_convert_config(cmd_list:list[str]):
    parser = argparse.ArgumentParser(description='This command is used for transferring structural files between different apps.')
    parser.add_argument('-i', '--input',         type=str, required=True, help='The input file path')
    parser.add_argument('-f', '--input_format',  type=str, required=False, default=None, help="The input file format, if not specified, the format will be automatically inferred based on the input file. the supported format as ['pwmat/config','vasp/poscar', 'lammps/lmp', 'cp2k/scf']")
    parser.add_argument('-s', '--savename',      type=str, required=False, default=None, help="The output file name, if not provided, the 'atom.config' for pwmat/config, 'POSCAR' for vasp/poscar, 'lammps.lmp' for lammps/lmp will be used")
    parser.add_argument('-o', '--output_format', type=str, required=False, default=None, help="the output file format, only support the format ['pwmat/config','vasp/poscar', 'lammps/lmp'], if not provided, the input format be used. \nNote: that outputting cp2k/scf format is not supported. In this case, the default will be adjusted to pwmat atom.config")
    parser.add_argument('-c', '--cartesian',     action='store_true', help="if '-c' is set, the cartesian coordinates will be used, otherwise the fractional coordinates will be used. 'pwmat/config' only supports fractional coordinates, in which case this parameter becomes invalid")
    parser.add_argument('-t', '--atom_types',    type=str, required=False, default=None, nargs='+', help="the atom type list of 'lammps/lmp' or 'lammps/dump' input file, the order is same as the input file")
    args = parser.parse_args(cmd_list)
    # FORMAT.check_format(args.input_format, FORMAT.support_config_format)
    # if args.savename is None:
    #     args.savename = FORMAT.get_filename_by_format(args.input_format)
    # if args.output_format is None:
    #     if args.input_format == FORMAT.cp2k_scf:
    #         args.output_format = FORMAT.pwmat_config
    #         args.savename = FORMAT.pwmat_config_name
    #         print("Warning: The input format is 'cp2k/scf', the output automatically adjust to to atom.config with format pwmat/config\n")
    #     args.output_format = args.input_format
    # else:
    #     FORMAT.check_format(args.output_format, [FORMAT.pwmat_config, FORMAT.vasp_poscar, FORMAT.lammps_lmp])
    do_convert_config(args.input, args.input_format, args.atom_types, args.savename, args.output_format, args.cartesian is False)
    print("scaled the config done!")

def run_convert_configs(cmd_list:list[str]):
    parser = argparse.ArgumentParser(description='This command is used for transferring structural files between different apps. For extxyz format, all configs will save to one file, \nFor pwmlff/npy, configs with same atom types and atom nums in each type will save to one dir.\n')

    parser.add_argument('-i', '--input',         type=str, required=True, nargs='+', help="The directory or file path of the datas.\nYou can also use JSON file to list all file paths in 'datapath': [], such as 'pwdata/test/meta_data.json'")
    parser.add_argument('-f', '--input_format',  type=str, required=False, default=None, help="The input file format,  if not specified, the format will be automatically inferred based on the input files. the supported format as {}".format(FORMAT.support_images_format))
    parser.add_argument('-s', '--savepath',      type=str, required=False, help="The output dir path, if not provided, the current dir will be used", default="./")
    parser.add_argument('-o', '--output_format', type=str, required=False, default='pwmlff/npy', help="the output file format, only support the format ['pwmlff/npy','extxyz'], if not provided, the 'pwmlff/npy' format be used. ")
    # parser.add_argument('-c', '--cartesian',  action='store_true', help="if '-c' is set, the cartesian coordinates will be used, otherwise the fractional coordinates will be used.")
    parser.add_argument('-p', '--train_valid_ratio', type=float, required=False, default=1.0, help='The division ratio of the training set and test set, such as 0.8, meaning the first 0.8 of the structures are allocated to the training set, and the remaining 0.2 are allocated to the test set. The default=1.0')
    parser.add_argument('-r', '--split_rand', action='store_true', help="Whether to randomly divide the dataset into training and test sets, '-r' is randomly")
    parser.add_argument('-m', '--merge', type=int, required=False, default=1, help="if '-m 1' the output config files will save into one xyzfile. Otherwise, the out configs will be saved separately according to the structural element types. The default value is 1")
    parser.add_argument('-g', '--gap', help='Take a config every gap steps from the middle of the trajectory, default is 1', type=int, default=1)
    parser.add_argument('-q', '--query', type=str, required=False, help='For meta data, advanced query statement, filter Mata data based on query criteria, detailed usage reference http://doc.lonxun.com/PWMLFF/Appendix-2', default=None)
    parser.add_argument('-n', '--cpu_nums', type=int, default=1, required=False, help='For meta data, parallel reading of meta databases using kernel count, default to using all available cores')
    parser.add_argument('-t', '--atom_types',    type=str, required=False, nargs='+', help="For 'lammps/lmp', 'lammps/dump': the atom type list of lammps lmp/dump file, the order is same as lammps dump file.\nFor meta data: Query structures that only exist for that element type", default=None)
    
    args = parser.parse_args(cmd_list)
    try:
        atom_types = get_atomic_name_from_number(args.atom_types)
    except Exception as e:
        atom_types = args.atom_types
    input_list = []
    for _input in args.input:
        if os.path.isfile(_input) and "json" in os.path.basename(_input) and os.path.exists(_input):
                input = json.load(open(_input))['datapath']
                if isinstance(input, str):
                    input = [input]
                input_list.extend(input)
        else:
            assert os.path.exists(_input)
            input_list.append(_input)

    # FORMAT.check_format(args.input_format, FORMAT.support_images_format)
    FORMAT.check_format(args.output_format, [FORMAT.pwmlff_npy, FORMAT.extxyz])

    merge = True if args.merge == 1 else False
    do_convert_images(input_list, args.input_format, args.savepath, args.output_format, args.train_valid_ratio, args.split_rand, args.gap, atom_types, args.query, args.cpu_nums, merge)


def count_configs(cmd_list:list[str]):
    parser = argparse.ArgumentParser(description='This command is used to count the number of input structures\n')
    parser.add_argument('-i', '--input',         type=str, required=True, nargs='+', help="The directory or file path of the datas.\nYou can also use JSON file to list all file paths in 'datapath': [], such as 'pwdata/test/meta_data.json'")
    parser.add_argument('-f', '--input_format',  type=str, required=False, default=None, help="The input file format,  if not specified, the format will be automatically inferred based on the input files. the supported format as {}".format(FORMAT.support_images_format))
    parser.add_argument('-q', '--query', type=str, required=False, help='For meta data, advanced query statement, filter Mata data based on query criteria, detailed usage reference http://doc.lonxun.com/PWMLFF/Appendix-2', default=None)
    parser.add_argument('-n', '--cpu_nums', type=int, default=1, required=False, help='For meta data, parallel reading of meta databases using kernel count, default to using all available cores')
    parser.add_argument('-t', '--atom_types',    type=str, required=False, nargs='+', help="For 'lammps/lmp', 'lammps/dump': the atom type list of lammps lmp/dump file, the order is same as lammps dump file.\nFor meta data: Query structures that only exist for that element type", default=None)
    
    args = parser.parse_args(cmd_list)
    try:
        atom_types = get_atomic_name_from_number(args.atom_types)
    except Exception as e:
        atom_types = args.atom_types
    input_list = []
    for _input in args.input:
        if os.path.isfile(_input) and "json" in os.path.basename(_input) and os.path.exists(_input):
                input = json.load(open(_input))['datapath']
                dicts = json.load(open(_input))
                input = dicts['datapath'] if 'datapath' in dicts.keys() else None
                if input is None:
                    input = dicts['raw_files'] if 'raw_files' in dicts.keys() else None
                if isinstance(input, str):
                    input = [input]
                input_list.extend(input)
        else:
            assert os.path.exists(_input)
            input_list.append(_input)

    do_count_images(input_list, args.input_format, atom_types, args.query, args.cpu_nums)

if __name__ == "__main__":
    main()
