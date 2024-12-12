try:
    import utillites
except:
    from . import utillites

class HandlerBlock:
    def __init__(self, block_code: str) -> None:
        self.block_code = block_code

    def Handler(self) -> dict:
        element_data = self.__handler_element()
        return element_data
    

    def __handler_element(self) -> dict:
        finder = utillites.Finder(self.block_code)
        elements = finder.find_without_class()
        out_put: dict[str, list] = {}


        for item in elements:
            path = self.__get_item_path(finder=finder, item=item)

            if out_put.get(path) != None:
                out_put[path].append(item)
            else:
                out_put[path] = [item]

        return out_put


    def __get_item_path(self, finder: utillites.Finder, item) -> str:
        out_puts = []
        element_type = "class"
        
        while item != None:
            if element_type:
                name = item.get(element_type)
                if name == None:
                    name = [item.name]

            if name != None:
                out_puts.append(name[0])
            item = item.parent
        
        output_str: str = ""
        out_puts.reverse()
        for out_put in out_puts:
            output_str += f'/{out_put}'

        return output_str[11:]


if __name__ == "__main__":
    block_html = ""
    with open("test.txt", "r") as file:
        block_html = file.read()
    HB = HandlerBlock(block_code=block_html)
    out = HB.Handler()
    print(list(out.keys()))
    