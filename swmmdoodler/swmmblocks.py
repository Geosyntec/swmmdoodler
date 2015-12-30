from .textblocks import (
    simple_restricted,
    simple_unrestricted,
    complex_restricted,
    complex_unrestricted
)

IEMULTFACTOR=1.1
CMULTFACTOR=0.01

class _BaseBlocks(object):
    """
    Basically a dictionary formatter of predefined SWMM relationships
    """
    def __init__(self, node, node_elev, dmax, x, y, stype, num):
        """
        Requires:
        - node: str, the name of the target node.
        - node_elev: float, the target node's elevation.
        - dmax: float, the target nodes's max depth.
        - x: float, the target node's x coordinate.
        - y: float, the target node's y coordinate.
        - stype: the structure type to create upstream.
        """
        self.node = node
        self.base_elevation = node_elev
        self.dmax = dmax
        self.x = x
        self.y = y
        self.num = num

        self._invert_elevations = None
        self._coords = None

        self._formatdict = None

        if stype == 'simple_restricted':
            self.sformatter = simple_restricted
        if stype == 'simple_unrestricted':
            self.sformatter = simple_unrestricted
        if stype == 'complex_restricted':
            self.sformatter = complex_restricted
        if stype == 'complex_unrestricted':
            self.sformatter = complex_unrestricted

    @property
    def formatdict(self):
        if self._formatdict is None:
            formatdict = self.invert_elevations
            formatdict.update(dict(node=self.node, num=self.num))
            formatdict.update(self.coords)
            self._formatdict = formatdict.copy()
        return self._formatdict

    @property
    def junctions(self):
        txtout = self.sformatter['junctions']
        txtout = txtout.format(**self.formatdict)

        return txtout

    @property
    def storage(self):
        txtout = self.sformatter['storage']
        txtout = txtout.format(**self.formatdict)

        return txtout

    @property
    def conduits(self):
        txtout = self.sformatter['conduits']
        txtout = txtout.format(**self.formatdict)

        return txtout

    @property
    def weirs(self):
        txtout = self.sformatter['weirs']
        txtout = txtout.format(**self.formatdict)

        return txtout

    @property
    def outlets(self):
        txtout = self.sformatter['outlets']
        txtout = txtout.format(**self.formatdict)

        return txtout

    @property
    def xsections(self):
        txtout = self.sformatter['xsections']
        txtout = txtout.format(**self.formatdict)

        return txtout

    @property
    def inflows(self):
        txtout = self.sformatter['inflows']
        txtout = txtout.format(**self.formatdict)

        return txtout

    @property
    def time_series(self):
        txtout = self.sformatter['time_series']
        txtout = txtout.format(**self.formatdict)

        return txtout

    @property
    def coordinates(self):
        txtout = self.sformatter['coordinates']
        txtout = txtout.format(**self.formatdict)

        return txtout


class SimpleRestricted(_BaseBlocks):
    """docstring for SimpleBlocks"""
    def __init__(self, node, node_elev, dmax, x, y, num):
        super().__init__(node, node_elev, dmax, x, y, 'simple_restricted', num)

    @property
    def invert_elevations(self):
        if self._invert_elevations is None:
            ie = {
                # for the simple case I'll space these out so we can see it's
                # working
                'offset_rCon': 1.5,
                'offset_rGully': self.dmax,
                'invert_rJ': self.base_elevation + self.dmax + 0.5,
                'invert_rGS': self.base_elevation + self.dmax + 1,
                'invert_R': self.base_elevation + self.dmax + 3,
            }
            self._invert_elevations = ie
        return self._invert_elevations.copy()

    @property
    def coords(self):
        if self._coords is None:
            coords = {
                'xcoord_rJ': self.x + (self.x * (CMULTFACTOR**2) * -1),
                'xcoord_rGS': self.x + (self.x * (CMULTFACTOR**2) * -1),
                'xcoord_R': self.x + (self.x * (CMULTFACTOR**2) * -1),

                'ycoord_rJ': self.y + (self.y * (CMULTFACTOR**2)),
                'ycoord_rGS': self.y + (self.y * (CMULTFACTOR**2)),
                'ycoord_R': self.y + (self.y * (CMULTFACTOR**2)),
            }
            self._coords = coords
        return self._coords.copy()


class SimpleUnrestricted(_BaseBlocks):
    """docstring for SimpleBlocks"""
    def __init__(self, node, node_elev, dmax, x, y, num):
        super().__init__(node, node_elev, dmax, x, y, 'simple_unrestricted', num)

    @property
    def invert_elevations(self):
        if self._invert_elevations is None:
            ie = {
                'invert_U': self.base_elevation + self.dmax + 0.5,
            }
            self._invert_elevations = ie
        return self._invert_elevations.copy()

    @property
    def coords(self):
        if self._coords is None:
            coords = {
                'xcoord_U': self.x + (self.x * (CMULTFACTOR**2)),
                'ycoord_U': self.y + (self.y * (CMULTFACTOR**2)),
            }
            self._coords = coords
        return self._coords.copy()


class ComplexRestricted(_BaseBlocks):
    """docstring for SimpleBlocks"""
    def __init__(self, node, node_elev, dmax, x, y, num):
        super().__init__(node, node_elev, dmax, x, y, 'complex_restricted', num)

        self._max_depth = None
        self._scoeff = None

    @property
    def formatdict(self):
        if self._formatdict is None:
            formatdict = self.invert_elevations
            formatdict.update(node=self.node, num=self.num)
            formatdict.update(self.coords)
            formatdict.update(self.max_depth)
            formatdict.update(self.scoeff)
            self._formatdict = formatdict.copy()
        return self._formatdict

    @property
    def invert_elevations(self):
        if self._invert_elevations is None:
            ie = {
                'invert_R_nP': self.base_elevation + self.dmax + 1,
                'invert_R_P': self.base_elevation + self.dmax + 13.5,
                'invert_R_nB': self.base_elevation + self.dmax + 1,
                'invert_R_B': self.base_elevation + self.dmax + 13.5,
                'invert_R_nR': self.base_elevation + self.dmax + 1,
                'invert_R_r': self.base_elevation + self.dmax + 13.5,
                'invert_R_nC': self.base_elevation + self.dmax + 1,
                'invert_R_C': self.base_elevation + self.dmax + 13.5,
                'invert_R_No': self.base_elevation + self.dmax + 3.5,
                'invert_R_n0': self.base_elevation + self.dmax + 3,
                'invert_R_nOt': self.base_elevation + self.dmax + 0.5,

                # storage
                'invert_R_sP': self.base_elevation + self.dmax + 3,
                'invert_R_sB': self.base_elevation + self.dmax + 3,
                'invert_R_sR': self.base_elevation + self.dmax + 3,
                'invert_R_sC': self.base_elevation + self.dmax + 3,
                'invert_R_sG': self.base_elevation + self.dmax + 1,
            }
            self._invert_elevations = ie
        return self._invert_elevations.copy()

    @property
    def max_depth(self):
        if self._max_depth is None:
            md = {
                # junctions based on Marc's parameters. It is my understanding
                # that these are dummies and will be changed
                'node_dmax': self.dmax,
                'dmax_R_nP': 0,
                'dmax_R_P': 0,
                'dmax_R_nB': 0,
                'dmax_R_B': 0,
                'dmax_R_nR': 0,
                'dmax_R_r': 0,
                'dmax_R_nC': 0,
                'dmax_R_C': 0,
                'dmax_R_No': 0,
                'dmax_R_n0': 0,
                'dmax_R_nOt': 0,

                # storage
                'dmax_R_sP': 10,
                'dmax_R_sB': 10,
                'dmax_R_sR': 10,
                'dmax_R_sC': 10,
                'dmax_R_sG': 1.5,
            }
            self._max_depth = md
        return self._max_depth.copy()

    @property
    def scoeff(self):
        """
        storage coefficient
        """
        if self._scoeff is None:
            # based on Marc's parameters. It is my understanding
            # that these are dummies and will be changed
            md = {
                'scoeff_R_sP': 0.19,
                'scoeff_R_sB': 0.26,
                'scoeff_R_sR': 0.22,
                'scoeff_R_sC': 0.06,
            }
            self._scoeff = md
        return self._scoeff.copy()

    @property
    def coords(self):
        if self._coords is None:
            coords = {
                'xcoord_R_nP': self.x + (self.x * (CMULTFACTOR**2) * -1),
                'xcoord_R_P': self.x + (self.x * (CMULTFACTOR**2) * -1),
                'xcoord_R_nB': self.x + (self.x * (CMULTFACTOR**2) * -1),
                'xcoord_R_B': self.x + (self.x * (CMULTFACTOR**2) * -1),
                'xcoord_R_nR': self.x + (self.x * (CMULTFACTOR**2) * -1),
                'xcoord_R_r': self.x + (self.x * (CMULTFACTOR**2) * -1),
                'xcoord_R_nC': self.x + (self.x * (CMULTFACTOR**2) * -1),
                'xcoord_R_C': self.x + (self.x * (CMULTFACTOR**2) * -1),
                'xcoord_R_No': self.x + (self.x * (CMULTFACTOR**2) * -1),
                'xcoord_R_n0': self.x + (self.x * (CMULTFACTOR**2) * -1),
                'xcoord_R_nOt': self.x + (self.x * (CMULTFACTOR**2) * -1),
                'xcoord_R_sP': self.x + (self.x * (CMULTFACTOR**2) * -1),
                'xcoord_R_sB': self.x + (self.x * (CMULTFACTOR**2) * -1),
                'xcoord_R_sR': self.x + (self.x * (CMULTFACTOR**2) * -1),
                'xcoord_R_sC': self.x + (self.x * (CMULTFACTOR**2) * -1),
                'xcoord_R_sG': self.x + (self.x * (CMULTFACTOR**2) * -1),

                'ycoord_R_nP': self.y + (self.y * (CMULTFACTOR**2)),
                'ycoord_R_P': self.y + (self.y * (CMULTFACTOR**2)),
                'ycoord_R_nB': self.y + (self.y * (CMULTFACTOR**2)),
                'ycoord_R_B': self.y + (self.y * (CMULTFACTOR**2)),
                'ycoord_R_nR': self.y + (self.y * (CMULTFACTOR**2)),
                'ycoord_R_r': self.y + (self.y * (CMULTFACTOR**2)),
                'ycoord_R_nC': self.y + (self.y * (CMULTFACTOR**2)),
                'ycoord_R_C': self.y + (self.y * (CMULTFACTOR**2)),
                'ycoord_R_No': self.y + (self.y * (CMULTFACTOR**2)),
                'ycoord_R_n0': self.y + (self.y * (CMULTFACTOR**2)),
                'ycoord_R_nOt': self.y + (self.y * (CMULTFACTOR**2)),
                'ycoord_R_sP': self.y + (self.y * (CMULTFACTOR**2)),
                'ycoord_R_sB': self.y + (self.y * (CMULTFACTOR**2)),
                'ycoord_R_sR': self.y + (self.y * (CMULTFACTOR**2)),
                'ycoord_R_sC': self.y + (self.y * (CMULTFACTOR**2)),
                'ycoord_R_sG': self.y + (self.y * (CMULTFACTOR**2)),
            }
            self._coords = coords
        return self._coords.copy()


class ComplexUnrestricted(_BaseBlocks):
    """docstring for SimpleBlocks"""
    def __init__(self, node, node_elev, dmax, x, y, num):
        super().__init__(node, node_elev, dmax, x, y, 'complex_unrestricted', num)

        self._max_depth = None
        self._scoeff = None

    @property
    def formatdict(self):
        if self._formatdict is None:
            formatdict = self.invert_elevations
            formatdict.update(node=self.node, num=self.num)
            formatdict.update(self.coords)
            formatdict.update(self.max_depth)
            formatdict.update(self.scoeff)
            self._formatdict = formatdict.copy()
        return self._formatdict

    @property
    def invert_elevations(self):
        if self._invert_elevations is None:
            ie = {
                # junctions
                'invert_U_NoGI': self.base_elevation + self.dmax + 1.5,
                'invert_U_P': self.base_elevation + self.dmax + 12,
                'invert_U_B': self.base_elevation + self.dmax + 12,
                'invert_U_r': self.base_elevation + self.dmax + 12,
                'invert_U_C': self.base_elevation + self.dmax + 12,
                'invert_U_n0': self.base_elevation + self.dmax + 1,
                'invert_U_nP': self.base_elevation + self.dmax + 1,
                'invert_U_nB': self.base_elevation + self.dmax + 1,
                'invert_U_nR': self.base_elevation + self.dmax + 1,
                'invert_U_nC': self.base_elevation + self.dmax + 1,
                'invert_U_nOt': self.base_elevation + self.dmax + 0.5,

                # storage
                'invert_U_sP': self.base_elevation + self.dmax + 1.5,
                'invert_U_sB': self.base_elevation + self.dmax + 1.5,
                'invert_U_sR': self.base_elevation + self.dmax + 1.5,
                'invert_U_sC': self.base_elevation + self.dmax + 1.5,
            }
            self._invert_elevations = ie
        return self._invert_elevations.copy()

    @property
    def max_depth(self):
        if self._max_depth is None:
            md = {
                # junctions
                'node_dmax': self.dmax,
                'dmax_U_NoGI': 0,
                'dmax_U_P': 0,
                'dmax_U_B': 0,
                'dmax_U_r': 0,
                'dmax_U_C': 0,
                'dmax_U_n0': 0,
                'dmax_U_nP': 0,
                'dmax_U_nB': 0,
                'dmax_U_nR': 0,
                'dmax_U_nC': 0,
                'dmax_U_nOt': 0,

                # storage
                'dmax_U_sP':10,
                'dmax_U_sB':10,
                'dmax_U_sR':10,
                'dmax_U_sC':10,
            }
            self._max_depth = md
        return self._max_depth.copy()

    @property
    def scoeff(self):
        """
        storage coefficient
        """
        if self._scoeff is None:
            md = {
                'scoeff_U_sP': 0.18,
                'scoeff_U_sB': 0.15,
                'scoeff_U_sR': 0.22,
                'scoeff_U_sC': 0.06,
            }
            self._scoeff = md
        return self._scoeff.copy()

    @property
    def coords(self):
        if self._coords is None:
            coords = {
                'xcoord_U_NoGI': self.x + (self.x * (CMULTFACTOR**2) * -1),
                'xcoord_U_P': self.x + (self.x * (CMULTFACTOR**2) * -1),
                'xcoord_U_B': self.x + (self.x * (CMULTFACTOR**2) * -1),
                'xcoord_U_r': self.x + (self.x * (CMULTFACTOR**2) * -1),
                'xcoord_U_C': self.x + (self.x * (CMULTFACTOR**2) * -1),
                'xcoord_U_n0': self.x + (self.x * (CMULTFACTOR**2) * -1),
                'xcoord_U_nP': self.x + (self.x * (CMULTFACTOR**2) * -1),
                'xcoord_U_nB': self.x + (self.x * (CMULTFACTOR**2) * -1),
                'xcoord_U_nR': self.x + (self.x * (CMULTFACTOR**2) * -1),
                'xcoord_U_nC': self.x + (self.x * (CMULTFACTOR**2) * -1),
                'xcoord_U_nOt': self.x + (self.x * (CMULTFACTOR**2) * -1),
                'xcoord_U_sP': self.x + (self.x * (CMULTFACTOR**2) * -1),
                'xcoord_U_sB': self.x + (self.x * (CMULTFACTOR**2) * -1),
                'xcoord_U_sR': self.x + (self.x * (CMULTFACTOR**2) * -1),
                'xcoord_U_sC': self.x + (self.x * (CMULTFACTOR**2) * -1),

                'ycoord_U_NoGI': self.y + (self.y * (CMULTFACTOR**2)),
                'ycoord_U_P': self.y + (self.y * (CMULTFACTOR**2)),
                'ycoord_U_B': self.y + (self.y * (CMULTFACTOR**2)),
                'ycoord_U_r': self.y + (self.y * (CMULTFACTOR**2)),
                'ycoord_U_C': self.y + (self.y * (CMULTFACTOR**2)),
                'ycoord_U_n0': self.y + (self.y * (CMULTFACTOR**2)),
                'ycoord_U_nP': self.y + (self.y * (CMULTFACTOR**2)),
                'ycoord_U_nB': self.y + (self.y * (CMULTFACTOR**2)),
                'ycoord_U_nR': self.y + (self.y * (CMULTFACTOR**2)),
                'ycoord_U_nC': self.y + (self.y * (CMULTFACTOR**2)),
                'ycoord_U_nOt': self.y + (self.y * (CMULTFACTOR**2)),
                'ycoord_U_sP': self.y + (self.y * (CMULTFACTOR**2)),
                'ycoord_U_sB': self.y + (self.y * (CMULTFACTOR**2)),
                'ycoord_U_sR': self.y + (self.y * (CMULTFACTOR**2)),
                'ycoord_U_sC': self.y + (self.y * (CMULTFACTOR**2)),
            }
            self._coords = coords
        return self._coords.copy()


class Upstream(object):
    """
    Wrapper class for different structures
    """
    def __init__(self, uptype, node, node_elev, dmax, x, y, num):

        if uptype == 'simple_restricted':
            self.Structure = SimpleRestricted(node, node_elev, dmax, x, y, num)
        elif uptype == 'simple_unrestricted':
            self.Structure = SimpleUnrestricted(node, node_elev, dmax, x, y, num)
        elif uptype == 'complex_restricted':
            self.Structure = ComplexRestricted(node, node_elev, dmax, x, y, num)
        elif uptype == 'complex_unrestricted':
            self.Structure = ComplexUnrestricted(node, node_elev, dmax, x, y, num)
        else:
            e = ('`uptype` must be `simple_restricted`, `simple_unrestricted`'
                ', `complex_restricted`, or `complex_unrestricted`')
            raise ValueError(e)
