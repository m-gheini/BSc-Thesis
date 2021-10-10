#!/usr/bin/env python

import PySimpleGUI as sg

HEADER_FONT = ("Arial Rounded MT Bold", 25)
BUTTON_FONT = ("Franklin Gothic Book", 12)
FRAME_NAME_FONT = ("Arial Rounded MT Bold", 11)


def createUploadPlacement():
    uploadProgress = sg.ProgressBar(1000, orientation='h', size=(20, 20), key="-PROGRESS BAR-", visible=False,
                                    pad=((65, 0), (20, 0)))

    completeMessage = sg.Text(key="-MESSAGE-", visible=False, pad=((65, 0), (0, 0)))

    uploadIcon = [sg.Image("Assets/uploadIcon.png", key="-UPLOAD ICON-", pad=((153, 153), (0, 0)))]

    fileNamePlacement = sg.In(size=(30, 10), enable_events=True, key="-FILE-", visible=False)

    uploadButton = sg.FileBrowse("Upload New Data", font=BUTTON_FONT,
                                 file_types=(("CSV Files", "*.csv"), ("excel Files", "*.xlsx")), initial_folder="C:\\",
                                 key="-CHOOSE-")

    defaultFileButton = sg.Button("Use Default Data", font=BUTTON_FONT, key="-DEFAULT-")

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

    # uploadButton = sg.FileBrowse("Upload New Data", font=BUTTON_FONT,
    #                              file_types=(("CSV Files", "*.csv"), ("excel Files", "*.xlsx")), initial_folder="C:\\",
    #                              key="-CHOOSE-")

    outFrameContentLayout = [[defineOutFile, outFileNamePlacement], [defineOutPath, outPathPlacement]]

    outFrameContent = [
        sg.Column(outFrameContentLayout, size=(360, 110))]

    outputFrame = [sg.Frame('Result File:', [outFrameContent], expand_x=True,
                            font=FRAME_NAME_FONT)]

    outPlace = sg.Column([outputFrame], pad=(0, 0), expand_x=True)
    return outPlace


# def createMoreOptionForDataPlace():
#     option1 = sg.Checkbox("", pad=((10, 0), (0, 0)))
#
#     option1Text = sg.Text("ادغام تقاضای نهایی مربوط به چین", justification='r', font=BUTTON_FONT,
#                           enable_events=True, expand_x=True, pad=((140, 0), (0, 0)))
#
#     option2 = sg.Checkbox("", pad=((10, 0), (0, 0)))
#
#     option2Text = sg.Text("ادغام تقاضای نهایی مربوط به مکزیک", justification='r', font=BUTTON_FONT,
#                           enable_events=True, expand_x=True, pad=((140, 0), (0, 0)))
#
#     moreOptionFrameContentLayout = [[option1Text, option1], [option2Text, option2]]
#
#     moreOptionFrameContent = [
#         sg.Column(moreOptionFrameContentLayout, size=(360, 400), element_justification='r', justification='right')]
#
#     moreOptionFrame = [sg.Frame('', [moreOptionFrameContent], element_justification='r', expand_x=True)]
#
#     moreOptionPlace = sg.Column([moreOptionFrame], pad=(0, 0), expand_x=True)
#     return moreOptionPlace


def createDataLayout():
    # moreOptionForDataPlace = createMoreOptionForDataPlace()
    uploadPlace = createUploadPlacement()
    # return [moreOptionForDataPlace, uploadPlace]
    return [uploadPlace]


def createShockAttrPlacement():
    shockFrame = [sg.Frame('Parameters And Shock Attributes:', [[sg.T("HI")]], expand_x=True,
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


dataSection = [createDataLayout()]

resultSection = [createOutputFilePlacement()]

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
              [shockSection],
              [scenarioSection]]
    return sg.Window('Shock Diffusion Tool', layout, resizable=True)


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
        print("DATA::", DATA)
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
