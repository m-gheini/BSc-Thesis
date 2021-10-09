#!/usr/bin/env python

import PySimpleGUI as sg

SYMBOL_MORE = '+'
SYMBOL_LESS = 'ـ'
HEADER_FONT = ("Titr", 20)
SECTION_NAME_FONT = ("B Nazanin", 16)
BUTTON_FONT = ("B Nazanin", 12)
SEC1_KEY = '-SECTION1-'
SEC2_KEY = '-SECTION2-'


def createCollapsible(layout, key, title='', arrow=(SYMBOL_LESS, SYMBOL_MORE), collapsed=True):
    sectionName = [sg.T(title, enable_events=True, key=key + '-TITLE-', font=SECTION_NAME_FONT),
                   sg.T((arrow[1] if collapsed else arrow[0]), enable_events=True, k=key + '-BUTTON-',
                        font=SECTION_NAME_FONT)]

    sectionContent = [sg.pin(
        sg.Column(layout, key=key, visible=not collapsed, metadata=arrow), expand_x=True)]

    return sg.Column([sectionName, sectionContent], pad=(0, 0), element_justification='r', expand_x=True)


def createUploadPlacement():
    # infoPlace = [sg.Text()]

    uploadIcon = [sg.Image("Assets/uploadIcon.png", pad=((105, 0), (30, 100)))]

    fileNamePlacement = sg.In(size=(30, 100), enable_events=True, key="-FILE-", visible=False)

    uploadButton = sg.FileBrowse(" انتخاب و آپلود داده ", font=BUTTON_FONT, pad=((105, 0), (30, 0)),
                                 file_types=(("CSV Files", "*.csv"), ("excel Files", "*.xlsx")), initial_folder="C:\\",
                                 key="-CHOOSE-")

    defaultFileButton = [sg.Button(" استفاده از داده پیش فرض ", font=BUTTON_FONT, pad=((105, 0), (30, 0)),
                                   key="-DEFAULT-")]

    uploadFrameContentLayout = [uploadIcon, [fileNamePlacement, uploadButton], defaultFileButton]

    uploadFrameContent = [
        sg.Column(uploadFrameContentLayout, size=(360, 400), element_justification='c', justification='center')]

    uploadFrame = [sg.Frame('', [uploadFrameContent], element_justification='c', expand_x=True)]

    uploadPlace = sg.Column([uploadFrame], pad=(0, 0), expand_x=True)
    return uploadPlace


def createMoreOptionForDataPlace():
    option1 = sg.Checkbox("", pad=((10, 0), (0, 0)))

    option1Text = sg.Text("ادغام تقاضای نهایی مربوط به چین", justification='r', font=BUTTON_FONT,
                          enable_events=True, expand_x=True, pad=((140, 0), (0, 0)))

    option2 = sg.Checkbox("", pad=((10, 0), (0, 0)))

    option2Text = sg.Text("ادغام تقاضای نهایی مربوط به مکزیک", justification='r', font=BUTTON_FONT,
                          enable_events=True, expand_x=True, pad=((140, 0), (0, 0)))

    moreOptionFrameContentLayout = [[option1Text, option1], [option2Text, option2]]

    moreOptionFrameContent = [
        sg.Column(moreOptionFrameContentLayout, size=(360, 400), element_justification='r', justification='right')]

    moreOptionFrame = [sg.Frame('', [moreOptionFrameContent], element_justification='r', expand_x=True)]

    moreOptionPlace = sg.Column([moreOptionFrame], pad=(0, 0), expand_x=True)
    return moreOptionPlace


def createDataLayout():
    moreOptionForDataPlace = createMoreOptionForDataPlace()
    uploadPlace = createUploadPlacement()
    return [moreOptionForDataPlace, uploadPlace]


dataSection = [createDataLayout()]

shockSection = [[sg.I('Input sec 2', k='-IN2-')],
                [sg.I(k='-IN21-')],
                [sg.B('Button section 2', button_color=('yellow', 'purple')),
                 sg.B('Button2 section 2', button_color=('yellow', 'purple')),
                 sg.B('Button3 section 2', button_color=('yellow', 'purple'))]]


def makeWindow(theme):
    sg.theme(theme)

    menu_def = [['&File', ['Settings', 'Exit']],
                ['&Help', ['Help', 'About']]]

    # dataLayout = []

    layout = [[sg.Menu(menu_def, key='-MENU-')],
              [sg.Text('ابزار انتشار شوک', size=(38, 1), justification='center', font=HEADER_FONT,
                       relief=sg.RELIEF_RIDGE, k='-TEXT HEADING-', enable_events=True, expand_x=True)],
              [createCollapsible(dataSection, SEC1_KEY, 'داده')],
              [sg.HorizontalSeparator()],
              [createCollapsible(shockSection, SEC2_KEY, 'شوک و سناریوها')]]
    return sg.Window('Shock Diffusion Tool', layout, resizable=True)


def main():
    window = makeWindow(sg.theme())
    while True:
        event, values = window.read(timeout=100)
        if event in (None, 'Exit'):
            break

        if event.startswith(SEC1_KEY):
            window[SEC1_KEY].update(visible=not window[SEC1_KEY].visible)
            window[SEC1_KEY + '-BUTTON-'].update(
                window[SEC1_KEY].metadata[0] if window[SEC1_KEY].visible else window[SEC1_KEY].metadata[1])

        if event.startswith(SEC2_KEY):
            window[SEC2_KEY].update(visible=not window[SEC2_KEY].visible)
            window[SEC2_KEY + '-BUTTON-'].update(
                window[SEC2_KEY].metadata[0] if window[SEC2_KEY].visible else window[SEC2_KEY].metadata[1])

        if event == "-FILE-":
            file = values["-FILE-"]
            window["-CHOOSE-"].update(visible=False)
            window["-DEFAULT-"].update(visible=False)
            print(file)

    window.close()
    exit(0)


if __name__ == '__main__':
    main()
