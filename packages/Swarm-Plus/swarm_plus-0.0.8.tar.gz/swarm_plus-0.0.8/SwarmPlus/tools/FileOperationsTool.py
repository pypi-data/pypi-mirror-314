import sys
sys.dont_write_bytecode =True

import os
import shutil
from pydantic import BaseModel, Field
from typing import List

class SaveFile(BaseModel):
    """
    Use this tool to save content to a file.
    """
    reasoning :str = Field(description="Why you are using this tool")

    file_content: str = Field(
        ..., description="File content to save."
    )
    file_path: str = Field(
        ..., description="File path with proper extension."
    )

    class Config:

        extra = "allow"


    def run(self):
        with open(self.file_path, "w") as f:
            f.write(self.file_content)
        return f"File saved successfully. File name: {self.file_path}",self.context_variables
    
class ReadTextFile(BaseModel):
    """
    Use this tool to read the content of a text file. 
    """
    reasoning : str = Field(description="Why you are using this tool")

    file_name: str = Field(
        ..., description="File name to read."
    )

    class Config:

        extra = "allow"


    def run(self):
        try:
            if self.file_name.endswith((".csv","xlsx")):
                return "To read a excel file you need to write a python script. This tool is just to read text files.",self.context_variables
            with open(self.file_name, "r") as file:
                content = file.read()
            return content,self.context_variables
        except FileNotFoundError:
            return f"File not found: {self.file_name}",self.context_variables
        except Exception as e:
            return f"An error occurred while reading the file: {str(e)}",self.context_variables


class AppendToFile(BaseModel):
    """
    Use this tool to append content to an existing file.
    """
    reasoning : str = Field(description="Why you are using this tool")

    file_name: str = Field(..., description="File name to append to.")
    content: str = Field(..., description="Content to append.")

    class Config:

        extra = "allow"

    def run(self):
        try:
            with open(self.file_name, "a") as file:
                file.write(self.content)
            return f"Content appended to file: {self.file_name}",self.context_variables
        except Exception as e:
            return f"An error occurred while appending to the file: {str(e)}",self.context_variables


class DeleteFile(BaseModel):
    """
    Use this tool to delete a specified file.
    """
    reasoning : str = Field(description="Why you are using this tool")

    file_name: str = Field(..., description="File name to delete.")

    class Config:
        extra = "allow"

    def run(self):
        try:
            os.remove(self.file_name)
            return f"File deleted successfully: {self.file_name}",self.context_variables
        except FileNotFoundError:
            return f"File not found: {self.file_name}",self.context_variables
        except Exception as e:
            return f"An error occurred while deleting the file: {str(e)}",self.context_variables


class ListFilesInDirectory(BaseModel):
    """
    Use this tool to list all files in a specified directory.
    """
    reasoning : str = Field(description="Why you are using this tool")

    directory: str = Field(..., description="Directory to list files from.")

    class Config:
        extra = "allow"

    def run(self):
        try:
            files = os.listdir(self.directory)
            return str(files),self.context_variables
        except FileNotFoundError:
            return f"Directory not found: {self.directory}",self.context_variables
        except Exception as e:
            return f"An error occurred while listing files: {str(e)}",self.context_variables


class MoveFile(BaseModel):
    """
    Use this tool to move a file from one location to another.
    """
    reasoning : str = Field(description="Why you are using this tool")
    source: str = Field(..., description="Source file path.")
    destination: str = Field(..., description="Destination file path.")

    class Config:
        extra = "allow"

    def run(self):
        try:
            shutil.move(self.source, self.destination)
            return f"File moved from {self.source} to {self.destination}",self.context_variables
        except FileNotFoundError:
            return f"File not found: {self.source}",self.context_variables
        except Exception as e:
            return f"An error occurred while moving the file: {str(e)}",self.context_variables


class CopyFile(BaseModel):
    """
    Use this tool to copy a file from one location to another.
    """
    reasoning : str = Field(description="Why you are using this tool")
    source: str = Field(..., description="Source file path.")
    destination: str = Field(..., description="Destination file path.")

    class Config:
        extra = "allow"

    def run(self):
        try:
            shutil.copy(self.source, self.destination)
            return f"File copied from {self.source} to {self.destination}",self.context_variables
        except FileNotFoundError:
            return f"File not found: {self.source}",self.context_variables
        except Exception as e:
            return f"An error occurred while copying the file: {str(e)}",self.context_variables


class GetAvailableFilesandFolders(BaseModel):
    """
    Use this tool to get all the available files and folders starting from a given directory.
    """
    reasoning : str = Field(description="Why you are using this tool")

    directory: str = Field(..., description="Starting directory to get the project structure from.",examples=[".","/project"])

    class Config:
        extra = "allow"

    def run(self):
        try:
            project_structure = ""
            for root, dirs, files in os.walk(self.directory):
                level = root.replace(self.directory, '').count(os.sep)
                indent = ' ' * 4 * level
                project_structure += f"{indent}{os.path.basename(root)}/\n"
                sub_indent = ' ' * 4 * (level + 1)
                for f in files:
                    project_structure += f"{sub_indent}{f}\n"
            return project_structure,self.context_variables
        except FileNotFoundError:
            return f"Directory not found: {self.directory}",self.context_variables
        except Exception as e:
            return f"An error occurred while getting the project structure: {str(e)}",self.context_variables


class CreateFolder(BaseModel):
    """
    Use this tool to create a new folder.
    """
    reasoning : str = Field(description="Why you are using this tool")

    folder_path: str = Field(..., description="Path of the folder to create.")

    class Config:
        extra = "allow"

    def run(self):
        try:
            os.makedirs(self.folder_path, exist_ok=True)
            return f"Folder created successfully: {self.folder_path}",self.context_variables
        except Exception as e:
            return f"An error occurred while creating the folder: {str(e)}",self.context_variables


class DeleteFolder(BaseModel):
    """
    Use this tool to delete a specified folder and its contents.
    """
    reasoning : str = Field(description="Why you are using this tool")

    folder_path: str = Field(..., description="Path of the folder to delete.")

    class Config:
        extra = "allow"

    def run(self):
        try:
            shutil.rmtree(self.folder_path)
            return f"Folder deleted successfully: {self.folder_path}",self.context_variables
        except FileNotFoundError:
            return f"Folder not found: {self.folder_path}",self.context_variables
        except Exception as e:
            return f"An error occurred while deleting the folder: {str(e)}",self.context_variables


class MoveFolder(BaseModel):
    """
    Use this tool to move a folder from one location to another.
    """
    reasoning : str = Field(description="Why you are using this tool")

    source: str = Field(..., description="Source folder path.")
    destination: str = Field(..., description="Destination folder path.")

    class Config:
        extra = "allow"

    def run(self):
        try:
            shutil.move(self.source, self.destination)
            return f"Folder moved from {self.source} to {self.destination}",self.context_variables
        except FileNotFoundError:
            return f"Folder not found: {self.source}",self.context_variables
        except Exception as e:
            return f"An error occurred while moving the folder: {str(e)}",self.context_variables
