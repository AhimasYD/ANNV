def clear_layout(layout):
    while layout and layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()
