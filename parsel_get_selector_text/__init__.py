#!/usr/bin/env python3

import bs4

import ftfy

import parsel


def remove_trailing_chars(text: str) -> str:
    """
    Removes any trailing whitespace characters from the input string.
    """
    text: list[str] = text.split()
    text: list[str] = [word for word in text if word != ""]
    text = " ".join(text)
    return text


class ParselGetSelectorInText:
    def traverse_soup(self, root) -> None:
        """
        Traverses a BeautifulSoup object recursively, extracting all NavigableStrings,
        removing mojibake and extracting their text.
        """
        children_list = list(root.children)
        for child in children_list:
            if isinstance(child, bs4.element.NavigableString):
                text: str = child.get_text(separator=" ")
                text = remove_trailing_chars(text=text)
                if text != "":
                    text = ftfy.fix_text(text=text)
                    self.total_text += text
            else:
                self.traverse_soup(root=child)
        return None

    def get_sel_results(self, sel_results: parsel.SelectorList) -> None:
        """
        Takes a list of Selector objects and extracts
        all NavigableStrings from their HTML.
        """
        for row in sel_results:
            html: str = row.get()
            soup = bs4.BeautifulSoup(html, features="lxml")
            self.traverse_soup(root=soup)
        return None

    def get_xpath_results(
        self,
        parsel_sel: parsel.Selector,
        xpath: str
            ) -> str:
        """
        Extracts all text results from an XPath
        query on a parsel Selector object.
        """
        self.total_text: str = ""
        sel_results = parsel_sel.xpath(xpath)
        self.get_sel_results(sel_results=sel_results)
        self.total_text.rstrip("\n")
        return self.total_text


def parsel_sel_get_text(parsel_sel: parsel.Selector, xpath: str) -> str:
    """
    Extracts all text results from an XPath
    query on a parsel Selector object.
    """
    sel_text_obj = ParselGetSelectorInText()

    total_text: str = sel_text_obj.get_xpath_results(
        parsel_sel=parsel_sel,
        xpath=xpath
    )
    return total_text