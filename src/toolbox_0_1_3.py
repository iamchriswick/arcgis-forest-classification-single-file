import arcpy

class MyTool(object):
    def getParameterInfo(self):
        choice = arcpy.Parameter(
            displayName="Choice",
            name="choice",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        # Static dropdown:
        choice.filter.list = ["OptionA", "OptionB", "OptionC"]
        choice.value = "OptionA"

        # Example value-table column with dropdown:
        vt = arcpy.Parameter(
            displayName="Stats",
            name="stats",
            datatype="GPValueTable",
            parameterType="Optional",
            direction="Input"
        )
        vt.columns = [["Field", "Input Field"], ["GPString", "Statistic Type"]]
        # Add dropdown to 2nd column:
        vt.filters = [None, arcpy._gp.Filter()]  # Pro will attach Filter objects
        vt.filters[1].type = "ValueList"
        vt.filters[1].list = ["SUM", "MEAN", "MIN", "MAX"]

        return [choice, vt]

    def execute(self, parameters, messages):
        pass
