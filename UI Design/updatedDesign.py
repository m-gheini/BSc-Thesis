#!/usr/bin/env python

import PySimpleGUI as sg

HEADER_FONT = ("Arial Rounded MT Bold", 25)
BUTTON_FONT = ("Franklin Gothic Book", 10)
FRAME_NAME_FONT = ("Arial Rounded MT Bold", 11)
SUB_FRAME_FONT = ("Arial Rounded MT Bold", 9)
IM_SE_OP1 = "Based on the change of imports, production WOULD CHANGE; therefore, exports would change."
IM_SE_OP2 = "Based on the change of imports, production WOULD NOT CHANGE; therefore, imports would change."
IM_CO_OP1 = "The importer chooses the next best option as an alternative."
IM_CO_OP2 = "The importer chooses the front list as an alternative"
EX_SE_OP1 = "Based on the change of exports, production WOULD CHANGE; therefore, imports would change."
EX_SE_OP2 = "Based on the change of exports, production WOULD NOT CHANGE; therefore, exports would change."
EX_CO_OP1 = "The exporter chooses the next best option as an alternative."
EX_CO_OP2 = "The exporter chooses the front list as an alternative"

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
    uploadProgress = sg.ProgressBar(100, orientation='h', size=(20, 20), key="-PROGRESS BAR-", visible=False)

    percent = sg.Text("  0%", size=(4, 1), key='-PERCENT-', visible=False)

    completeMessage = sg.In(key="-MESSAGE-", visible=False)

    uploadIcon = [sg.Image("../Assets/uploadIcon.png", key="-UPLOAD ICON-", pad=((153, 153), (0, 0)))]

    fileNamePlacement = sg.In(size=(30, 10), enable_events=True, key="-FILE-", visible=False)

    uploadButton = sg.FileBrowse("Upload New Data", font=BUTTON_FONT,
                                 file_types=(("CSV Files", "*.csv"), ("excel Files", "*.xlsx")), initial_folder="C:\\",
                                 key="-CHOOSE-", size=(14, 1))

    defaultFileButton = sg.Button("Use Default Data", font=BUTTON_FONT, key="-DEFAULT-", size=(14, 1))

    uploadFrameContentLayout = [[uploadProgress, percent, completeMessage], uploadIcon,
                                [fileNamePlacement, uploadButton, defaultFileButton]]

    uploadFrameContent = [
        sg.Column(uploadFrameContentLayout, size=(360, 110), element_justification='c', justification='center')]

    uploadFrame = [sg.Frame('Input-Output Table:', [uploadFrameContent], expand_x=True,
                            font=FRAME_NAME_FONT)]

    uploadPlace = sg.Column([uploadFrame], pad=(0, 0), expand_x=True)
    return uploadPlace


def createOutputFilePlacement():
    defineOutFile = sg.Text('Result File Name:')

    outFileNamePlacement = sg.Input(key='-OUT NAME-', size=(19, 1))

    defineOutPath = sg.Text('Path To Save Result:')

    outPathPlacement = sg.Input(key='-OUT PATH-', size=(50, 1))

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
    shockSourcePlacement = sg.Column([[sg.Text('Source Of Shock:'), sg.Radio("Importer", "RadioDemo"),
                                       sg.Radio("Exporter", "RadioDemo")]], expand_x=True)
    space = sg.Column([], size=(90, 1), expand_x=True)

    shockAmountPlacement = sg.Column([[sg.Text("Shock Amount:"), sg.Radio("+", "RadioDemo1", font='bold'),
                                       sg.Radio("--", "RadioDemo1"), sg.Input(key="-SHK-AMNT-", size=(10, 1))]],
                                     expand_x=True)

    shockToPlacement = sg.Column([[sg.Text('Shock To:'), sg.Radio("Intermediate Goods", "RadioDemo2"),
                                   sg.Radio("Final Demands", "RadioDemo2")]], expand_x=True)

    shockIterationPlacement = sg.Column([[sg.Text("Iteration Count:"), sg.Input(key="-SHK-ITR-", size=(5, 1))]],
                                        expand_x=True)

    shockThresholdPlacement = sg.Column([[sg.Text("Threshold:"), sg.Input(key="-SHK-THR-", size=(5, 1))]],
                                        expand_x=True)
    shockFrameContentLayout = [[shockSourcePlacement, space, shockAmountPlacement],
                               [shockToPlacement, shockIterationPlacement, shockThresholdPlacement]]

    shockFrameContent = [sg.Column(shockFrameContentLayout, expand_x=True)]

    shockFrame = [sg.Frame('Shock Attributes:', [shockFrameContent], expand_x=True,
                           font=FRAME_NAME_FONT)]

    shockPlace = sg.Column([shockFrame], pad=(0, 0), expand_x=True)
    return shockPlace


def createScenarioPlacement():
    imSideEfLayout = [[sg.T("Side Effects", font=SUB_FRAME_FONT)], [sg.Radio(IM_SE_OP1, "RadioDemo3")],
                      [sg.Radio(IM_SE_OP2, "RadioDemo3")]]
    imSideEf = sg.Column(imSideEfLayout, expand_x=True)
    imComLayout = [[sg.T("Compensation", font=SUB_FRAME_FONT)], [sg.Radio(IM_CO_OP1, "RadioDemo3")],
                   [sg.Radio(IM_CO_OP2, "RadioDemo3"), sg.Multiline('')]]
    imCom = sg.Column(imComLayout, expand_x=True)
    importerFrameContent = sg.Column([[imSideEf], [imCom]], expand_x=True)
    importerScenarioFrame = sg.Frame("Scenario For Importer:", [[importerFrameContent]], expand_x=True,
                                     font=FRAME_NAME_FONT)

    exSideEfLayout = [[sg.T("Side Effects", font=SUB_FRAME_FONT)], [sg.Radio(EX_SE_OP1, "RadioDemo4")],
                      [sg.Radio(EX_SE_OP2, "RadioDemo4")]]
    exSideEf = sg.Column(exSideEfLayout, expand_x=True)
    exComLayout = [[sg.T("Compensation", font=SUB_FRAME_FONT)], [sg.Radio(EX_CO_OP1, "RadioDemo4")],
                   [sg.Radio(EX_CO_OP2, "RadioDemo4"), sg.Multiline('')]]
    exCom = sg.Column(exComLayout, expand_x=True)
    exporterFrameContent = sg.Column([[exSideEf], [exCom]])
    exporterScenarioFrame = sg.Frame("Scenario For Exporter:", [[exporterFrameContent]], expand_x=True,
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
              [createScenarioPlacement()]]

    scrollableLayout = [[sg.Column(layout, expand_x=True, expand_y=True, scrollable=True, vertical_scroll_only=True)]]
    return sg.Window('Shock Diffusion Tool', scrollableLayout, resizable=True, auto_size_buttons=False)


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
    for i in range(100):
        window['-PROGRESS BAR-'].UpdateBar(i + 1)
        window['-PERCENT-'].update(value=f'{i + 1:>3d}%')
    window['-PROGRESS BAR-'].update(visible=False, current_count=0)
    window['-PERCENT-'].update(visible=False)
    window["-MESSAGE-"].update(visible=True)
    window["-MESSAGE-"].update(DATA)


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
            if DATA != '':
                changeLayoutAfterUpload(window, DATA)

        if event == "-DEFAULT-":
            DATA = "../Assets/ICIO2018_2015.CSV"
            changeLayoutAfterUpload(window, DATA)

    window.close()
    exit(0)


if __name__ == '__main__':
    main()
