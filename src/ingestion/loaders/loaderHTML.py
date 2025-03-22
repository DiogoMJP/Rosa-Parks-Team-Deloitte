from src.ingestion.loaders.loaderBase import LoaderBase
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
        with open("a.txt", "w+", encoding="utf-8") as file:
            file.write(text)
        return text