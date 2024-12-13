"""
Author: University of Liege, HECE
Date: 2024

Copyright (c) 2024 University of Liege. All rights reserved.

This script and its content are protected by copyright law. Unauthorized
copying or distribution of this file, via any medium, is strictly prohibited.
"""
from .acceptability import Base_data_creation, Database_to_raster, Vulnerability, Acceptability
from .acceptability import steps_base_data_creation, steps_vulnerability, steps_acceptability
from .func import Accept_Manager
from ..scenario.config_manager import Config_Manager_2D_GPU 
import wx
import glob
import wx.lib.dialogs
import logging
import subprocess
import matplotlib
import shutil
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar2Wx
import os
from pathlib import Path
from gettext import gettext as _

from wolfhece.Results2DGPU import wolfres2DGPU
from pathlib import Path 

def read_result(fn) :
    wolfres2DGPU_X= wolfres2DGPU(fn)
    return wolfres2DGPU_X

def nullvalue_for_hole(WA):
    #WolfArray
    WA.nullvalue = 0.
    WA.set_nullvalue_in_mask()  

def read_export_z_bin(fn_read, fn_write):
    wolfres2DGPU_test = read_result(fn_read)
    wolfres2DGPU_test.read_oneresult(-1)
    wd = wolfres2DGPU_test.get_h_for_block(1)
    top = wolfres2DGPU_test.get_top_for_block(1)
    nullvalue_for_hole(wd)
    nullvalue_for_hole(top)
    wd.array = wd.array + top.array 
    wd.write_all(fn_write)
    
def empty_folder(folder):
    if os.path.exists(folder):
        for files in os.listdir(folder):
            fn = os.path.join(folder, files)
            try:
                if os.path.isfile(fn) or os.path.islink(fn):
                    os.unlink(fn)  
                elif os.path.isdir(fn):
                    shutil.rmtree(fn)  
            except Exception as e:
                print(f"Error when deleting file {fn}: {e}")
    else:
        print("The folder does not exist.")



class AcceptabilityGui(wx.Frame):
    """ The main frame for the vulnerability/acceptability computation """

    def __init__(self, parent=None, width=1024, height=500):

        super(wx.Frame, self).__init__(parent, title='Acceptability', size=(width, height))

        self._manager = None
        self._mapviewer = None
        self.InitUI()

    @property
    def mapviewer(self):
        return self._mapviewer

    @mapviewer.setter
    def mapviewer(self, value):
        from ..PyDraw import WolfMapViewer

        if not isinstance(value, WolfMapViewer):
            raise TypeError("The mapviewer must be a WolfMapViewer")

        self._mapviewer = value

    def InitUI(self):

        sizer_hor_main = wx.BoxSizer(wx.HORIZONTAL)

        sizer_vert1 = wx.BoxSizer(wx.VERTICAL)

        sizer_hor_threads = wx.BoxSizer(wx.HORIZONTAL)
        sizer_hor1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_hor1_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_hor2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_hor3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_hor4 = wx.BoxSizer(wx.HORIZONTAL)

        # 1st LINE
        panel = wx.Panel(self)
        self._but_maindir = wx.Button(panel, label='Main Directory')
        self._but_maindir.Bind(wx.EVT_BUTTON, self.OnMainDir)

        self._listbox_studyarea = wx.ListBox(panel, choices=[], style=wx.LB_SINGLE)
        self._listbox_studyarea.Bind(wx.EVT_LISTBOX, self.OnStudyArea)
        self._listbox_studyarea.SetToolTip("Choose the study area")

        self._listbox_scenario = wx.ListBox(panel, choices=[], style=wx.LB_SINGLE)
        self._listbox_scenario.Bind(wx.EVT_LISTBOX, self.OnScenario)
        self._listbox_scenario.SetToolTip("Choose the scenario")


        # 3nd LINE
        self._text_process = wx.StaticText(panel, label='Number of threads:')

        self._nb_process = wx.SpinCtrl(panel, value=str(os.cpu_count()), min=1, max=os.cpu_count())
        self._nb_process.SetToolTip("Number of threads to use")

        sizer_hor_threads.Add(self._text_process, 1, wx.ALL | wx.EXPAND, 0)
        sizer_hor_threads.Add(self._nb_process, 1, wx.ALL | wx.EXPAND, 0)

        sizer_hor1.Add(self._but_maindir, 2, wx.ALL | wx.EXPAND, 0)
        sizer_hor1.Add(self._listbox_studyarea, 1, wx.ALL | wx.EXPAND, 0)
        sizer_hor1.Add(self._listbox_scenario, 1, wx.ALL | wx.EXPAND, 0)

        # 2nd LINE
        self._but_checkfiles = wx.Button(panel, label='Check directories structure')
        self._but_checkfiles.Bind(wx.EVT_BUTTON, self.OnCheckFiles)

        sizer_hor1_1.Add(self._but_checkfiles, 1, wx.ALL | wx.EXPAND, 0)
        
        # Hydrodynamic part
        self._but_checkfiles = wx.Button(panel, label='Check input water depths')
        self._but_checkfiles.Bind(wx.EVT_BUTTON, self.OnHydrodynInput)

        sizer_hor1_1.Add(self._but_checkfiles, 1, wx.ALL | wx.EXPAND, 0)
        
        self._but_checkfiles = wx.Button(panel, label='Change / Load water depths results')
        self._but_checkfiles.Bind(wx.EVT_BUTTON, self.OnLastStepBin)

        sizer_hor1_1.Add(self._but_checkfiles, 1, wx.ALL | wx.EXPAND, 0)
        
        #Other lines with functions of algorithm
        self._but_creation = wx.Button(panel, label='DataBase Creation')
        self._but_creation.Bind(wx.EVT_BUTTON, self.OnCreation)

        self._steps_db = wx.CheckListBox(panel, choices=steps_base_data_creation.get_list_names(), style=wx.LB_MULTIPLE | wx.CHK_CHECKED)

        self._but_vulnerability = wx.Button(panel, label='Vulnerability')
        self._but_vulnerability.Bind(wx.EVT_BUTTON, self.OnVulnerability)

        self._steps_vulnerability = wx.CheckListBox(panel, choices=steps_vulnerability.get_list_names(), style=wx.LB_MULTIPLE | wx.CHK_CHECKED)

        self._but_acceptability = wx.Button(panel, label='Acceptability')
        self._but_acceptability.Bind(wx.EVT_BUTTON, self.OnAcceptability)

        self._steps_acceptability = wx.CheckListBox(panel, choices=steps_acceptability.get_list_names(), style=wx.LB_MULTIPLE | wx.CHK_CHECKED)

        sizer_hor2.Add(self._but_creation, 1, wx.ALL | wx.EXPAND, 0)
        sizer_hor2.Add(self._steps_db, 1, wx.ALL | wx.EXPAND, 0)

        sizer_hor3.Add(self._but_vulnerability, 1, wx.ALL | wx.EXPAND, 0)
        sizer_hor3.Add(self._steps_vulnerability, 1, wx.ALL | wx.EXPAND, 0)

        sizer_hor4.Add(self._but_acceptability, 1, wx.ALL | wx.EXPAND, 0)
        sizer_hor4.Add(self._steps_acceptability, 1, wx.ALL | wx.EXPAND, 0)

        sizer_vert1.Add(sizer_hor1, 2, wx.EXPAND, 0)
        sizer_vert1.Add(sizer_hor1_1, 1, wx.EXPAND, 0)
        sizer_vert1.Add(sizer_hor_threads, 0, wx.EXPAND, 0)
        sizer_vert1.Add(sizer_hor2, 1, wx.EXPAND, 0)
        sizer_vert1.Add(sizer_hor3, 1, wx.EXPAND, 0)
        sizer_vert1.Add(sizer_hor4, 1, wx.EXPAND, 0)

        # ------

        sizer_vert2 = wx.BoxSizer(wx.VERTICAL)

        self._listbox_returnperiods = wx.ListBox(panel, choices=[], style=wx.LB_SINGLE)
        self._listbox_returnperiods.SetToolTip("All available return periods in the database")

        self._listbox_sims = wx.ListBox(panel, choices=[], style=wx.LB_SINGLE)
        self._listbox_sims.SetToolTip("All available simulations in the database")

        self._listbox_sims.Bind(wx.EVT_LISTBOX, self.OnSims)
        self._listbox_sims.Bind(wx.EVT_LISTBOX_DCLICK, self.OnSimsDBLClick)

        sizer_vert2.Add(self._listbox_returnperiods, 1, wx.EXPAND, 0)
        sizer_vert2.Add(self._listbox_sims, 1, wx.EXPAND, 0)

        # ------

        sizer_vert3 = wx.BoxSizer(wx.VERTICAL)

        matplotlib.use('WXAgg')

        self._figure = Figure(figsize=(5, 4), dpi=100)
        self._axes = self._figure.add_subplot(111)
        self._canvas = FigureCanvas(panel, -1, self._figure)
        self._toolbar = NavigationToolbar2Wx(self._canvas)
        self._toolbar.Realize()

        sizer_vert3.Add(self._canvas, 1, wx.EXPAND, 0)
        sizer_vert3.Add(self._toolbar, 0, wx.LEFT | wx.EXPAND, 0)

        # ------

        sizer_hor_main.Add(sizer_vert1, 1, wx.EXPAND, 0)
        sizer_hor_main.Add(sizer_vert2, 1, wx.EXPAND, 0)
        sizer_hor_main.Add(sizer_vert3, 1, wx.EXPAND, 0)

        panel.SetSizer(sizer_hor_main)
        panel.Layout()

        self._but_acceptability.Enable(False)
        self._but_vulnerability.Enable(False)
        self._but_creation.Enable(False)

    def OnSims(self, e:wx.ListEvent):
        """ Load sim into the mapviewer """
        pass

    def OnSimsDBLClick(self, e:wx.ListEvent):
        """ Load sim into the mapviewer """
        if self.mapviewer is None:
            return

        from ..PyDraw import draw_type

        idx_sim = e.GetSelection()
        tmppath = self._manager.get_filepath_for_return_period(self._manager.get_return_periods()[idx_sim])
        if tmppath.stem not in self.mapviewer.get_list_keys(drawing_type=draw_type.ARRAYS):
            self.mapviewer.add_object('array', filename=str(tmppath), id=tmppath.stem)
            self.mapviewer.Refresh()

    def OnCheckFiles(self, e):
        """ Check the files """

        if self._manager is None:
            logging.error("No main directory selected -- Nothing to check")
            return

        ret = self._manager.check_files()

        if ret == "":
            logging.info("The folder is well structured")
            with wx.MessageDialog(self, "The folder is well structured", "Info", wx.OK | wx.ICON_INFORMATION) as dlg:
                dlg.ShowModal()
        else:
            logging.error(f"Missing files: {ret}")
            with wx.MessageDialog(self, f"Missing files: \n{ret}", "Error", wx.OK | wx.ICON_ERROR) as dlg:
                dlg.ShowModal()

            
    def OnHydrodynInput(self,e):
        """ A test to check if the FILLED water depths files exist.
            -If YES : the code can go on
            -If NO : either need to be computed, either the code will use the baseline ones
        """
        
        if self._manager is None:
            logging.error("No main directory selected -- Nothing to check")
            return

        paths_FilledWD = self._manager.get_sims_files_for_baseline()
        
        if len(paths_FilledWD) == 0 :
            logging.info("There are no interpolated free surface files. Need for them to go on the acceptability computations.")
            dialog = wx.MessageDialog(None, "There are no interpolated free surface files. Need for them to go on the acceptability computations. Please choose an action.", "Choose an option", 
                                   wx.YES_NO | wx.CANCEL | wx.ICON_QUESTION)
        
            dialog.SetYesNoLabels("Use _baseline simulations", "Load simulations")  
            response = dialog.ShowModal() 

            if response == wx.ID_YES:
                logging.info("Decision of using baseline simulations.")
                paths_FilledWD_base = self._manager.get_sims_files_for_baseline()
                if len(paths_FilledWD_base) == 0 :
                    logging.info("Cannot select files in the _baseline folder.")
                else:
                    self._manager.copy_tif_files(paths_FilledWD_base, self._manager.IN_SCEN_DIR)
                                
            elif response == wx.ID_NO:
                logging.info("Decision of loading simulations.")
                with wx.MessageDialog(self, f"Please use the 'Change / Load water depths results' button of the manager and follow the instructions.", "Redirecting", 
                                      wx.OK | wx.ICON_INFORMATION) as dlg:                        
                    dlg.ShowModal()
            else:
                print("Cancelled")
            
            dialog.Destroy() 
                
        else:
            for names in paths_FilledWD:
                logging.info(f"Interpolated free surface file found: {names.name}.")
            with wx.MessageDialog(self, 
                                f"{len(paths_FilledWD)} files of interpolated free surface found in the folder (see logs window). If you want to change it, click the 'Change/ Load' water depths results?", 
                                "Information", 
                                style=wx.OK | wx.ICON_INFORMATION) as dlg:
                dlg.ShowModal()
                
    def OnLastStepBin(self,e):
        """ Link between acceptability and simulations
            -Either the last steps of the steady simulations for the scenarios already exist : only have to point towards them, then the free surfaces are filled
            -Or they dont exist and need to be done outside this manager
        """
       
        dlg = wx.DirDialog(None, "Please select the simulation folder that contains the folders 'sim_' to use.", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            datadir = Path(dlg.GetPath()) 
            logging.info(f"Selected folder : {datadir}")
        else:
            logging.info('No folder found / selected. Please try again..')

        sims = {}
        path_LastSteps = Path(self._manager.IN_SA_EXTRACTED)
        empty_folder(path_LastSteps)
        for subdir in datadir.iterdir():
            if subdir.is_dir() and subdir.name.startswith("sim_"):
                sims[subdir.name] = subdir
                fn_read = Path(subdir / "simul_gpu_results")
                logging.info(f"Found simulation folder: {subdir}")
                
                parts = subdir.name.split("sim_")
                if len(parts) > 1:
                    name = parts[1]
                    fn_write = Path(path_LastSteps / (name + '.bin'))
                    read_export_z_bin(fn_read, fn_write)
                else:
                    logging.info(f"Please, ensure your simulations are named with the return period, e.g sim_T4")
 
            else:
                logging.info('No folder found / selected. Please try again...')
        
        End = False                
        path_Interp =  Path(self._manager.IN_SA_INTERP)
        bat_file_path = os.path.join(self._manager.IN_SCEN_DIR, "process_files.bat")
        if os.path.exists(bat_file_path):
            logging.info(f"The file {bat_file_path} already exists and will be replaced.")
            os.remove(bat_file_path)
        path_code = os.path.join(self._manager.IN_WATER_DEPTH, "holes.exe") 
        
        C = None
        D = None
        
        for file in os.listdir(Path(self._manager.IN_SA_DEM)):
            file_path = Path(self._manager.IN_SA_DEM) / file

            if file_path.is_file() and file.startswith("MNT_") and file_path.suffix == ".bin":
                if "mask" not in file:
                    D = file_path
                else:
                    C = file_path
                    
        if D == None:
            logging.info("DEM (.bin) not found. The file must begins by 'MNT' and CANNOT include 'mask'")
            
        if C == None:
            logging.info("DEM mask (.bin) not found. The file must begins by 'MNT' and must include 'mask'")
        
        A = [os.path.join(path_LastSteps, f) for f in os.listdir(path_LastSteps) if f.endswith(".bin")]            
        B = [os.path.join(path_Interp, os.path.splitext(os.path.basename(f))[0]) for f in A]
        
        
        with open(bat_file_path, "w") as bat_file:
            for a, b in zip(A, B):
                line = f'"{path_code}" filling in="{a}" out="{b}" mask="{C}" dem="{D}"\n'
                bat_file.write(line)
            End = True
                        
        if End == True :  
            logging.info("Please wait for the filling computations. A message will appear to notify you when operations are completed.")
            with wx.MessageDialog(self, f"The interpolation of the given free surface will begin when you press OK, please wait.",
                        "Redirecting", wx.OK | wx.ICON_INFORMATION) as dlg:
                dlg.ShowModal()

            empty_folder(self._manager.IN_SA_INTERP)
            subprocess.run([bat_file_path], check=True)
            
            renamed_files = []
            path_fichier=self._manager.IN_SA_INTERP
            for file in path_fichier.glob("*.tif"):
                if "_h" in file.name:  
                    new_name = file.stem.split("_h")[0].replace(".bin", "") + ".tif"
                    file.rename(file.with_name(new_name))
                    renamed_files.append(new_name) 
            #delete the other
            for file in path_fichier.glob("*.tif"):
                if "_combl" in file.name or file.name not in renamed_files:
                    file.unlink()
            logging.info("Filling completed.")
            with wx.MessageDialog(self, f"Filling completed. Created files : {renamed_files}",
                        "Redirecting", wx.OK | wx.ICON_INFORMATION) as dlg:
                dlg.ShowModal()
            

    
    def OnMainDir(self, e):

        with wx.DirDialog(self, "Choose the main directory containing the data (folders INPUT, TEMP and OUTPUT):",
                          style=wx.DD_DEFAULT_STYLE
                          ) as dlg:

            if dlg.ShowModal() == wx.ID_OK:
                self._manager = Accept_Manager(dlg.GetPath(), Study_area=None)

                self._listbox_studyarea.Clear()
                self._listbox_studyarea.InsertItems(self._manager.get_list_studyareas(), 0)

                self._listbox_scenario.Clear()

                ret = self._manager.check_files()

                if ret == "":
                    logging.info("All the files are present")
                    self._but_acceptability.Enable(True)
                    self._but_vulnerability.Enable(True)
                    self._but_creation.Enable(True)
                else:
                    logging.error(f"Missing files: {ret}")
                    with wx.MessageDialog(self, f"Missing files: \n{ret}", "Error", wx.OK | wx.ICON_ERROR) as dlg:
                        dlg.ShowModal()

            else:
                return

    def OnStudyArea(self, e):
        """ Change the study area """

        if self._manager is None:
            return

        study_area:str = self._manager.get_list_studyareas(with_suffix=True)[e.GetSelection()]
        self._manager.change_studyarea(study_area)

        self._listbox_scenario.Clear()
        sc = self._manager.get_list_scenarios()
        self._listbox_scenario.InsertItems(sc, 0)
                   
        if self.mapviewer is not None:
            tmp_path = self._manager.IN_STUDY_AREA / study_area

            from ..PyDraw import draw_type
            if not tmp_path.stem in self.mapviewer.get_list_keys(drawing_type=draw_type.VECTORS):
                self.mapviewer.add_object('vector', filename=str(tmp_path), id=tmp_path.stem)
                self.mapviewer.Refresh()

    def OnScenario(self, e):
        """ Change the scenario """
        if self._manager is None:
            return

        scenario = self._manager.get_list_scenarios()[e.GetSelection()]
        self._manager.change_scenario(scenario)
               
        self._listbox_returnperiods.Clear()
        rt = self._manager.get_return_periods()
        if len(rt) != 0 :
            self._listbox_returnperiods.InsertItems([str(crt) for crt in rt],0)
            self._listbox_sims.Clear()
            sims = [str(self._manager.get_filepath_for_return_period(currt).name) for currt in rt]
            self._listbox_sims.InsertItems(sims, 0)
            ponds = self._manager.get_ponderations()
            if isinstance(ponds, list):
                self._axes.clear()
                ponds.plot(ax=self._axes, kind='bar')
                self._canvas.draw()

    def OnCreation(self, e):
        """ Create the database """

        if self._manager is None:
            return
        
        wx.MessageBox(
                    "The database will now be created. This process may take some time, and the window may temporarily stop responding.",
                    "Information",
                    wx.OK | wx.ICON_INFORMATION
                    )
        
        steps = list(self._steps_db.GetCheckedStrings())
        steps = [int(cur.split('-')[1]) for cur in steps]
        
        if len(steps) != 0:
            Base_data_creation(self._manager.main_dir, number_procs=self._nb_process.GetValue(), steps=steps)
            
            wx.MessageBox(
                        "The database is created with the selected steps.",
                        "Information",
                        wx.OK | wx.ICON_INFORMATION
                        )
        else :
            wx.MessageBox(
                        "No database created because no steps were selected.",
                        "Attention",
                        wx.OK | wx.ICON_INFORMATION
                        )

    def OnVulnerability(self, e):
        """ Run the vulnerability """

        if self._manager is None:
            return

        steps = list(self._steps_vulnerability.GetCheckedStrings())
        steps = [int(cur.split('-')[1]) for cur in steps]

        if len(steps) == 0:
            logging.error("No steps selected. By default every steps will be performed.")
            Vulnerability(str(self._manager.main_dir),
                      scenario=str(self._manager.scenario),
                      Study_area=str(self._manager.Study_area),
                      steps=[1,10,11,2,3])
            wx.MessageBox(
                        "Vulnerability computed with every steps.",
                        "Information",
                        wx.OK | wx.ICON_INFORMATION
                        )
                        
        else :
            Vulnerability(self._manager.main_dir,
                        scenario=self._manager.scenario,
                        Study_area=self._manager.Study_area,
                        steps=steps)
            wx.MessageBox(
                        "Vulnerability computed with the selected steps.",
                        "Information",
                        wx.OK | wx.ICON_INFORMATION
                        )

    def OnAcceptability(self, e):
        """ Run the acceptability """

        if self._manager is None:
            return

        steps = list(self._steps_acceptability.GetCheckedStrings())
        steps = [int(cur.split('-')[1]) for cur in steps]

        if len(steps) == 0:
            logging.error("No steps selected. By default every steps will be performed.")
            Acceptability(self._manager.main_dir,
                        scenario=self._manager.scenario,
                        Study_area=self._manager.Study_area,
                        steps=[1,2,3,4,5])
            wx.MessageBox(
                        "Acceptability computed with every steps.",
                        "Information",
                        wx.OK | wx.ICON_INFORMATION
                        )
        else :
            Acceptability(self._manager.main_dir,
                        scenario=self._manager.scenario,
                        Study_area=self._manager.Study_area,
                        steps=steps)
            wx.MessageBox(
                        "Acceptability computed with the selected steps.",
                        "Information",
                        wx.OK | wx.ICON_INFORMATION
                        )