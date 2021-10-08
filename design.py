#!/usr/bin/env python

import PySimpleGUI as sg

SYMBOL_MORE = '+'
SYMBOL_LESS = 'ـ'
HEADER_FONT = ("Titr", 20)
SECTION_NAME_FONT = ("B Nazanin", 16)
SEC1_KEY = '-SECTION1-'
SEC2_KEY = '-SECTION2-'


def createCollapsible(layout, key, title='', arrow=(SYMBOL_LESS, SYMBOL_MORE), collapsed=True):
    sectionName = [sg.T(title, enable_events=True, key=key + '-TITLE-', font=SECTION_NAME_FONT),
                   sg.T((arrow[1] if collapsed else arrow[0]), enable_events=True, k=key + '-BUTTON-',
                        font=SECTION_NAME_FONT)]

    sectionContent = [sg.pin(
        sg.Column(layout, key=key, visible=not collapsed, metadata=arrow), expand_x=True)]

    return sg.Column([sectionName, sectionContent], pad=(0, 0), element_justification='r', expand_x=True)


def createDataLayout():
    uploadFrameContentLayout = [
        sg.Listbox(['Account ' + str(i) for i in range(1, 25)], key='-ACCT-LIST-', size=(15, 20))]

    uploadFrameContent = [sg.Column([uploadFrameContentLayout], expand_x=True)]

    uploadFrame = [sg.Frame('', [uploadFrameContent], element_justification='c')]

    # uploadPlace = sg.Column([uploadFrame], pad=(0, 0), expand_x=True)

    # More Options
    # optionFrameContentLayout = [
    #     sg.Listbox(['Account ' + str(i) for i in range(1, 25)], key='-AC-LIST-', size=(15, 20))]
    #
    # optionFrameContent = [sg.Column([optionFrameContentLayout], size=(365, 400))]
    #
    # optionFrame = [sg.Frame('', [optionFrameContent])]
    #
    # optionPlace = sg.Column([optionFrame], pad=(0, 0))

    # return [uploadPlace]
    return [sg.Column([uploadFrame], pad=(0, 0), expand_x=True)]


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

    window.close()
    exit(0)


if __name__ == '__main__':
    main()
