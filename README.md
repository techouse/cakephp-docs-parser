# CakePHP Documentation parser for Algolia Search

## Installation and usage
```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
sh get_docs.sh
python parser.py
```

The above commands will make a virtual environment in a folder called `env` and install all the requirements listed in `requirements.txt` into that virtual environment.
Once that is done running `sh get_docs.sh` will `clone` the `git` repository of the [CakePHP Documentation](https://github.com/cakephp/docs) and build the CakePHP HTML English documentation using Sphinx.
Then running `python parser.py` will parse that documentation.
It will output a file called `data.json` which you can later use to your avail.

The output JSON file looks like this:
```json
[
    {
        "version": 2.0,
        "id": "Inflector::underscore",
        "title": "Inflector::underscore",
        "permalink": "https://book.cakephp.org/2/en/core-utility-libraries/inflector.html#Inflector::underscore",
        "categories": [
            "static"
        ],
        "default": "",
        "content": "It should be noted that underscore will only convert camelCase formatted words. Words that contains spaces will be lower-cased, but will not contain an underscore."
    }
]
```