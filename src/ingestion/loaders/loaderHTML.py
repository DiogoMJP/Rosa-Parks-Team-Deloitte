from src.ingestion.loaders.loaderBase import LoaderBase
from src.ingestion.chunking.token_chunking import text_to_chunks
import html2text

class LoaderHTML(LoaderBase):

    def __init__(self,filepath:str):
        self.filepath=filepath
    

    def extract_metadata(self):
        raise NotImplementedError
    
    def extract_text(self):
        text_maker = html2text.HTML2Text()
        text_maker.ignore_links = True
        text_maker.bypass_tables = False
        html = "".join(open(self.filepath, "r", encoding="utf-8").readlines())
        text = text_maker.handle(html)
        return text
    
    def extract_chunks(self):
        text = self.extract_text()
        return text_to_chunks(text)