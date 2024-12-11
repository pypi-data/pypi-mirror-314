from dataclasses import dataclass
import csv
import glob
import os
import typing
 
 
@dataclass
class IterPathsCsvDir:
    path: str
 
    def __post_init__(self) -> None:
        self.csv_file_paths = glob.glob(os.path.join(self.path, '*.csv'))
        self.reader = self.dict_rows()
       
    def dict_rows(self) -> typing.Generator[tuple[str, dict], None, None]:
        for path in self.csv_file_paths:
            with open(path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    yield path, row
           
    def __next__(self) -> tuple[str, dict]:
        return next(self.reader)
 
    def __iter__(self):
        return self
 
 
class IterNamesCsvDir(IterPathsCsvDir):
    def dict_rows(self) -> typing.Generator[tuple[str, dict], None, None]:
        for full_path, row in IterPathsCsvDir.dict_rows(self):
            yield os.path.basename(full_path), row
 
 
class IterCsvDir(IterPathsCsvDir):
    def dict_rows(self) -> typing.Generator[dict, None, None]:
        for _, row in IterPathsCsvDir.dict_rows(self):
            yield row
           
    def __next__(self) -> dict:
        return next(self.reader)
 
 
 
@dataclass
class CsvDir:
    path: str | None = None
 
    def __post_init__(self) -> None:
        if self.path is None:
            self.path = os.getcwd()
 
    def __iter__(self) -> IterCsvDir:
        return IterCsvDir(self.path)
 
    def names(self) -> IterNamesCsvDir:
        return IterNamesCsvDir(self.path)
 
    def paths(self) -> IterNamesCsvDir:
        return IterPathsCsvDir(self.path)
    

def read_dir(path: str | None = None) -> CsvDir:
    return CsvDir(path)