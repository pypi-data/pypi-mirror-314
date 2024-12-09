##########################################################
# PROJECT.PY                                             #
# Containts structures and functions around the projects #
##########################################################

from enum import Enum
import os

class Languages(Enum):
    C=1,
    CXX=2,
    ASM=3

class Project:
    def __init__(self, name: str, language: Languages):
        # Init the variables from __init__ to self
        self.name = name
        self.language = language

        # Create Files list, empty right now
        self.files = []
        self.compile_args = []
        self.link_args = []

        # Default Varaibles. Can be changed with the appropriate functions
        self.out_dir = "build/"
        self.compiler = "/usr/bin/clang" # clang based
        self.assembler = "/usr/bin/nasm" # nasm is also based
        self.linker = "/usr/bin/ld"

        self.executable = name.lower()
        
    def info(self):
        """
        Prints info about the current project
        """
        print(f"Project Info:")
        print(f"  Name: {self.name}")
        print(f"  Language: {self.language.name}")
        print(f"  Build Dir: {self.out_dir}")
        print(f"  Compiler: {self.compiler}")
        print(f"  Assembler: {self.assembler}")
        print(f"  Linker: {self.linker}")
        print(f"  Source Files: {self.files}")
        print(f"  Executable Name: {self.executable}")

    def add_src_file(self, path: str):
        """
        Adds a source file to the project, that will be compiled or assembeld

        Args:
            path (str): The path to the file (relative or absolute)

        Raises:
            FileNotFoundError: If the file doesnt exists
        """
        if not os.path.isfile(path):
            raise FileNotFoundError(f"The file '{path}' does not exist.")
        
        self.files.append(path)

    def add_src_dir(self, dir_path: str, file_type: str):
        """
        Adds every file with the extension file_type that is located in dir_path and its subfolders to the source files

        Args:
            dir_path (str): Path to the directory with all the files
            file_type (str): The file extension for the files used (e.g. ".c")
        """
        for root, _, files in os.walk(dir_path):
            for file in files:
                if file.endswith(file_type):
                    self.files.append(os.path.join(root, file))


    #
    # Getters and setters
    #

    def get_build_dir(self) -> str:
        """
        Returns the path to the build dir

        Returns:
            out_dir (str): The current build directory
        """
        return self.out_dir # yea i know its called out dir here but stfu
    
    def set_build_dir(self, new_dir: str):
        """
        Sets the new build dir

        Args:
            new_dir (str): The new build directory
        """
        self.out_dir = new_dir

    def get_compiler(self) -> str:
        """
        Returns the path of the compiler binary

        Returns:
            compiler (str): The path to the compiler binary
        """
        return self.compiler
    
    def set_compiler(self, compiler: str):
        """
        Sets the new compiler binary

        Args:
            compiler (str): The path to the new compiler binary
        """
        self.compiler = compiler

    def get_assembler(self) -> str:
        """
        Gets the assembler binary

        Returns:
            assembler (str): The path to the assembler binary
        """
        return self.assembler
    
    def set_assember(self, assembler: str):
        """
        Sets the new assembler binary
        """
        self.assembler = assembler    

    def get_linker(self) -> str:
        """
        Gets the linker binary

        Returns:
            linker (str): The path to the linker binary
        """
        return self.linker
    
    def set_linker(self, linker: str):
        """
        Sets the linker binary

        Args:
            linker (str): The path to the linker binary
        """
        self.linker = linker
    

    def get_src_files(self) -> list:
        """
        Returns the list of the source files

        Returns:
            files (list): The list of added source files
        """
        return self.files
    
    def set_executable_name(self, name: str):
        """
        Sets the name of the final execuatble

        Args:
            name (str): The name of the final executable
        """
        self.executable = name
        
    def get_executable_name(self) -> str:
        """
        Gets the name of the final exeutable

        Returns:
            executable (str): The name of the final executable
        """
        return self.executable
    
    def add_compile_argument(self, argument: str):
        """
        Adds an argument to the compile command

        Args:
            argument (str): The argument to add (with the "-")
        """
        self.compile_args.append(argument)

    def add_link_argument(self, argument: str):
        """
        Adds and argument to the link command. ONLY USED IN ASM PROJECTS RN

        Args:
            argument (str): The argument to add (with the "-")
        """
        self.link_args.append(argument)