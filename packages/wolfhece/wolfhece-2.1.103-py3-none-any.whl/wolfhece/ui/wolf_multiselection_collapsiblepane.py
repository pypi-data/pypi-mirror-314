"""
Author: HECE - University of Liege, Pierre Archambeau
Date: 2024

Copyright (c) 2024 University of Liege. All rights reserved.

This script and its content are protected by copyright law. Unauthorized
copying or distribution of this file, via any medium, is strictly prohibited.
"""

import wx
import logging

class Wolf_TwoLists_Transfer(wx.Panel):
    """ Panel with 2 lists to select multiple items from 1 to 2 or from 2 to 1"""

    def __init__(self, parent, **kwargs):
        """
        :param parent : wx.Window
        :param kwargs : dict - other arguments for wx.Panel (example : max_selected_items=3, delete_if_transfer=True)
        """

        super().__init__(parent)

        self.delete_if_transfer = True
        self.max_selected_items = None

        if 'max_selected_items' in kwargs:
            self.max_selected_items = kwargs['max_selected_items']
            assert isinstance(self.max_selected_items, int), "max_selected_items must be an integer"

        if 'delete_if_transfer' in kwargs:
            self.delete_if_transfer = kwargs['delete_if_transfer']
            assert isinstance(self.delete_if_transfer, bool), "delete_if_transfer must be a boolean"

        # Créer les deux listes à sélection multiples
        self.list1 = wx.ListBox(self, style=wx.LB_EXTENDED | wx.LB_NEEDED_SB)
        self.list2 = wx.ListBox(self, style=wx.LB_EXTENDED | wx.LB_NEEDED_SB)

        # Créer les boutons pour transférer les éléments sélectionnés
        self.button1to2 = wx.Button(self, label=">>")
        self.button2to1 = wx.Button(self, label="<<")

        # Créer les boutons pour trier les listes
        self.buttonSort1 = wx.Button(self, label="Sort left")
        self.buttonSort2 = wx.Button(self, label="Sort right")
        self.buttonall1to2 = wx.Button(self, label="All 1 >> 2")
        self.buttonall2to1 = wx.Button(self, label="All 1 << 2")

        # créer le sizer vertical pour les boutons
        sizer_vertical = wx.BoxSizer(wx.VERTICAL)
        sizer_vertical.Add(self.button1to2, proportion=1, flag=wx.GROW | wx.ALL, border=2)
        sizer_vertical.Add(self.button2to1, proportion=1, flag=wx.GROW | wx.ALL, border=2)
        sizer_vertical.Add(self.buttonSort1, proportion=1, flag=wx.GROW | wx.ALL, border=2)
        sizer_vertical.Add(self.buttonSort2, proportion=1, flag=wx.GROW | wx.ALL, border=2)
        sizer_vertical.Add(self.buttonall1to2, proportion=1, flag=wx.GROW | wx.ALL, border=2)
        sizer_vertical.Add(self.buttonall2to1, proportion=1, flag=wx.GROW | wx.ALL, border=2)

        # Créer le sizer horizontal pour aligner les éléments
        sizer_horizontal = wx.BoxSizer(wx.HORIZONTAL)

        # Ajouter les éléments au sizer horizontal
        sizer_horizontal.Add(self.list1, proportion=1, flag=wx.GROW | wx.ALL, border=2)
        sizer_horizontal.Add(sizer_vertical,proportion=1, flag=wx.GROW | wx.ALL, border=2)
        sizer_horizontal.Add(self.list2, proportion=1, flag=wx.GROW | wx.ALL, border=2)

        # Définir le sizer pour le panneau
        self.SetSizer(sizer_horizontal)
        # self.Layout()
        sizer_horizontal.SetSizeHints(self)

        self._ui_bind_actions()

    def get_values(self):
        """ Get values of the lists """
        return self.list2.Items

    def set_max_selected_items(self, max_selected_items:int):
        """ set the maximum number of selected items that list1 can transfer to list2 """

        assert isinstance(max_selected_items, int), "max_selected_items must be an integer"
        assert len(self.list1.Items) >= max_selected_items, "len(self.list1.Items) must be >= max_selected_items"
        self.max_selected_items = max_selected_items

    def _ui_bind_actions(self):
        """ Bind actions to buttons """
        self.button1to2.Bind(wx.EVT_BUTTON, self._on_button1to2)
        self.button2to1.Bind(wx.EVT_BUTTON, self._on_button2to1)
        self.buttonSort1.Bind(wx.EVT_BUTTON, self._on_buttonSort1)
        self.buttonSort2.Bind(wx.EVT_BUTTON, self._on_buttonSort2)
        self.buttonall1to2.Bind(wx.EVT_BUTTON, self._on_buttonAll1to2)
        self.buttonall2to1.Bind(wx.EVT_BUTTON, self._on_buttonAll2to1)

    def _on_buttonAll1to2(self, event):
        """ Clear list 2 """
        for i in range(len(self.list1.Items)):
            self.list1.Select(i)
        self._on_button1to2(wx.EVT_BUTTON)

    def _on_buttonAll2to1(self, event):
        """ Clear list 2 """
        for i in range(len(self.list2.Items)):
            self.list2.Select(i)
        self._on_button2to1(wx.EVT_BUTTON)

    def _on_buttonSort1(self, event):
        """ Sort items of list 1 """
        if len(self.list1.Items)==0:
            return
        # Récupérer les éléments de la liste 1
        items = self.list1.Items
        # Trier les éléments
        items.sort()
        # Supprimer les éléments de la liste 1
        self.list1.Clear()
        # Ajouter les éléments triés à la liste 1
        self.list1.InsertItems(items, 0)

    def _on_buttonSort2(self, event):
        """ Sort items of list 2 """
        if len(self.list2.Items)==0:
            return
        # Récupérer les éléments de la liste 2
        items = self.list2.Items
        # Trier les éléments
        items.sort()
        # Supprimer les éléments de la liste 2
        self.list2.Clear()
        # Ajouter les éléments triés à la liste 2
        self.list2.InsertItems(items, 0)

    def _on_button1to2(self, event):
        """ Transfer selected items from list 1 to list 2 """
        # Récupérer les éléments sélectionnés de la liste 1
        selected_items = self.list1.GetSelections()
        if len(selected_items) == 0:
            return

        if self.max_selected_items is not None:
            if self.max_selected_items > -1:
                if len(selected_items) > self.max_selected_items:
                    logging.warning(f"Max selected items is {self.max_selected_items}")
                    return
                if len(self.list2.Items) + len(selected_items) > self.max_selected_items:
                    logging.warning(f"Max selected items is {self.max_selected_items}")
                    return

        # Ajouter les éléments sélectionnés à la liste 2
        self.list2.InsertItems([self.list1.GetString(item) for item in selected_items], 0)

        if self.delete_if_transfer:
            # Supprimer les éléments sélectionnés de la liste 1
            selected_items.sort(reverse=True)
            for n in selected_items:
                self.list1.Delete(n)

    def _on_button2to1(self, event):
        """ Transfer selected items from list 2 to list 1 """
        # Récupérer les éléments sélectionnés de la liste 2
        selected_items = self.list2.GetSelections()
        if len(selected_items) == 0:
            return
        # Ajouter les éléments sélectionnés à la liste 1
        self.list1.InsertItems([self.list2.GetString(item) for item in selected_items], 0)

        # Supprimer les éléments sélectionnés de la liste 2
        selected_items.sort(reverse=True)
        for n in selected_items:
            self.list2.Delete(n)


class Wolf_MultipleSelection(wx.Dialog):
    """
    Dialog with multiple 'collapsiblepanes' containing 2 lists to select multiple items
    """
    def __init__(self,
                 parent,
                 title,
                 values_dict:dict,
                 callback = None,
                 info:str='',
                 cmdApply:bool=False,
                 styles = wx.LB_EXTENDED,
                 destroyOK = False,
                 **kwargs):
        """
        :param parent : wx.Window
        :param title : str - title of the frame
        :param values_dict : dict - {'label1':[item1, item2, ...], 'label2':[item1, item2, ...], ...}
        :param callback : function - callback function when OK or Apply button is pressed
        :param info : str - information to display upper the collapsiblepanes
        :param cmdApply : bool - if True, Apply button is displayed
        :param styles : wx.ListBox styles - wx constant or list of wx constants
        :param kwargs : dict - other arguments for wx.Frame (example : max_selected_items=[1, 2, 3], delete_if_transfer=[True, False, True])
        """
        if isinstance(styles, list):
            assert len(styles) == len(values_dict), "styles must be a list of len(values_dict)"

        if 'max_selected_items' in kwargs:
            self.max_selected_items = kwargs['max_selected_items']
            assert isinstance(self.max_selected_items, list), "max_selected_items must be a list"
            assert len(self.max_selected_items) == len(values_dict), "max_selected_items must be a list of len(values_dict)"
            for i, values in enumerate(values_dict.values()):
                assert len(values) >= self.max_selected_items[i], "len(values) must be >= max_selected_items"
        else:
            self.max_selected_items = None

        if 'delete_if_transfer' in kwargs:
            self.delete_if_transfer = kwargs['delete_if_transfer']
            assert isinstance(self.delete_if_transfer, list), "delete_if_transfer must be a list"
            assert len(self.delete_if_transfer) == len(values_dict), "delete_if_transfer must be a list of len(values_dict)"
            for i, values in enumerate(values_dict.values()):
                assert isinstance(self.delete_if_transfer[i], bool), "delete_if_transfer must be a list of boolean"

        super().__init__(parent, title=title)

        self.destroyOK = destroyOK
        # Créer le panneau principal
        main_panel = wx.Panel(self)

        # Créer les collapsiblepanes
        self.panes = []
        for key, values in values_dict.items():
            pane = wx.CollapsiblePane(main_panel, label=key)
            self.panes.append(pane)

        # Créer les panneaux internes pour les collapsiblepanes
        pane_panels = [pane.GetPane() for pane in self.panes]

        # Créer l'objet Wolf_TwoLists_Transfer pour chaque panneau interne
        self.transfers = []
        for i, values in enumerate(values_dict.values()):
            transfer = Wolf_TwoLists_Transfer(pane_panels[i])

            if isinstance(styles, list):
                transfer.list1.SetWindowStyle(styles[i])
                transfer.list2.SetWindowStyle(styles[i])
            else:
                transfer.list1.SetWindowStyle(styles)
                transfer.list2.SetWindowStyle(styles)

            transfer.list1.Items = values

            if self.max_selected_items is not None:
                transfer.set_max_selected_items(self.max_selected_items[i])

            if self.delete_if_transfer is not None:
                transfer.delete_if_transfer = self.delete_if_transfer[i]

            self.transfers.append(transfer)

        # Créer le sizer vertical pour les collapsiblepanes
        sizer_vertical = wx.BoxSizer(wx.VERTICAL)

        text = wx.StaticText(main_panel, label=info)
        sizer_vertical.Add(text, proportion=0, flag=wx.GROW | wx.ALL, border=5)

        for i, pane in enumerate(self.panes):
            sizer_vertical.Add(pane, proportion=0, flag=wx.GROW | wx.ALL, border=5)

        # Créer les boutons OK et Apply
        sizer_horizontal_buttons = wx.BoxSizer(wx.HORIZONTAL)
        self.buttonOK = wx.Button(main_panel, label="OK")
        sizer_horizontal_buttons.Add(self.buttonOK, proportion=0, flag=wx.ALL, border=5)
        if cmdApply:
            self.buttonApply = wx.Button(main_panel, label="Apply")
            sizer_horizontal_buttons.Add(self.buttonApply, proportion=0, flag=wx.ALL, border=5)
            sizer_vertical.Add(sizer_horizontal_buttons, proportion=0, flag=wx.ALIGN_RIGHT | wx.ALL, border=5)
        else:
            self.buttonApply = None
        sizer_vertical.Add(sizer_horizontal_buttons, proportion=0, flag=wx.ALIGN_RIGHT | wx.ALL, border=5)

        # Callback if ok/apply button is pressed
        self.callback = callback

        # Définir le sizer pour le panneau principal
        main_panel.SetSizer(sizer_vertical)

        # Définir le sizer pour la frame
        self.SetSizer(wx.BoxSizer(wx.VERTICAL))  # Use SetSizerAndFit instead of SetSizer

        # Ajouter le panneau principal à la frame
        self.GetSizer().Add(main_panel, proportion=0, flag=wx.EXPAND)

        # Définir la taille de la frame
        self.Fit()

        # Mise en page des éléments de la frame
        sizer_vertical.SetSizeHints(self)

        self.Layout()

        self._ui_bind_actions()
        # Afficher la frame
        self.CenterOnScreen()

    # def MakeModal(self, modal=True):
    #     if modal and not hasattr(self, '_disabler'):
    #         self._disabler = wx.WindowDisabler(self)
    #     if not modal and hasattr(self, '_disabler'):
    #         del self._disabler

    # def ShowModal(self):
    #     """ Show the frame """
    #     self.Show()
    #     return self

    # def Show(self):
    #     """ Show the frame """
    #     super().Show()
        # return self

    def get_values(self):
        """ Get values of the lists """
        keys = [curpane.GetLabel() for curpane in self.panes]
        return {key: transfer.get_values() for key, transfer in zip(keys, self.transfers)}

    def _ui_bind_actions(self):
        """ Bind actions to buttons """

        self.buttonOK.Bind(wx.EVT_BUTTON, self._on_buttonOK)

        if self.buttonApply is not None:
            self.buttonApply.Bind(wx.EVT_BUTTON, self._on_buttonApply)

    def _on_buttonOK(self, event):
        if self.callback is not None:
            self.callback(self)

        if self.destroyOK:
            self.Destroy()
        else:
            self.Hide()

    def _on_buttonApply(self, event):
        """ callback """
        if self.buttonApply is None:
            return
        if self.callback is not None:
            self.callback(self)

if __name__ == "__main__":
    # Utilisation de la classe Wolf_MultipleSelection
    app = wx.App()
    frame = Wolf_MultipleSelection(None,
                                title="Exemple de Wolf_MultipleSelection",
                                values_dict={'domain':["Item 1", "Item 2", "Item 3", "Item 4"],
                                                'u':["Item 3", "Item 4", "Item 5", "Item 6"],
                                                'v':["Item v1", "Item v2", "Item v3", "Item v4"]},
                                info="You can define :                     \n   - the domain\n   - u\n   -v",
                                callback=None,
                                styles=[wx.LB_SINGLE, wx.LB_EXTENDED, wx.LB_EXTENDED],
                                max_selected_items=[1, -1, -1],)
    frame.ShowModal()
    pass
    app.MainLoop()
