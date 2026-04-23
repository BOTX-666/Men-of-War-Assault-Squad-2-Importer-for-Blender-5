# coding=utf-8

# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# Men of War MDL importer for Blender
# Script Copyright (C) by Björn Martins Paz

import argparse
import os
import struct

from mdl import MDL
from mowdef import MOWDEF

parser = argparse.ArgumentParser()
parser.add_argument('infile', nargs='?', help='Input file')
args = parser.parse_args()
infile = args.infile

# Process MDL file
if infile != None and os.path.splitext(infile)[1][1:].strip() == "mdl":
	mdl = MDL(infile)
# Process DEF file
elif infile != None and os.path.splitext(infile)[1][1:].strip() == "def":
	mowdef = MOWDEF(infile)
else:
    print("No .MDL or .DEF file found")
    parser.print_help()