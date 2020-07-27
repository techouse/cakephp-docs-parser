#!/usr/bin/env python
import os.path
import re
from urllib.parse import urljoin

import simplejson as json
from bs4 import BeautifulSoup

CAKE_DOCS_URL = "https://book.cakephp.org/{version}/en/"

EXCLUDED_IDS = {"index-", "module-"}

VERSIONS = {"2", "3", "4"}


def parse():
    entries = []

    for version in VERSIONS:
        with open(
            os.path.abspath(os.path.join("docs", version, "genindex.html")), "r"
        ) as genindex:
            index_soup = BeautifulSoup(genindex, "lxml")

            for table in index_soup.find_all("table", class_="genindextable"):
                for a in table.find_all("a"):
                    href = a.get("href")
                    file, id = href.split("#")

                    if any(id.startswith(pattern) for pattern in EXCLUDED_IDS):
                        continue

                    with open(
                        os.path.abspath(os.path.join("docs", version, file))
                    ) as html:
                        try:
                            topic_soup = BeautifulSoup(html, "lxml")
                            topic = topic_soup.find(id=id)
                            parent = topic.parent

                            entry_data = {
                                "version": float(version),
                                "id": id,
                                "title": "",
                                "permalink": urljoin(
                                    CAKE_DOCS_URL.format(version=version), href,
                                ),
                                "categories": [],
                                "default": "",
                                "content": "",
                            }

                            # set the title
                            if any(character.isupper() for character in id):
                                entry_data["title"] = id[
                                    re.search("[A-Z]", id).start() :
                                ]
                            else:
                                if topic.find(class_="descclassname"):
                                    entry_data["title"] += topic.find(
                                        class_="descclassname"
                                    ).get_text()
                                if topic.find(class_="descname"):
                                    entry_data["title"] += topic.find(
                                        class_="descname"
                                    ).get_text()
                                if parent.get("class") == "glossary docutils":
                                    entry_data["title"] += topic.get_text()
                            # set the content
                            if parent.find("dd"):
                                if parent.find("dd").find("p"):
                                    entry_data["content"] = " ".join(
                                        parent.find("dd").find("p").get_text().split()
                                    )
                            # set the categories
                            if topic.find(class_="property"):
                                property_value = (
                                    topic.find(class_="property").get_text().strip()
                                )
                                if property_value.startswith("="):
                                    entry_data["default"] = " ".join(
                                        property_value.replace("=", "").split()
                                    )
                                else:
                                    entry_data["categories"].append(property_value)
                            if id.startswith("flask."):
                                entry_data["categories"] += id.split(".")[1:-1]

                            entries.append(entry_data)
                        except Exception:
                            print(href)
                            if parent:
                                print(parent.name)
                            raise

                if entries:
                    with open(os.path.abspath("data.json"), "w") as fh:
                        json.dump(entries, fh, indent=2)


if __name__ == "__main__":
    parse()
