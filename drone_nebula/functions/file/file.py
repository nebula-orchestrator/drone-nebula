from string import Template
from typing import Optional
import json
import ast


def read_file(file_path: str) -> dict:
    """Read a file and returns it's contents (as a string), raise FileNotFoundError if file does not exist

        Arguments:
            file_path -- the path of the file to be read
        Returns:
            file_contents -- a dict of the file contents
    """
    with open(file_path) as f:
        file_contents = f.read()
    app_dict = json.loads(file_contents)
    return app_dict


# populate string from template
def populate_template_string(pre_template_string: dict, template_values_dict: Optional[dict]) -> dict:
    """Takes a pre_template_string dict and populates it with dynamic values from the given template_values_dict

        Arguments:
            pre_template_string -- a dict to apply the templating to
            template_values_dict -- a dict of values to to be inserted in the template
        Returns:
            post_template_string -- the result dict after the templating
    """
    if template_values_dict is None:
        template_values_dict = {}

    pre_template_string = str(pre_template_string)
    post_template_string = Template(pre_template_string).safe_substitute(template_values_dict)
    post_template_string = ast.literal_eval(post_template_string)
    return post_template_string
