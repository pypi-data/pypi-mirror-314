import numpy as np
import laspy
from laspy.compression import LazBackend
from PIL import Image
from os.path import exists,join
import matplotlib.pyplot as plt
from os import stat,remove,listdir,scandir, makedirs
import pathlib
import math
from time import sleep
from typing import Literal, Union
import zipfile
import logging
from enum import Enum
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from shapely.geometry import LineString, Point, CAP_STYLE, Polygon
from shapely.ops import prep
import wx

from . import viewer
from ..PyWMS import getWalonmap
from ..PyTranslate import _
from ..color_constants import Colors
from ..PyParams import Wolf_Param

"""
Importation et visualisation de données LAS et LAZ

@author Pierre Archambeau
"""
class Colors_Lazviewer(Enum):
    ORTHO_2012_2013 = 2013
    ORTHO_2015 = 2015
    ORTHO_2021 = 2021
    ORTHO_2023 = 2023
    ORTHO_2006_2007 = 2006
    CODE_2013 = 0
    CODE_2023 = 2
    FROM_FILE = 1

class Classification_LAZ():

    def __init__(self) -> None:
        self.classification:dict[str,str,list[float,float,float,float]] = {}
        self.test_wx()

        self._choose_colors = None

    def test_wx(self):
        self.wx_exists = wx.App.Get() is not None

    def init_2013(self):

        self.classification={
            1  : ['Hors-sol', 'building, toits et autres', Colors.rgb_withalpha_float('white',.2),],
            2  : ['Sol', 'y compris talus et digues', Colors.rgb_withalpha_float('brown',1.)],
            4  : ['Végétation', 'y compris la végétation linéaire', Colors.rgb_withalpha_float('forestgreen',1.)],
            9  : ['Eau', 'Eau',Colors.rgb_withalpha_float('aqua',1.)],
            10 : ['Ponts', 'Ponts',Colors.rgb_withalpha_float('lightyellow1',1.)]}

    def init_2023(self):

        self.classification={
            1  : ['Défaut', 'Voiture, câbles électrique, points de végétation diffus, Sursol non utile', Colors.rgb_withalpha_float('white',.2),],
            2  : ['Sol', 'Tous les éléments du sol y compris les descentes de garage en sous-sol', Colors.rgb_withalpha_float('gray',1.)],
            4  : ['Végétation', 'Végétation', Colors.rgb_withalpha_float('forestgreen',1.)],
            6  : ['Bâtiments', 'Bâtiments',Colors.rgb_withalpha_float('lightslategray',1.)],
            9  : ['Eau', 'Points de la surface d\’eau brute mesurés par le scanner 2',Colors.rgb_withalpha_float('royalblue',.3)],
            10 : ['Ponts', 'Les ponts ont été classés à part pour améliorer la définition du MNT. Ils ont été ouverts grâce',Colors.rgb_withalpha_float('lightyellow1',1.)],
            11 : ['Mur de berges', 'Mur et muret en berge de la Vesdre dépassant le sol à des vocation de réaliser une modélisation 3D hydraulique avec ces obstacles.',Colors.rgb_withalpha_float('red1',1.)],
            15 : ['Tranche d\'eau', 'Echo intermédiaire dans l\’eau n\’appartenant ni à la surface d\’eau ni au fond du lit', Colors.rgb_withalpha_float('lightblue',.2)],
            16 : ['Surface bathymétrique', 'Fond du lit de la Vesdre et de ses affluents et des autres surfaces d\’eau mesurées à partir du scanner 3 FWF discrétisé',Colors.rgb_withalpha_float('sandybrown',1.)],
            17 : ['Surface bathymétrique incertaine', 'Surface bathymétrique sur les zones peu profondes principalement sous végétation où les intensités des échos sont parfois trop faibles pour avoir la certitude qu\’ils représentent le fond de rivière. La classe 17 est néanmoins plus certaine que la classe 18. Elle est utilisée dans la génération des MNT par défaut.',Colors.rgb_withalpha_float('rosybrown',.5)],
            19 : ['Surface d\eau calculée', 'Points sous échantillonnés de la surface d\’eau ayant servis à faire les calculs de correction de réfraction bathymétrique',Colors.rgb_withalpha_float('lightblue',.2)],
            20 : ['Surface bathymétrique incertaine profonde', 'Surface bathymétrique sur les zones plus profondes principalement au centre de la rivière où les intensités des échos sont parfois trop faibles pour avoir la certitude qu\’ils représentent le fond de rivière. Non utilisée dans la génération du MNT. + Surface proche bathy mais potentiellement émergée pour les scanner 1 à 3',Colors.rgb_withalpha_float('lightblue',.5)],
            29 : ['Surface d\'eau héliportée', 'La hauteur d\’eau du vol héliporté étant largement supérieure (de 30 à 40cm au vol Titan, les points matérialisant cette surface ont été reclassés dans cette classe séparée pour ne pas perturbé le reste du nuage de point.',Colors.rgb_withalpha_float('cyan',.3)]}

    def callback_colors(self):
        """ Update from wx GUI """

        for key, curclass in self.classification.items():
            name, comment, col = curclass
            cur_color = [float(cur)/255. for cur in self._choose_colors[(_('Colors'), name)]]

            self.classification[key] = [name, comment, cur_color]

    def callback_destroy(self):
        self.callback_colors()
        self._choose_colors = None

    def interactive_update_colors(self):
        """ set GUI """
        self.test_wx()

        if self._choose_colors is None and self.wx_exists:
            self._choose_colors = Wolf_Param(None, _('Colors of classification LAZ 2023'), w=600, h=800, to_read=False, withbuttons=True, toShow=False, force_even_if_same_default=True)
            self._choose_colors.callback        = self.callback_colors
            self._choose_colors.callbackdestroy = self.callback_destroy
            self._choose_colors.hide_selected_buttons()

        for key, curclass in self.classification.items():
            name, comment, color = curclass
            self._choose_colors.addparam(_('Colors'), name, [int(cur*255) for cur in color], 'Color', comment, whichdict='All')

        self._choose_colors.Populate()
        self._choose_colors.SetSize((600,500))
        self._choose_colors.Show()


def choices_laz_colormap() -> list[str]:

    choices = [cur.name for cur in Colors_Lazviewer]
    values  = [cur.value for cur in Colors_Lazviewer]

    return choices, values

class xyz_laz():
    """
    Classe de gestion des fichiers XYZ+Class issus d'un gros fichier laz
    """

    def __init__(self, fn:str='', format:Literal['las', 'numpy']='las', to_read:bool=True) -> None:

        # Emprise spatiale
        self.origx = -99999.
        self.origy = -99999.
        self.endx  = -99999.
        self.endy  = -99999.

        # format de fichier
        self.format = format
        self.dtype = np.float32

        if fn !='':
            self.filename = fn

            if not (exists(self.filename) or exists(self.filename+'.zip')):
                self.data = []
                return

            last_part = pathlib.Path(fn).name
            parts = last_part.split('_')

            # L'origine est codée dans le nom de fichier
            self.origx = float(parts[2])
            self.origy = float(parts[3])

            dx = 2500.
            dy = 3500.

            # Récupération du lien vers le fichier GridInfo.txt
            gridinfo=join(pathlib.Path(fn).parent,'gridinfo.txt')

            if exists(gridinfo):
                with open(gridinfo,'r') as f:
                    myinfos=f.read().splitlines()

                    myinfos[0]=np.float32(myinfos[0].split(',')) # xmin, xmax
                    myinfos[1]=np.float32(myinfos[1].split(',')) # ymin, ymax
                    myinfos[2]=np.float32(myinfos[2].split(',')) # NbX, NbY

                    # calcul du pas spatial de découpage selon X et Y
                    dx = (myinfos[0][1]-myinfos[0][0])/myinfos[2][0]
                    dy = (myinfos[1][1]-myinfos[1][0])/myinfos[2][1]

                    if len(myinfos)==5:
                        self.dtype = np.float64 if myinfos[4].lower()=='xy_float64' else np.float32

            # extrêmité de fichier
            self.endx = self.origx + dx
            self.endy = self.origy + dy

            if to_read:
                 self.read_bin_xyz()

    @property
    def size(self):
        return len(self.data)

    def split(self, dir_out:str, nbparts:int):
        """ Split file into 'nb' parts along X and Y"""

        xparts = np.linspace(self.origx,self.endx,nbparts+1)
        yparts = np.linspace(self.origy,self.endy,nbparts+1)

        dx = (self.endx-self.origx)/nbparts
        dy = (self.endy-self.origy)/nbparts

        for curx in xparts[:-1]:
            for cury in yparts[:-1]:
                with open(join(dir_out,'LIDAR_2013_2014_'+str(int(curx))+'_'+str(int(cury))+'_xyz.bin'),'wb') as f:

                    curbounds = [[curx,curx+dx],[cury,cury+dy]]
                    mypts = find_pointsXYZ(self.data,curbounds)
                    if len(mypts)>0:
                        f.write(np.int32(mypts.shape[0]))
                        f.write(np.float32(mypts[:,0]).tobytes())
                        f.write(np.float32(mypts[:,1]).tobytes())
                        f.write(np.float32(mypts[:,2]).tobytes())
                        f.write(np.int8(mypts[:,3]).tobytes())

    def get_bounds(self):
        # Return geographic bounds of the file
        return ((self.origx,self.endx),(self.origy,self.endy))

    def test_bounds(self, bounds:list[list[float, float],list[float, float]]):
        # Test current bounds relating to parameter bounds

        x1=bounds[0][0]
        x2=bounds[0][1]
        y1=bounds[1][0]
        y2=bounds[1][1]

        mybounds = self.get_bounds()

        test = not(x2 < mybounds[0][0] or x1 > mybounds[0][1] or y2 < mybounds[1][0] or y1 > mybounds[1][1])

        return test

    def read_bin_xyz(self):
        """
        Lecture d'un fichier binaire de points XYZ+classification généré par la fonction sort_grid_np
        Le format est une succession de trame binaire de la forme :

        nbpoints (np.int32)
        X[nbpoints] (np.float32) ou (np.float64)
        Y[nbpoints] (np.float32) ou (np.float64)
        Z[nbpoints] (np.float32)
        Classif[nbpoints] (np.int8)

        Il est possible de récupérer une matrice numpy shape(nbtot,4)
        ou un objet laspy via l'argument 'out' (par défaut à 'las')
        """
        fn=self.filename

        if exists(fn+'.zip'):
            with zipfile.ZipFile(fn+'.zip','r') as zip_file:
                fn = zip_file.namelist()[0]
                zip_file.extract(fn, path=pathlib.Path(fn).parent)
                fn = join(pathlib.Path(fn).parent, fn)
        elif not exists(fn):
            return

        fnsize=stat(fn).st_size

        nb=0
        count=0
        myret=[]

        with open(fn,'rb') as f:
            while count<fnsize:
                nbloc = np.frombuffer(f.read(4),np.int32)[0]
                nb+=nbloc

                dtype_file = self.dtype

                blocsize = nbloc*4 if dtype_file == np.float32 else nbloc*8

                x=np.frombuffer(f.read(blocsize),dtype_file)
                y=np.frombuffer(f.read(blocsize),dtype_file)
                z=np.frombuffer(f.read(nbloc*4),np.float32)
                classi=np.frombuffer(f.read(nbloc),np.int8)

                count+=4+(2*blocsize+nbloc*(4+1))

                if classi.shape[0] != nbloc:
                    logging.warning(_('Bad classification size - file {}'.format(fn)))
                else:
                    if len(myret)==0:
                        # dt=[('x',np.float32),('y',np.float32),('z',np.float32),('classification',np.int8)]
                        myret=np.array([x,y,z,classi]).transpose()
                    else:
                        if len(x)>1:
                            added = np.array([x,y,z,classi]).transpose()

                            if myret.shape[1] == added.shape[1]:
                                myret=np.concatenate((myret,added))
                            else:
                                logging.warning(_('Incompatible shapes'))

        # Format Numpy
        self.data = myret

        if self.format=='las':
            self.to_las()

        # suppressdion du fichier extrait
        if exists(self.filename+'.zip'):
            remove(fn)

    def to_las(self):
        if self.format=='las':
            return
        else:
            # self.data=xyz_to_las(self.data)
            self.format='las'

class xyz_laz_grid():
    """
    Gestion d'un grid de données LAZ
    """

    def __init__(self, mydir:str) -> None:

        # répertoire de stockage des données griddées, y compris fichier 'gridinfo.txt'
        self.mydir = mydir

        gridinfo=join(mydir,'gridinfo.txt')

        self.origx,self.endx, self.origy,self.endy, self.nbx,self.nby, self.genfile = self._read_gridinfo(gridinfo)

        if self.nbx>0 and self.nby>0:
            self.dx = (self.endx-self.origx)/float(self.nbx)
            self.dy = (self.endy-self.origy)/float(self.nby)

    def _read_gridinfo(self, gridinfo:str) -> list:

        if exists(gridinfo):
            with open(gridinfo,'r') as f:
                myinfos=f.read().splitlines()

                origx, endx=np.float32(myinfos[0].split(','))
                origy, endy=np.float32(myinfos[1].split(','))
                nbx, nby=np.int32(myinfos[2].split(','))
                genfile = myinfos[3] # nom à pister avec x1 et y1 comme paramètres

            return [origx, endx, origy, endy, nbx, nby, genfile]
        else:
            return [99999.,99999.,99999.,99999.,0,0,'']

    def scan(self, bounds:Union[tuple[tuple[float,float],tuple[float,float]], list[list[float, float],list[float, float]]]):
        """ Find all points in bounds """
        x1=bounds[0][0]
        x2=bounds[0][1]
        y1=bounds[1][0]
        y2=bounds[1][1]

        file1= self.genfile.split('x1')[0]
        file2= self.genfile.split('y1')[-1]

        data=[]

        for x in range(int(self.origx), int(self.endx), int(self.dx)):
            for y in range(int(self.origy), int(self.endy), int(self.dy)):

                locbounds=np.float64(((x,x+self.dx),(y,y+self.dy)))

                test = not(x2 < locbounds[0][0] or x1 > locbounds[0][1] or y2 < locbounds[1][0] or y1 > locbounds[1][1])

                if test:
                    fxyz = file1+str(int(x))+'_'+str(int(y))+file2

                    fn = join(self.mydir,fxyz)
                    locxyz=xyz_laz(fn)
                    if locxyz.size > 0:
                        data.append(locxyz.data)

        if len(data)>0:
            retdata=find_pointsXYZ(np.concatenate(data), bounds)
        else:
            retdata = np.asarray([])

        return retdata

    def _split_xyz(self, dirout:str, nbparts:int = 10):
        """ Split XYZ file into 'nb' parts along X and Y """
        for entry in scandir(self.mydir):
            if entry.is_file():
                if entry.name.endswith('.bin'):

                    myxy = xyz_laz(entry.path)
                    myxy.split(dirout, nbparts)
                    print(entry.name)

    def _sort_grid_np(self,
                     fn_in:str,  # laz file
                     fn_out:str, # generic file name in dir out
                     bounds:Union[tuple[tuple[float,float],tuple[float,float]], list[list[float, float],list[float, float]]],
                     gridsize:list[int],
                     chunksize:int=5000000,
                     force_format = np.float64):

        """ Create .bin files from .laz """
        xbounds=bounds[0]
        ybounds=bounds[1]

        xloc = np.linspace(xbounds[0], xbounds[1], gridsize[0]+1)
        yloc = np.linspace(ybounds[0], ybounds[1], gridsize[1]+1)

        dirout = pathlib.Path(fn_out).parent
        fn=join(dirout,'gridinfo.txt')

        if exists(fn):
            remove(fn)

        with open(fn,'w') as f:
            f.write(str(int(xbounds[0]))+','+str(int(xbounds[1]))+'\n')
            f.write(str(int(ybounds[0]))+','+str(int(ybounds[1]))+'\n')
            f.write(str(int(gridsize[0]))+','+str(int(gridsize[1]))+'\n')
            f.write(pathlib.Path(fn_out).name+'_'+'x1'+'_'+'y1'+'_xyz.bin'+'\n')
            if force_format == np.float64:
                f.write('xy_float64')
            else:
                f.write('xy_float32')

        k=0
        with laspy.open(fn_in, laz_backend=LazBackend.Laszip) as f:
            nb = (f.header.point_count // chunksize) +1
            print('Points from Header:', f.header.point_count)

            #création des objets d'écriture
            writers=[]
            for i in range(gridsize[0]):
                writers.append([])

                for j in range(gridsize[1]):
                    fn=fn_out+'_'+str(int(xloc[i]))+'_'+str(int(yloc[j]))+'_xyz.bin'
                    if exists(fn):
                        remove(fn)

                    writers[i].append(open(fn, "wb"))

            for las in f.chunk_iterator(chunksize):
                print(k,' / ',nb)
                for i in range(gridsize[0]):
                    for j in range(gridsize[1]):
                        mypts=find_points(las,(xloc[i],xloc[i+1]),(yloc[j],yloc[j+1]))
                        if mypts is not None:
                            print(len(mypts))

                            print(int(xloc[i]),int(yloc[j]))
                            writers[i][j].write(np.int32(len(mypts)))

                            if force_format == np.float64:
                                writers[i][j].write(np.float64(mypts.x).tobytes())
                                writers[i][j].write(np.float64(mypts.y).tobytes())
                            else:
                                writers[i][j].write(np.float32(mypts.x).tobytes())
                                writers[i][j].write(np.float32(mypts.y).tobytes())

                            writers[i][j].write(np.float32(mypts.z).tobytes())
                            writers[i][j].write(np.int8(mypts.classification).tobytes())

                k+=1
                print('--')

        self.origx = xbounds[0]
        self.origy = ybounds[0]
        self.endx = xbounds[1]
        self.endy = ybounds[1]
        self.nbx = gridsize[0]
        self.nby = gridsize[1]
        self.dx = (self.endx-self.origx)/float(self.nbx)
        self.dy = (self.endy-self.origy)/float(self.nby)
        self.genfile=fn_out+'_'+'x1'+'_'+'y1'+'_xyz.bin'

        for curwriter in writers:
            for curfile in curwriter:
                curfile.close()

        for i in range(gridsize[0]):
            for j in range(gridsize[1]):
                fn = fn_out+'_'+str(int(xloc[i]))+'_'+str(int(yloc[j]))+'_xyz.bin'
                curstat = stat(fn)
                if curstat.st_size==0:
                    remove(fn)
                else:
                    if force_format == np.float64:
                        fnzip = fn + '.zip'
                        with zipfile.ZipFile(fnzip,'w',zipfile.ZIP_DEFLATED) as zip_file:
                            zip_file.write(fn, pathlib.Path(fn).name)
                        remove(fn)


class xyz_laz_grids():
    """ Ensemble de grids """

    def __init__(self, dir_grids:str, create:bool=False) -> None:
        self.grids = []
        self.colors = Classification_LAZ()
        self.colors.init_2023()

        if exists(dir_grids):
            self.dir = dir_grids
            self.read_dir(dir_grids)
        else:
            if create:
                makedirs(dir_grids, exist_ok=True)
                self.dir = dir_grids
            else:
                self.dir = None

    def scan(self, bounds:Union[tuple[tuple[float,float],tuple[float,float]], list[list[float, float],list[float, float]]]) -> np.ndarray:
        """
        Scan all LAZ to find used data

        :param bounds: [[xmin,xmax], [ymin,ymax]]
        :type bounds: Union[tuple[tuple[float,float],tuple[float,float]], list[list[float, float],list[float, float]]]
        :return: np.ndarray
        """
        ret = [cur.scan(bounds) for cur in self.grids]
        ret = [cur for cur in ret if len(cur)>0]

        if len(ret)==0:
            return np.asarray([])
        else:
            return np.concatenate(ret)

    def read_dir(self, dir_grids):
        dirs = listdir(dir_grids)

        for curdir in dirs:
            self.grids.append(xyz_laz_grid(join(dir_grids,curdir)))

    def scan_around(self, xy:Union[LineString,list[list[float], list[float]]], length_buffer=5.):
        """
        Récupération de points LAZ autour de la section
        """

        if isinstance(xy, LineString):
            myls = xy
        else:
            myls = LineString([Point(x,y) for x,y in xy])

        logging.info(_('Create buffer around polyline'))
        # Création d'un buffer autour de la LineString
        mypoly:Polygon
        mypoly = myls.buffer(length_buffer,cap_style=CAP_STYLE.square)

        logging.info(_('Get bounding box'))
        # Récupération des bornes
        mybounds = ((mypoly.bounds[0],mypoly.bounds[2]),(mypoly.bounds[1],mypoly.bounds[3]))
        logging.info(_('Get LAZ points bounding box'))
        # scan sur base du rectangle
        myxyz = self.scan(mybounds)

        logging.info(_('Select interior points'))
        # Vérification des points intérieurs
        prep_poly = prep(mypoly)
        mytests = [prep_poly.contains(Point(cur[:3])) for cur in myxyz]

        usedlaz = np.asarray(myxyz[mytests])

        logging.info(_('Compute distance along polyline'))
        # Projection des points utiles le long du vecteur
        s = np.asarray([myls.project(Point(cur[:2])) for cur in usedlaz])

        # smax = myls.length
        # usedlaz = usedlaz[np.logical_and((s !=0.),(s != smax))]

        logging.info(_('Compute colors'))
        # couleurs
        colors=np.ones((usedlaz.shape[0],4),dtype=np.float32)

        for key, val in self.colors.classification.items():
            name, comment, color = val
            colors[usedlaz[:,3] == key] = color

        logging.info(_('Compute distance perpendicular to polyline'))
        # distance normale au vecteur --> alpha/transparence
        orig = np.asarray(myls.coords[0])
        extr = np.asarray(myls.coords[-1])
        a    = extr-orig
        s_perp = np.asarray([float(np.cross(a, cur[:3] - orig)[2])  for cur in usedlaz])
        smax = np.max(np.abs(s_perp))

        logging.info(_('Alpha blending'))
        colors[:,3] = 1.-np.abs(s_perp)/smax

        logging.info(_('Find up and Down points'))
        # recherche des points à l'amont
        up=np.where(s_perp[:]<0.)[0]
        # recherche des points à l'aval
        down=np.where(s_perp[:]>=0.)[0]

        up_s = s[up]
        down_s = s[down]

        up_z = usedlaz[up,2]
        down_z = usedlaz[down,2]

        up_colors = colors[up]
        down_colors = colors[down]

        logging.info(_('Number of points upstream : {}'.format(len(up_s))))
        logging.info(_('Number of points downstream : {}'.format(len(down_s))))

        return (up_s, up_z, up_colors), (down_s, down_z, down_colors)

    def plot_laz(self, xy:Union[LineString, list[list[float], list[float]]], length_buffer=5., figax:tuple[Figure, Axes]=None, show=False):
        """
        Dessin des points LAZ sur un graphique Matplotlib
        """

        (up_s, up_z, up_color), (down_s, down_z, down_color) = self.scan_around(xy, length_buffer)

        if figax is None:
            fig = plt.figure()
            ax=fig.add_subplot(111)
        else:
            fig,ax = figax

        logging.info(_('Plotting'))
        ax.scatter(up_s,   up_z,  c=up_color  ,marker='.')
        ax.scatter(down_s, down_z,c=down_color,marker='+')

        if show:
            fig.show()

        return fig,ax

    def create_from_laz(self, dir_laz:str, shape:str, ds:float = 50, force_format = np.float64):

        try:
            from ..PyVertexvectors import Zones
        except:
            from wolfhece.PyVertexvectors import Zones
        vecs = Zones(shape)

        for entry in scandir(dir_laz):
            if entry.is_file():
                if entry.name.endswith('.laz'):

                    file_wo_suf = entry.name.removesuffix('.laz')
                    dirname = join(self.dir, file_wo_suf)

                    if not exists(dirname):
                        makedirs(dirname, exist_ok=True)

                        newlaz = xyz_laz_grid(mydir=dirname)

                        vec = vecs.get_zone(file_wo_suf)
                        bounds = vec.myvectors[0].get_bounds()

                        dx = bounds[1][0] -bounds[0][0]
                        dy = bounds[1][1] -bounds[0][1]
                        nb = max(int(dx/ds), int(dy/ds))

                        self.grids.append(newlaz._sort_grid_np(entry.path,
                                                            join(dirname, file_wo_suf),
                                                            bounds=[[bounds[0][0], bounds[1][0]], [bounds[0][1], bounds[1][1]]],
                                                            gridsize=[int(dx/ds), int(dy/ds)],
                                                            force_format=force_format))

def find_pointsXYZ(xyz:np.ndarray, bounds:Union[tuple[tuple[float,float],tuple[float,float]], list[list[float, float],list[float, float]]]) -> np.ndarray:

    xb=bounds[0]
    yb=bounds[1]
    # Get arrays which indicate invalid X, Y, or Z values.
    X_valid = np.logical_and((xb[0] <= xyz[:,0]), (xb[1] >= xyz[:,0]))
    Y_valid = np.logical_and((yb[0] <= xyz[:,1]), (yb[1] >= xyz[:,1]))
    good_indices = np.where(X_valid & Y_valid)[0]

    return xyz[good_indices]

def find_points(las:laspy.LasData, xb:list[float, float], yb:list[float, float]) -> laspy.LasData:
    """Get arrays which indicate invalid X, Y, or Z values"""

    X_valid = (xb[0] <= las.x) & (xb[1] >= las.x)
    Y_valid = (yb[0] <= las.y) & (yb[1] >= las.y)

    good_indices = np.where(X_valid & Y_valid)[0]
    if len(good_indices)>0:
        return las[good_indices]
    else:
        return None


def read_laz(fn:str, bounds:Union[tuple[tuple[float,float],tuple[float,float]], list[list[float, float],list[float, float]]] = None) -> Union[np.ndarray,laspy.LasData]:
    """  Lecture d'un fichier LAZ, LAS ou NPZ """
    if exists(fn):

        if fn.endswith('.npz'):
            return np.load(fn)['arr_0']

        elif fn.endswith('.laz') or fn.endswith('.las'):
            if exists(fn):
                with laspy.open(fn,laz_backend=LazBackend.Laszip) as f:
                    laz = f.read()
                    if bounds is None:
                        return laz
                    else:
                        return find_points(laz, bounds[0], bounds[1])
    else:
        return None

def xyzlaz_scandir(mydir:str, bounds:Union[tuple[tuple[float,float],tuple[float,float]], list[list[float, float],list[float, float]]]):
    """ Scan for XYZ files """
    first=[]
    for curfile in listdir(mydir):
        if curfile.endswith('.bin'):
            mydata = xyz_laz(join(mydir,curfile), format='numpy', to_read=False)
            if mydata.test_bounds(bounds):
                print(curfile)
                mydata.read_bin_xyz()
                first.append(mydata.data)

    for entry in scandir(mydir):
        if entry.is_dir():
            locf=xyzlaz_scandir(entry,bounds)
            if len(locf)>0:
                first.append(locf)

    data=[]

    if len(first)>0:
        data=find_pointsXYZ(np.concatenate(first),bounds)

    return data

def laz_scandir(mydir:str, bounds:Union[tuple[tuple[float,float],tuple[float,float]], list[list[float, float],list[float, float]]]) -> list[laspy.LasData]:
    """  Scan directory and treat .laz files """
    ret=[]

    for curfile in listdir(mydir):
        if curfile.endswith('.laz'):
            print(curfile)

            mydata = read_laz(join(mydir,curfile))
            mydata = find_points(mydata, bounds[0], bounds[1])

            if mydata is not None:
                if mydata.header.point_count>0:
                    ret.append(mydata)

    return ret

def clip_data_xyz(dir_in:str,
                  fn_out:str,
                  bounds:Union[tuple[tuple[float,float],tuple[float,float]], list[list[float, float],list[float, float]]]):
    """  Get data and write zip numpy file """

    myxyz = xyzlaz_scandir(dir_in, bounds)

    np.savez_compressed(fn_out,myxyz)

    return fn_out

def clip_data_laz(fn_in:str,
                  fn_out:str,
                  bounds:Union[tuple[tuple[float,float],tuple[float,float]], list[list[float, float],list[float, float]]],
                  chunksize:int=5000000):
    pts=[]
    k=0
    xbounds=bounds[0]
    ybounds=bounds[1]

    with laspy.open(fn_in,laz_backend=LazBackend.Laszip) as f:
        nb = (f.header.point_count // chunksize) +1
        print('Points from Header:', f.header.point_count)
        with laspy.open(fn_out, mode="w", header=f.header) as writer:
            for las in f.chunk_iterator(chunksize):
                print(k,' / ',nb)
                mypts=find_points(las,xbounds,ybounds)
                if len(mypts)>0:
                    pts.append(mypts)
                    print(len(mypts))
                    writer.write_points(mypts)
                k+=1
                print('--')
    pts=[]

def get_concat_h(im1:Image.Image, im2:Image.Image):
    """ Concatenate 2 images horizontally """
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst

def get_concat_v(im1:Image.Image, im2:Image.Image):
    """ Concatenate 2 images vertically """
    dst = Image.new('RGB', (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst

def get_Orthos_Walonmap(bounds, fn, cat='IMAGERIE/ORTHO_2012_2013',size=3000):
    """
    Récupération des orthos depuis Walonmap
    fn = filename sans extension --> .png sera ajouté automatiquement

    catégories possibles :
     - 'IMAGERIE/ORTHO_2012_2013'
     - 'IMAGERIE/ORTHO_2015'
     - 'IMAGERIE/ORTHO_2021'
     - 'IMAGERIE/ORTHO_2006_2007'
    """

    resmin=.3
    xbounds=bounds[0]
    ybounds=bounds[1]
    dx = xbounds[1]-xbounds[0]
    dy = ybounds[1]-ybounds[0]

    sizex=size
    sizey=size
    if dx>dy:
        sizey=math.ceil(float(size)*float(dy/dx))
    elif dx<dy:
        sizex=math.ceil(float(size)*float(dx/dy))

    resx = dx/float(size)
    resy = dy/float(size)

    if resx<=resmin and resy <=resmin:
        try:
            im = Image.open(getWalonmap(cat,xbounds[0],ybounds[0],xbounds[1],ybounds[1],sizex,sizey,tofile=False))
        except:
            im = Image.open(getWalonmap(cat,xbounds[0],ybounds[0],xbounds[1],ybounds[1],sizex/2,sizey/2,tofile=False))
    elif resx>resmin and resy <=resmin:
        nbx = math.ceil(resx/resmin)
        liste=[]
        x1=xbounds[0]
        dx = dx/float(nbx)
        for i in range(nbx):
            liste.append(Image.open(getWalonmap(cat,x1,ybounds[0],x1+dx,ybounds[1],sizex,sizey,tofile=False)))
            sleep(.5)
            x1+=dx
        im = liste[0]
        for i in range(1,nbx):
            im = get_concat_h(im,liste[i])
    elif resx<=resmin and resy >resmin:
        nby= math.ceil(resy/resmin)
        liste=[]
        y1=ybounds[0]
        dy = dy/float(nby)
        for j in range(nby):
            liste.append(Image.open(getWalonmap(cat,xbounds[0],y1,xbounds[1],y1+dy,sizex,sizey,tofile=False)))
            sleep(.5)
            y1+=dy
        im = liste[0]
        for j in range(1,nby):
            im = get_concat_v(liste[j],im)
    elif resx>resmin and resy >resmin:
        nbx = math.ceil(resx/resmin)
        nby = math.ceil(resy/resmin)

        liste=[]

        x1=xbounds[0]
        y1=ybounds[0]

        dx = dx/float(nbx)
        dy = dy/float(nby)

        print('Awaiting image from Walonmap - be patient !')
        for i in range(nbx):
            liste.append([])
            y1=ybounds[0]
            for j in range(nby):
                liste[i].append(Image.open(getWalonmap(cat,x1,y1,x1+dx,y1+dy,sizex,sizey,tofile=False)))
                y1+=dy
                print(str(i)+'/'+str(nbx-1)+' -- '+str(j)+'/'+str(nby-1))
                sleep(.5)
            x1+=dx
            print('--')

        for i in range(nbx):
            im = liste[i][0]
            for j in range(1,nby):
                im = get_concat_v(liste[i][j],im)
            liste[i][0]=im

        im = liste[0][0]
        for i in range(1,nbx):
            im = get_concat_h(im,liste[i][0])

    Image.Image.save(im,fn +'.png')
    with open(fn+'.png_bounds.txt','w') as f:
        f.write(str(xbounds[0])+','+str(xbounds[1])+'\n')
        f.write(str(ybounds[0])+','+str(ybounds[1]))

def get_colors(las:laspy.LasData, which_colors:Colors_Lazviewer, imsize=2000, fname='', palette_classif: Classification_LAZ = None):

    curlas:laspy.LasData

    if type(las) is laspy.LasData:
        nb = las.header.point_count
    elif type(las) is list:
        nb=0
        for curlas in las:
            nb += curlas.header.point_count
    else:
        nb = len(las)

    colors=np.ones((nb,4),dtype=np.float32)

    if type(which_colors) == Colors_Lazviewer:
        which_colors = which_colors.value

    if which_colors==Colors_Lazviewer.CODE_2013.value:
        """
        - Hors-sol (building, toits et autres) - Code 1;
        - Sol (y compris talus et digues) - Code 2;
        - Végétation haute (y compris la végétation linéaire) - Code 4;
        - Eau - Code 9;
        - Pont – Code 10.
        """
        if type(las) is laspy.LasData:
            myclass = las.classification
        elif type(las) is list:
            myclass=[]
            for curlas in las:
                myclass.append(curlas.classification)
            myclass = np.concatenate(myclass)
        else:
            myclass = np.int8(las[:,3])

        if palette_classif is None:
            palette_classif = Classification_LAZ()
            palette_classif.init_2013()

        for key, value in palette_classif.classification.items():
            name, comment, color = value
            colors[myclass==int(key)] = color

    elif which_colors==Colors_Lazviewer.CODE_2023.value:

        if palette_classif is None:
            palette_classif = Classification_LAZ()
            palette_classif.init_2023()

        """
        - Defaut                - Code 1;           Voiture, câbles électrique, points de végétation diffus, Sursol non utile…
        - Sol                   - Code 2;           Tous les éléments du sol y compris les descentes de garage en sous-sol
        - Végétation            - Code 4;           Végétation
        - Bâtiments             - Code 6;           Bâtiments
        - Eau                   – Code 9;           Points de la surface d’eau brute mesurés par le scanner 2
        - Ponts                 – Code 10;          Les ponts ont été classés à part pour améliorer la définition du MNT. Ils ont été ouverts grâce
        - Mur de berge          – Code 11;          Mur et muret en berge de la Vesdre dépassant le sol à des vocation de réaliser une modélisation 3D hydraulique avec ces obstacles.
        - Tranche d'eau         – Code 15;          Echo intermédiaire dans l’eau n’appartenant ni à la surface d’eau ni au fond du lit
        - Surface bathymétrique – Code 16;          Fond du lit de la Vesdre et de ses affluents et des autres surfaces d’eau mesurées à partir du scanner 3 FWF discrétisé
        - Surface bathymétrique incertaine - Code 17    Surface bathymétrique sur les zones peu profondes principalement sous végétation où les intensités des échos sont parfois trop faibles pour avoir la certitude qu’ils représentent le fond de rivière. La classe 17 est néanmoins plus certaine que la classe 18. Elle est utilisée dans la génération des MNT par défaut.
        - Surface d'eau calculée - Code 19          Points sous échantillonnés de la surface d’eau ayant servis à faire les calculs de correction de réfraction bathymétrique
        - Surface bathymétrique incertaine profonde – Code 20;  Surface bathymétrique sur les zones plus profondes principalement au centre de la rivière où les intensités des échos sont parfois trop faibles pour avoir la certitude qu’ils représentent le fond de rivière. Non utilisée dans la génération du MNT. + Surface proche bathy mais potentiellement émergée pour les scanner 1 à 3
        - Surface d'eau héliportée – Code 29;       La hauteur d’eau du vol héliporté étant largement supérieure (de 30 à 40cm au vol Titan, les points matérialisant cette surface ont été reclassés dans cette classe séparée pour ne pas perturbé le reste du nuage de point.
        """

        if type(las) is laspy.LasData:
            myclass = las.classification
        elif type(las) is list:
            myclass=[]
            for curlas in las:
                myclass.append(curlas.classification)
            myclass = np.concatenate(myclass)
        else:
            myclass = np.int8(las[:,3])

        for key, value in palette_classif.classification.items():
            name, comment, color = value
            colors[myclass==int(key)] = color

    elif which_colors==Colors_Lazviewer.FROM_FILE.value and fname != '':
        im=Image.open(fname)
        width = im.width
        height = im.height

        if exists(fname+'_bounds.txt'):
            with open((fname+'_bounds.txt'),'r') as f:
                mylines=f.read().splitlines()
                xb = np.float64(mylines[0].split(','))
                yb = np.float64(mylines[1].split(','))

        myPPNC = np.asarray(im)

        if type(las) is laspy.LasData:
            x = las.x
            y = las.y
        elif type(las) is list:
            xy=[]
            for mypts in las:
                xy.append(np.vstack((mypts.x,mypts.y)).transpose())
            xy=np.concatenate(xy)
            x=xy[:,0]
            y=xy[:,1]
        else:
            x = las[:,0]
            y = las[:,1]

        i = np.int16((x-xb[0])/(xb[1]-xb[0])*(width-1))
        j = np.int16((yb[1]-y)/(yb[1]-yb[0])*(height-1))

        jmax,imax,_ = myPPNC.shape
        i[np.where(i<0)]=0
        j[np.where(j<0)]=0
        i[np.where(i>=imax)]=imax-1
        j[np.where(j>=jmax)]=jmax-1

        # print(np.max(i),np.max(j))
        colors[:,:3]=myPPNC[j,i]/255.

    else:
        if which_colors==Colors_Lazviewer.ORTHO_2012_2013.value:
            mycat='IMAGERIE/ORTHO_2012_2013'
        elif which_colors==Colors_Lazviewer.ORTHO_2015.value:
            mycat='IMAGERIE/ORTHO_2015'
        elif which_colors==Colors_Lazviewer.ORTHO_2021.value or which_colors is None:
            mycat='IMAGERIE/ORTHO_2021'
        elif which_colors==Colors_Lazviewer.ORTHO_2006_2007.value:
            mycat='IMAGERIE/ORTHO_2006_2007'
        elif which_colors==Colors_Lazviewer.ORTHO_2023.value:
            mycat='IMAGERIE/ORTHO_2023_ETE'

        if type(las) is laspy.LasData:
            x = las.x
            y = las.y
        elif type(las) is list:
            xy=[]
            for mypts in las:
                xy.append(np.vstack((mypts.x,mypts.y)).transpose())
            xy=np.concatenate(xy)
            x=xy[:,0]
            y=xy[:,1]
        else:
            x = las[:,0]
            y = las[:,1]

        mins = np.amin(np.vstack((x,y)).transpose(),axis=0)
        maxs = np.amax(np.vstack((x,y)).transpose(),axis=0)

        width = min(int((maxs[0]-mins[0])/.3),imsize)
        height = min(int((maxs[1]-mins[1])/.3),imsize)

        im = Image.open(getWalonmap(mycat,mins[0],mins[1],maxs[0],maxs[1],width,height,tofile=False))
        myPPNC = np.asarray(im)

        i = np.int16((x-mins[0])/(maxs[0]-mins[0])*float(width -1))
        j = np.int16((maxs[1]-y)/(maxs[1]-mins[1])*float(height-1))

        jmax,imax,_ = myPPNC.shape
        i[np.where(i<0)]=0
        j[np.where(j<0)]=0
        i[np.where(i>=imax)]=imax-1
        j[np.where(j>=jmax)]=jmax-1

        colors[:,:3]=myPPNC[j,i,:3]/255.

    return colors

def myviewer(las:Union[np.ndarray, list[laspy.LasData], laspy.LasData], which_colors:Colors_Lazviewer, fname='', palette_classif:Classification_LAZ = None):
    """ Get viewer for las data """

    if type(las) is list:
        xyz=[]
        for mypts in las:
            xyz.append(np.vstack((mypts.x,mypts.y,mypts.z)).transpose())

        xyz=np.concatenate(xyz)

    elif type(las) is laspy.LasData:
        xyz = np.vstack((las.x,las.y,las.z)).transpose()

    else:
        assert las.shape[1]>2
        xyz=las[:,:3]

    colors = get_colors(las, which_colors, fname=fname, palette_classif= palette_classif)

    v=viewer(xyz,colors)
    v.set(point_size=.05)
    return v

if __name__ == '__main__':
    # # création des fichiers

    grids = xyz_laz_grids(r'D:\OneDrive\OneDrive - Universite de Liege\Crues\2021-07 Vesdre\CSC - Convention - ARNE\Data\LAZ_Vesdre\2023\grids_flt32', True)

    grids.create_from_laz(r'D:\OneDrive\OneDrive - Universite de Liege\Crues\2021-07 Vesdre\CSC - Convention - ARNE\Data\LAZ_Vesdre\2023\LAZ',
                          shape=r'D:\OneDrive\OneDrive - Universite de Liege\Crues\2021-07 Vesdre\CSC - Convention - ARNE\Data\2023\Tableau_d_assemblage_v3\Vesdre_Tableau_d_Assemblage_L72.shp',
                          force_format=np.float32)

    # mygrids = xyz_laz_grids(r'D:\OneDrive\OneDrive - Universite de Liege\Crues\2021-07 Vesdre\CSC - Convention - ARNE\Data\LAZ_Vesdre\2023\grids')

    # xyz = mygrids.scan([[252500, 252700],[136400,136500]])
    # newview = myviewer(xyz,2021)
    pass