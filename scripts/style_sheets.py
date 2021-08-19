BLACK_BACKGROUND = "#2b2b2b"
LESSER_BLACK_BACKGROUND = "#3c3f41"
WHITE = "#a9b7c6"
GREEN = "#3aff22"
RED = "red"


wndw_style = "background-color: " + BLACK_BACKGROUND + ";" \
             "font: 10pt JetBrains Mono;" \
             "color: " + WHITE + ";" \

btn_style = "QPushButton {" \
            "   background-color: " + LESSER_BLACK_BACKGROUND + ";" \
            "   border-style: outset;" \
            "    border-width: 2px;" \
            "    border-radius: 10px;" \
            "    border-color: black;" \
            "   font: 10pt JetBrains Mono;" \
            "    color: " + WHITE + ";" \
            "    min-width: 150px;" \
            "    padding: 0px;" \
            "}" \
            "QPushButton:hover {" \
            "    border-color: " + WHITE + ";" \
            "    border-style: inset;}" \
            "QPushButton:pressed {" \
            "    border-color: " + WHITE + ";" \
            "    border-style: inset;}"

btn_style_selected = "QPushButton {" \
                     "   background-color: " + LESSER_BLACK_BACKGROUND + ";" \
                     "   border-style: inset;" \
                     "    border-width: 2px;" \
                     "    border-radius: 10px;" \
                     "    border-color: " + WHITE + ";" \
                     "    font: 10pt JetBrains Mono;" \
                     "    color: " + WHITE + ";" \
                     "    min-width: 150px;" \
                     "    padding: 0px;" \
                     "}" \

btn_style_red = "QPushButton {" \
            "   background-color: " + RED + ";" \
            "   border-style: outset;" \
            "    border-width: 2px;" \
            "    border-radius: 10px;" \
            "    border-color: black;" \
            "    padding: 0px;" \
            "}" \
            "QPushButton:hover {" \
            "    border-color: " + WHITE + ";" \
            "    border-style: inset;}" \
            "QPushButton:pressed {" \
            "    border-color: " + WHITE + ";" \
            "    border-style: inset;}"

btn_style_red_selected = "QPushButton {" \
            "   background-color: " + RED + ";" \
            "   border-style: inset;" \
            "    border-width: 2px;" \
            "    border-radius: 10px;" \
            "    border-color: " + WHITE + ";" \
            "    padding: 0px;" \
            "}" \


btn_style_green = "QPushButton {" \
            "   background-color: " + GREEN + ";" \
            "   border-style: outset;" \
            "    border-width: 2px;" \
            "    border-radius: 10px;" \
            "    border-color: black;" \
            "    padding: 0px;" \
            "}" \
            "QPushButton:hover {" \
            "    border-color: " + WHITE + ";" \
            "    border-style: inset;}" \
            "QPushButton:pressed {" \
            "    border-color: " + WHITE + ";" \
            "    border-style: inset;}"

btn_style_green_selected = "QPushButton {" \
            "   background-color: " + GREEN + ";" \
            "   border-style: inset;" \
            "    border-width: 2px;" \
            "    border-radius: 10px;" \
            "    border-color: " + WHITE + ";" \
            "    padding: 0px;" \
            "}" \


lbl_style = "QLabel {" \
            "   font: 10pt JetBrains Mono;" \
            "   color: " + WHITE + ";}"

lbl_state_style = "QLabel {" \
            "   font: 16pt JetBrains Mono;" \
            "   qproperty-alignment: AlignCenter;" \
            "   color: " + WHITE + ";}"

entry_style = "QLineEdit {" \
            "   font: 10pt JetBrains Mono;" \
            "   color: " + WHITE + ";}"

dsply_txt_style = "QTextEdit {" \
                  "   background-color: " + BLACK_BACKGROUND + ";"\
                  "   font: 12pt JetBrains Mono;" \
                  "   color: " + WHITE + ";}"

progress_bar_style = "QProgressBar {" \
                     "background-color: " + LESSER_BLACK_BACKGROUND + ";"\
                     "border-radius: 15px;" \
                     "color: " + BLACK_BACKGROUND + ";" \
                     "font: 12pt JetBrains Mono;" \
                     "qproperty-alignment: AlignCenter;" \
                     "}" \
                     "QProgressBar::chunk " \
                     "{" \
                     "background-color: " + WHITE + ";" \
                     "border-radius :15px;}"
qmsg_box_style = "QMessageBox{" \
                 "  background-color: " + BLACK_BACKGROUND + ";" \
                 "  font: 10pt JetBrains Mono;" \
                 "  color: " + WHITE + ";}" \
                 "QMessageBox QPushButton{" \
                 "   background-color: " + LESSER_BLACK_BACKGROUND + ";" \
                 "   border-style: outset;" \
                 "   border-width: 2px;" \
                 "   border-radius: 10px;" \
                 "   border-color: black;" \
                 "   font: 10pt JetBrains Mono;" \
                 "   color: " + WHITE + ";" \
                 "   min-width: 50px;" \
                 "   padding: 0px;" \
                 "}" \
                 "QMessageBox QPushButton:hover {" \
                 "    border-color: " + WHITE + ";" \
                 "    border-style: inset;}" \
                 "QMessageBox QPushButton:pressed {" \
                 "    border-color: " + WHITE + ";" \
                 "    border-style: inset;}"
