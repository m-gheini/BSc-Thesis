#!/usr/bin/env python

import PySimpleGUI as sg
import appLogic as func

configToElements = {"inputFile": "-MESSAGE-", "outputName": "-OUT NAME-", "outputPath": "-OUT PATH-",
                    "imCountry": "-IM COUNTRIES-", "imSector": "-IM SECTORS-", "exCountry": "-EX COUNTRIES-",
                    "exSector": "-EX SECTORS-", "shockAmount": "-SHK AMOUNT-"}

enableAfterUpload = ["-SRC SHK IM-", "-SRC SHK EX-", "-SHK SGN POS-", "-SHK SGN NEG-", "-SHK AMOUNT-", "-SHK TO IG-",
                     "-SHK TO FD-", "-SHK STP ITR-", "-SHK STP THR-", "-SCN IM OP1-", "-SCN IM OP2-", "-SCN IM OP3-",
                     "-SCN IM OP4-", "-SCN EX OP1-", "-SCN EX OP2-", "-SCN EX OP3-", "-SCN EX OP4-"]

HEADER_FONT = ("Arial Rounded MT Bold", 25)
BUTTON_FONT = ("Franklin Gothic Book", 10)
FRAME_NAME_FONT = ("Arial Rounded MT Bold", 11)
SUB_FRAME_FONT = ("Arial Rounded MT Bold", 9)
IM_SE_OP1 = "Based on the change of imports, production WOULD CHANGE; therefore, exports would change."
IM_SE_OP2 = "Based on the change of imports, production WOULD NOT CHANGE; therefore, imports would change."
IM_CO_OP1 = "The importer chooses the next best option as an alternative."
IM_CO_OP2 = "The importer chooses other countries/sectors as an alternative"
EX_SE_OP1 = "Based on the change of exports, production WOULD CHANGE; therefore, imports would change."
EX_SE_OP2 = "Based on the change of exports, production WOULD NOT CHANGE; therefore, exports would change."
EX_CO_OP1 = "The exporter chooses the next best option as an alternative."
EX_CO_OP2 = "The exporter chooses other countries/sectors as an alternative"

listDict = {}
# countries = ['AUS', 'AUT', 'BEL', 'CAN', 'CHL', 'CZE', 'DNK', 'EST', 'FIN', 'FRA', 'DEU', 'GRC', 'HUN', 'ISL', 'IRL',
#              'ISR', 'ITA', 'JPN', 'KOR', 'LVA', 'LTU', 'LUX', 'MEX', 'NLD', 'NZL', 'NOR', 'POL', 'PRT', 'SVK', 'SVN',
#              'ESP', 'SWE', 'CHE', 'TUR', 'GBR', 'USA', 'ARG', 'BRA', 'BRN', 'BGR', 'KHM', 'CHN', 'COL', 'CRI', 'HRV',
#              'CYP', 'IND', 'IDN', 'HKG', 'KAZ', 'MYS', 'MLT', 'MAR', 'PER', 'PHL', 'ROU', 'RUS', 'SAU', 'SGP', 'ZAF',
#              'TWN', 'THA', 'TUN', 'VNM', 'ROW']
countries = []
# sectors = ['01T03', '05T06', '07T08', '09', '10T12', '13T15', '16', '17T18', '19', '20T21', '22', '23', '24', '25',
#            '26', '27', '28', '29', '30', '31T33', '35T39', '41T43', '45T47', '49T53', '55T56', '58T60', '61', '62T63',
#            '64T66', '68', '69T82', '84', '85', '86T88', '90T96', '97T98']
sectors = []


def createUploadPlacement():
    uploadProgress = sg.ProgressBar(1000, orientation='h', size=(20, 20), key="-PROGRESS BAR-", visible=False)

    percent = sg.Text("0%", size=(5, 1), key='-PERCENT-', visible=False)

    completeMessage = sg.In(key="-MESSAGE-", visible=False)

    uploadIcon = [sg.Image("./Assets/uploadIcon.png", key="-UPLOAD ICON-", pad=((153, 153), (0, 0)))]

    fileNamePlacement = sg.In(size=(30, 10), enable_events=True, key="-FILE-", visible=False)

    uploadButton = sg.FileBrowse("Upload New Data", font=BUTTON_FONT,
                                 file_types=(("CSV Files", "*.csv"), ("excel Files", "*.xlsx")), initial_folder="C:\\",
                                 key="-CHOOSE-", size=(14, 1))

    defaultFileButton = sg.Button("Use Default Data", font=BUTTON_FONT, key="-DEFAULT-", size=(14, 1))

    uploadFrameContentLayout = [[uploadProgress, percent, completeMessage], uploadIcon,
                                [fileNamePlacement, uploadButton, defaultFileButton]]

    uploadFrameContent = [
        sg.Column(uploadFrameContentLayout, size=(365, 110), element_justification='c', justification='center')]

    uploadFrame = [sg.Frame('Input-Output Table:', [uploadFrameContent], expand_x=True,
                            font=FRAME_NAME_FONT)]

    uploadPlace = sg.Column([uploadFrame], pad=(0, 0), expand_x=True)
    return uploadPlace


def createOutputFilePlacement():
    defineOutFile = sg.Text('Result File Name (without specifying file type):')

    outFileNamePlacement = sg.In(key="-OUT NAME-", size=(19, 1), enable_events=True)

    defineOutPath = sg.Text('Path To Save Result:')

    outPathPlacement = sg.In(key="-OUT PATH-", size=(50, 1), enable_events=True)

    browseButton = sg.FolderBrowse("Browse", font=BUTTON_FONT, initial_folder="C:\\", key="-BROWSE OUT-", size=(10, 1))

    outFrameContentLayout = [[defineOutFile, outFileNamePlacement], [defineOutPath, outPathPlacement, browseButton]]

    outFrameContent = [
        sg.Column(outFrameContentLayout, size=(600, 75))]

    outputFrame = [sg.Frame('Result File:', [outFrameContent], expand_x=True,
                            font=FRAME_NAME_FONT)]

    outPlace = sg.Column([outputFrame], pad=(0, 0), expand_x=True)
    return outPlace


def createImExporterPlacement():
    importerCountryInfo = [[sg.Text('Country', justification='left')],
                           [sg.Combo(countries, default_value='-Select-', key='-IM COUNTRIES-', size=(10, 1),
                                     disabled=True, enable_events=True)]]
    importerSectorInfo = [[sg.Text('Sector', justification='left')],
                          [sg.Combo(sectors, default_value='-Select-', key='-IM SECTORS-', size=(10, 1),
                                    disabled=True, enable_events=True)]]
    importerFrameContent0 = sg.Column(importerCountryInfo)
    importerFrameContent = sg.Column(importerSectorInfo)
    importerFrame = sg.Frame('Importer(Demander):', [[importerFrameContent0, importerFrameContent]], expand_x=True,
                             font=FRAME_NAME_FONT)

    exporterCountryInfo = [[sg.Text('Country', justification='left')],
                           [sg.Combo(countries, default_value='-Select-', key='-EX COUNTRIES-', size=(10, 1),
                                     disabled=True, enable_events=True)]]
    exporterSectorInfo = [[sg.Text('Sector', justification='left')],
                          [sg.Combo(sectors, default_value='-Select-', key='-EX SECTORS-', size=(10, 1),
                                    disabled=True, enable_events=True)]]
    exporterFrameContent0 = sg.Column(exporterCountryInfo)
    exporterFrameContent = sg.Column(exporterSectorInfo)
    exporterFrame = sg.Frame('Exporter(Provider):', [[exporterFrameContent0, exporterFrameContent]], expand_x=True,
                             font=FRAME_NAME_FONT)

    imExporterPlace = sg.Column([[importerFrame, exporterFrame]], pad=(0, 0), expand_x=True)
    return imExporterPlace


def createShockAttrPlacement():
    shockSourcePlacement = sg.Column(
        [[sg.Text('Source Of Shock:'),
          sg.Radio("Importer", "RadioDemo", disabled=True, key="-SRC SHK IM-", enable_events=True),
          sg.Radio("Exporter", "RadioDemo", disabled=True, key="-SRC SHK EX-", enable_events=True)]], expand_x=True)
    space = sg.Column([], size=(90, 1), expand_x=True)

    shockAmountPlacement = sg.Column([[sg.Text("Shock Amount:"),
                                       sg.Radio("+", "RadioDemo1", font='bold', disabled=True, key="-SHK SGN POS-",
                                                enable_events=True),
                                       sg.Radio("--", "RadioDemo1", disabled=True, key="-SHK SGN NEG-",
                                                enable_events=True),
                                       sg.Input(key="-SHK AMOUNT-", size=(10, 1), disabled=True,
                                                enable_events=True),
                                       sg.T("%")]],
                                     expand_x=True)

    shockToPlacement = sg.Column([[sg.Text('Shock To:'),
                                   sg.Radio("Intermediate Goods", "RadioDemo2", disabled=True, key="-SHK TO IG-",
                                            enable_events=True),
                                   sg.Radio("Final Demands", "RadioDemo2", disabled=True, key="-SHK TO FD-",
                                            enable_events=True)]], expand_x=True)
    shockStopPlacement = sg.Column([[sg.Text('Stop At:'),
                                     sg.Radio("Iteration Count", "RadioDemo5", disabled=True, key="-SHK STP ITR-",
                                              enable_events=True),
                                     sg.Input(key="-SHK ITR-", size=(5, 1), disabled=True,
                                              enable_events=True, visible=False),
                                     sg.Radio("Threshold", "RadioDemo5", disabled=True, key="-SHK STP THR-",
                                              enable_events=True),
                                     sg.Input(key="-SHK THR-", size=(5, 1), disabled=True,
                                              enable_events=True, visible=False)
                                     ]], expand_x=True)
    # shockIterationPlacement = sg.Column(
    #     [[sg.Text("Iteration Count:"), sg.Input(key="-SHK ITR-", size=(5, 1), disabled=True,
    #                                             enable_events=True)]],
    #     expand_x=True)
    #
    # shockThresholdPlacement = sg.Column([[sg.Text("Threshold:"), sg.Input(key="-SHK THR-", size=(5, 1), disabled=True,
    #                                                                       enable_events=True)]],
    #                                     expand_x=True)
    shockFrameContentLayout = [[shockSourcePlacement, space, shockAmountPlacement],
                               [shockToPlacement, shockStopPlacement]]

    shockFrameContent = [sg.Column(shockFrameContentLayout, expand_x=True)]

    shockFrame = [sg.Frame('Shock Attributes:', [shockFrameContent], expand_x=True,
                           font=FRAME_NAME_FONT)]

    shockPlace = sg.Column([shockFrame], pad=(0, 0), expand_x=True)
    return shockPlace


def createScenarioPlacement():
    imSideEfLayout = [[sg.T("Side Effects", font=SUB_FRAME_FONT)],
                      [sg.Radio(IM_SE_OP1, "RadioDemo3", disabled=True, key="-SCN IM OP1-",
                                enable_events=True)],
                      [sg.Radio(IM_SE_OP2, "RadioDemo3", disabled=True, key="-SCN IM OP2-",
                                enable_events=True)]]
    imSideEf = sg.Column(imSideEfLayout, expand_x=True)
    imComLayout = [[sg.T("Compensation", font=SUB_FRAME_FONT)],
                   [sg.Radio(IM_CO_OP1, "RadioDemo3", disabled=True, key="-SCN IM OP3-",
                             enable_events=True)],
                   [sg.Radio(IM_CO_OP2, "RadioDemo3", disabled=True, key="-SCN IM OP4-",
                             enable_events=True), sg.Multiline('', disabled=True, key="-IM ALTER-",
                                                               enable_events=True, visible=False)]]
    imCom = sg.Column(imComLayout, expand_x=True)
    importerFrameContent = sg.Column([[imSideEf], [imCom]], expand_x=True)
    importerScenarioFrame = sg.Frame("Scenario For Importer(Demander):", [[importerFrameContent]], expand_x=True,
                                     font=FRAME_NAME_FONT)

    exSideEfLayout = [[sg.T("Side Effects", font=SUB_FRAME_FONT)],
                      [sg.Radio(EX_SE_OP1, "RadioDemo4", disabled=True, key="-SCN EX OP1-",
                                enable_events=True)],
                      [sg.Radio(EX_SE_OP2, "RadioDemo4", disabled=True, key="-SCN EX OP2-",
                                enable_events=True)]]
    exSideEf = sg.Column(exSideEfLayout, expand_x=True)
    exComLayout = [[sg.T("Compensation", font=SUB_FRAME_FONT)],
                   [sg.Radio(EX_CO_OP1, "RadioDemo4", disabled=True, key="-SCN EX OP3-",
                             enable_events=True)],
                   [sg.Radio(EX_CO_OP2, "RadioDemo4", disabled=True, key="-SCN EX OP4-",
                             enable_events=True), sg.Multiline('', disabled=True, key="-EX ALTER-",
                                                               enable_events=True, visible=False)]]
    exCom = sg.Column(exComLayout, expand_x=True)
    exporterFrameContent = sg.Column([[exSideEf], [exCom]])
    exporterScenarioFrame = sg.Frame("Scenario For Exporter(Provider):", [[exporterFrameContent]], expand_x=True,
                                     font=FRAME_NAME_FONT)

    scenarioPlace = sg.Column([[importerScenarioFrame], [exporterScenarioFrame]], pad=(0, 0), expand_x=True)
    return scenarioPlace


dataSection = [createUploadPlacement()]

resultSection = [createOutputFilePlacement()]

imExporterSection = [createImExporterPlacement()]

shockSection = [createShockAttrPlacement()]

scenarioSection = [createScenarioPlacement()]


def makeWindow(theme):
    sg.theme(theme)

    menu_def = [['&File', ['Settings', 'Exit']],
                ['&Help', ['Help', 'About']]]

    # dataLayout = []

    layout = [[sg.Menu(menu_def, key='-MENU-')],
              [sg.Text('Shock Diffusion Tool', size=(38, 1), justification='center', font=HEADER_FONT,
                       relief=sg.RELIEF_RIDGE, k='-TEXT HEADING-', enable_events=True, expand_x=True)],
              [createUploadPlacement()],
              [createOutputFilePlacement()],
              [createImExporterPlacement()],
              [createShockAttrPlacement()],
              [createScenarioPlacement()],
              [sg.Button("Start Shock Diffusion", font=BUTTON_FONT, key="-START-", size=(20, 1),
                         pad=((350, 350), (0, 0)), button_color="green", border_width=3, enable_events=True)]]

    scrollableLayout = [[sg.Column(layout, expand_x=True, expand_y=True, scrollable=True, vertical_scroll_only=True)]]
    return sg.Window('Shock Diffusion Tool', scrollableLayout, resizable=True, auto_size_buttons=False,
                     enable_close_attempted_event=True)


# def findFileName(path):
#     temp = 0
#     lastSlash = 0
#     while temp != -1:
#         lastSlash = temp
#         temp = path.find("/", temp + 1)
#     # dot = path.find(".")
#     return path[(lastSlash + 1):]


def changeLayoutAfterUpload(window, DATA):
    window["-UPLOAD ICON-"].update(visible=False)
    window["-CHOOSE-"].update(visible=False)
    window["-DEFAULT-"].update(visible=False)
    window['-PROGRESS BAR-'].update(visible=True, current_count=0)
    window['-PERCENT-'].update(visible=True)
    for i in range(1000):
        window['-PROGRESS BAR-'].UpdateBar((i + 1))
        window['-PERCENT-'].update(value=f'{(i + 1) / 10:.1f}%')
    window['-PROGRESS BAR-'].update(visible=False, current_count=0)
    window['-PERCENT-'].update(visible=False)
    window["-MESSAGE-"].update(visible=True)
    window["-MESSAGE-"].update(DATA)
    updatedCountries = func.produceCountries(DATA)
    updatedSectors = func.produceSectors(DATA)
    window["-EX COUNTRIES-"].update(disabled=False, values=updatedCountries)
    window["-IM COUNTRIES-"].update(disabled=False, values=updatedCountries)
    window["-EX SECTORS-"].update(disabled=False, values=updatedSectors)
    window["-IM SECTORS-"].update(disabled=False, values=updatedSectors)
    for element in enableAfterUpload:
        window[element].update(disabled=False)


def changeLayoutUsingSavedConfig(window, configData):
    window["-UPLOAD ICON-"].update(visible=False)
    window["-CHOOSE-"].update(visible=False)
    window["-DEFAULT-"].update(visible=False)
    window["-MESSAGE-"].update(visible=True)
    updatedCountries = func.produceCountries(configData["inputFile"])
    updatedSectors = func.produceSectors(configData["inputFile"])
    window["-EX COUNTRIES-"].update(disabled=False, values=updatedCountries)
    window["-IM COUNTRIES-"].update(disabled=False, values=updatedCountries)
    window["-EX SECTORS-"].update(disabled=False, values=updatedSectors)
    window["-IM SECTORS-"].update(disabled=False, values=updatedSectors)
    for element in enableAfterUpload:
        window[element].update(disabled=False)
    for key in configToElements:  # update window with the values read from settings file
        window[configToElements[key]].update(value=configData[key])
    if "shockSrc" in configData:
        if configData["shockSrc"] == "importer":
            window["-SRC SHK IM-"].update(value=True)
        else:
            window["-SRC SHK EX-"].update(value=True)
    if "shockSign" in configData:
        if configData["shockSign"] == "+":
            window["-SHK SGN POS-"].update(value=True)
        else:
            window["-SHK SGN NEG-"].update(value=True)
    if "shockTo" in configData:
        if configData["shockTo"] == "intermediate goods":
            window["-SHK TO IG-"].update(value=True)
        else:
            window["-SHK TO FD-"].update(value=True)
    if "shockStopAttribute" in configData:
        if configData["shockStopAttribute"] == "iteration":
            window["-SHK STP ITR-"].update(value=True)
            window["-SHK THR-"].update(visible=False, disabled=True)
            window["-SHK ITR-"].update(visible=True, disabled=False)
            if "shockItr" in configData:
                window["-SHK ITR-"].update(value=configData["shockItr"])
        else:
            window["-SHK STP THR-"].update(value=True)
            window["-SHK ITR-"].update(visible=False, disabled=True)
            window["-SHK THR-"].update(visible=True, disabled=False)
            if "shockThr" in configData:
                window["-SHK THR-"].update(value=configData["shockThr"])
    if "imScenario" in configData:
        if configData["imScenario"] == "option 1":
            window["-SCN IM OP1-"].update(value=True)
        elif configData["imScenario"] == "option 2":
            window["-SCN IM OP2-"].update(value=True)
        elif configData["imScenario"] == "option 3":
            window["-SCN IM OP3-"].update(value=True)
        else:
            if "imAlter" in configData:
                window["-SCN IM OP4-"].update(value=True)
                window["-IM ALTER-"].update(configData["imAlter"])
                window["-IM ALTER-"].update(disabled=False, visible=True)
    if "exScenario" in configData:
        if configData["exScenario"] == "option 1":
            window["-SCN EX OP1-"].update(value=True)
        elif configData["exScenario"] == "option 2":
            window["-SCN EX OP2-"].update(value=True)
        elif configData["exScenario"] == "option 3":
            window["-SCN EX OP3-"].update(value=True)
        else:
            if "exAlter" in configData:
                window["-SCN EX OP4-"].update(value=True)
                window["-EX ALTER-"].update(configData["exAlter"])
                window["-EX ALTER-"].update(disabled=False, visible=True)


def optionFourLayout(DATA):
    countries = func.produceCountries(DATA)
    sectors = func.produceSectors(DATA)
    # 1
    countryOne = [[sg.Text('Country', justification='left')],
                  [sg.Combo(countries, default_value='-Select-', key='-COUNTRY1-', size=(10, 1),
                            disabled=False, enable_events=True)]]
    sectorOne = [[sg.Text('Sector', justification='left')],
                 [sg.Combo(sectors, default_value='-Select-', key='-SECTOR1-', size=(10, 1),
                           disabled=False, enable_events=True)]]
    percentageOne = [[sg.Text('Percentage', justification='left')],
                     [sg.Input(key='-PERCENT1-', enable_events=True)]]
    optionOne = [sg.Column(countryOne), sg.Column(sectorOne), sg.Column(percentageOne)]
    # 2
    countryTwo = [[sg.Combo(countries, default_value='-Select-', key='-COUNTRY2-', size=(10, 1),
                            disabled=False, enable_events=True)]]
    sectorTwo = [[sg.Combo(sectors, default_value='-Select-', key='-SECTOR2-', size=(10, 1),
                           disabled=False, enable_events=True)]]
    percentageTwo = [[sg.Input(key='-PERCENT2-', enable_events=True)]]
    optionTwo = [sg.Column(countryTwo), sg.Column(sectorTwo), sg.Column(percentageTwo)]
    # 3
    countryThree = [[sg.Combo(countries, default_value='-Select-', key='-COUNTRY3-', size=(10, 1),
                              disabled=False, enable_events=True)]]
    sectorThree = [[sg.Combo(sectors, default_value='-Select-', key='-SECTOR3-', size=(10, 1),
                             disabled=False, enable_events=True)]]
    percentageThree = [[sg.Input(key='-PERCENT3-', enable_events=True)]]
    optionThree = [sg.Column(countryThree), sg.Column(sectorThree), sg.Column(percentageThree)]
    # 4
    countryFour = [[sg.Combo(countries, default_value='-Select-', key='-COUNTRY4-', size=(10, 1),
                             disabled=False, enable_events=True)]]
    sectorFour = [[sg.Combo(sectors, default_value='-Select-', key='-SECTOR4-', size=(10, 1),
                            disabled=False, enable_events=True)]]
    percentageFour = [[sg.Input(key='-PERCENT4-', enable_events=True)]]
    optionFour = [sg.Column(countryFour), sg.Column(sectorFour), sg.Column(percentageFour)]
    layout = [optionOne, optionTwo, optionThree, optionFour]
    return layout


def getDataFromAlterWin(tradeType, event, values):
    if event == '-COUNTRY1-':
        func.getAlternatives(tradeType, "1", "Country", values['-COUNTRY1-'])
    elif event == '-SECTOR1-':
        func.getAlternatives(tradeType, "1", "Sector", values['-SECTOR1-'])
    elif event == '-PERCENT1-':
        print("IN PERCENT")
        func.getAlternatives(tradeType, "1", "Percent", values['-PERCENT1-'])
    elif event == '-COUNTRY2-':
        func.getAlternatives(tradeType, "2", "Country", values['-COUNTRY2-'])
    elif event == '-SECTOR2-':
        func.getAlternatives(tradeType, "2", "Sector", values['-SECTOR2-'])
    elif event == '-PERCENT2-':
        func.getAlternatives(tradeType, "2", "Percent", values['-PERCENT2-'])
    elif event == '-COUNTRY3-':
        func.getAlternatives(tradeType, "3", "Country", values['-COUNTRY3-'])
    elif event == '-SECTOR3-':
        func.getAlternatives(tradeType, "3", "Sector", values['-SECTOR3-'])
    elif event == '-PERCENT3-':
        func.getAlternatives(tradeType, "3", "Percent", values['-PERCENT3-'])
    elif event == '-COUNTRY4-':
        func.getAlternatives(tradeType, "4", "Country", values['-COUNTRY4-'])
    elif event == '-SECTOR4-':
        func.getAlternatives(tradeType, "4", "Sector", values['-SECTOR4-'])
    elif event == '-PERCENT4-':
        func.getAlternatives(tradeType, "4", "Percent", values['-PERCENT4-'])


def main():
    global DATA
    window = makeWindow(sg.theme())
    # layout2 = [[sg.Text('Window 2')],
    #            [sg.Input('')],
    #            [sg.Button('Read')]]

    # DATA = ''
    # outFileName = ''
    # outFilePath = ''
    while True:
        # print("DATA::", DATA)
        event, values = window.read()
        print(event)
        if event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT:
            toSave = sg.popup_yes_no('Do you want to save current project?')
            if toSave == 'No':
                break
            # elif toSave == 'Yes':
            #     filename = sg.popup_get_file('Choose file to save to', save_as=True)

        if event == "-FILE-":
            DATA = values["-FILE-"]
            if DATA != '':
                configData = func.getConfigData(DATA)
                changeLayoutUsingSavedConfig(window, configData)

        elif event == "-DEFAULT-":
            DATA = "./Assets/I_2015.CSV"
            func.getInput(DATA)
            changeLayoutAfterUpload(window, DATA)

        elif event == "-OUT NAME-":
            print("-OUT NAME-")
            outFileName = values["-OUT NAME-"]
            func.getOutName(outFileName)

        elif event == "-OUT PATH-":
            print("-OUT PATH-")
            outFilePath = values["-OUT PATH-"]
            func.getOutPath(outFilePath)
            # if outFileName != '' and outFilePath != '':
            #     print("IN IF")
            #     func.getResultFileAttr(outFileName, outFilePath)

        elif event == "-IM COUNTRIES-":
            imCountry = values["-IM COUNTRIES-"]
            func.getImCountry(imCountry)

        elif event == "-IM SECTORS-":
            imSector = values["-IM SECTORS-"]
            func.getImSector(imSector)

        elif event == "-EX COUNTRIES-":
            exCountry = values["-EX COUNTRIES-"]
            func.getExCountry(exCountry)

        elif event == "-EX SECTORS-":
            exSector = values["-EX SECTORS-"]
            func.getExSector(exSector)

        elif event == "-SRC SHK IM-" or event == "-SRC SHK EX-":
            if values["-SRC SHK IM-"]:
                func.getShockSrc("importer")
            elif values["-SRC SHK EX-"]:
                func.getShockSrc("exporter")

        elif event == "-SHK SGN POS-" or event == "-SHK SGN NEG-":
            if values["-SHK SGN POS-"]:
                func.getShockSign("+")
            elif values["-SHK SGN NEG-"]:
                func.getShockSign("-")

        elif event == "-SHK AMOUNT-":
            amount = values["-SHK AMOUNT-"]
            func.getShockAmount(amount)

        elif event == "-SHK TO IG-" or event == "-SHK TO FD-":
            if values["-SHK TO IG-"]:
                func.getShockTo("intermediate goods")
            elif values["-SHK TO FD-"]:
                func.getShockTo("final demand")

        elif event == "-SHK STP ITR-" or event == "-SHK STP THR-":
            if values["-SHK STP ITR-"]:
                func.getShockStopAttribute("iteration")
                window["-SHK THR-"].update(visible=False, disabled=True)
                window["-SHK ITR-"].update(visible=True, disabled=False)
            elif values["-SHK STP THR-"]:
                func.getShockStopAttribute("threshold")
                window["-SHK ITR-"].update(visible=False, disabled=True)
                window["-SHK THR-"].update(visible=True, disabled=False)

        elif event == "-SHK ITR-":
            itr = values["-SHK ITR-"]
            func.getShockIteration(itr)
            func.getShockThreshold("NOT CHOSEN")

        elif event == "-SHK THR-":
            thr = values["-SHK THR-"]
            func.getShockThreshold(thr)
            func.getShockIteration("NOT CHOSEN")

        elif event == "-SCN IM OP1-" or event == "-SCN IM OP2-" or event == "-SCN IM OP3-" or event == "-SCN IM OP4-":
            if values["-SCN IM OP1-"]:
                func.getImScenario("option 1")
            elif values["-SCN IM OP2-"]:
                func.getImScenario("option 2")
            elif values["-SCN IM OP3-"]:
                func.getImScenario("option 3")
            elif values["-SCN IM OP4-"]:
                func.getImScenario("option 4")
                window2 = sg.Window('My new window', optionFourLayout(DATA), location=(800, 625),
                                    return_keyboard_events=True)
                while True:
                    event2, values2 = window2.read()
                    getDataFromAlterWin("Im", event2, values2)
                    if event2 == sg.WIN_CLOSED:
                        window2.close()
                        window["-IM ALTER-"].update(func.changeDataFromWindowToStr("Im"))
                        window["-IM ALTER-"].update(disabled=False, visible=True)
                        break

        elif event == "-IM ALTER-":
            imAltr = values["-IM ALTER-"]
            func.getImAlternatives(imAltr)

        elif event == "-SCN EX OP1-" or event == "-SCN EX OP2-" or event == "-SCN EX OP3-" or event == "-SCN EX OP4-":
            if values["-SCN EX OP1-"]:
                func.getExScenario("option 1")
            elif values["-SCN EX OP2-"]:
                func.getExScenario("option 2")
            elif values["-SCN EX OP3-"]:
                func.getExScenario("option 3")
            elif values["-SCN EX OP4-"]:
                func.getExScenario("option 4")
                window2 = sg.Window('My new window', optionFourLayout(DATA), location=(800, 625),
                                    return_keyboard_events=True)
                while True:
                    event2, values2 = window2.read()
                    getDataFromAlterWin("Ex", event2, values2)
                    if event2 == sg.WIN_CLOSED:
                        window2.close()
                        window["-EX ALTER-"].update(func.changeDataFromWindowToStr("Ex"))
                        window["-EX ALTER-"].update(disabled=False, visible=True)
                        break

        elif event == "-EX ALTER-":
            exAltr = values["-EX ALTER-"]
            func.getExAlternatives(exAltr)

        elif event == "-START-":
            sg.popup(func.getStartMessage())

    func.welcome()
    print("CLOSE!!")
    window.close()
    exit(0)


if __name__ == '__main__':
    main()
