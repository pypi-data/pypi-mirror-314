from bs4 import BeautifulSoup


class Finder:
    def __init__(self, html_code: str) -> None:
        self.html_code = BeautifulSoup(html_code, 'html.parser')

    def find_classes(self, type_item, class_name) -> list:
        if class_name:
            return self.html_code.find_all(type_item, class_=class_name)
        else:
            return self.html_code.find_all(class_=True)
    
    def find_without_class(self) ->list:
        return self.html_code.find_all()


        