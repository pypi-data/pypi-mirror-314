# imports
import os
import numpy as np
import pandas as pd
import pickle

from . import rawDataHelper
from . import models


def modelInitilization(parameters, exp):
    '''
    This function is used to initialize the model
    
    Parameters
    ----------------------------------------------------------
    parameters: dict
        The parameters in dictionary format.
    exp: dict
        The experiment dictionary: file_name -> MSData object
    '''

    parameterInit(parameters)

    # Model initialization
    mainModel = models.gpModel()
    # Generate the search space
    print("Generating the search space...")
    mainModel.genSearchSpace(parameters)

    print("Search space contains {} gradient settings.".format(len(mainModel.gridX)))

    # BAGO needs two gradients to initiate the model
    # The first gradient is specified by the user
    # Generate the second gradient if not specified
    if len(parameters["grads"].keys()) == 1:
        print("Only one gradient is specified, the second gradient will be generated to initiate BAGO.")
        parameters["grads"]["Init_2"] = rawDataHelper.computeSecondGradient(parameters, mainModel)

    # output the first and second gradient to csv file
    gtempName = parameters["methodDir"] + "/Init_{}".format(1)
    rawDataHelper.outputConfig(gtempName, parameters["timePoints"], parameters["grads"]["Init_1"])
    gtempName = parameters["methodDir"] + "/Init_{}".format(2)
    rawDataHelper.outputConfig(gtempName, parameters["timePoints"], parameters["grads"]["Init_2"])

    print("First gradient: {}.".format(parameters["grads"]["Init_1"]))
    print("Second gradient: {}.".format(parameters["grads"]["Init_2"]))

    for k in parameters["grads"].keys():
        # if k is not a key in exp
        if k not in exp.keys():
            exp[k] = None
    
    return mainModel


def getNextGradient(exp, parameters, mainModel):
    '''
    This function is used to get the next gradient from the model
    '''

    # Read new MS data
    readNewMSData(exp, parameters)

    # Update the model
    mainModel.updateModel(exp, parameters)

    # Get the next gradient
    nextGrad = np.copy(parameters["grads"]['Init_1'])
    nextGrad[parameters["isChangable"]] = mainModel.computeNextGradient()
    parameters["gradIdx"] += 1

    # Print the next gradient
    print("Next gradient: {}.".format(nextGrad))

    k = "Computed_{}".format(parameters["gradIdx"])
    parameters["grads"][k] = nextGrad
    nextGradName = parameters["methodDir"] + "/" + k
    rawDataHelper.outputConfig(nextGradName, parameters["timePoints"], nextGrad)


def readNewMSData(exp, parameters):
    '''
    This function is used to read new MS data and add them to the experiment dictionary

    Parameters
    ----------------------------------------------------------
    exp: dict
        The experiment dictionary
    parameters: dict
        Global parameters.
    '''

    # Read and process the MS data that have not been processed
    # Obtain file names that end with .mzML or .mzXML
    fileNames = [file for file in os.listdir(parameters['rawDatadir']) if file.endswith('.mzML') or file.endswith('.mzXML')]

    # Read the MS data
    for fn in fileNames:
        # Skip the file if it has been processed
        if fn.split(".")[0] in exp.keys():
            if exp[fn.split(".")[0]] is not None:
                continue
        
        print("Processing file: " + fn)
        fntemp = parameters['rawDatadir']+ "/" + fn
        tempFile = rawDataHelper.MSData()
        tempFile.readRawData(fileName=fntemp, rtRange=parameters["rtRange"])
        tempFile.findTopSignals(parameters=parameters)
        tempFile.computeSepEff(rtRange=parameters["rtRange"])
        
        # Print global separation index with 4 decimal places
        print("Global separation index: {:.4f}".format(tempFile.sepEff))
        exp[fn.split(".")[0]] = tempFile
        print("----------------------------------------------------------------")


def runEvaluation(exp, parameters):
    '''
    This function is used to run the evaluation

    Parameters
    ----------------------------------------------------------
    exp: dict
        The experiment dictionary
    parameters: dict
        Global parameters.
    '''
    
    parameterInit(parameters)
    readNewMSData(exp, parameters)

    # Obtain the global separation index of each data
    sepEffs = [exp[k].sepEff for k in exp.keys()]
    parameters["sepEffs"] = {k: v for k, v in zip(exp.keys(), sepEffs)}

    # Find the key of the data with the highest global separation index
    maxSepEffKey = list(exp.keys())[np.argmax(sepEffs)]

    # Find the number of unique MS/MS spectra
    parameters['uniqueMS2'] = [rawDataHelper.getUniqueMS2(d=exp[k], returnNum=True) for k in exp.keys()]

    if maxSepEffKey in parameters["grads"].keys():
        # Find the gradient setting that gives the highest global separation index
        maxSepEffGrad = parameters["grads"][maxSepEffKey]

        # Print the gradient setting that gives the highest global separation index
        print("The gradient setting that gives the highest global separation index is: {}.".format(maxSepEffGrad))

    else:
        print("The gradient setting that gives the highest global separation index is: {}.".format(maxSepEffKey))

    # Create a data frame of two columns: gradient name, global separation index, and number of unique MS/MS spectra
    df = pd.DataFrame({"Gradient": exp.keys(), "Global separation index": sepEffs, "Unique MS/MS": parameters['uniqueMS2']})

    # Save the data frame to a csv file
    df.to_csv("Evaluation.csv", index=False)


def parameterInit(parameters):
    '''
    This function is used to initialize the parameters.

    Parameters
    ----------------------------------------------------------
    parameters: dict
        Global parameters.
    '''

    # Preprocess the parameters
    if parameters["gradPoints"] is None:
        rawDataHelper.calGradPoints(parameters)
    if parameters["rtRange"] is None:
        parameters["rtRange"] = (parameters["timePoints"][0], parameters["timePoints"][-1])
    # if parameters["isChangable"] is not a numpy array
    if not isinstance(parameters["isChangable"], np.ndarray):
        if parameters["isChangable"] is False:
            parameters["isChangable"] = np.ones(len(parameters["timePoints"]), dtype=bool)
            parameters["isChangable"][np.array([0,1,-1])] = False
        
        else:
            parameters["isChangable"] = np.ones(len(parameters["timePoints"]), dtype=bool)
            parameters["isChangable"][np.array([0,-1])] = False


def saveParameters(parameters, fileName="parameters"):
    '''
    This function is used to save the project using pickle.

    Parameters
    ----------------------------------------------------------
    parameters: dict
        Global parameters.
    fileName: str
        The name of the file to save the parameters.
    '''

    # Save the parameters
    fileName = fileName + ".pkl"
    with open(fileName, "wb") as f:
        pickle.dump(parameters, f)


parametersTemplate = {
    'timePoints': np.array([], dtype=float),
    'rtRange': None,
    'isChangable': False,
    'gradRange': (5.0, 95.0),
    'gradStep': 5,
    'gradPoints': None,
    'mpBound': (35.0, 50.0),
    'grads': {
        'Init_1': np.array([], dtype=float),
    },
    'rawDatadir': "RawData",
    'methodDir': "GradientMethod",
    'sNum': 500,
    'rtTol': 1.0,
    'intTol': 1000,
    'precsMzTol': 0.01,
    'prodMzTol': 0.02,
    'gradIdx': 0,
    'flowRate': None,
    'acqFunc': 'ei',
    'sepEffs': None,
}