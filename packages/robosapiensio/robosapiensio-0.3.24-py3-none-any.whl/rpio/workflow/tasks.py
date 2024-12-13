# **********************************************************************************
# * Copyright (C) 2024-present Bert Van Acker (B.MKR) <bert.vanacker@uantwerpen.be>
# *
# * This file is part of the roboarch R&D project.
# *
# * RAP R&D concepts can not be copied and/or distributed without the express
# * permission of Bert Van Acker
# **********************************************************************************

from rpio.transformations.transformations import swc2code_py, message2code_py, swc2launch, swc2main, swc2dockerCompose, update_robosapiensIO_ini, add_backbone_config, robochart2aadlmessages, robochart2logical
from rpio.utils.auxiliary import *
from rpio.parsers.parsers import *
from rpio.metamodels.aadl2_IL import *

import configparser

# ------------------------------------------------------------------------------------
# ------------------------------AADL2CODE TASKS --------------------------------------
# ------------------------------------------------------------------------------------
def t_load_design():

    # load name and description from ini
    config = configparser.ConfigParser()
    config.read('../robosapiensIO.ini')
    name=config['RoboSAPIENSIO']['name']
    description = config['RoboSAPIENSIO']['description']

    # load design
    design = system(name=name, description=description,JSONDescriptor='../Design/design.json')    #TODO: load AADL when AADL parser is complete

    return design
def t_generate_messages():
    try:
        # load design
        design = t_load_design()
        # generate messages
        message2code_py(system=design, path="../Realization/ManagingSystem/Messages")
        message2code_py(system=design, path="../Realization/ManagedSystem/Messages")
        return True
    except:
        print("Failed to generate the messages")
        return False


def t_generate_swc_skeletons():
    try:
        # load design
        design = t_load_design()
        # generate swc code skeletons
        swc2code_py(system=design, path="../Realization/ManagingSystem/Nodes")
        return True
    except:
        print("Failed to generate the software components")
        return False


def t_generate_swc_launch():
    try:
        # load design
        design = t_load_design()
        # generate launch files
        swc2launch(system=design.systems[0], path="../Realization/ManagingSystem/Platform")
        swc2launch(system=design.systems[1], path="../Realization/ManagedSystem/Platform")
        return True
    except:
        print("Failed to generate the software component launch files")
        return False

def t_generate_main():
    try:
        # load packageName and prefix from ini
        config = configparser.ConfigParser()
        config.read('../robosapiensIO.ini')
        packageName = config['PACKAGE']['name']
        prefix = config['PACKAGE']['prefix']
        # load design
        design = t_load_design()
        # generate main launch file
        if prefix != "":
            swc2main(system=design.systems[0], package=packageName, prefix=prefix, path="../Resources")
        else:
            swc2main(system=design.systems[0], package=packageName, prefix=None, path="../Resources")
        return True
    except:
        print("Failed to generate the software component main file for the given platforms")
        return False

def t_generate_docker():
    try:
        # load design
        design = t_load_design()
        # generate docker compose file
        swc2dockerCompose(system=design.systems[0], path="../Realization/ManagingSystem/Platform")
        add_backbone_config(system=design, path="../Resources")
        return True
    except:
        print("Failed to generate the docker compose for the given platforms")
        return False

def t_update_robosapiensIO_ini():
    try:
        # load packageName and prefix from ini
        config = configparser.ConfigParser()
        config.read('../robosapiensIO.ini')
        packageName = config['PACKAGE']['name']
        prefix = config['PACKAGE']['prefix']
        # load design
        design = t_load_design()
        # update robosapiensIO ini file
        update_robosapiensIO_ini(system=design,package=packageName,prefix=prefix, path="../")
        return True
    except:
        print("Could not update robosapiensIO.ini")
        return False



# ------------------------------------------------------------------------------------
# --------------------------RoboChart2AADL TASKS -------------------------------------
# ------------------------------------------------------------------------------------

def t_robochart_to_messages():
    try:
        # Parse robochart models
        parser = robochart_parser(MAPLEK='../Concept/MAPLE-K.rct',Monitor='../Concept/Monitor.rct',Analysis='../Concept/Analysis.rct',Plan='../Concept/Plan.rct',Legitimate='../Concept/Legitimate.rct',Execute='../Concept/Execute.rct',Knowledge='../Concept/Knowledge.rct')
        # generate messages
        robochart2aadlmessages(maplek=parser.maplek_model,path='../Design')
        return True
    except:
        print("Failed to generate AADL messages from provided RoboChart models")
        return False

def t_robochart_to_logical():

    try:
        # Parse robochart models
        models_parsed = robochart_parser(MAPLEK='../Concept/MAPLE-K.rct',Monitor='../Concept/Monitor.rct',Analysis='../Concept/Analysis.rct',Plan='../Concept/Plan.rct',Legitimate='../Concept/Legitimate.rct',Execute='../Concept/Execute.rct',Knowledge='../Concept/Knowledge.rct')
        # generate logical architecture
        robochart2logical(parsed=models_parsed,path='../Design')
        print("RoboChart to AADL logical architecture is not implemented yet!")
        return True

    except:
        print("Failed to generate AADL logical architecture from provided RoboChart models")
        return False


# ------------------------------------------------------------------------------------
# ------------------------------ CHECKING TASKS --------------------------------------
# ------------------------------------------------------------------------------------
def t_check_robosapiensio():
    check = check_package_installation(package='robosapiensio')
    return check