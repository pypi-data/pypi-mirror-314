# Quick Documentation Generator Overview

Quick documentation is an interactive tool for generating project documentation. It allows users to easily create documentation by providing a user-friendly interface and integrating with various programming languages and APIs. This tool aims to simplify the process of creating comprehensive documentation for your projects, saving time and effort.

## Features

- User-friendly graphical user interface.
- Support for different programming languages and programming environments.
- Advanced and accurate syntax highlighting.
- Customizable prompts for a tailored documentation experience.

## Structure

The codebase is organized in different directories and files for easy navigation and maintenance. Here's an overview of the main components:

- `pyproject.toml`: Project configuration file, defining dependencies, scripts, and other project-related settings.
- `backend.py`: Main backend file that handles communication with APIs and logic for generating documentation.
- `DataHandler.py`: A class responsible for managing languages, versions, and other data-related operations.
- `AutoDock.py`: A class for handling user input and generating documentation based on the provided project-specific data.
- `GUI/index.html`: The main HTML file for the graphical user interface.
- `GUI/script.js`: Contains JavaScript code to manage user inputs and interactions with the frontend.
- `GUI/style.css`: Defines the style for the user interface.
- `visual.py`: A script that creates and initializes the GUI and handles the communication between frontend and backend.

## Usage

To use the Quick documentation generator, follow these steps:

1. Install the required dependencies by running `pip install -r requirements.txt`.
2. Launch the application by running `python visual.py` in your terminal or command prompt.
3. The tool will open a graphical user interface in the web browser.
4. Enter the required information (project name, project path, ignored files, and prompts) in the appropriate fields.
5. Choose the desired programming languages and GPT version from the respective dropdowns.
6. Click the "Gen doc" button to generate the documentation.

The generated documentation will be saved in the specified project directory, depending on your project requirements and settings.
# Quick-doc-py UI Documentation

## Usage

To use Quick-doc-py UI, please follow the steps below:

1. Install the required dependencies by running the command:

```
pip install -r requirements.txt
```

2. Open your terminal or command prompt and navigate to the root directory of your Python project.

3. Run the following command to generate the documentation:

```
python -m quick_doc_ui.visual
```

```
gen-doc-ui
```

4. Follow the on-screen prompts to generate your documentation.

## Methods

This section describes the methods available within the Quick-doc-py UI.

### `gen-doc-ui`

This command generates the documentation for your Python project. It is defined in `pyproject.toml`.

**Command:** `gen-doc-ui`

**Description:** Generates documentation for your Python project.

## Quick-doc-ui Backend Module Documentation

This module provides the functionality to generate documentation for a given project using Quick-doc-py. The main classes provided by this module are `AutoDock` and `DataHandler`.

### AutoDock Class

The `AutoDock` class is responsible for setting up the required parameters for the Quick-doc-py and generating the documentation.

#### Constructor
```python
def __init__(self, 
            name_project: str,
            ignore: list[str],
            root_dir: str,
            languages: list[str],
            with_git: bool = True,
            gpt_version: str = "gpt-3.5-turbo",
            provider: str = "DarkAI",
            general_prompt: str = "",
            default_prompt: str = ""
            ):
```
- `name_project`: Name of the project for which the documentation needs to be generated.

- `ignore`: List of files/folders to ignore while scanning for source code.

- `root_dir`: path to the root directory of the project.

- `languages`: List of languages to be included for generating documentation.

- `with_git` (optional): This parameter is set to `True` if git information is to be used. Default value is `True`.

- `gpt_version` (optional): GPT version for generating documentation. Default value is "gpt-3.5-turbo".

- `provider` (optional): Provider name for generating documentation. Default value is "DarkAI".

- `general_prompt` (optional): General prompt for generating documentation.

- `default_prompt` (optional): Default prompt for generating documentation.

#### Methods
```python
def gen_doc(self):
```
- This method sets up the required arguments and calls Quick-doc-py to generate documentation for the given project.

### DataHandler Class

The `DataHandler` class provides information about supported languages and versions.

#### Methods
```python
def get_active_providers(self, gpt_version: str):
def support_languages(self):
def support_versions(self):
```
- `get_active_providers`: Returns the active providers for the given GPT version.

- `support_languages`: Returns the list of supported languages.

- `support_versions`: Returns the list of supported GPT versions.

#### Example Usage
```python
data_handler = DataHandler()
active_providers = data_handler.get_active_providers("gpt-3.5-turbo")
supported_languages = data_handler.support_languages()
supported_versions = data_handler.support_versions()
```
- This code initializes the DataHandler class and retrieves the list of active providers, supported languages, and supported versions.

#### AutoDock Usage Example
```python
from quick_doc_ui.backend import AutoDock

auto_dock = AutoDock(
    name_project="Test Project UI", 
    ignore=[".venv"], 
    root_dir="C:/Users/sinic/Python_Project/Quick-doc-py UI/",
    languages=["en"]
)

auto_dock.gen_doc()
```
- This code initializes the AutoDock class with provided parameters and generates documentation for the given project.

Please note that this documentation is a supplementary addition to the existing document.
# QuickDocPy GUI

This guide describes the usage and methods of the QuickDocPy GUI application.

## Usage

To use the QuickDocPy GUI, follow these steps:

1. Open the `index.html` file in a web browser.

2. Input the project details:

    - **Name of project**: Specify the name of your project.
    - **Project path**: Enter the directory path for your project.
    - **Ignore file**: If you want to specify an ignore file for your project, do so here.
    - **General prompt**: Write a general prompt to describe your project's documentation.
    - **Default prompt**: Write a default prompt for any parts of the documentation you would like to automatically generate.

3. Select the programming language for your project from the dropdown menu.

4. Choose the GPT version from the dropdown menu within the "Chose GPT version" section.

5. Click the "Gen doc" button to generate the documentation for your project.

This will create an HTML document containing the generated documentation for your specified project, populated with the content provided by the GPT model.

## Method Descriptions

1. `gen_doc()`:
    - This function is called when the "Gen doc" button is clicked. It generates the project documentation using the provided prompts and GPT model.

Please note that this documentation is an addition to the existing documentation and may not cover all aspects or configurations of the application.
# Quick-doc UI Script Documentation

This documentation provides an overview of the script's usage, explaining the different methods and their respective functionalities.

## Table of Contents

- [Window.onload](#windowonload)
- [getInfo](#getinfo)
- [add\_languages](#add\_languages)
- [add\_gpt](#add\_gpt)
- [gen\_doc](#gendoc)
- [get\_lang](#getlang)

<a name="windowonload"></a>

## Window.onload

This function initializes the window dimensions and calls the `getInfo` method to retrieve and display info from another extension.

```javascript
window.onload = function () {
    window.resizeTo(500, 800);
    info = getInfo();
    console.log(info.languages);
}
```

<a name="getinfo"></a>

## getInfo

The `getInfo` function communicates with an external extension, retrieves information using the `eel.get_info()` method, and parses the obtained information into separate components for further processing. It handles errors that may occur during the data retrieval.

```javascript
async function getInfo() {
    try {
        const info = await eel.get_info()(); 
        console.log(info); 
        console.log("Languages:", info.languages);
        console.log("Versions:", info.versions);

        add_languages(info.languages)
        add_gpt(info.versions)
    } catch (error) {
        console.error("Error:", error); 
    }
}
```

<a name="add_languages"></a>

## add\_languages

The `add_languages` function populates a scrolling list on the GUI. It creates individual language elements and assigns each one a checkbox. These elements are added onto the designated parent DOM node.

```javascript
function add_languages(langs){
    parent = document.querySelector(".input .current .left")
    for (i in langs){
        language = document.createElement("div")
        language.classList.add("language");

        name_class = document.createElement("div");
        name_class.classList.add("name");

        p_text = document.createElement("p");
        p_text.innerHTML = langs[i]

        name_class.appendChild(p_text)
        language.appendChild(name_class)

        tick_class = document.createElement("div");
        tick_class.classList.add("tick");

        tick = document.createElement("input");
        tick.setAttribute("type", "checkbox")
        tick.setAttribute("lang", langs[i])


        tick_class.appendChild(tick)
        language.appendChild(tick_class)

        parent.appendChild(language)
    }
}
```

<a name="add_gpt"></a>

## add\_gpt

The `add_gpt` function populates a dropdown menu on the GUI. It iterates over a list of gpt\_versions, creates `option` elements, and appends them to the designated parent DOM node.

```javascript
function add_gpt(gpt_vesions){
    parent = document.querySelector(".input .current .right select")
    for (i in gpt_vesions){
        op = document.createElement("option")
        op.setAttribute("value", gpt_vesions[i])
        op.innerHTML = gpt_vesions[i]

        parent.appendChild(op)
    }
}
```

<a name="gen_doc"></a>

## gen\_doc

The `gen_doc` function collects user input from the GUI (project\_name, path, ignored\_files, gpt, languages, and prompts) and passes the collected information to the external extension to generate documentation.

```javascript
function gen_doc(){
    name_project = document.getElementById("name").value
    path = document.getElementById("path").value
    ignore = document.getElementById("ignore").value
    g_prompt = document.getElementById("g_prompt").value
    d_prompt = document.getElementById("d_prompt").value

    gpt = document.getElementById("gpt").value
    languages = get_lang()

    eel.gen_doc(name_project, path, ignore, languages, g_prompt, d_prompt, gpt)
}
```

<a name="getlang"></a>

## get\_lang

The `get_lang` function retrieves the selected languages from the GUI. It iterates over input elements within a specific DOM node and returns the language values of the checked inputs.

```javascript
function get_lang(){
    inputs = document.querySelectorAll(".input .current .left .language .tick input")
    ex = []
    for (i in inputs){
        if (inputs[i].checked){
            ex.push(inputs[i].lang)
        }
    }

    return ex
}
```

Feel free to use and customize this documentation for further clarity and application-specific instructions.
# style.css Documentation

This `style.css` file is responsible for the styling of the Quick-doc-py UI (User Interface) application, providing users with a modern and visually appealing experience.

## Usage

To use this CSS file in your project, simply import it into your HTML file using the following line in the `<head>` section of your HTML document:

```html
<link rel="stylesheet" href="./style.css">
```

Ensure that you place the `style.css` file at the appropriate location relative to your HTML file. In this example, it is assumed to be in the same directory.

## Methods

No methods are present in this CSS file.

---

Please note that this documentation is an addition to the full documentation of the `style.css` file, focusing primarily on usage and describing the methods. For further details on the styling techniques used, please refer to the full documentation or additional resources, as needed.
# visual.py Documentation

This document describes the usage and functionality of the `visual.py` file in Markdown format using the Google style guide. The file is part of the Quick-doc-py UI project.

## Usage

The `visual.py` file is a Python module designed to interact with the graphical user interface (GUI) built using Eel. It exposes various methods to generate documentation based on user input.

### Requirements

Ensure that you have the following packages installed:

* `eel` for embedding web-based GUIs in Python
* `backend` for handling data and generating documentation

To install the required packages, you can use the following command:

```bash
pip install eel
```

If the `backend` module is not in the same directory, you need to import it from the relative path as shown in the code below:

```python
from . import backend
```

### Functions and Mets

##hod## `get_info()`

The `get_info()` function retrieves the list of supported programming languages and versions available for document generation. This method is exposed to the GUI through Eel and can be called using the following JavaScript code:

```javascript
window.onloaded('get_info');
```

The returned `data` object includes the following fields:
```python
{
    "languages": [list_of_supported_languages],
    "versions": [list_of_supported_versions]
}
```

#### `gen_doc()`

The `gen_doc()` function generates documentation based on user input. It requires the following parameters:
- `name`: The name of the project for which documentation is generated.
- `root_dir`: The root directory where the project files are located.
- `ignore`: A list of file patterns to ignore during the documentation generation.
- `languages`: A list of programming languages to be included in the documentation.
- `g_prompt`: The general prompt for the language model to use during documentation generation.
- `d_prompt`: The default prompt for the language model to use during documentation generation.
- `version`: The specific version of the language model to use.

The function initializes an instance of `AutoDock` with the provided parameters and calls its `gen_doc()` method to generate the documentation.

### Running the GUI

To start the GUI, you need to call the `main()` function. This will initialize the Eel module, specifying the location of the HTML file (`index.html`) and the desired window size and mode.

```python
if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    eel.init(os.path.join(current_dir, 'GUI'))
    eel.start("index.html", port=809, size=(400, 300), mode="chrome")
```

## Conclusion

The `visual.py` file provides a Python interface to interact with the Quick-doc-py UI's graphical user interface. It allows users to retrieve information about supported languages and versions as well as generate documentation based on provided project parameters.

Feel free to use and modify this documentation as needed, while keeping the required formatting and style.
# quick_doc_ui

Welcome to the Quick-doc UI Module! This documentation page will guide you through the usage of the methods provided within the `__init__.py` file of the Quick-doc UI Python project.

## Table of Contents
- [Initialization](#initialization)
- [close_quick_doc](#close_quick_doc)
- [update_command](#update_command)

## Initialization
To use the Quick-doc UI module, you'll need to initialize an instance of the `QuickDocUI` class. This will set up the necessary environment for the other methods to function properly.

```python
from quick_doc_ui import QuickDocUI

quick_doc = QuickDocUI()
```

## close_quick_doc
This method is used to close the Quick-doc UI interface.

```python
quick_doc.close_quick_doc()
```

## update_command
This method allows you to replace the current Quick-doc UI command.

```python
quick_doc.update_command(new_command)
```

- `new_command`: (string) The new command to be added to the Quick-doc UI.
- **Returns**: None

By utilizing the methods provided by this module, you'll be able to effectively control the Quick-doc UI project within your Python environment.
