"""
Author: HECE - University of Liege, Pierre Archambeau
Date: 2024

Copyright (c) 2024 University of Liege. All rights reserved.

This script and its content are protected by copyright law. Unauthorized
copying or distribution of this file, via any medium, is strictly prohibited.
"""

import logging

from .PyVertexvectors import Triangulation, vector,Zones, zone

class Dike(Triangulation,Zones):

    def __init__(self, trace:vector, width:float, slopeup:float, slopedown:float, fn='', pts=..., tri=..., idx: str = '', plotted: bool = True, mapviewer=None, need_for_wx: bool = False) -> None:

        super().__init__(fn, pts, tri, idx, plotted, mapviewer, need_for_wx)

        self.slopeup = slopeup
        self.slopedown = slopedown
        self.width = width
        self.trace = trace

        newzone = zone(name='dike',parent=self)
        self.add_zone(newzone)
        newzone.add_vector(trace)

    def create(self,zmin,zmax,ds):

        myzone:zone
        myzone = self.myzones[0]

        parright = self.trace.parallel_offset(self.width/2.,'right')
        parleft = self.trace.parallel_offset(self.width/2.,'left')

        myzone.add_vector(parright)
        myzone.add_vector(parleft,0)

        allpar = [parright,parleft, self.trace]
        for curpar in allpar:
            for curv in curpar.myvertices:
                curv.z=zmax

        distup = (zmax-zmin)/self.slopeup
        parup  = parright.parallel_offset(distup,'right')

        distdown = (zmax-zmin)/self.slopedown
        pardown  = parleft.parallel_offset(distdown,'left')

        myzone.add_vector(parup)
        myzone.add_vector(pardown,0)

        allpar = [parup,pardown]
        for curpar in allpar:
            for curv in curpar.myvertices:
                curv.z=zmin

        # on dispose de 5 vecteurs dans la zone, orientés de l'aval vers l'amont

        self.trace.update_lengths()
        nb = int(self.trace.length3D/ds)
        nb2 = int(max(distup,distdown)/ds)

        mytri = myzone.createmultibin(nb,nb2)
        self.tri = mytri.tri
        self.pts = mytri.pts
        self.nb_pts = mytri.nb_pts
        self.nb_tri = mytri.nb_tri

        pass
