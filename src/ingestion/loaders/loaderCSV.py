from src.ingestion.loaders.loaderBase import LoaderBase
import csv
import json

class LoaderCSV(LoaderBase):

    def __init__(self,filepath:str):
        self.filepath=filepath
    
    def extract_metadata(self):
        raise NotImplementedError
    
    def extract_text(self):
        json_array = []
        with open(self.filepath, 'r') as file:
            csvReader = csv.DictReader(file) 
            for row in csvReader: 
                json_array.append(row)
        text = "\n".join([json.dumps(entry) for entry in json_array])
        return text

    def extract_chunks(self):
        json_array = []
        with open(self.filepath, 'r') as file:
            csvReader = csv.DictReader(file) 
            for row in csvReader: 
                json_array.append(row)
        chunks = [json.dumps(entry) for entry in json_array]
        return chunks
