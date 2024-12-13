# -*- coding: utf-8 -*-
# This software is part of the 'astrophysix' software project.
#
# Copyright © Commissariat a l'Energie Atomique et aux Energies Alternatives (CEA)
#
#  FREE SOFTWARE LICENCING
#  -----------------------
# This software is governed by the CeCILL license under French law and abiding by the rules of distribution of free
# software. You can use, modify and/or redistribute the software under the terms of the CeCILL license as circulated by
# CEA, CNRS and INRIA at the following URL: "http://www.cecill.info". As a counterpart to the access to the source code
# and rights to copy, modify and redistribute granted by the license, users are provided only with a limited warranty
# and the software's author, the holder of the economic rights, and the successive licensors have only limited
# liability. In this respect, the user's attention is drawn to the risks associated with loading, using, modifying
# and/or developing or reproducing the software by the user in light of its specific status of free software, that may
# mean that it is complicated to manipulate, and that also therefore means that it is reserved for developers and
# experienced professionals having in-depth computer knowledge. Users are therefore encouraged to load and test the
# software's suitability as regards their requirements in conditions enabling the security of their systems and/or data
# to be ensured and, more generally, to use and operate it in the same conditions as regards security. The fact that
# you are presently reading this means that you have had knowledge of the CeCILL license and that you accept its terms.
#
#
# COMMERCIAL SOFTWARE LICENCING
# -----------------------------
# You can obtain this software from CEA under other licencing terms for commercial purposes. For this you will need to
# negotiate a specific contract with a legal representative of CEA.
#
"""
@author: Damien CHAPON (damien.chapon@cea.fr)
"""
import sys
import argparse
import os
import tempfile
if sys.version_info.major == 2:
    from SocketServer import TCPServer
    from SimpleHTTPServer import SimpleHTTPRequestHandler
else:
    from http.server import SimpleHTTPRequestHandler
    from socketserver import TCPServer

# import webbrowser
import logging

from astrophysix.simdm.datafiles.plot import PlotInfo

D3_WEB_DIR = os.path.abspath(os.path.dirname(__file__))
os.chdir(D3_WEB_DIR)

log = logging.getLogger()
log.setLevel(logging.DEBUG)
_info_formatter = logging.Formatter(fmt="[%(levelname)s] %(message)s")
_console_handler = logging.StreamHandler(stream=sys.stdout)
_console_handler.setLevel(logging.DEBUG)
_console_handler.setFormatter(_info_formatter)
log.addHandler(_console_handler)


class GalD3HttpRequestHandler(SimpleHTTPRequestHandler):
    LOCAL_PLOT_DATA_JSON_FNAME = "plot_data.json"

    def do_GET(self):
        if self.path == '/chart':
            log.info(" -> fetch HTML page (no MathJax.js)")
            self.path = 'plot_no_mathjax.html'
        elif self.path == "/img/loading_icon.png":
            self.path = "loading.png"
        elif self.path == "/img/d3_plot.gif":
            self.path = "d3_plot.gif"
        elif self.path == "/data/plot.json":
            self.path = self.LOCAL_PLOT_DATA_JSON_FNAME

        return SimpleHTTPRequestHandler.do_GET(self)


class GalD3HttpRequestHandlerMathJax(GalD3HttpRequestHandler):
    def do_GET(self):
        if self.path == '/chart':
            log.info(" -> fetch HTML page (with MathJax.js)")
            self.path = 'plot.html'
        elif self.path == "/js/gald3.js":
            log.info(" -> Fetch GalD3.js local JS script")
            self.path = "gald3.js"
        elif self.path == "/static/MathJax_local.js?V=2.7.4":
            log.info(" -> Fetch MathJax local JS config")
            self.path = 'MathJax_local.js?V=2.7.4'

        return GalD3HttpRequestHandler.do_GET(self)


def main():
    """The main routine."""
    log.info("# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #")
    log.info("# ~~~~~~~~~~~~~~~~~~~~ Galactica D3js rendering preview server ~~~~~~~~~~~~~~~~~~~~~~ #")
    log.info("# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #")
    log.info("Press Ctrl+C to terminate the HTTP server.")
    # Do argument parsing here (eg. with argparse) and anything else you want your project to do. Return values are
    # exit codes.

    parser = argparse.ArgumentParser(description="Run GalD3 plot preview HTTP server for the Galactica astrophysical "
                                                 "simulation database")
    parser.add_argument('--debug', dest='debug', action='store_true', help='Run in debug mode')
    parser.add_argument("-n", "--no-mathjax", dest="disable_mathjax", action="store_true", help="Disable MathJax")
    parser.add_argument("-p", "--port", dest="http_port", type=int, default=8076, help="HTTP ser port (default 8076).")
    pargs = parser.parse_args()

    if pargs.disable_mathjax:
        handler = GalD3HttpRequestHandler
    else:
        handler = GalD3HttpRequestHandlerMathJax
    # is_debug = pargs.debug

    tmp_file_path = os.path.join(tempfile.gettempdir(), PlotInfo.PLOT_DATA_JSON_FPATH)
    if not os.path.islink(handler.LOCAL_PLOT_DATA_JSON_FNAME):
        log.info("Linking to temporary JSON data file '{fp:s}'.".format(fp=tmp_file_path))
        os.symlink(tmp_file_path, handler.LOCAL_PLOT_DATA_JSON_FNAME)

    PORT = pargs.http_port
    with TCPServer(("", PORT), handler) as serv:
        log.info("Serving plot preview page at : http://127.0.0.1:{p:d}/chart".format(p=pargs.http_port))

        # Star the server
        # webbrowser.open("http://127.0.0.1:{port:d}/chart".format(port=PORT))
        try:
            serv.serve_forever()
        except KeyboardInterrupt:
            log.info("Server stopped...")
            if os.path.islink(handler.LOCAL_PLOT_DATA_JSON_FNAME):
                log.info("Deleting link to temporary JSON data file '{fp:s}'.".format(fp=tmp_file_path))
                os.remove(handler.LOCAL_PLOT_DATA_JSON_FNAME)
            log.info("# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #")
    return 0


if __name__ == "__main__":
    sys.exit(main())
