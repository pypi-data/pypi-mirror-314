##########################
# __INIT__.PY            #
# The librarys main file #
##########################

# Codes
MIP_SUCCESS = 0x0
MIP_FAILURE = 0x1

from . import project
from . import shell
import os
import re

def build_proj(proj: project.Project) -> int:

    obj_files = []

    """
    Buils the project specified in proj

    Args:
        proj (project.Project): The project that you want to build

    Returns:
        result: MIP_SUCCESS (0) on success and MIP_FAILURE (1) on error
    """

    # Create a new shell
    bs = shell.Shell(name="build shell", shell="/bin/bash")

    if os.path.exists(proj.get_build_dir()) == True:
        bs.execute(f"rm -rf {proj.get_build_dir()}")

    # create the build dir
    bs.execute(f"mkdir -p {proj.get_build_dir()}")
    print("Successfully created the build directory")

    if proj.language is project.Languages.C or proj.language is project.Languages.CXX:
        for file in proj.get_src_files():
            bs.execute(f"{proj.get_compiler()} {' '.join(proj.compile_args)} -c {file} -o {proj.get_build_dir()}/{re.sub(r'^.*/', '', file)}.o")

            obj_files.append(f"{proj.get_build_dir()}/{re.sub(r'^.*/', '', file)}.o")
     
        bs.execute(f"{proj.get_compiler()} {' '.join(obj_files)} -o {proj.get_build_dir()}/{proj.get_executable_name()}")

        if os.path.exists(f"{proj.get_build_dir()}/{proj.get_executable_name()}") == False:
            raise FileNotFoundError(f"The executable {proj.get_build_dir()}/{proj.get_executable_name()} wasnt found!")
    
        print(f"Linked final executable {proj.get_build_dir()}/{proj.get_executable_name()}!")

    elif proj.language is project.Languages.ASM:
        for file in proj.get_src_files():
            bs.execute(f"{proj.get_assembler()} {' '.join(proj.compile_args)}  -felf64 {file} -o {proj.get_build_dir()}/{re.sub(r'^.*/', '', file)}.o")

            obj_files.append(f"{proj.get_build_dir()}/{re.sub(r'^.*/', '', file)}.o")

        bs.execute(f"{proj.get_linker()} {' '.join(proj.link_args)} {' '.join(obj_files)} -o {proj.get_build_dir()}/{proj.get_executable_name()}")

        if os.path.exists(f"{proj.get_build_dir()}/{proj.get_executable_name()}") == False:
            raise FileNotFoundError(f"The executable {proj.get_build_dir()}/{proj.get_executable_name()} wasnt found!")
    
        print(f"Linked final executable {proj.get_build_dir()}/{proj.get_executable_name()}!")


    return MIP_SUCCESS