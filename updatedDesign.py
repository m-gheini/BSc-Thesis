#!/usr/bin/env python

import PySimpleGUI as sg

HEADER_FONT = ("Arial Rounded MT Bold", 25)
BUTTON_FONT = ("Franklin Gothic Book", 10)
FRAME_NAME_FONT = ("Arial Rounded MT Bold", 11)
listDict = {}
countries = ['AUS', 'AUT', 'BEL', 'CAN', 'CHL', 'CZE', 'DNK', 'EST', 'FIN', 'FRA', 'DEU', 'GRC', 'HUN', 'ISL', 'IRL',
             'ISR', 'ITA', 'JPN', 'KOR', 'LVA', 'LTU', 'LUX', 'MEX', 'NLD', 'NZL', 'NOR', 'POL', 'PRT', 'SVK', 'SVN',
             'ESP', 'SWE', 'CHE', 'TUR', 'GBR', 'USA', 'ARG', 'BRA', 'BRN', 'BGR', 'KHM', 'CHN', 'COL', 'CRI', 'HRV',
             'CYP', 'IND', 'IDN', 'HKG', 'KAZ', 'MYS', 'MLT', 'MAR', 'PER', 'PHL', 'ROU', 'RUS', 'SAU', 'SGP', 'ZAF',
             'TWN', 'THA', 'TUN', 'VNM', 'ROW']
sectors = ['01T03', '05T06', '07T08', '09', '10T12', '13T15', '16', '17T18', '19', '20T21', '22', '23', '24', '25',
           '26', '27', '28', '29', '30', '31T33', '35T39', '41T43', '45T47', '49T53', '55T56', '58T60', '61', '62T63',
           '64T66', '68', '69T82', '84', '85', '86T88', '90T96', '97T98']


def createUploadPlacement():
    uploadProgress = sg.ProgressBar(1000, orientation='h', size=(20, 20), key="-PROGRESS BAR-", visible=False,
                                    pad=((65, 0), (20, 0)))

    completeMessage = sg.Text(key="-MESSAGE-", visible=False, pad=((65, 0), (0, 0)))

    uploadIcon = [sg.Image("Assets/uploadIcon.png", key="-UPLOAD ICON-", pad=((153, 153), (0, 0)))]

    fileNamePlacement = sg.In(size=(30, 10), enable_events=True, key="-FILE-", visible=False)

    uploadButton = sg.FileBrowse("Upload New Data", font=BUTTON_FONT,
                                 file_types=(("CSV Files", "*.csv"), ("excel Files", "*.xlsx")), initial_folder="C:\\",
                                 key="-CHOOSE-", size=(14, 1))

    defaultFileButton = sg.Button("Use Default Data", font=BUTTON_FONT, key="-DEFAULT-", size=(14, 1))

    uploadFrameContentLayout = [[uploadProgress, completeMessage], uploadIcon,
                                [fileNamePlacement, uploadButton, defaultFileButton]]

    uploadFrameContent = [
        sg.Column(uploadFrameContentLayout, size=(360, 110), element_justification='c', justification='center')]

    uploadFrame = [sg.Frame('Input-Output Table:', [uploadFrameContent], expand_x=True,
                            font=FRAME_NAME_FONT)]

    uploadPlace = sg.Column([uploadFrame], pad=(0, 0), expand_x=True)
    return uploadPlace


def createOutputFilePlacement():
    defineOutFile = sg.Text('Result File Name:')

    outFileNamePlacement = sg.Input(key='-OUT-NAME-', size=(19, 1))

    defineOutPath = sg.Text('Path To Save Result:')

    outPathPlacement = sg.Input(key='-OUT-PATH-', size=(50, 1))

    browseButton = sg.FolderBrowse("Browse", font=BUTTON_FONT, initial_folder="C:\\", key="-BROWSE-OUT-", size=(10, 1))

    outFrameContentLayout = [[defineOutFile, outFileNamePlacement], [defineOutPath, outPathPlacement, browseButton]]

    outFrameContent = [
        sg.Column(outFrameContentLayout, size=(600, 75))]

    outputFrame = [sg.Frame('Result File:', [outFrameContent], expand_x=True,
                            font=FRAME_NAME_FONT)]

    outPlace = sg.Column([outputFrame], pad=(0, 0), expand_x=True)
    return outPlace


def createImExporterPlacement():
    importerCountryInfo = [[sg.Text('Country', justification='left')],
                           [sg.Combo(countries, default_value='-Select-', key='board', size=(10, 1))]]
    importerSectorInfo = [[sg.Text('Sector', justification='left')],
                          [sg.Combo(sectors, default_value='-Select-', key='board1', size=(10, 1))]]
    importerFrameContent0 = sg.Column(importerCountryInfo)
    importerFrameContent = sg.Column(importerSectorInfo)
    importerFrame = sg.Frame('Importer:', [[importerFrameContent0, importerFrameContent]], expand_x=True,
                             font=FRAME_NAME_FONT)

    exporterCountryInfo = [[sg.Text('Country', justification='left')],
                           [sg.Combo(countries, default_value='-Select-', key='board2', size=(10, 1))]]
    exporterSectorInfo = [[sg.Text('Sector', justification='left')],
                           [sg.Combo(sectors, default_value='-Select-', key='board3', size=(10, 1))]]
    exporterFrameContent0 = sg.Column(exporterCountryInfo)
    exporterFrameContent = sg.Column(exporterSectorInfo)
    exporterFrame = sg.Frame('Exporter:', [[exporterFrameContent0, exporterFrameContent]], expand_x=True,
                             font=FRAME_NAME_FONT)

    imExporterPlace = sg.Column([[importerFrame, exporterFrame]], pad=(0, 0), expand_x=True)
    return imExporterPlace


def createShockAttrPlacement():
    shockFrame = [sg.Frame('Shock Attributes:', [[sg.T("HI")]], expand_x=True,
                           font=FRAME_NAME_FONT)]

    shockPlace = sg.Column([shockFrame], pad=(0, 0), expand_x=True)
    return shockPlace


def createScenarioPlacement():
    scenarioFrame = [sg.Frame('Scenario:', [[sg.T("HI")]], expand_x=True,
                              font=FRAME_NAME_FONT)]

    scenarioPlace = sg.Column([scenarioFrame], pad=(0, 0), expand_x=True)
    return scenarioPlace


# def chooseImporterExporter():
#     importerChoices =
#
# # def createShockDatePlace():
#
# # def createScenarioPlace():
#
# def createShockScenarioLayout():
#     # importerExporterPlace = chooseImporterExporter()
#     # shockDataPlace = createShockDatePlace()
#     # scenarioPlace = createScenarioPlace()
#     # return [importerExporterPlace, shockDataPlace, scenarioPlace]


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
              [dataSection],
              [resultSection],
              [imExporterSection],
              [shockSection],
              [scenarioSection]]
    return sg.Window('Shock Diffusion Tool', layout, resizable=True, auto_size_buttons=False)


def findFileName(path):
    temp = 0
    lastSlash = 0
    while temp != -1:
        lastSlash = temp
        temp = path.find("/", temp + 1)
    # dot = path.find(".")
    return path[(lastSlash + 1):]


def main():
    window = makeWindow(sg.theme())
    DATA = ''
    while True:
        # print("DATA::", DATA)
        event, values = window.read(timeout=100)
        if event in (None, 'Exit'):
            break

        if event == "-FILE-":
            DATA = values["-FILE-"]
            window["-UPLOAD ICON-"].update(visible=False)
            window["-CHOOSE-"].update(visible=False)
            window["-DEFAULT-"].update(visible=False)
            window['-PROGRESS BAR-'].update(visible=True, current_count=0)
            for i in range(1000):
                window['-PROGRESS BAR-'].UpdateBar(i + 1)
            window["-MESSAGE-"].update(visible=True)
            window["-MESSAGE-"].update(findFileName(DATA))

        if event == "-DEFAULT-":
            DATA = "Assets/ICIO2018_2015.CSV"
            window["-UPLOAD ICON-"].update(visible=False)
            window["-CHOOSE-"].update(visible=False)
            window["-DEFAULT-"].update(visible=False)
            window['-PROGRESS BAR-'].update(visible=True, current_count=0)
            for i in range(1000):
                window['-PROGRESS BAR-'].UpdateBar(i + 1)
            window["-MESSAGE-"].update(visible=True)
            window["-MESSAGE-"].update(findFileName(DATA))

    window.close()
    exit(0)


if __name__ == '__main__':
    main()