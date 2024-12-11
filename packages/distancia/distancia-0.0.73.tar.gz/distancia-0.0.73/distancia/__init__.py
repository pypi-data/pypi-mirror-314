#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  __init__.py
#  
#  Copyright 2020 Yves <yves@mercadier>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

"""
	Have you ever wanted a world where distances would have no limits ? This package is for you then
"""
 
__version__ = "0.0.73"

from .mainClass          import *
from .distancia          import *
from .vectorDistance     import *
from .matrixDistance     import *
from .lossFunction       import *
from .timeSeriesDistance import *
from .graphDistance      import *
from .markovChain        import *
from .imageDistance      import *
from .soundDistance      import *
from .fileDistance       import *
from .textDistance       import *
from .tools              import *
