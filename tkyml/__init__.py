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

        if isinstance(master, tkinter.Tk):
            self.pack(fill="both", expand=1)

    def _parseYAML(self, y):
        self._createWidgets(self, y["widgets"])
        self._configGrids(y["grids"])
        self._bindEvents(y["bind"])

    def _configGrids(self, conf):
        for targetName in conf:
            subconf = conf[targetName]
            if targetName == '__root__':
                target = self
            else:
                target = getattr(self, targetName)
            if "rows" in subconf:
                for i in subconf["rows"]:
                    target.grid_rowconfigure(int(i), **subconf["rows"][i])
            if "cols" in subconf:
                for i in subconf["cols"]:
                    target.grid_columnconfigure(int(i), **subconf["cols"][i])

    def _createWidgets(self, master, conf):
        for declaration in conf:
            widgetconf = conf[declaration]
            self._createWidget(master, declaration, widgetconf)

    def __suggestWidgetName(self):
        self.__widgetNameCounter += 1
        return "_widget%d" % self.__widgetNameCounter

    def _createWidget(self, master, declaration, argv):
        """Create the configured widgets and associate them to the class as
        attributes."""

        declaration = declaration.strip()

        # ---- 1. parse type specification

        try:
            match1 = re.match(
                "^([a-zA-Z]+)\s*\(([0-9,\-\s]+)\)(\(([NSWE]{1,4})\))?\s*([0-9a-zA-Z_]+)?$",
                declaration
            )
            widgetType, posSpec, stickySpec, widgetName = \
                match1.group(1), match1.group(2),\
                match1.group(4), match1.group(5)
        except:
            raise ValueError("Invalid widget declaration: %s" % declaration)

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
        if stickySpec: gridOptions["sticky"] = stickySpec

        # ---- 4. parse initializing specifications

        configOptions = argv or {}
        containedDeclarations = None
        if "contains" in configOptions:
            containedDeclarations = configOptions["contains"]
            del configOptions["contains"]

        widget = getattr(tkinter, widgetType)(master)
        widget.grid(**gridOptions)
        widget.config(**configOptions)

        if containedDeclarations:
            self._createWidgets(widget, containedDeclarations)
        
        # ---- finally, record this widget

        setattr(self, widgetName, widget)

    def _bindEvents(self, bindings):
        if not bindings: return

        def callbackWrapper(callbackName):
            def callback(event):
                if hasattr(self, callbackName):
                    getattr(self, callbackName)(event)
            return callback
                
        def bind(widget, eventName, callbackName):
            eventName = eventName.strip().lower()
            translate = {
                "click": "Button-1",
                "dblclick": "Double-Button-1",
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
