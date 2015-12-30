from . import swmmblocks
import warnings

class SWMMformatter(object):
    """
    A class to insert lines into a SWMM model based on predefined structures
    needed for the Chicago GI Infoworks to SWMM model.
    """
    def __init__(self, path):
        """
        Requires:
        - path: str, the full file path to the existing SWMM model .inp.
        """
        self.path = path
        self._orig_file = None #self.read_inp(path)
        self._new_file = None #self.orig_file.copy()
        self.modified_nodes = None

    @property
    def orig_file(self):
        if self._orig_file is None:
            self._orig_file = self.read_inp(self.path)
        return self._orig_file

    @property
    def new_file(self):
        if self._new_file is None:
            self._new_file = self.orig_file.copy()
        return self._new_file

        self.modified_nodes = None

    def _find_line(self, line):
        """
        Given a text string returns the line number that the string appears in.

        Requires:
        - line: str, tetx to look up.

        Returns:
        - n: int, the line number where line exists.
        """
        currentfile = self.new_file.copy()
        for n, l in enumerate(currentfile):
            if l.find(line) > -1:
                break
        return n

    def read_inp(self, filename):
        """
        A wrapper for the standard `open` function implemented using `with`.

        Requires:
        - filename: str, the path to the text file.

        Returns:
        - lines: list, a list of lines from `open(filename).readlines()`
        """

        with open(filename, 'r') as openfile:
            lines = openfile.readlines()
        return lines

    def find_block(self, block):
        """
        Finds the start of a SWMM parameter block such as the `[JUNCTIONS]`
        block.

        Requires:
        - block: str, acceptable values include: 'junctions', 'storage',
            'conduits', 'weirs', 'outlets', 'xsections', 'coordinates',
            'inflows', 'time_series', 'outfalls'

        Returns:
        blockstart: int, the start of the block after the comment lines (3).
        """
        startlines = {
            'junctions': '[JUNCTIONS]',
            'storage': '[STORAGE]',
            'conduits': '[CONDUITS]',
            'weirs': '[WEIRS]',
            'outlets': '[OUTLETS]',
            'xsections': '[XSECTIONS]',
            'coordinates': '[COORDINATES]',
            'inflows': '[INFLOWS]',
            'time_series': '[TIMESERIES]',
            'outfalls': '[OUTFALLS]',
        }


        blockstart = startlines[block]

        return self._find_line(blockstart) + 3 #b/c comments

    def _check_node_type(self, nodes, block):
        """
        Helper function to check of the list of nodes provided to create
        upstream branches actually exist in the SWMM model.
        """
        if not isinstance(nodes, list):
            # allows for a single node to be a str for lazy people
            if isinstance(nodes, str):
                nodes = [nodes]
            else:
                e='`nodes` must be of type list or str.'
                raise TypeError(e)

        # inspection block to make sure that the input
        # nodes are in the swmm file.
        # doesn't seem to be computationally costly so it can stay for now
        check_start = self.find_block(block)
        for node in nodes:
            for n, l in enumerate(self.orig_file[check_start:]):
                if l.find(node) > -1:
                    ln = n
                    break
                else:
                    ln = n
            if ln == len(self.orig_file):
                e = '{} not in the file'
                raise ValueError(e)

            return nodes

    def get_node_param(self, nodename, nodeblock, position, dfloat=True):
        """
        Returns the value of a parameter from a SWMM node.

        Requires:
        - nodename: str, the exact name of the target node name.
        - nodeblock: the SWMM block that the node is part of, e.g., `junctions`.
        - position: the ordinal position of the parameter by column order in the
            node block.
        - dfloat: bool, optional (True). If true, returns a float of the value,
            else a str.

        Returns:
        target: float or str.
        """
        # Because we are appending the original node names with new things we
        # need to find the original by looking for spaces at the end
        nodename += ' '
        blockstart = self.find_block(nodeblock)
        for n, l in enumerate(self.new_file[blockstart:]):
            n += blockstart
            if l.find(nodename) > -1:
                break
        node_params = tuple(a for a in self.new_file[n].split(' ') if a != '')

        if dfloat:
            target = float(node_params[position])
        else:
            target = node_params[position]

        return target

    def create_upstream(self, nodes, num, nodetype, uptype):
        """
        Creates an upstream structure based on the predefined Chicago GI SWMM
        models for 'Restricted' and 'Unrestricted' branches of a simple and
        complex case.

        Requires:
        - nodes: str or list of str, the nodes to create the upstream branch.
        - uptype: str, either `simple_restricted`, `simple_unrestricted`,
            `complex_restricted`, `complex_unrestricted`
        - nodetype: str, the block the target node exists in. Acceptable values
            include: 'junctions', 'storage', 'conduits', 'weirs', 'outlets',
            'xsections', 'coordinates', 'inflows', 'time_series', 'outfalls'.

        Returns:
        - None. self.new_file is updated
        """

        def _base_formatter(sb):
            """
            Common attributes for all branch types.
            sb: a swmmblocks class of upstream formatter
            """
            self.new_file.insert(
                self.find_block('junctions'),
                sb.junctions
                )
            self.new_file.insert(
                self.find_block('conduits'),
                sb.conduits
                )
            self.new_file.insert(
                self.find_block('xsections'),
                sb.xsections
                )
            self.new_file.insert(
                self.find_block('coordinates'),
                sb.coordinates
                )
            self.new_file.insert(
                self.find_block('inflows'),
                sb.inflows
                )
            self.new_file.insert(
                self.find_block('time_series'),
                sb.time_series
                )


        nodes = self._check_node_type(nodes, nodetype)

        for node in nodes:
            invert = self.get_node_param(node, nodetype, 1)
            # invert + Dmax = the top of the loading node
            dmax = self.get_node_param(node, nodetype, 2)

            x = self.get_node_param(node, 'coordinates', 1)
            y = self.get_node_param(node, 'coordinates', 2)

            sb = swmmblocks.Upstream(uptype, node, invert, dmax, x, y, num)
            _base_formatter(sb.Structure)
            if uptype == 'simple_restricted':
                self.new_file.insert(
                    self.find_block('storage'),
                    sb.Structure.storage
                    )
                self.new_file.insert(
                    self.find_block('outlets'),
                    sb.Structure.outlets
                    )

            elif uptype == 'simple_unrestricted':
                pass

            elif uptype == 'complex_restricted':
                self.new_file.insert(
                    self.find_block('storage'),
                    sb.Structure.storage
                    )
                self.new_file.insert(
                    self.find_block('weirs'),
                    sb.Structure.weirs
                    )
                self.new_file.insert(
                    self.find_block('outlets'),
                    sb.Structure.outlets
                    )
                self.new_file.insert(
                    self.find_block('xsections'),
                    sb.Structure.xsections
                    )

            elif uptype == 'complex_unrestricted':
                self.new_file.insert(
                    self.find_block('storage'),
                    sb.Structure.storage
                    )
                self.new_file.insert(
                    self.find_block('weirs'),
                    sb.Structure.weirs
                    )
                self.new_file.insert(
                    self.find_block('outlets'),
                    sb.Structure.outlets
                    )

            else:
                e = ('`uptype` must be `simple_restricted`, `simple_unrestricted`'
                    ', `complex_restricted`, or `complex_unrestricted`')
                raise ValueError(e)

    def delete_attribute(self, line, block, comment=True):
        """
        Delete (or comment out) a line from the SWMM input file.

        Requires:
        - line: str, the start of the line enough to identify it.
        - block: str, the block the line is located in. This function will find
            the first occurrence of the line even if it is not in that block. So
            be careful!
        - comment: bool, optional (True). If True comments the line out, else
            deletes the line. Opening input files in SWMM will clobber the comments,
            so be sure to make a copy if you want to track all of the changes that
            are made.
        """
        blockstart = self.find_block(block)
        for n, l in enumerate(self.new_file[blockstart:]):
            n += blockstart
            if l.find(line) > -1:
                break
        if not n == len(self.new_file):
            if comment:
                self.new_file[n] = '; ' + self.new_file[n]
            else:
                self.new_file.pop(n)
        else:
            warnings.warn('Line not in file!')

    def write_new_file(self, filename):
        """
        wrapper for open(filename).writelines(self.new_file) using `with`.
        """
        with open(filename, 'w') as openfile:
            openfile.writelines(self.new_file)
