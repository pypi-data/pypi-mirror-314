from taurus.external.qt import QtWidgets

EVALUATION_KEYS = {
    "{attr.label}": lambda proxy: proxy.label,
    "{attr.name}": lambda proxy: proxy.name,
    "{attr.fullname}": lambda proxy: proxy.fullname,
    "{dev.name}": lambda proxy: proxy.parentObj.name,
    "{dev.fullname}": lambda proxy: proxy.parentObj.fullname
}


class TitlePatternEditor:

    def __init__(self):
        self.legend_pattern = "{attr.label}"

    def showDialog(self):
        """Show pop up to change title on curves"""
        msg = (
            "Choose the title format. \n"
            + "You may use Python format() syntax. The TaurusDevice object\n"
            + 'can be referenced as "dev" and the TaurusAttribute object\n'
            + 'as "attr"'
        )

        evaluation_keys = {
            "{attr.label}": lambda proxy: proxy.label,
            "{attr.name}": lambda proxy: proxy.name,
            "{attr.fullname}": lambda proxy: proxy.fullname,
            "{dev.name}": lambda proxy: proxy.parentObj.name,
            "{dev.fullname}": lambda proxy: proxy.parentObj.fullname
        }

        if self.legend_pattern not in evaluation_keys:
            evaluation_keys[self.legend_pattern] = lambda proxy: ""

        selected_option_index = (list(evaluation_keys.keys())
                                 .index(self.legend_pattern))

        label_config, ok = QtWidgets.QInputDialog.getItem(
            None, "Change Title Pattern", msg, evaluation_keys,
            selected_option_index, True
        )

        if ok:
            self.legend_pattern = label_config
            return label_config
        else:
            return False
