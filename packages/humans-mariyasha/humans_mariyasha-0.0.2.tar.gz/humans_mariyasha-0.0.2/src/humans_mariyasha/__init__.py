## Welcome to the Humans Library
########################################
## by: Mariya Sha

########################################
## classes
########################################

class Father:
    def __init__(self):
        self.name = ""
        self.wife = []
        self.children = {}
        self.n_children = self.get_n_children()
    
    def get_n_children(self):
        n_children = sum([
            len(i) for i in self.children.values()
        ])
        return n_children
    
class Abraham(Father):
    def __init__(self):
        self.name = "Abraham"
        self.wife = ["Sarah", "Keturah"]
        self.children = {
            "Sarah": ["Isaac"],
            "Hagar": ["Ishmael"],
            "Keturah": ["Zimran", "Jokshan", "Medan", "Midian", "Ishbak", "Shuah"]
        }
        self.n_children = self.get_n_children()
    
class Isaac(Father):
    def __init__(self):
        self.name = "Isaac"
        self.wife = ["Rebecca"]
        self.children = {
            "Rebecca": ["Esau", "Jacob"]
        }
        self.n_children = self.get_n_children()
        
class Jacob(Father):
    def __init__(self):
        self.name = "Jacob"
        self.wife = ["Leah", "Rachel"]
        self.children = {
            "Leah": ["Reuben", "Simeon", "Levi", "Judah", "Issachar", "Zebulun", "Dinah"],
            "Rachel": ["Joseph", "Benjamin"],
            "Bilhah": ["Dan", "Naphtali"],
            "Zilpah": ["Gad", "Asher"]
        }
        self.n_children = self.get_n_children()

class Joseph(Father):
    def __init__(self):
        self.name = "Joseph"
        self.wife = ["Asenath"]
        self.children = {
            "Asenath": ["Ephraim", "Manasseh"]
        }
        self.n_children = self.get_n_children()
        
########################################
## functions
########################################

def read_humans(kind):
    """
    - input: string of either [fathers, mothers, children, all]
    - output: list of matching humans
    """
    
    abraham = Abraham()
    isaac = Isaac()
    jacob = Jacob()
    joseph = Joseph()
    
    fathers = [abraham, isaac, jacob, joseph]
    fathers_name = [i.name for i in fathers]
    
    mothers = sum([i.wife for i in fathers], [])
    children = sum([sum(i.children.values(), []) for i in fathers], [])
    
    if kind == "fathers":
        return sorted(fathers_name)
    if kind == "mothers":
        return sorted(mothers)
    if kind == "children":
        return sorted(children)
    if kind == "all":
        return sorted(list(set(fathers_name + mothers + children)))
    return None

########################################
## variables
########################################

fathers = read_humans("fathers")
mothers = read_humans("mothers")
children = read_humans("children")
all_humans = read_humans("all")

    
