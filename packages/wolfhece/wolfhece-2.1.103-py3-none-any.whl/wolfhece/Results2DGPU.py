"""
Author: HECE - University of Liege, Pierre Archambeau
Date: 2024

Copyright (c) 2024 University of Liege. All rights reserved.

This script and its content are protected by copyright law. Unauthorized
copying or distribution of this file, via any medium, is strictly prohibited.
"""

import numpy as np
import numpy.ma as ma
from os import path
from pathlib import Path
from scipy.sparse import csr_array
from multiprocessing import Pool
from typing import Union
from tqdm import tqdm
import logging

from .PyTranslate import _
from .wolf_array import WolfArray
from .wolfresults_2D import Wolfresults_2D, views_2D, getkeyblock, OneWolfResult, vector, zone, Zones
from .PyVertex import wolfvertex
from .CpGrid import CpGrid
from .PyPalette import wolfpalette

try:
    from wolfgpu.results_store import ResultsStore, ResultType
except ImportError:
    logging.debug(_("Unable to import wolfgpu.results_store.ResultsStore. Please install wolfgpu package or add a symlink to the wolfgpu package in the wolfhece directory"))

def _load_res(x) -> tuple[csr_array, csr_array, csr_array]:
    store:ResultsStore
    i:int

    store, i = x
    _, _, _, _, wd_np, qx_np, qy_np = store.get_result(i+1)

    if isinstance(wd_np, csr_array) and isinstance(qx_np, csr_array) and isinstance(qy_np, csr_array):
        return wd_np, qx_np, qy_np
    else:
        return csr_array(wd_np), csr_array(qx_np), csr_array(qy_np)

def _load_res_h(x) -> tuple[csr_array, csr_array, csr_array]:
    store:ResultsStore
    i:int

    store, i = x
    wd_np = store.get_named_result('h',i+1)

    if isinstance(wd_np, csr_array):
        return wd_np
    else:
        return csr_array(wd_np)

class Cache_Results2DGPU():
    """
    Gestion en mémoire de plusieurs résultats GPU
    Stockage CSR afin d'économiser la mémoire (Scipy CSR)
    """

    def __init__(self, fname:str, start_idx:int, end_idx:int = -1, only_h=False) -> None:
        """
        Chargement de résultats sur base du répertoire de sauvegarde de la simulation GPU

        Lecture des résultats depuis start_idx jusque end_idx

        only_h force la lecture de la hauteur d'eau seulement, sinon (h,qx,qy)

        :param fname: nom du répertoire de sauvegarde
        :param start_idx: index de départ (0-based)
        :param end_idx: index de fin (0-based)
        :param only_h: lecture de la hauteur d'eau seulement
        """

        self._results:Union[dict[str,tuple[csr_array, csr_array, csr_array]], dict[str,csr_array]] # typage

        # ResultsStore unique
        self._result_store = ResultsStore(Path(fname), mode='r')
        self._only_h = only_h

        if end_idx == -1:
            end_idx = self._result_store.nb_results

        if end_idx>start_idx:
            self.start_idx = int(max(start_idx,0))
            self.end_idx   = int(min(end_idx, self._result_store.nb_results))

            # Lecture en multiprocess des résultats
            if only_h:
                with Pool() as pool:
                    _results = pool.map(_load_res_h, [(self._result_store,i) for i in range(self.start_idx, self.end_idx)])
                    self._results = {i+1:res for i,res in enumerate(_results)}
            else:
                with Pool() as pool:
                    _results = pool.map(_load_res, [(self._result_store,i) for i in range(self.start_idx, self.end_idx)])
                    self._results = {i+1:res for i,res in enumerate(_results)}

    @property
    def only_h(self):
        return self._only_h

    def __getitem__(self,i:int):
        """Surcharge de l'opérateur []"""
        return self._results[i]

    def get_h(self, idx:int, dense:bool=True) -> Union[np.ndarray, csr_array]:
        """
        Retourne la matrice de hauteur d'eau de la position idx (0-based)
            - en CSR (Scipy CSR)
            - en dense (Numpy array)
        """
        if not self.only_h:
            return self._results[idx][0].toarray() if dense else self._results[idx][0]
        else:
            return self._results[idx].toarray() if dense else self._results[idx]

    def get_qx(self,idx:int, dense:bool=True) -> Union[np.ndarray, csr_array]:
        """
        Retourne la matrice de débit X d'eau de la position idx (0-based)
            - en CSR (Scipy CSR)
            - en dense (Numpy array)
        """

        if not self.only_h:
            return self._results[idx][1].toarray() if dense else self._results[idx][1]
        else:
            return None

    def get_qy(self,idx:int, dense:bool=True) -> Union[np.ndarray, csr_array]:
        """
        Retourne la matrice de débit Y d'eau de la position idx (0-based)
            - en CSR (Scipy CSR)
            - en dense (Numpy array)
        """

        if not self.only_h:
            return self._results[idx][2].toarray() if dense else self._results[idx][2]
        else:
            return None


class wolfres2DGPU(Wolfresults_2D):
    """
    Gestion des résultats du code GPU 2D
    Surcharge de "Wolfresults_2D"
    """

    def __init__(self,
                 fname:str,
                 eps=0.,
                 idx: str = '',
                 plotted: bool = True,
                 mapviewer=None,
                 store = None):

        fname = Path(fname)

        if not fname.name.lower() == 'simul_gpu_results':
            for curdir in fname.iterdir():
                if curdir.name.lower() == 'simul_gpu_results':
                    fname = curdir
                    break

        super().__init__(fname = str(fname), eps=eps, idx=idx, plotted=plotted, mapviewer=mapviewer, loader=self._loader)

        # MERGE Inheriting is a bad idea in general because it allows
        # classes to look inside others, and induces hard
        # coupling. It's better to connect with instances and use
        # their functions so that the provider can better enforce what
        # is available to class's users.


        self._result_store = None
        self.setup_store(store)
        # if store is None:
        #     if (Path(fname) / "simul_gpu_results/nb_results.txt").exists():
        #         self._result_store = ResultsStore(sim_path = Path(fname), mode='r')
        #     else:
        #         logging.warning(_("No results find in the directory, please check the path to the results directory (simul_gpu_results)"))
        # else:
        #     self._result_store = store

        self._cache = None

    def setup_store(self, store = None):
        """
        Setup results store
        """

        if store is None:
            if self._result_store is None:
                if (Path(self.filename) / "nb_results.txt").exists():
                    self._result_store = ResultsStore(sim_path = Path(self.filename), mode='r')
                else:
                    logging.warning(_("No results find in the directory, please check the path to the results directory (simul_gpu_results)"))
        else:
            self._result_store = store

    def setup_cache(self, start_idx:int=0, end_idx:int = -1, only_h:bool = False):
        """
        Setup cache from start_idx result to end_idx result

        if only_h is True, only waterdepth is loaded into memory

        :param start_idx: start index (0-based)
        :param end_idx: end index (0-based)
        :param only_h: only waterdepth is loaded into memory
        """
        self._cache = Cache_Results2DGPU(self.filename, start_idx, end_idx, only_h= only_h)

    def clear_cache(self):
        """
        Clear cache
        """
        self._cache = None

    def _loader(self, fname:str) -> int:
        # 2D GPU

        self.filename = fname
        sim_path = Path(fname).parent

        nb_blocks = 1
        self.myblocks = {}
        curblock = OneWolfResult(0, parent=self)
        self.myblocks[getkeyblock(0)] = curblock

        if (sim_path / 'simul.top').exists():

            curblock.top = WolfArray(path.join(sim_path, 'simul.top'), nullvalue=99999.)
            curblock.waterdepth = WolfArray(path.join(sim_path, 'simul.hbin'))
            curblock.qx = WolfArray(path.join(sim_path, 'simul.qxbin'))
            curblock.qy = WolfArray(path.join(sim_path, 'simul.qybin'))
            curblock.rough_n = WolfArray(path.join(sim_path, 'simul.frot'))

        else:

            if (sim_path / 'parameters.json').exists():

                import json
                with open(path.join(sim_path, 'parameters.json'), 'r') as fp:

                    params = json.load(fp)

                    try:
                        curblock.top.dx = params["parameters"]["dx"]
                        curblock.top.dy = params["parameters"]["dy"]

                        curblock.dx = curblock.top.dx
                        curblock.dy = curblock.top.dy

                    except:
                        logging.error(_('No spatial resolution (dx,dy) in parameters.json -- Results will not be shown in viewer'))
                        return -1

                    try:
                        curblock.top.origx = params["parameters"]["base_coord_x"]
                        curblock.top.origy = params["parameters"]["base_coord_y"]

                        curblock.origx = curblock.top.origx
                        curblock.origy = curblock.top.origy

                    except:
                        logging.error(_('No spatial position (base_coord_x,base_coord_y) in parameters.json -- Results will not be spatially based'))
                        return -2
            else:
                logging.error(_('No parameters.json file found in the simulation directory -- Results will not be shown in viewer'))
                return-3

            pathbathy = sim_path / params['maps']['bathymetry']
            if pathbathy.exists():
                curblock.top = WolfArray(pathbathy)
            else:
                logging.error(_('No bathymetry file found in the simulation directory -- Results will not be shown in viewer'))
                return -4

            pathh = sim_path / params['maps']['h']
            if pathh.exists():
                curblock.waterdepth = WolfArray(pathh)
            else:
                logging.error(_('No waterdepth file found in the simulation directory -- Results will not be shown in viewer'))
                return -5

            pathqx = sim_path / params['maps']['qx']
            if pathqx.exists():
                curblock.qx = WolfArray(pathqx)
            else:
                logging.error(_('No qx file found in the simulation directory -- Results will not be shown in viewer'))
                return -6

            pathqy = sim_path / params['maps']['qy']
            if pathqy.exists():
                curblock.qy = WolfArray(pathqy)
            else:
                logging.error(_('No qy file found in the simulation directory -- Results will not be shown in viewer'))
                return -7

            pathmanning = sim_path / params['maps']['manning']
            if pathmanning.exists():
                curblock.rough_n = WolfArray(pathmanning)
            else:
                logging.error(_('No manning file found in the simulation directory -- Results will not be shown in viewer'))
                return -8

        # Force nullvalue to zero because it will influence the size of the arrow in vector field views
        curblock.qx.nullvalue = 0.
        curblock.qy.nullvalue = 0.

        self.loaded_rough = True

        self.head_blocks[getkeyblock(0)] = curblock.top.get_header()

        to_check =[curblock.waterdepth, curblock.qx, curblock.qy, curblock.rough_n]
        check = False
        for curarray in to_check:
            check |= curarray.dx != curblock.top.dx
            check |= curarray.dy != curblock.top.dy
            check |= curarray.origx != curblock.top.origx
            check |= curarray.origy != curblock.top.origy
            check |= curarray.translx != curblock.top.translx
            check |= curarray.transly != curblock.top.transly

        if check:
            if (sim_path / 'simul.top').exists():
                logging.error(_("Inconsistent header file in .top, .qxbin, .qybin or .frot files"))
                logging.error(_("Forcing information into memory from the .top file -- May corrupt spatial positionning -- Please check your data !"))
            elif pathbathy.exists():
                logging.error(_("Inconsistent header file"))
                logging.error(_("Forcing information into memory from the bathymetry file -- May corrupt spatial positionning -- Please check your data !"))


            for curarray in to_check:
                curarray.dx    = curblock.top.dx
                curarray.dy    = curblock.top.dy
                curarray.origx = curblock.top.origx
                curarray.origy = curblock.top.origy
                curarray.translx = curblock.top.translx
                curarray.transly = curblock.top.transly

        if (sim_path / 'simul.trl').exists():
            with open(sim_path / 'simul.trl') as f:
                trl=f.read().splitlines()
                self.translx=float(trl[1])
                self.transly=float(trl[2])

        curblock.set_current(views_2D.WATERDEPTH)

        self.myparam = None
        self.mymnap = None
        self.myblocfile = None

        return 0

    def get_nbresults(self, force_update_timessteps=True):
        """
        Récupération du nombre de résultats

        Lecture du fichier de tracking afin de permettre une mise à jour en cours de calcul
        """
        if self._result_store is None:
            self.setup_store()
            if self._result_store is None:
                logging.warning(_("No results store available"))
                return

        self._result_store.reload()
        if force_update_timessteps:
            self.get_times_steps()

        self._nb_results = self._result_store.nb_results
        return self._result_store.nb_results

    def read_oneresult(self, which:int=-1):
        """
        Lecture d'un pas de sauvegarde

        which: result number to read; 0-based; -1 == last one
        """

        which = self._sanitize_result_step(which)

        # stored result files are 1-based -> which+1
        if self._cache is not None:
            if (which >= self._cache.start_idx and which < self._cache.end_idx) and (not self._cache.only_h):
                wd_np = self._cache.get_h(which+1, True)
                qx_np = self._cache.get_qx(which+1, True)
                qy_np = self._cache.get_qy(which+1, True)
            else:
                _, _, _, _, wd_np, qx_np, qy_np = self._result_store.get_result(which+1)
        else:
            __, __, __, __, wd_np, qx_np, qy_np = self._result_store.get_result(which+1)

        wd_np = wd_np.T
        qx_np = qx_np.T
        qy_np = qy_np.T

        curblock = self.myblocks[getkeyblock(1,False)]

        curblock.waterdepth.array.data[:,:] = curblock.waterdepth.nullvalue
        curblock.qx.array.data[:,:] = curblock.qx.nullvalue
        curblock.qy.array.data[:,:] = curblock.qy.nullvalue

        curblock.waterdepth.array.mask[:,:] = True
        curblock.qx.array.mask[:,:] = True
        curblock.qy.array.mask[:,:] = True

        if self.epsilon > 0.:
            # curblock.waterdepth.array=ma.masked_less_equal(wd_np.astype(np.float32).T, self.epsilon)

            ij = np.where(wd_np >= self.epsilon)
            curblock.waterdepth.array.data[ij] = wd_np[ij]
            curblock.waterdepth.array.mask[ij] = False
        else:
            # curblock.waterdepth.array=ma.masked_equal(wd_np.astype(np.float32).T, 0.)

            ij = np.where(wd_np > 0.)
            curblock.waterdepth.array.data[ij] = wd_np[ij]
            curblock.waterdepth.array.mask[ij] = False

        # curblock.qx.array=ma.masked_where(curblock.waterdepth.array.mask,qx_np.astype(np.float32).T)
        # curblock.qy.array=ma.masked_where(curblock.waterdepth.array.mask,qy_np.astype(np.float32).T)

        curblock.qx.array.data[ij]  = qx_np[ij]
        curblock.qy.array.data[ij]  = qy_np[ij]

        curblock.qx.array.mask[ij] = False
        curblock.qy.array.mask[ij] = False

        curblock.waterdepth.count()
        curblock.qx.count()
        curblock.qy.count()

        # curblock.waterdepth.set_nullvalue_in_mask()
        # curblock.qx.set_nullvalue_in_mask()
        # curblock.qy.set_nullvalue_in_mask()

        if self.to_filter_independent:
            self.filter_independent_zones()

        self.current_result = which
        self.loaded=True

    def _read_oneresult_only_h(self, which:int=-1):
        """
        Lecture d'un pas de sauvegarde

        which: result number to read; 0-based; -1 == last one
        """

        which = self._sanitize_result_step(which)

        # stored result files are 1-based -> which+1
        if self._cache is not None:
            if (which >= self._cache.start_idx and which < self._cache.end_idx):
                wd_np = self._cache.get_h(which+1, True)
            else:
                _, _, _, _, wd_np, qx_np, qy_np = self._result_store.get_result(which+1)
        else:
            __, __, __, __, wd_np, qx_np, qy_np = self._result_store.get_result(which+1)

        wd_np = wd_np.T

        curblock = self.myblocks[getkeyblock(1,False)]

        curblock.waterdepth.array.data[:,:] = curblock.waterdepth.nullvalue

        curblock.waterdepth.array.mask[:,:] = True

        if self.epsilon > 0.:
            ij = np.where(wd_np >= self.epsilon)
            curblock.waterdepth.array.data[ij] = wd_np[ij]
            curblock.waterdepth.array.mask[ij] = False
        else:
            ij = np.where(wd_np > 0.)
            curblock.waterdepth.array.data[ij] = wd_np[ij]
            curblock.waterdepth.array.mask[ij] = False

        curblock.waterdepth.count()

        if self.to_filter_independent:
            self.filter_independent_zones()

        self.current_result = which
        self.loaded=True

    def _update_result_view(self):
        """
        Procédure interne de mise à jour du pas

        Etapes partagées par read_next et read_previous
        """
        self.current_result = self._sanitize_result_step(self.current_result)
        self.read_oneresult(self.current_result)

    # def read_next(self):
    #     """
    #     Lecture du pas suivant
    #     """
    #     self.current_result+= self._step_interval
    #     self._update_result_view()

    def get_times_steps(self, nb:int = None):
        """
        Récupération des temps réels et les pas de calcul de chaque résultat sur disque

        :param nb : nombre de résultats à lire

        """

        if self._result_store is None:
            self.setup_store()
            if self._result_store is None:
                logging.warning(_("No results store available"))
                return

        self.times = [time[ResultType.T.value] for time in self._result_store._sim_times]
        self.timesteps = [time[ResultType.STEP_NUM.value] for time in self._result_store._sim_times]

        if nb is None:
            return self.times, self.timesteps
        elif nb == 0:
            self.times, self.timesteps = [],[]
            return self.times, self.timesteps
        else:
            if nb <= len(self.times):
                return self.times[:nb], self.timesteps[:nb]
            else:
                return self.times, self.timesteps

    @property
    def all_dt(self):
        return self._result_store.get_named_series(ResultType.LAST_DELTA_T)

    @property
    def all_mostly_dry_mesh(self):
        return self._result_store.get_named_series(ResultType.NB_MOSTLY_DRY_MESHES)

    @property
    def all_clock_time(self):
        return self._result_store.get_named_series(ResultType.CLOCK_T)

    @property
    def all_wet_meshes(self):
        return self._result_store.get_named_series(ResultType.NB_WET_MESHES)

    # def read_previous(self):
    #     """
    #     Lecture du pas suivant
    #     """
    #     self.current_result -= self._step_interval
    #     self._update_result_view()

    def get_cached_h(self, idx):
        """ Return cached water depth according to WOLF convention """

        if self._cache is not None:
            return self._cache.get_h(idx+1, True).T
        else:
            return None

    def get_cached_qx(self, idx):
        """ Return cached specific discharge along X according to WOLF convention """

        if self._cache is not None:
            return self._cache.get_qx(idx+1, True).T
        else:
            return None

    def get_cached_qy(self, idx):
        """ Return cached specific discharge along Y according to WOLF convention """

        if self._cache is not None:
            return self._cache.get_qy(idx+1, True).T
        else:
            return None

    def show_tiles(self):
        """ Show tiles in mapviewer """

        if self.mapviewer is None:
            logging.error(_("No mapviewer available"))
            return

        grid_tiles = Zones()

        ox = self.origx
        oy = self.origy

        tile_size = 16

        dx_tiles = self[0].dx * tile_size
        dy_tiles = self[0].dy * tile_size

        nbx = int(self[0].nbx // tile_size + (1 if np.mod(self[0].nbx, tile_size) else 0))
        nby = int(self[0].nby // tile_size + (1 if np.mod(self[0].nby, tile_size) else 0))

        tiles_zone = zone(name = 'Tiles', parent = grid_tiles)
        grid_tiles.add_zone(tiles_zone)

        grid_x = vector(name = 'tiles_x', parentzone=tiles_zone)
        grid_y = vector(name = 'tiles_y', parentzone=tiles_zone)
        tiles_zone.add_vector(grid_x)
        tiles_zone.add_vector(grid_y)

        for i in range(nbx+1):
            if np.mod(i, 2) == 0:
                grid_x.add_vertex(wolfvertex(ox + i * dx_tiles, oy))
                grid_x.add_vertex(wolfvertex(ox + i * dx_tiles, oy + nby * dy_tiles))
            else:
                grid_x.add_vertex(wolfvertex(ox + i * dx_tiles, oy + nby * dy_tiles))
                grid_x.add_vertex(wolfvertex(ox + i * dx_tiles, oy))

        for j in range(nby+1):
            if np.mod(j, 2) == 0:
                grid_y.add_vertex(wolfvertex(ox, oy + j * dy_tiles))
                grid_y.add_vertex(wolfvertex(ox + nbx * dx_tiles, oy + j * dy_tiles))
            else:
                grid_y.add_vertex(wolfvertex(ox + nbx * dx_tiles, oy + j * dy_tiles))
                grid_y.add_vertex(wolfvertex(ox, oy + j * dy_tiles))


        self.mapviewer.add_object('vector', newobj = grid_tiles, id = 'Tiles')

    def set_hqxqy_as_initial_conditions(self, idx:int = None, as_multiblocks:bool = False):
        """
        Set the result as IC

        :param idx : 0-based index
        """

        if idx is not None:
            if idx>=0 and idx<self.get_nbresults():
                self.read_oneresult(idx)
            elif idx ==-1:
                self.read_oneresult(-1) # last one
            else:
                logging.error(_('Bad index for initial conditions'))
                return

        self.set_currentview(views_2D.WATERDEPTH)

        hini = self.as_WolfArray()

        self.set_currentview(views_2D.QX)

        qxini = self.as_WolfArray()

        self.set_currentview(views_2D.QY)

        qyini = self.as_WolfArray()

        if (hini is not None) and (qxini is not None) and (qyini is not None):

            # hini = hini.as_WolfArray()
            # qxini = qxini.as_WolfArray()
            # qyini = qyini.as_WolfArray()

            hini.write_all(self.filename.parent  / 'h.npy')
            qxini.write_all(self.filename.parent / 'qx.npy')
            qyini.write_all(self.filename.parent / 'qy.npy')

            logging.info(_('Initial conditions saved as Numpy files'))
        else:
            logging.error(_('No initial conditions saved'))
