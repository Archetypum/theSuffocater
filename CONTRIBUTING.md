## Contributing to theSuffocater

We appreciate contributing on theSuffocater, please, if you want to contribute read this file to know the main rules in code writing and code style.

We appreciate contributing in:

- Code

- Testing

- Giving new ideas

## Development environment

Installation:

You can see proper installation of theSuffocater in README.md.

OS: 

GNU/Linux, BSD

## Code writing

Please consider next rules of writing if you want to help theSuffocater:

- PEP8

- Docstring after shebang in python modules:

Example:

```python3
#!/usr/bin/python3

"""
---------------------------------------
"Type description here"
"What OS your code supports here"

Author: "Type author here"
Date: "Type  date here"
---------------------------------------
"""
```

- Use Explicit Type Conversion in python scripts:

Examples:

```python3
number: int = 1984
```

```python3
string: str = "theSuffocater"
```

```python3
def function(arg: str = "default_value") -> None:
	"""
    Function documentation.

    Args:
        arg (str): Something. "default_value" if not specified        

    Returns:
        None: none.
    """

    ...
```

- And don't forget to add at the end of your code:

```python3
if __name__ == "__main__":
	function()
```

## Pull Requests

**To create and send pull request, please, follow next steps**

To create a pull request in GitHub:

- Fork the repository you want to contribute to
- Make your changes in a new branch
- Push those changes to your fork 
- Go to the original repository, click on "Compare & pull request," and fill out the necessary details before clicking "Create pull request."

* **Please check if the PR fulfills these requirements**
- [ ] The commit follows our code writing
- [ ] Tests for the changes have been added (for bug fixes / features)
- [ ] Docs have been added / updated (for bug fixes / features)


* **What kind of change does this PR introduce?** (Bug fix, feature, docs update, ...)



* **What is the current behavior?** (You can also link to an open issue here)



* **What is the new behavior (if this is a feature change)?**



* **Other information**:

## Issues Tracker

You can send the issue on GitHub theSuffocater in "Issues" -> "New Issue" -> "Submit New Issue"

Provide us next information about your issue:

- Your OS

- Line of code where issue is detected

- Expected behavior

- The thing you're encountered

## License

More information in LICENSE.md

## Code of Conduct

More information in CODE_OF_CONDUCT.md
