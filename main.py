from drafter import *
from dataclasses import dataclass
from random import randint

set_website_title("Water Treatment Process")
set_site_information(
    author="Lillian Emerson",
    description="See overviews of different water treatment processes.",
    sources="Thanks to the Drafter docs.",
    planning=["plan.pdf", "design.pdf"],
    links=["https://github.com/your-username/your-repository"]
)
hide_debug_information()
set_website_framed(False)

@dataclass
class Process:
    name: str
    defn: str
    waterorigin: str
    order: int

@dataclass
class State:
    #groundwater stuff
    testingfor: str
    chemcontaminant: str
    #surfacewater stuff
    filtertype: str
    
surfaceprocess = [Process("Coagulation", "Chemicals are added to water to help bind together dirt and other small particles.", "surface", 1),
                  Process("Flocculation", "The mixing of water to help form larger particles, Chemicals often added to help this.", "surface", 2),
                  Process("Sedimentation", "Separates out solids from water", "surface.", 3),
                  Process("Filtration", "Different pore sized filters are used to remove germs and dissolved particles.", "surface", 4),
                  Process("Disinfection", "Either UV light or chemical disinfectants used to kill any remaining germs.", "surface", 5)
                  ]

groundprocess = [Process("Testing", "Tests for Iron and Manganese, Arsenic, and Hydrogen Sulfide most commonly.", "ground", 1),
                 Process("Chemical Treatment", "Removes chemical contaminants from groundwater.", "ground", 2),
                 Process("Stabilization", "pH gets adjusted by the addition of chemicals to optimal levels.", "ground", 3)
                 ]

wasteprocess = [Process("1st Removal", "Removes trash and particles, and 99% of germs.", "waste", 1),
                     Process("Chemical Removal", "Removes harmful chemicals and improves taste and smell of water.", "waste", 2),
                     Process("Environmental Buffer", "Blended with other water sources, like a reservoir.", "waste", 3)
                     ]

groundwatercontaminants = ["Iron and Manganese", "Arsenic", "Hydrogen Sulfide"]

def contaminant_picker(contaminants:list[str]) -> str:
    indexnum = randint(0,2)
    chem_contmnt = contaminants[indexnum]
    return chem_contmnt

State.chemcontaminant = contaminant_picker(groundwatercontaminants)

#STARTPAGE
@route
def index(state:State) -> Page:
    return Page(state, [
        Header("Water Treatment Processes!"),
        "Welcome! By clicking one of these 3 buttons you can see an overview of how water from different sources gets treated! \n",
        Button("Groundwater", "groundwater"),
        Button("Surface Water", 'surfacewater'),
        Button("Wastewater", 'wastewater')
            ])

#smth wrong with if statements or state attribute updates (idontfeelliketracingthroughitrn)
@route
def groundwater(state:State) -> Page:
    return Page(state, [
        Header("Welcome to the Groundwater Treatment Process!"),
        "An overview: Testing -> Chemical Treatment -> Stabilization \n",
        Button("Testing!", "testing")
        ])

@route
def testing(state: State) -> Page:
    content = [
        Header("Welcome to Testing!"),
        "in this step we will be testing for Iron and Manganese, Arsenic, and Hydrogen Sulfide.\n",
        "Type which of the three types of contaminants you would like to test for first \n",
        TextBox("contaminantname", state.testingfor),
        Button("Submit!", "update_")
        ]
    return Page(state, content)

def test_water(user_says: str, chem_contmnt:str) -> str:
    user_says = user_says.lower()
    if "iron" or "manganese" in user_says:
        if chem_contmnt == "Iron and Manganese":
            return "Iron and Manganese found in water! Treat this in next step!"
        else:
            return "No Iron and Manganese found. Test again!"
        
    if "arsenic" in user_says:
        if chem_contmnt == "Arsenic":
            return "Arsenic found in water! Treat this in next step!"
        else:
            return "No Arsenic found in water. Test again!"
        
    if "hydrogen sulfide" in user_says:
        if chem_contmnt == "Hydrogen Sulfide":
            return "Hydrogen Sulfide found in water! Treat this in next step!"
        else:
            return "No Hydrogen Sulfide found in water. Test again!"
    else:
        return "message unclear. please try again!"

@route
def update_(state:State, contaminantname: str) -> Page:
    state.testingfor = contaminantname #this may be an issue
    test_result = test_water(state.testingfor, state.chemcontaminant)
    if test_result[:1] == "No":
        content = [
            Header("Welcome to Testing!"),
            "in this step we will be testing for Iron and Manganese, Arsenic, and Hydrogen Sulfide.\n",
            "Test type did not match contaminant type. Test for a different chemical!\n",
            TextBox("contaminantname", state.testingfor),
            Button("Submit!", "update_")
            ]
    else:
        content = [
            Header("Welcome to Testing!"),
            "in this step we will be testing for Iron and Manganese, Arsenic, and Hydrogen Sulfide.\n",
            "You found the contaminant! Good job! Remember this for the next step!\n",
            Button("Chemical Treatment!", "chemtreatment")
            ]
    return Page(state, content)

@route
def chemtreatment(state:State) -> Page:
    content = [
        Header("Welcome to Chemical Treatment!"),
        "in this step we will be removing the chemical contaminants from groundwater.\n",
        "Select which contaminant you will be treating the water for! \n",
        Button("Iron and Manganese", "ironmanganese"),
        Button("Arsenic", "arsenic"),
        Button("Hydrogen Sulfide", "hydrosulfide")
        ]
    return Page(state, content)

@route
def ironmanganese(state:State) -> Page:
    if state.chemcontaminant == "Iron and Manganese":
        content = [
        Header("Welcome to Chemical Treatment!"),
        "in this step we will be removing the chemical contaminants from groundwater.\n",
        "Good job! you successfully oxidized the water and then filtered out the metal contaminants!\n",
        Button("Stabilization", "stabilization")
        ]
    else:
        content = [
        Header("Welcome to Chemical Treatment!"),
        "in this step we will be removing the chemical contaminants from groundwater.\n",
        "Oops! That wasnt the correct treatment for your contaminant. Try a different treatment! \n",
        Button("Arsenic", "arsenic"),
        Button("Hydrogen Sulfide", "hydrosulfide")
        ]
    return Page(state, content)

@route
def arsenic(state:State) -> Page:
    if state.chemcontaminant == "Arsenic":
        content = [
        Header("Welcome to Chemical Treatment!"),
        "in this step we will be removing the chemical contaminants from groundwater.\n",
        "Good job! you oxidized the water and then removed the arsenic using coagulation, flocculation, and filtration!\n",
        Button("Stabilization", "stabilization")
        ]
    else:
        content = [
        Header("Welcome to Chemical Treatment!"),
        "in this step we will be removing the chemical contaminants from groundwater.\n",
        "Oops! That wasnt the correct treatment for your contaminant. Try a different treatment! \n",
        Button("Iron and Manganese", "ironmanganese"),
        Button("Hydrogen Sulfide", "hydrosulfide")
        ]
    return Page(state, content)

@route
def hydrosulfide(state:State) -> Page:
    if state.chemcontaminant == "Hydrogen Sulfide":
        content = [
        Header("Welcome to Chemical Treatment!"),
        "in this step we will be removing the chemical contaminants from groundwater.\n",
        "Good job! you aerated and chlorinated the water to remove the Hydrogen Sulfide!\n",
        Button("Stabilization", "stabilization")
        ]
    else:
        content = [
        Header("Welcome to Chemical Treatment!"),
        "in this step we will be removing the chemical contaminants from groundwater.\n",
        "Oops! That wasnt the correct treatment for your contaminant. Try a different treatment! \n",
        Button("Iron and Manganese", "ironmanganese"),
        Button("Arsenic", "arsenic")
        ]
    return Page(state, content)

@route
def stabilization(state:State) -> Page:
    content = [
        Header("Welcome to Chemical Treatment!"),
        "in this step the pH gets adjusted by the addition of chemicals to optimal levels.\n",
        Button("Adjust pH!", "pHchange")
        ]
    return Page(state, content)

@route
def pHchange(state:State) -> Page:
    content = [
        Header("Welcome to Chemical Treatment!"),
        "in this step the pH gets adjusted by the addition of chemicals to optimal levels.\n",
        "Good job! you successfully adjusted the pH to optimal levels by adding chemicals!\n",
        "You successfully completed the Groundwater treatment process! \n",
        Button("Return to Start", "startpage")
        ]
    return Page(state, content)


#SURFACEWATER SECTION
@route
def surfacewater(state:State) -> Page:
    return Page(state, [
        Header("Welcome to the Surface Water Treatment Process!"),
        "An overview: Coagulation -> Flocculation -> Sedimentation -> Filtration -> Disinfection \n",
        Button("Coagulation!", "coagulation")
        ])

@route
def coagulation(state: State) -> Page:
    content = [
        Header("Welcome to Coagulation!"),
        "in this step chemicals are added to water to help bind together dirt and other small particles. \n",
        Button("Add Chemicals!", 'addchemicals')
        ]
    return Page(state, content)

@route
def addchemicals(state:State) -> Page:
    content = [
        Header("Welcome to Coagulation!"),
        "in this step chemicals are added to water to help bind together dirt and other small particles. \n",
        "You added A common coagulant, Aluminum Sulfate, to the water to help coagulation! Good job! \n",
        Button("Flocculation!", "flocculation")
        ]
    return Page(state, content)

@route
def flocculation(state:State) -> Page:
    content = [
        Header("Welcome to Flocculation!"),
        "in this step the water is mixed to help form larger particles. The collection of particles is called a floc! \n",
        Button("Mix Water!", 'mixwater')
        ]
    return Page(state, content)

@route
def mixwater(state:State) -> Page:
    content = [
        Header("Welcome to Flocculation!"),
        "in this step the water is mixed to help form larger particles. The collection of particles is called a floc! \n",
        "Good job! you mixed the water quickly enough to allow floc contact, but not too quick as to break the fragile flocs! \n",
        Button("Sedimentation!", 'sedimentation')
        ]
    return Page(state, content)

@route
def sedimentation(state:State) -> Page:
    content = [
        Header("Welcome to Sedimentation!"),
        "in this step solids get separated out from water via gravity. \n",
        Button("Let that sludge sink!", 'sludgelol')
        ]
    return Page(state, content)

@route
def sludgelol(state:State) -> Page:
    content = [
        Header("Welcome to Sedimentation!"),
        "in this step solids get separated out from water via gravity. \n",
        "Yay! gravity did its job and settled the flocs to the bottom, forming a sludge layer that is removable! \n",
        Button("Filtration!", 'filtration')
        ]
    return Page(state, content)

@route
def filtration(state:State) -> Page:
    content = [
        Header("Welcome to Filtration!"),
        "in this step different pore sized filters are used to remove germs and dissolved particles. \n",
        Button("Filter!", 'filter')
        ]
    return Page(state, content)

#this need linked in helper functions, and needs figureing out text box
@route
def filter(state:State) -> Page:
    content = [
        Header("Welcome to Filtration!"),
        "in this step different pore sized filters are used to remove germs and dissolved particles. \n",
        "There are 3 different filters commonly used in this step, and they are sand, gravel, and activated carbon filters. \n",
        "Which filter do you think we should start with? \n",
        TextBox("filter_", state.filtertype),
        Button("Submit", "submit")
        ]
    return Page(state, content)

@route
def submit(state:State, filter_:str) -> Page:
    state.filtertype = filter_.lower()
    if state.filtertype == "sand":
        pass
    if state.filtertype == "gravel":
        pass
    if state.filtertype == "activated carbon":
        pass
    else:
        return "something doesnt look quite right. Please try again!"
    


#WASTEWATER SECTION
@route
def wastewater(state:State) -> Page:
    return Page(state, [
        Header("Welcome to the Waste Water Treatment Process!"),
        "An overview: First Removal -> Chemical Removal -> Environmental Buffer \n",
        Button("First Removal!", "firstremoval")
        ])

@route
def firstremoval(state:State) -> Page:
    content = [
        Header("Welcome to First Removal!"),
        "in this step trash and particles get removed, along with most of the germs. \n",
        Button("Remove trash!", 'removetrash')
        ]
    return Page(state, content)

@route
def removetrash(state:State) -> Page:
    content = [
        Header("Welcome to First Removal!"),
        "in this step trash and particles get removed, along with most of the germs. \n",
        "Good job! You removed trash, particles, and around 80% of germs in the water!\n",
        Button("Chemical Removal!", 'chemremoval')
        ]
    return Page(state, content)

@route
def chemremoval(state:State) -> Page:
    content = [
        Header("Welcome to Chemical Removal!"),
        "in this step harmful chemicals get removed, and the taste and smell of the water is improved. \n",
        Button("Banish the Chemicals!", 'banishchemicals')
        ]
    return Page(state, content)

@route
def banishchemicals(state:State) -> Page:
    content = [
        Header("Welcome to Chemical Removal!"),
        "in this step harmful chemicals get removed, and the taste and smell of the water is improved. \n",
        "Good job! You removed harmful chemicals from the water and improved smell and taste quality!\n",
        Button("Environmental Buffer!", 'envirobuffer')
        ]
    return Page(state, content)

@route
def envirobuffer(state:State) -> Page:
    content = [
        Header("Welcome to Environmental Buffer!"),
        "in this step treated water is blended with other water sources, like a reservoir. \n",
        "Where would you like to send the treated water? \n",
        SelectBox("choice",
                  ["Reservoir","Aquifer","Groundwater Recharge", "River"]),
        Button("Choose", "choose")
        ]
    return Page(state, content)

#possibly updates a state attribute with the choice and then can display a description of water when it gets there?
@route
def choose(state:State, choice:str) -> Page:
    content = [
        Header("Welcome to Environmental Buffer!"),
        "in this step treated water is blended with other water sources, like a reservoir. \n",
        "Good Job! You successfully completed the Wastewater treatment process! You sent the water to: " + choice + "\n",
        Button("Return to Start", "startpage")
        ]
    return Page(state, content)

@route
def startpage(state:State) -> Page:
    return index(state)

start_server(State("unknown","unknown","unknown"))

