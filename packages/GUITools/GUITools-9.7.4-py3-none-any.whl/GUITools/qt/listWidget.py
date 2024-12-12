# -*- coding: latin -*-
from PyQt6.QtWidgets import  QListWidget

class ListWidget(object):
    
    @staticmethod
    def update(listWidget : QListWidget, new_data : list[str]):
        all_items = [listWidget.item(i).text() for i in range(listWidget.count())]
      
        if all_items != new_data:

            for programa in new_data:
                if programa not in all_items:
                    listWidget.addItem(programa)

            for index, item in enumerate(all_items):
                if item not in new_data:
                    listWidget.takeItem(index)

    @staticmethod
    def select_item(listWidget : QListWidget, item_text : str):
        AllItems = [listWidget.item(i) for i in range(listWidget.count())]
        for item in AllItems:
            if item.text() == item_text:
                if listWidget.currentRow() != -1:
                    if listWidget.currentItem().text() != item_text:
                        listWidget.setCurrentItem(item)
                else:
                    listWidget.setCurrentItem(item)

    @staticmethod
    def get_currentItem(listWidget : QListWidget):
        if listWidget.currentRow() != -1:
            return listWidget.currentItem()
        else:
            return None

    @classmethod
    def get_currentItem_several(cls, *ListWidgets : QListWidget):
        for lista in ListWidgets:
             currentItem = cls.get_currentItem(lista)
             if currentItem:
                return currentItem



