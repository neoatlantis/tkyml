#!/usr/bin/env python3

import yaml
import tkinter
import re

class TKYML(tkinter.Frame):
    
    def __init__(self, master, yamldata):
        tkinter.Frame.__init__(self, master)
        y = yaml.load(yamldata)

        self.__widgetNameCounter = 0

        self._parseYAML(y)

    def _parseYAML(self, y):
        widgets = y["widgets"]
        bindings = y["bind"]
        self._createWidgets(widgets)
        self._bindEvents(bindings)

    def _createWidgets(self, conf):
        for declaration in conf:
            widgetconf = conf[declaration]
            self._createWidget(declaration, widgetconf)

    def __suggestWidgetName(self):
        self.__widgetNameCounter += 1
        return "_widget%d" % self.__widgetNameCounter

    def _createWidget(self, declaration, argv):
        declaration = declaration.strip()

        # ---- 1. parse type specification

        match1 = re.match(
            "^([a-zA-Z]+)\s*\(([0-9,\-\s]+)\)\s*([0-9a-zA-Z_]+)?$",
            declaration
        )
        widgetType, posSpec, widgetName = \
            match1.group(1), match1.group(2), match1.group(3)

        # ---- 2. Widget name

        if not widgetName: widgetName = self.__suggestWidgetName()

        # ---- 3. parse gridding specification(row, col, rowspan, colspan)

        match2 = re.findall("([0-9]+)\s*(\-\s*([0-9]+))?", posSpec)
        rowSpec, colSpec = match2[0:2]
        rowStart, rowEnd = int(rowSpec[0]), int(rowSpec[2] or 0)
        colStart, colEnd = int(colSpec[0]), int(colSpec[2] or 0)
        if rowEnd < rowStart: rowEnd = rowStart
        if colEnd < colStart: colEnd = colStart
        rowspan = rowEnd - rowStart + 1
        colspan = colEnd - colStart + 1

        gridOptions = {
            "row": rowStart,
            "column": colStart,
            "rowspan": rowspan,
            "columnspan": colspan,
        }

        # ---- 4. parse initializing specifications

        configOptions = argv

        

        widget = getattr(tkinter, widgetType)(self)
        widget.grid(**gridOptions)
        widget.config(**configOptions)
        
        # ---- finally, record this widget

        setattr(self, widgetName, widget)

    def _bindEvents(self, bindings):
        def callbackWrapper(callbackName):
            def callback(event):
                if hasattr(self, callbackName):
                    getattr(self, callbackName)(event)
            return callback
                

        def bind(widget, eventName, callbackName):
            eventName = eventName.strip().lower()
            translate = {
                "click": "Button-1",
            }
            if not eventName in translate:
                raise ValueError("Unknown event name: %s" % eventName)
            eventName = translate[eventName]
            widget.bind("<%s>" % eventName, callbackWrapper(callbackName))
            
        for targetWidgetName in bindings:
            targetWidget = getattr(self, targetWidgetName)
            for eventName in bindings[targetWidgetName]:
                callbackName = "%s_%s" % (targetWidgetName, eventName)
                bind(targetWidget, eventName, callbackName)
