#!/usr/bin/env python

# Shellexpander
# Robert Bitsche, DTU Wind Energy
# E-mail: robi@dtu.dk

import sys
import re
import os
import shutil
import argparse
import textwrap
from copy import deepcopy
from time import perf_counter as clock
import math

try:
    import numpy as np
except:
    print("ERROR: The NumPy module is required.")
    print("Please download and install from http://www.scipy.org")
    sys.exit(1)


#############################################################################
def create_parser():
    ''' Creates a parser
    '''
    
    descriptiontext = textwrap.dedent('''\
        This program generates input files for the cross section analysis 
        software BECAS based on information contained in an finite element 
        shell model.
        ''')
    epilogtext = textwrap.dedent('''\
        Please see the shellexpander documentation for further details.
 
        Instead of typing a long command line, the list of arguments 
        can also be stored in a file. An argument starting with a @ charachter 
        is treated as a file, and is replaced by the arguments the file contains.
        The arguments in the file must be given one per line.
        for example: %(prog)s @options.txt

        Robert D. Bitsche, DTU Wind Energy
        Jose Pedro Albergaria Amaral Blasques, DTU Wind Energy
        Malo Rosemeier, IWES Fraunhofer
        Michael Kenneth McWilliam, DTU Wind Energy

        Please report bugs to Jose Blasques at jpbl@dtu.dk
        ''')
    
    parser = argparse.ArgumentParser(description=descriptiontext, 
        epilog=epilogtext,   
        fromfile_prefix_chars='@',
        formatter_class=argparse.RawDescriptionHelpFormatter)
            
    parser.add_argument('--in', dest='inputfile', metavar='inputfile', 
                       default='shellmodel.inp',
                       help='The name of the input file containing the \
                             finite element shell model; \
                             default: %(default)s')

    parser.add_argument('--elsets', nargs='+', metavar='elset', required=True, 
                       help='The element sets to be considered (required). \
                               If more than one element set is given, \
                               nodes appearing in more the one \
                               element sets are considered \"corners\".')
    
    parser.add_argument('--subelsets', dest='subelsets', nargs='+',
                        metavar='subelset', default=None,
                       help='The sub element sets representing the returned mesh.')
                              
    
    parser.add_argument('--sec', dest='sections', metavar='secname', 
                       help='First part of the name of element sets \
                             defining BECAS sections. If this option \
                             is omitted, no BECAS input files are created.')
    
    parser.add_argument('--layers', dest='layers', type=int, metavar='n',
                       default=5,
                       help='The number of layers to be generated; \
                             default: %(default)d')
    
    parser.add_argument('--nthick', dest='nodal_thickness', 
                       choices=['min','max','average'],
                       default='min',
                       help='Method used to determine the nodal thickness \
                             distribution; default: %(default)s')

    parser.add_argument('--dom', dest='dominant_elsets', metavar='elset', nargs='+',
                       help='The dominant element sets. \
                             The elements in these element sets take \
                             precendence when defining the nodal thickness \
                             distribution.')

    parser.add_argument('--cline', dest='centerline', metavar='filename',
                       help='File defining the centerline of the beam and, \
                             optionally, additional nodes for local axis \
                             definition.')

    parser.add_argument('--bdir', dest='becasdir', metavar='dirname',
                       default='becas_input',
                       help='Directory name where BECAS input files \
                             should be created; default: %(default)s')

    parser.add_argument('--debug', dest='debug', action='store_true', \
                       help='Write the extruded 3D cross-sections to an \
                             ABAQUS input file. This is for debugging only.')
 
    parser.add_argument('--quiet', dest='verbose', action='store_false', \
                       help='Indicates that the ShellExpander should suppress status messages')
 
    parser.add_argument('--version', action='version', 
                       version='%(prog)s 1.6 \nJose Blasques, DTU Wind Energy \njpbl@dtu.dk')
    
    return parser

def parse_command_line():
    """Parses Command Line Arguments"""
    
    parser = create_parser()
    args = parser.parse_args()
    return args
#############################################################################


#############################################################################
def parse_abaqus_input_file(list_of_lines):
    """Parse ABAQUS input file. Returns a list of keywords
    and data lines.
    Example:
    [['*KEYWORD1', 'dataline1', 'dataline2'], 
     ['*KEYWORD2', 'dataline1', 'dataline2', 'dataline3'],
     ['*KEYWORD3', 'dataline1', 'dataline2']]
    """
  
    keywords = []  # empty list
    currentkeyword = []
    
    for line in list_of_lines:
        if line[:2] != '**':   # if not a comment
            if line[0] == '*':   # end of old and beginning of new keyword
                if len(currentkeyword) > 0:
                    keywords.append(currentkeyword) # append the current keyw. 
                currentkeyword = []         # start with a new current keyword
            currentkeyword.append(line.strip()) # strips the line from 
                                                # whitespace and "\n"
    keywords.append(currentkeyword) # append also the last keyword
    
  
    if keywords[0][0][0] != '*':
        print("ERROR! .inp-file (stripped from comments)")
        print("       should start with *")
        sys.exit(1)
    
    return keywords
#############################################################################


#############################################################################
def element_info(element_type):
    """Determine the element family and number of nodes per element 
    from an Abaqus element type string using the Abaqus naming conventions"""

    con_pattern = r'C(1D|2D|3D|PE|PS|PEG|AX|GAX)(\d{1,2})(R|I|M)?(H?)(D|T|E|P)?'
    shell_pattern = r'(S|SC|STRI|DS)(\d{1})(R?)(5|T|S)?'
    warp_pattern = r'(WARP)2D(\d{1})'

    if re.search(con_pattern, element_type):
        match = re.search(con_pattern, element_type)
        family = match.group(1)
        numnodes = int(match.group(2))
    elif re.search(shell_pattern, element_type):
        match = re.search(shell_pattern, element_type)
        family = match.group(1)
        numnodes = int(match.group(2))
    elif re.search(warp_pattern, element_type):
        match = re.search(warp_pattern, element_type)
        family = match.group(1)
        numnodes = int(match.group(2))
    else:
        print('ERROR: Could not determine number of nodes for element type', element_type)
        sys.exit(1)

    return family, numnodes
#############################################################################


#############################################################################
def splitline(string):
    """Split a string at every "," and strip
    individual strings from whitespace."""
    list=[]
    for word in string.split(","):
        strip = word.strip()
        if strip != '': list.append(strip)
    return list
#############################################################################


#############################################################################
def getparameters(keyword):
    """
    Returns a small dictionary holding the parameters of the keyword.
    The input argument 'keyword' is a list of strings.
    """

    firstline = keyword[0]
    dictionary = {}
    parameterlist = splitline(firstline)

    for parameterstring in parameterlist[1:]:  # Without the keyword
        try:
            key, value = parameterstring.split('=')
        except:
            key, value = (parameterstring, 'YES')
        key = key.strip()
        value = value.strip()
        dictionary[key.upper()] = value

    return dictionary
#############################################################################


#############################################################################
def read_nested_files(filename, verbose=True):
    """
    Read an Abaqus input file including all files referenced using a
    "*INCLUDE" statement. (recursive function)
    Return a list of lines in uppercase.
    """
    try:
        infile = open(filename, 'r')
    except:
        print("ERROR! Could not open", filename)
        sys.exit(1)
    status('reading from file %s' % (filename), verbose)

    list_of_lines = []
    for line in infile:
        if line.upper().startswith('*INCLUDE'):
            parameters = getparameters([line])
            fullpath = os.path.join(os.path.dirname(infile.name),parameters['INPUT'])
            list_of_lines_nested = read_nested_files(fullpath, verbose)
            list_of_lines = list_of_lines + list_of_lines_nested
            print(('    --> %s' % (parameters['INPUT'])))
        else:
            list_of_lines.append(line.strip().upper())
    infile.close()
    return list_of_lines
#############################################################################


#############################################################################
def read_cline_file(filename, verbose=True):
    """
    Read the file defining the centerline of the beam
    """
    try:
        infile = open(filename, 'rU')
    except:
        print("ERROR! Could not open", filename)
        sys.exit(1)
    status('reading from file %s' % (filename), verbose)

    list_of_coords = []
    for line in infile:
        coords = np.array([float(item) for item in line.strip().split(',')])
        if len(coords) == 3:
            add_node = coords + np.array([1.0, 0.0, 0.0])
            coords = np.hstack(coords,add_node)
        if len(coords) != 6:
            print('ERROR: Three or six coordiantes per line must be')
            print('defined in %s' %(filename))
            sys.exit(1)
        list_of_coords.append(coords)
    infile.close()
    return list_of_coords
#############################################################################


#############################################################################
def get_csys_rot_mat(list_of_coords):
    """
    Compute the rotation matrices for the local coordinate systems.
    """
    try:
        from scipy import interpolate
    except:
        print("ERROR: The SciPy module is required.")
        print("Please download and install from http://www.scipy.org")
        sys.exit(1)

    if len(list_of_coords) == 1:
        print('ERROR: if the --cline option is used, a minimum of')
        print('two cross sections must be defined.')
        sys.exit(1)
    elif len(list_of_coords) in [2,3]: # use a linear or quadr. spline
        degree_spline = len(list_of_coords)-1
    elif len(list_of_coords) > 3: # use a cubic spline
        degree_spline = 3

    # Compute interpolating spline for centerline
    cl_x = np.array([item[0] for item in list_of_coords])
    cl_y = np.array([item[1] for item in list_of_coords])
    cl_z = np.array([item[2] for item in list_of_coords])
    tck,u = interpolate.splprep([cl_x,cl_y],u=cl_z,s=0,k=degree_spline)

    csys_rot_mat = []
    for coords in list_of_coords:
        A = coords[0:3]; B = coords[3:6]
        Pder = interpolate.splev(A[2],tck,der=1)
        t = np.hstack((Pder, np.array([1.0])))
        t = t / np.linalg.norm(t)
        n1s = B - A; n1s = n1s / np.linalg.norm(n1s)
        n2 = np.cross(t,n1s)
        n1 = np.cross(n2,t)
        M = np.vstack((n1, n2, t))
        csys_rot_mat.append(M)

    return csys_rot_mat
#############################################################################


#############################################################################
def keyword_line(key,dict):
    """
    Converts the keyword in key (e.g. *NODE) and the parameter, value information
    in the dictionary dict into an Abaqus keyword line of the form:
    *KEYWORD, PARAMETER1=VALUE1, PARAMETER2=VALUE2
    """
    line = key
    for parameter, value in dict.items():
        if value == 'YES':  # do not write "VALUE=YES", write: "VALUE"
            line = line + ', ' + parameter
        else:
            line = line + ', ' + parameter + '=' + value

    return line
#############################################################################


#############################################################################
def offset_and_intersect(normals, thicknesses, rel_offset):
    """Offset the planes defined by the point (0,0,0) and the two normals by
    the respective thickness * rel_offset and compute the intersection 
    point of the two offset planes and the plane spanned by the two normals.
    Return the coordinates of the intersection point.
    normals ....... list containing two normals as numpy arrays
    thicknesses ... list containing two scalar thicknesses
    rel_offest .... scalar to be multiplied with both thickness values
    """
    if len(normals) != 2 or len(thicknesses) !=2:
        print('ERROR: Exactly two normals and two thicknesses are required')
        print('to compute the intersection point.')
        sys.exit(1)

    n1 = normals[0]
    n2 = normals[1]
    n3 = np.cross(n1,n2)
    t1 = thicknesses[0]
    t2 = thicknesses[1]

    A1 = n1 * t1 * rel_offset
    A2 = n2 * t2 * rel_offset
    n_matrix = np.vstack((n1, n2, n3))
    B = np.array([np.dot(n1, A1), np.dot(n2, A2), 0.0])
    
    intersection_point = np.linalg.solve(n_matrix,B)

    return intersection_point
#############################################################################


#############################################################################
def elset2nset(elements, element_definitions):
    """Return all nodes belonging to an element set
    elements .............. list of element numbers
    element_definitions ... dictionary holding nodenumbers for each
                            element number
    """
    nodes = [] # empty list
    for elementnumber in elements:
        for nodenumber in element_definitions[elementnumber]:
            nodes.append(nodenumber)
    nodes = list(set(nodes)) # get rid of duplicates!

    return nodes
#############################################################################


#############################################################################
def write_element_definition(outfile, elementnumber, nodenumbers):
    """Write a dataline defining one element to the outfile
    """
    outfile.write('%d, ' % (elementnumber))
    for i in range(len(nodenumbers)):
        n = nodenumbers[i]
        outfile.write('%d' % (n))
        if i < len(nodenumbers)-1: outfile.write(', ')
    outfile.write('\n')
#############################################################################


#############################################################################
def write_node_definition(outfile, nodenumber, coordinates):
    """Write a dataline defining one node to the outfile
    """
    outfile.write('%d, ' % (nodenumber))
    for i in range(len(coordinates)):
        coord = coordinates[i]
        outfile.write('%14.8E' % (coord))
        if i < len(coordinates)-1: outfile.write(', ')
    outfile.write('\n')
#############################################################################


#############################################################################
def write_n_int_per_line(list_of_int,outfile,n):
  """Write the integers in list_of_int to the output file - n integers 
  per line, separated by commas"""
  i=0
  for number in list_of_int:
      i=i+1
      outfile.write('%d' %(number ))
      if i < len(list_of_int):
          outfile.write(',  ')
      if i%n == 0:
          outfile.write('\n')
  if i%n != 0: 
      outfile.write('\n')
#############################################################################


#############################################################################
def findnormal3(node1, node2, node3):
    """Find the normal of the triangular element defined by the nodes
    node1, node2 and node3.
    The nodes are NumPy arrays.
    """
    a = node2 - node1
    b = node3 - node1
    v = np.cross(a,b)
    n = v / np.linalg.norm(v)
    return n
#############################################################################


#############################################################################
def findnormal4(node1, node2, node3, node4):
    """Find the average normal of the 4-noded element defined by the nodes
    node1, node2 node3 and node4.
    The nodes are NumPy arrays.
    """
    n1 = findnormal3(node1, node2, node3)
    n2 = findnormal3(node2, node3, node4)
    n3 = findnormal3(node3, node4, node1)
    n4 = findnormal3(node4, node1, node2)
    sum = n1+n2+n3+n4
    n = sum / np.linalg.norm(sum)
    return n
#############################################################################


#############################################################################
def effective_layup(layup):
    """Compute the effective layup for a given layup definition
    by joining identical layers"""

    effective_layup = [layup[0]]  # lets start with including the first layer

    for layer in layup[1:]:  # layup[1:] may be an empty list
        existing_layer = effective_layup[-1] # last layer in effective layup
        # if material and orientation are identical
        if layer[2] == existing_layer[2] and layer[3] == existing_layer[3]:
            t = existing_layer[0] + layer[0]       # add the thickness
            ip = max(existing_layer[1], layer[1])  # larger choice for integration points
            mat = layer[2]  # material identical
            ori = layer[3]  # orientation identical
            pn = existing_layer[4] + layer[4]  # concatenate ply names
            effective_layup[-1] = [t, ip, mat, ori, pn]
        else:
            effective_layup.append(layer)

    return effective_layup
#############################################################################


#############################################################################
def equalize_layup(layup,n):
    """Equalize the layup so that it is described by n layers.
    The following algorithm is used:
    1) find the (first) thickest layer in the layup definition
    2) split this layer up into two layers with half the thickness
       of the original layer, each.
    3) Starting from the two new layers, search for the beginning and 
       the end of the "physical layer", i.e. the region with constant
       material and orientation
    4) Change the thickness of all layers in the physical layer so the 
       the individual layers have identical thickness
    5) If number of layers is smaller than n, start over at 1)
    Formerly, step 4 was done by an individual function. However, this yiels
    better results, as balancing the layers in step 4 influences the thickest
    layer found in step 1.
    """
    if n < len(layup):
        print("ERROR: The layup has more layers than the desired number")
        print("of layers defined by the user.")
        sys.exit(1)

    equalized_layup = deepcopy(layup)  # prevent modifications in layup

    # n is larger or equal to len(layup)

    while n>len(equalized_layup):
        thickest_layer = max(equalized_layup, key=lambda list: abs(list[0]))
        i = equalized_layup.index(thickest_layer)  # index of thickest layer

        if len(thickest_layer)>4:
            t, ip, mat, ori, pn = thickest_layer
            layer1 = [t/2.0, ip, mat, ori, pn+'_1']
            layer2 = [t/2.0, ip, mat, ori, pn+'_2']
        else:
            t, ip, mat, ori = thickest_layer
            layer1 = [t/2.0, ip, mat, ori]
            layer2 = [t/2.0, ip, mat, ori]

        equalized_layup[i] = layer2
        equalized_layup.insert(i,layer1)

        start_phys_layer = i  # initial values for the start and end index
        end_phys_layer = i+1  # of the physical layer (-->ident. material)
        ref_layer = equalized_layup[i]

        while start_phys_layer > 0:  # find start_phys_layer
            testlayer = equalized_layup[start_phys_layer-1]
            if testlayer[2:4] == ref_layer[2:4]:
                start_phys_layer = start_phys_layer - 1
            else:
                break

        while end_phys_layer < len(equalized_layup)-1:  # find end_phys_layer
            testlayer = equalized_layup[end_phys_layer+1]
            if testlayer[2:4] == ref_layer[2:4]:
                end_phys_layer = end_phys_layer + 1
            else:
                break

        # Find balanced thickness for layers
        phys_layer_thickness = 0.0
        for layer in equalized_layup[start_phys_layer:end_phys_layer+1]:
            phys_layer_thickness = phys_layer_thickness + layer[0]
        balanced_thickness = phys_layer_thickness / (end_phys_layer-start_phys_layer+1)

        # Assign new thickness to layers:
        for j in range(start_phys_layer,end_phys_layer+1):
            equalized_layup[j][0] = balanced_thickness

    return equalized_layup
#############################################################################


#############################################################################
def orderedfacenodes(facenodes, hexelement):
    """
    Check if the 4 facenodes given correspond to one of the six
    faces of the hexelement. If yes, return the facenodes in the
    appropriate order.
    """
    if len(hexelement) == 8:  # linear hexahedron
        M = [[3,   2,   1,   4],   # outward pointing normals
             [7,   8,   5,   6], 
             [6,   5,   1,   2], 
             [7,   6,   2,   3], 
             [8,   7,   3,   4], 
             [5,   8,   4,   1]]

        # M = [[4,   1,   2,   3],  # innward pointing normals
        #      [6,   5,   8,   7], 
        #      [2,   1,   5,   6], 
        #      [3,   2,   6,   7], 
        #      [4,   3,   7,   8], 
        #      [1,   4,   8,   5]]

    else:  # quadratic hexahedron
        M = [[3,   2,   1,   4,   10,   9,  12,  11],  # outward pointing normals
             [7,   8,   5,   6,   15,  16,  13,  14], 
             [6,   5,   1,   2,   13,  17,   9,  18], 
             [7,   6,   2,   3,   14,  18,  10,  19], 
             [8,   7,   3,   4,   15,  19,  11,  20], 
             [5,   8,   4,   1,   16,  20,  12,  17]]

        # M = [[4,   1,   2,   3,  12,   9,  10,  11],  # innward pointing normals
        #      [6,   5,   8,   7,  13,  16,  15,  14], 
        #      [2,   1,   5,   6,   9,  17,  13,  18], 
        #      [3,   2,   6,   7,  10,  18,  14,  19], 
        #      [4,   3,   7,   8,  11,  19,  15,  20], 
        #      [1,   4,   8,   5,  12,  20,  16,  17]]

    facenodes_local = []  # local node numbers of facenodes
    for facenode in facenodes:
        facenodes_local.append(hexelement.index(facenode)+1)

    i = 0
    facenumber = 0  # no valid face number
    for m in M:
        if set(m) == set(facenodes_local):
            facenumber = i+1
            break
        i = i+1

    ordered_facenodes = []
    if facenumber != 0:  # facenumber found
        for j in M[facenumber-1]:
            ordered_facenodes.append(hexelement[j-1])
        return ordered_facenodes

#############################################################################


#############################################################################
def find_tangent_2D(element_definition,nodal_coordinates):
    """
    Return the in plane tangent of a 4-noded element pointing from 
    the midpoint between node 2 and 3 to the midpoint between node
    4 and 1.
    This also works for 8-noded elements ignoring the mid-side nodes
    """
    node1 = nodal_coordinates[element_definition[0]] 
    node2 = nodal_coordinates[element_definition[1]] 
    node3 = nodal_coordinates[element_definition[2]] 
    node4 = nodal_coordinates[element_definition[3]] 
    
    tangent = (node4+node1)*0.5 - (node2+node3)*0.5 
    tangent = tangent / np.linalg.norm(tangent)

    return tangent
#############################################################################


#############################################################################
def generous_round(t):
    """Round up t to the next decade. Return an integer.
    e.g. 9-->10; 10-->100; 11-->100
    """
    return int(10**round(math.log10(t)+0.5))
#############################################################################


#############################################################################
def status(message,verbose=True):
    """Print status message and time.clock() to screen
    """
    if verbose:
        print(('%4.2f: %s' % (clock(), message)))
#############################################################################


#############################################################################
def transformed_z(coord,rot_mat):
    """
    Returns the z-coordinate of the node after rotation defined by
    rotation matrix.
    """
    newcoord = np.dot(rot_mat, coord)
    return newcoord[2]
#############################################################################


#############################################################################
#                                MAIN PROGRAM                               #
#############################################################################


def main(args):
    
    # Initialize dictionaries
    element_definitions = {}      # node numbers of each element
    new_element_definitions = {}  # the newly generated hexahedral elements
    becas_element_definitions = {} # node numbers of each 2D BECAS 2D BECAS element
    element_stack = {}            # the stack of three hex elements generated from each shell element
    elset_definitions = {}        # element numbers for each ELSET
    new_elset_definitions = {}    # element numbers for each newly generated ELSET
    nodal_coordinates = {}        # original coordiantes for each node
    new_nodal_coordinates = {}    # the original and the generated nodes
    node_stack = {}               # the stack of four nodes generated for each original node
    nset_definitions = {}         # node numbers for each NSET
    new_nset_definitions ={}      # node numbers for each newly generated NSET
    shell_section_parameters = {} # the parameter value pairs for each shell section definition
                                  # using the respective elset as key
    new_shell_section_parameters = {} # the parameter value pairs for each new shell section definition
                                  # using the respective elset as key
    layup_of_elset = {}           # layup information for each ELSET 
    node_offset_of_elset = {}     # numerical value of the node offset parameter for each elset
    node_offset_of_element = {}   # numerical value of the node offset parameter for each element 
    new_layup_of_elset = {}       # layup information for each newly generated ELSET 
    layup_of_element = {}         # layup information for each element
    element_normals = {}          # the normal direction of each element
    layerthickness_of_node = {}   # *a list of* layer thicknesses found for each node
                                  # (Corner nodes have two layups)
    node_normals = {}             # *a list of* normal directions found for each node
                                  # (Corner nodes have two normals)
    node_offsets = {}             # *a list of* node offsets (numerical values) for each node
                                  # (Corner nodes have two offsets!)
    element_tangent = {}          # tangent unit vector for element --> BECAS fiber plane angle
    material_numbers = {}         # Dictionary to hold the material number for each Abaqus material
    material_names = {}           # Dictionary to hold the material name for each material number
    current_material_number = 0   # Number to be assigned to current_material (for BECAS)
    material_properties = {}      # Dictionary to hold the material properties for each material name
    material_of_element = {}      # Dictionary to hold the material name assigned to each element
    material_number_of_element = {}  # Dictionary to hold the material number assigned to each element
    orientation_of_element = {}   # Dictionary to hold material orientation angle of each new element
    domination_factor = {}        # Scalar defined for each element. Elements with higher values
                                  # dominate nodal thickness distribution
    layered_hexelem_definitions = {} # newly generated "layered" hexahedral elements
                                     # can be used as Abaqus continuum shell elements
    layered_hexelem_nset_def = {} # node set definitions for the layered hexahderal elements
    
    status('program has started', args.verbose)
    
    elsets_to_offset = [a.upper() for a in args.elsets]
    infilename = args.inputfile
    
    if args.centerline:
        cline_coords = read_cline_file(args.centerline, args.verbose)
        csys_rot_mat = get_csys_rot_mat(cline_coords)
    
    if args.dominant_elsets:
        dominant_elsets = [a.upper() for a in args.dominant_elsets]
    
    list_of_lines = read_nested_files(infilename, args.verbose)
    keywords = parse_abaqus_input_file(list_of_lines)
    status('%d ABAQUS keywords found.' % (len(keywords)), args.verbose)
    
    # -------------------------------

# Start of loop analyzing keywords
##################################    
    status('analyzing keywords...', args.verbose)
    for keyword in keywords:
    
        parameters = getparameters(keyword)
        key = splitline(keyword[0])[0]
    
        # Nodel coordinates
        if key == '*NODE':
            for dataline in keyword[1:]:    # loop through datalines
                datalinelist = splitline(dataline)
                nodenumber = int(datalinelist[0])
                coordinates = np.array( [float(item) for item in datalinelist[1:]] )
                nodal_coordinates[nodenumber] = coordinates
    
    
        # Element numbers for each ELSET
        elif key == '*ELSET':
            if parameters['ELSET'][0] == '_': # if the elset is internal, ignore it
                continue
            element_number_list = []
            if 'GENERATE' in parameters: 
                for dataline in keyword[1:]:    # loop through datalines
                    datalinelist = splitline(dataline)
                    e1 = int(datalinelist[0])
                    e2 = int(datalinelist[1])
                    i  = int(datalinelist[2])
                    expandedlist = list(range(e1,e2+i,i))
                    element_number_list = element_number_list + expandedlist
            else:
                for dataline in keyword[1:]:    # loop through datalines
                    datalinelist = [int(item) for item in splitline(dataline)] # convert to integer
                    element_number_list = element_number_list + datalinelist
            elset_definitions[parameters['ELSET']] = element_number_list
    
        # Node numbers for each NSET
        elif key == '*NSET':
            if parameters['NSET'][0] == '_': # if the nset is internal, ignore it
                continue
            node_number_list = []
            if 'GENERATE' in parameters: 
                for dataline in keyword[1:]:    # loop through datalines
                    datalinelist = splitline(dataline)
                    n1 = int(datalinelist[0])
                    n2 = int(datalinelist[1])
                    i  = int(datalinelist[2])
                    expandedlist = list(range(n1,n2+i,i))
                    node_number_list = node_number_list + expandedlist
            else:
                for dataline in keyword[1:]:    # loop through datalines
                    datalinelist = [int(item) for item in splitline(dataline)] # convert to integer
                    node_number_list = node_number_list + datalinelist
            nset_definitions[parameters['NSET']] = node_number_list
    
        # Layer thicknesses of each ELSET used in a composite shell section definition
        # Layer thickness is positive if the offset is in normal direction,
        # layer thickness is negative, else.
        elif key in ['*SHELL SECTION', '*SHELL GENERAL SECTION'] and 'COMPOSITE' in parameters:
    
            if 'OFFSET' not in parameters:
                offset = 0.0
            elif parameters['OFFSET'] == 'SNEG':
                offset = -0.5
            elif parameters['OFFSET'] == 'SPOS':
                offset = 0.5
            else:
                try:
                    offset = float(parameters['OFFSET'])
                except:
                    print('ERROR trying to interprate the OFFSET parameter of ')
                    print(keyword)
                    sys.exit(1)
    
            node_offset_of_elset[parameters['ELSET']] = offset
    
            shell_section_parameters[parameters['ELSET']] = parameters
    
            layup = []
            for dataline in keyword[1:]:    # loop through datalines
                datalinelist = splitline(dataline)
                layerthickness = float(datalinelist[0]) 
                integrationpoints = int(datalinelist[1])
                materialname = datalinelist[2]
                orientationangle = float(datalinelist[3])
                if len(datalinelist)>4:
                    plyname = datalinelist[4]
                    layup.append([layerthickness, integrationpoints, materialname, orientationangle, plyname])
                else:
                    layup.append([layerthickness, integrationpoints, materialname, orientationangle])
    
            layup_of_elset[parameters['ELSET']] = layup
    
    
        # Find the nodes for each element and the element normals
        elif key == '*ELEMENT':
            element_number_list = []
            family, nodes_per_element = element_info(parameters['TYPE'])
    
            # Join data lines if line ends with a comma
            joined_datalines = []
            newline = ''
            for line in keyword[1:]:
                newline = newline + line
                if not line.strip()[-1] == ',':  # if line ends with a comma
                    joined_datalines.append(newline)
                    newline = ''
    
            for dataline in joined_datalines:    # loop through datalines
                datalinelist = splitline(dataline)
    
                elementnumber = int(datalinelist[0])
                nodenumbers = [int(item) for item in datalinelist[1:]]
                element_number_list.append(elementnumber)
    
                element_definitions[elementnumber] = nodenumbers
    
                if family == 'S' and nodes_per_element in [4,8]:  # should work for 4 and 8-noded elements!
                    node1 = nodal_coordinates[nodenumbers[0]]
                    node2 = nodal_coordinates[nodenumbers[1]]
                    node3 = nodal_coordinates[nodenumbers[2]]
                    node4 = nodal_coordinates[nodenumbers[3]]
                    normal = findnormal4(node1, node2, node3, node4)
                    element_normals[elementnumber] = normal
                if family in ['S', 'STRI'] and nodes_per_element in [3,6]:  # should work for 4 and 8-noded elements!
                    node1 = nodal_coordinates[nodenumbers[0]]
                    node2 = nodal_coordinates[nodenumbers[1]]
                    node3 = nodal_coordinates[nodenumbers[2]]
                    normal = findnormal3(node1, node2, node3)
                    element_normals[elementnumber] = normal
            
            if 'ELSET' in parameters:
                elset_definitions[parameters['ELSET']] = element_number_list
    
        # Material name and number
        elif key == '*MATERIAL':
            current_material_number = current_material_number + 1
            current_material = parameters['NAME']
            material_numbers[current_material] = current_material_number
            material_names[current_material_number] = current_material
    
        # Material name, number and parameters
        elif key == '*ELASTIC':
            if 'TYPE' in parameters:
                materialtype = parameters['TYPE']
            else:
                materialtype = 'ISOTROPIC' # the default
    
            if materialtype == 'ENGINEERING CONSTANTS':
                datalinelist1 = [float(item) for item in splitline(keyword[1])] 
                datalinelist2 = [float(item) for item in splitline(keyword[2])] 
                E1, E2, E3, nu12, nu13, nu23, G12, G13 = datalinelist1
                G23, = datalinelist2
                elastic_prop = {'E1': E1, 'E2': E2, 'E3': E3, 
                                'nu12': nu12, 'nu13': nu13, 'nu23': nu23, 
                                'G12': G12, 'G13': G13, 'G23': G23}
                if current_material in material_properties:
                    material_properties[current_material].update(elastic_prop)
                else:
                    material_properties[current_material] = elastic_prop
    
            if materialtype in ['ISOTROPIC', 'ISO']:
                datalinelist1 = [float(item) for item in splitline(keyword[1])] 
                E, nu = datalinelist1
                G = E / (2*(1+nu))
                elastic_prop = {'E1': E, 'E2': E, 'E3': E, 
                                'nu12': nu, 'nu13': nu, 'nu23': nu, 
                                'G12': G, 'G13': G, 'G23': G}
                if current_material in material_properties:
                    material_properties[current_material].update(elastic_prop)
                else:
                    material_properties[current_material] = elastic_prop
    
        elif key == '*DENSITY':
            rho, = [float(item) for item in splitline(keyword[1])] 
            density_prop = {'rho': rho}
            if current_material in material_properties:
                material_properties[current_material].update(density_prop)
            else:
                material_properties[current_material] = density_prop
    
        elif key == '*FAIL STRESS':
            datalinelist1 = [float(item) for item in splitline(keyword[1])] 
            Xt, Xc, Yt, Yc, S = datalinelist1[:5]
            failstress_prop = {'Xt': Xt, 'Xc': Xc, 
                               'Yt': Yt, 'Yc': Yc, 'S': S} 
            if current_material in material_properties:
                material_properties[current_material].update(failstress_prop)
            else:
                material_properties[current_material] = failstress_prop
    
        elif key == '*FAIL STRAIN':
            datalinelist1 = [float(item) for item in splitline(keyword[1])] 
            Xet, Xec, Yet, Yec, Se = datalinelist1[:5]
            failstrain_prop = {'Xet': Xet, 'Xec': Xec, 
                               'Yet': Yet, 'Yec': Yec, 'Se': Se} 
            if current_material in material_properties:
                material_properties[current_material].update(failstrain_prop)
            else:
                material_properties[current_material] = failstrain_prop


##################################
# End of loop analyzing keywords


    # If the sections option is used (--> BECAS), delete all items
    # not relevant. This prevents problems that occur at radial thickness
    # changes ("transition elements").
    
    if args.sections:
        status('deleting all irrelevant items', args.verbose)
        becas_elsets_shell = []
        pattern = r'^' + args.sections.upper() + r'(.*)'
        for elset in elset_definitions.keys():
            if re.search(pattern, elset):
                becas_elsets_shell.append(elset)
    
        becas_elsets_shell.sort()
    
        all_section_elements = set([])  # all section elements combined in one set
        for elset in becas_elsets_shell:
            all_section_elements = all_section_elements | set(elset_definitions[elset])
    
        all_section_nodes = elset2nset(all_section_elements, element_definitions)
    
        if args.centerline:
            if len(cline_coords) != len(becas_elsets_shell):
                print('ERROR: The number of local coordinate systems defined in %s' % (args.centerline))
                print('is different from the number of elements starting with %s' % (args.sections))
                sys.exit(1)
    
    
        # Remove useless nodal coordinates
        nodes2delete = set(nodal_coordinates.keys()) - set(all_section_nodes)
        for nn in nodes2delete:
            del nodal_coordinates[nn]
    
        # Remove useless elset definitions / element numbers
        for elset, elements in list(elset_definitions.items()):
            new_element_number_list = list(set(elements) & all_section_elements)
            if len(new_element_number_list) == 0:
                del elset_definitions[elset]
            else:
                elset_definitions[elset] = new_element_number_list
    
        # Remove useless nset definitions / node numbers
        for nset, nodes in list(nset_definitions.items()):
            new_node_number_list = list(set(nodes) & set(all_section_nodes))
            if len(new_node_number_list) == 0:
                del nset_definitions[nset]
            else:
                nset_definitions[nset] = new_node_number_list
    
        # Remove useless elements
        excess_elements = set(element_definitions.keys())-all_section_elements
        for element in excess_elements:
            del element_definitions[element]
            if element in element_normals:
                del element_normals[element]
    
        # Remove useless layup definitions
        elsets2delete = set(layup_of_elset.keys()) - set(elset_definitions.keys())
        for elset in elsets2delete:
            del layup_of_elset[elset]
    
    
    # Check if all elsets_to_offset have been defined in the input file
    for elset in elsets_to_offset:
        if elset not in elset_definitions:
            print(('ERROR: Element Set %s not defined in input file.' % (elset)))
            #input('Press Enter to display a list of available element sets.')
            print('Element sets defined in the input file:')
            for defined_elset in sorted(list(elset_definitions)):
                print(defined_elset)
            sys.exit(1)
    
    # Calculate domination factor for each element:
    # Set domination_factor to 0.0 by default:
    for element in element_definitions:
        domination_factor[element] = 0.0
    
    if args.dominant_elsets:
        d = 0.0
        for elset in dominant_elsets:
            d = d + 1.0
            elements = elset_definitions[elset]
            for element in elements:
                domination_factor[element] = d
    
    
    # Find appropriate jump for nodenumber and elementnumber
    # from layer to layer
    # nnjump = generous_round(max(nodal_coordinates.keys()))
    # enjump = generous_round(max(element_definitions.keys()))
    
    # The generous round feature above is temporarely disabled, 
    # because BECAS has performance issues with large node and
    # element numbers...
    nnjump = max(nodal_coordinates.keys())
    enjump = max(element_definitions.keys())
    
    status('computing effective layup', args.verbose)
    # Compute the effective layup for the given layup definition
    # by joining identical layers
    for elset, layup in layup_of_elset.items():
        layup_of_elset[elset] = effective_layup(layup)
             
    # Modify the layup so that there are args.layers layers everywhere
    status('equalizing layup: %d layers everywhere' % (args.layers), args.verbose)
    equalized_layup = {} 
    for elset, layup in layup_of_elset.items():
        equalized_layup[elset] = equalize_layup(layup,args.layers)
    layup_of_elset.update(equalized_layup)
    
    # Find layup of each element
    for elset, layup in layup_of_elset.items():
        for elementnumber in elset_definitions[elset]:
            layup_of_element[elementnumber] = layup
    
    # Find node offset for each element
    #for elset, offset in node_offset_of_elset.items():
    for elset in layup_of_elset:
        offset = node_offset_of_elset[elset]
        for elementnumber in elset_definitions[elset]:
            node_offset_of_element[elementnumber] = offset 
    
    
    # Start loop over element sets to offset 
    ########################################

    status('determining layer thicknesses', args.verbose)
    for current_elset in elsets_to_offset:
    
        status('processing Element Set %s' % (current_elset), args.verbose)
    
        current_elements = elset_definitions[current_elset]  # list of current elements
        current_nodes = elset2nset(current_elements, element_definitions)
    
        # Find current elements of node
        current_elements_of_node = {}  # Dictionary to hold relevant elements attached to each node
        for elementnumber in current_elements:
            nodenumbers = element_definitions[elementnumber]
            for nodenumber in nodenumbers:
                current_elements_of_node.setdefault(nodenumber, []).append(elementnumber)
    
    
        # Find the layer thicknesses of the current nodes (the layer thicknesses corresponding
        # to the minimum (or maximum or average) total thickness of of any current element 
        # attached to it) and the current normal at each node, 
        # and store the information in the respective list.
    
        for nodenumber in current_nodes:
            elements = current_elements_of_node[nodenumber]
        
            vecsum = np.array([0.0, 0.0, 0.0]) # initialize vecsum
            eloffset = 0.0  # initialize element based node offset sum
            for elementnumber in elements:
                vecsum = vecsum + element_normals[elementnumber]  # vector sum of the normals
                eloffset = eloffset + node_offset_of_element[elementnumber]
            normal = vecsum / np.linalg.norm(vecsum)  # make unit vector
            noffset = eloffset / len(elements)
    
            node_normals.setdefault(nodenumber, []).append(normal)
            node_offsets.setdefault(nodenumber, []).append(noffset)
        
            domlist = [domination_factor[element] for element in elements]
            maxdom = max(domlist)
            domindices = np.where(np.array(domlist)==maxdom)[0]
            domelements = [elements[index] for index in domindices]
    
            thickness_list = []  # list of layer thicknesses of all (dominant) current elements sharing the node
            for elementnumber in domelements:
                thicknesses = [item[0] for item in layup_of_element[elementnumber]]
                thickness_list.append( thicknesses )
       
            if args.nodal_thickness=='min':
                min_thicknesses = min(thickness_list, key=sum) # Minimum based on total thickness!
                layerthickness_of_node.setdefault(nodenumber, []).append(min_thicknesses)
            elif args.nodal_thickness=='max':
                max_thicknesses = max(thickness_list, key=sum) # Maximum based on total thickness!
                layerthickness_of_node.setdefault(nodenumber, []).append(max_thicknesses)
            elif args.nodal_thickness=='average':
                min_thicknesses = min(thickness_list, key=sum) 
                max_thicknesses = max(thickness_list, key=sum)
                average_thicknesses = [(a+b)*0.5 for a,b in zip(min_thicknesses,max_thicknesses)]
                layerthickness_of_node.setdefault(nodenumber, []).append(average_thicknesses)
    
    ######################################
    # End loop over element sets to offset 
    
    
    status('computing the offset vectors', args.verbose)
    # Compute the offset vectors
    for nodenumber, normals in node_normals.items():
    
        offsets = []
    
        if len(normals) == 1: # normal situation
            normal = normals[0]
            noffset = node_offsets[nodenumber][0]
            layerthicknesses = layerthickness_of_node[nodenumber][0]
            total_thick = sum(layerthicknesses)
            
            interface_pos = [0.0, ]
            acct=0.0
            for layerthickness in layerthicknesses:
                acct = acct + layerthickness
                interface_pos.append(acct)
    
            for acct in interface_pos:
                # 1) move nodes to mid-surface: -noffset * total_thick * normal
                # 2) move nodes to bottom surface:  -0.5 * total_thick * normal
                # 3) move by layer thickness: +acct * normal
                offset = ( (-1) * total_thick * (noffset+0.5) + acct ) * normal
                offsets.append(offset)
    
    
        if len(normals) > 1: # the node is assumed to be a corner
    
            layerthicknesses1 = layerthickness_of_node[nodenumber][0]
            layerthicknesses2 = layerthickness_of_node[nodenumber][1]
            total_thick1 = sum(layerthicknesses1)
            total_thick2 = sum(layerthicknesses2)
            normal1 = normals[0]
            normal2 = normals[1]
            noffset1 = node_offsets[nodenumber][0]
            noffset2 = node_offsets[nodenumber][1]
    
            interface_pos1 = [0.0, ]
            acct1=0.0
            for layerthickness1 in layerthicknesses1:
                acct1 = acct1 + layerthickness1
                interface_pos1.append(acct1)
            interface_pos2 = [0.0, ]
            acct2=0.0
            for layerthickness2 in layerthicknesses2:
                acct2 = acct2 + layerthickness2
                interface_pos2.append(acct2)
    
            for acct1, acct2 in zip(interface_pos1,interface_pos2):
                offset = offset_and_intersect([normal1, normal2], [(-1)*total_thick1*(noffset1+0.5)+acct1, (-1)*total_thick2*(noffset2+0.5)+acct2], 1.0)
                offsets.append(offset)
    
        if len(normals) > 2: 
            print(('WARNING: %d normals found at node %d.' % (len(normals), nodenumber)))
            print('Only the first two normals (and the respective thicknesses) are used')
            print('to compute the offset.')
    
        # Find new nodal coordinates
        original_coordinate = nodal_coordinates[nodenumber]
        i=0
        stack = []
        for offset in offsets:
            new_coordinate = original_coordinate + offset
            new_node_number = nodenumber+(2*i)*nnjump  # jump 2*i - nodenumbers for mid-side nodes needed
            new_nodal_coordinates[new_node_number] = new_coordinate
            stack.append(new_node_number)
            i=i+1
        node_stack[nodenumber] = stack
    
    
    # Generate hexahedral elements
    # Loop only through the elsets_to_offset
    status('generating hexahedral elements', args.verbose)
    for current_elset in elsets_to_offset:
        current_elements = elset_definitions[current_elset]  
        for elementnumber in current_elements:
            nodenumbers = element_definitions[elementnumber]
            stack = []
            for i in range(args.layers):
                new_element_number = elementnumber + i * enjump
                stack.append(new_element_number)
                lower_nodes = [nn + 2*i*nnjump for nn in nodenumbers]
                upper_nodes = [nn + 2*(i+1)*nnjump for nn in nodenumbers]
                midside_nodes = [nn + nnjump + 2*i*nnjump for nn in nodenumbers[:4]]
        
                # Generate mid-side nodes 17, 18, 19 and 20
                # It is easier to do that here.
                if len(lower_nodes) == 8:  # 8-noded shell element
                    for lowernn, uppernn in zip(lower_nodes[:4], upper_nodes[:4]):
                        midnodecoord = 0.5 * (new_nodal_coordinates[lowernn] + new_nodal_coordinates[uppernn])
                        new_node_number = lowernn + nnjump
                        new_nodal_coordinates[new_node_number] = midnodecoord
        
                if len(lower_nodes) in [3,4]:  # 3- or 4-noded shell element
                    new_element_definitions[new_element_number] = lower_nodes + upper_nodes
                else: # 8-noded shell element
                    new_element_definitions[new_element_number] = lower_nodes[:4] + upper_nodes[:4] + lower_nodes[4:] + upper_nodes[4:] + midside_nodes
            element_stack[elementnumber] = stack
    
            # Generate 1 "layered" hexahedral element
            # --> can be used as continuum shell element in Abaqus
            lower_nodes = nodenumbers[:4]
            upper_nodes = [nn + 2*args.layers*nnjump for nn in lower_nodes]
            layered_hexelem_definitions[elementnumber] = lower_nodes + upper_nodes
    
    
    
    status('generating new elset and nset definitions', args.verbose)
    # generate new_elset_definitions for all element sets needed
    # for material assignment.
    # Append numbers to the original element set names to represent
    # the layers of elements: *_01, *_02, *_03, ...
    for elset, layup in layup_of_elset.items():
    
        original_elements = elset_definitions[elset]
        for i in range(args.layers):
            new_elset_name = elset + '_%02d' % (i+1)
            elements = [en + i*enjump for en in original_elements]
            new_elset_definitions[new_elset_name] = elements
    
            current_layup = layup_of_elset[elset][i]
            new_layup_of_elset[new_elset_name] = current_layup
    
            for element in elements:
                orientation_of_element[element] = current_layup[3]
            
            new_parameters = shell_section_parameters[elset]
            if 'OFFSET' in new_parameters:
                del(new_parameters['OFFSET'])
            new_parameters['ELSET'] = new_elset_name
            
            # deepcopy prevents new_shell_section_parameters from being updated
            # when new_parameters is overwritten in the next loop
            new_shell_section_parameters[new_elset_name] = deepcopy(new_parameters)
    
    
    # Generate equivalent new_elset_definitions for all 
    # element sets defined in the input file using the *ELSET keyword.
    # Append "_3D" to the original element set names 
    
    for elset, elements in elset_definitions.items():
        new_elements = []
        for element in elements:
            if element in element_stack:
                for item in element_stack[element]:
                    new_elements.append(item)
        if len(new_elements) > 0:
            new_elset_definitions[elset + '_3D'] = new_elements
    
    
    
    # Generate equivalent new_nset_definitions for all 
    # node sets defined in the input file using the *NSET keyword.
    # Append "_3D" to the original node set names 
    # Mid-side nodes 17, 18, 19 and 20 missing
    
    for nset, nodes in nset_definitions.items():
        new_nodes = []
        for node in nodes:
            if node in node_stack:
                for item in node_stack[node]:
                    new_nodes.append(item)
        if len(new_nodes) > 0:
            new_nset_definitions[nset + '_3D'] = new_nodes
    
    
    # Generate node sets for the layered hexelement model for all
    # node sets defined in the input file using the *NSET keyword.
    
    if args.debug:
        layered_hexelements = list(layered_hexelem_definitions.keys())
        layered_hexelem_nodes = elset2nset(layered_hexelements, layered_hexelem_definitions)
    
        for nset, nodes in nset_definitions.items():
            intersect_nodes = set(nodes) & set(layered_hexelem_nodes)
            new_nodes = [nn + 2*args.layers*nnjump for nn in intersect_nodes]
            new_set = list(intersect_nodes) + new_nodes
    
            if len(new_set) > 0:
                layered_hexelem_nset_def[nset] = new_set
    
    
    
    
    # Correct mid-side nodes:
    # Place the midsside nodes of elements with a thickness change of
    # larger than x
    # at the mid-point between the corresponding main nodes
    status('correcting mid-side nodes', args.verbose)
    for current_elset in elsets_to_offset:
    
        current_elements = elset_definitions[current_elset]  # list of current elements
        for elementnumber in current_elements:
            
            nodenumbers = element_definitions[elementnumber]
    
            if len(nodenumbers) == 8:  # 8-noded shell
    
                elementthicknesslist = []
                for nn in nodenumbers:
                    for tlist in layerthickness_of_node[nn]:
                        elementthicknesslist.append(abs(sum(tlist)))
                min_el_thick = min(elementthicknesslist)
                max_el_thick = max(elementthicknesslist)
                thick_ratio = min_el_thick / max_el_thick
        
                for newelementnumber in element_stack[elementnumber]:
                    newnodenumbers = new_element_definitions[newelementnumber]
    
                    # originally only elements with a thickness ratio < 0.9
                    # had there mid-side nodes corrected. However, after
                    # problems with mesh generation in the trailing edge
                    # this was activated for all elements
                    # this is especially relevant because BECAS does not (yet)
                    # plot the mid-side nodes when plotting the mesh.
                    #if thick_ratio < 0.9:
                    if 1==1:
                        # correct position of midside nodes 9-16
                        new_nodal_coordinates[newnodenumbers[8]] = 0.5 * (new_nodal_coordinates[newnodenumbers[0]] + new_nodal_coordinates[newnodenumbers[1]])
                        new_nodal_coordinates[newnodenumbers[9]] = 0.5 * (new_nodal_coordinates[newnodenumbers[1]] + new_nodal_coordinates[newnodenumbers[2]])
                        new_nodal_coordinates[newnodenumbers[10]] = 0.5 * (new_nodal_coordinates[newnodenumbers[2]] + new_nodal_coordinates[newnodenumbers[3]])
                        new_nodal_coordinates[newnodenumbers[11]] = 0.5 * (new_nodal_coordinates[newnodenumbers[3]] + new_nodal_coordinates[newnodenumbers[0]])
                        new_nodal_coordinates[newnodenumbers[12]] = 0.5 * (new_nodal_coordinates[newnodenumbers[4]] + new_nodal_coordinates[newnodenumbers[5]])
                        new_nodal_coordinates[newnodenumbers[13]] = 0.5 * (new_nodal_coordinates[newnodenumbers[5]] + new_nodal_coordinates[newnodenumbers[6]])
                        new_nodal_coordinates[newnodenumbers[14]] = 0.5 * (new_nodal_coordinates[newnodenumbers[6]] + new_nodal_coordinates[newnodenumbers[7]])
                        new_nodal_coordinates[newnodenumbers[15]] = 0.5 * (new_nodal_coordinates[newnodenumbers[7]] + new_nodal_coordinates[newnodenumbers[4]])
        
    
    # Generate 2D elements and find fiber plane angles for BECAS
    if args.sections:
        status('generating 2D mesh for BECAS', args.verbose)
        i = 0
        for elset in becas_elsets_shell:
            elements = new_elset_definitions[elset + '_3D']
            for element in elements:
                nodes = new_element_definitions[element]
                # sort nodes using their (transformed) z-coordinate
                if args.centerline:
                    sorted_nodes = sorted(nodes, key=lambda node: transformed_z(new_nodal_coordinates[node],csys_rot_mat[i]))
                else:
                    sorted_nodes = sorted(nodes, key=lambda node: new_nodal_coordinates[node][2])
                if len(nodes) == 8:  # linear hexahedron
                    backnodes = sorted_nodes[:4]
                    frontnodes = sorted_nodes[-4:]
                else: # quadratic hexahedron
                    backnodes = sorted_nodes[:8]
                    frontnodes = sorted_nodes[-8:]
                facenodes = orderedfacenodes(frontnodes, nodes) 
                if facenodes:
                    becas_element_definitions[element] = facenodes
                else:
                    print(('ERROR: Could not find suitable face of element %d' % (element)))
                    print('for the generation of a 2D element for BECAS.')
                    sys.exit(1)
    
                tangent = find_tangent_2D(facenodes, new_nodal_coordinates)
                element_tangent[element] = tangent
            i = i + 1
    
    
    # Find material name and BECAS material number for each element
    for elset, layup in new_layup_of_elset.items():
        materialname = layup[2]
        elements = new_elset_definitions[elset]
        for element in elements:
            material_of_element[element] = materialname
            material_number_of_element[element] = material_numbers[materialname]
        
    
    # If in debug mode: write two new Abaqus input files
    ####################################################
    # 1) File using stacked hexahedral elements
    # #########################################
    if args.debug:
        outfilename = 'shellexpander_debugfile.inp'
        outfile = open(outfilename, 'w')
        status('debugging mode: writing abaqus input file %s' % (outfilename), args.verbose)
    
        # Write new nodal coordinates
        outfile.write('**\n')
        outfile.write('********************\n')
        outfile.write('** NODAL COORDINATES\n')
        outfile.write('********************\n')
        outfile.write('*NODE\n')
        for nodenumber, coordinates in new_nodal_coordinates.items():
            write_node_definition(outfile, nodenumber, coordinates)
        
        # Write new element definitions
        outfile.write('**\n')
        outfile.write('***********\n')
        outfile.write('** ELEMENTS\n')
        outfile.write('***********\n')
        outfile.write('*ELEMENT, TYPE=SC8R\n')
        for elementnumber, nodenumbers in new_element_definitions.items():
            if len(nodenumbers) in [8, 20]:
                # in case of 20 noded elements write only 8 nodes
                # at this point, excess nodes are not deleted.
                write_element_definition(outfile, elementnumber, nodenumbers[:8])
    
        
        # Write new element sets
        outfile.write('**\n')
        outfile.write('***************\n')
        outfile.write('** ELEMENT SETS\n')
        outfile.write('***************\n')
        for elset, elements in new_elset_definitions.items():
            outfile.write('*ELSET, ELSET=%s\n' % (elset))
            write_n_int_per_line(elements, outfile, 8)
        
        # Write new node sets
        outfile.write('**\n')
        outfile.write('************\n')
        outfile.write('** NODE SETS\n')
        outfile.write('*************\n')
        for nset, nodes in new_nset_definitions.items():
            outfile.write('*NSET, NSET=%s\n' % (nset))
            write_n_int_per_line(nodes, outfile, 8)
        
        # Write new Shell Section definitions
        outfile.write('**\n')
        outfile.write('****************************\n')
        outfile.write('** SHELL SECTION DEFINITIONS\n')
        outfile.write('****************************\n')
        for elset, layup in new_layup_of_elset.items():
            parameters = new_shell_section_parameters[elset]
            line = keyword_line('*SHELL SECTION', parameters)
            outfile.write('%s\n' % (line))
            outfile.write('%g, %d, %s, %g, %s\n' % 
                    (layup[0], layup[1], layup[2], layup[3], layup[4]))
        
        
        
        # Deal with the other keywords:
        
        outfile.write('**\n')
        outfile.write('******************\n')
        outfile.write('** COPIED KEYWORDS\n')
        outfile.write('******************\n')
        
        for keyword in keywords:
            parameters = getparameters(keyword)
            key = splitline(keyword[0])[0]
        
            if key in ['*ORIENTATION','*MATERIAL','*DENSITY','*ELASTIC','*FAIL STRESS']:
                for line in keyword:
                    outfile.write('%s\n' % (line))
                outfile.write('**\n')
        
            # Write new *NODE keyword. This should work, even if the input file
            # has several *NODE keywords
            elif key == '*NODE':
                continue  # Do nothing, next keyword
        
            elif key == '*SHELL SECTION':
                continue  # Do nothing, next keyword
                
            elif key == '*ELEMENT':
                continue  # Do nothing, next keyword
        
            # Else: write the keywords as they have been read
            else:
                pass # What to do here?
                # for line in keyword:
                #     outfile.write('%s\n' % (line))
        
        outfile.close()
    
    # 2) File using layered hexahedral elements
    # #########################################
        outfilename = 'shellexpander_layeredhex.inp'
        outfile = open(outfilename, 'w')
        status('debugging mode: writing abaqus input file %s' % (outfilename), args.verbose)
    
        layered_hexelements = list(layered_hexelem_definitions.keys())
        layered_hexelem_nodes = elset2nset(layered_hexelements, layered_hexelem_definitions)
    
        # Write new nodal coordinates
        outfile.write('**\n')
        outfile.write('********************\n')
        outfile.write('** NODAL COORDINATES\n')
        outfile.write('********************\n')
        outfile.write('*NODE\n')
        for nodenumber in sorted(layered_hexelem_nodes):
            coordinates = new_nodal_coordinates[nodenumber]
            write_node_definition(outfile, nodenumber, coordinates)
        
        # Write new element definitions
        outfile.write('**\n')
        outfile.write('***********\n')
        outfile.write('** ELEMENTS\n')
        outfile.write('***********\n')
        outfile.write('*ELEMENT, TYPE=SC8R\n')
        for elementnumber, nodenumbers in layered_hexelem_definitions.items():
            write_element_definition(outfile, elementnumber, nodenumbers)
    
        # Write new element sets
        outfile.write('**\n')
        outfile.write('***************\n')
        outfile.write('** ELEMENT SETS\n')
        outfile.write('***************\n')
        for elset, elements in elset_definitions.items():
            intersect_elements = set(elements) & set(layered_hexelements)
            if len(intersect_elements) > 0:
                outfile.write('*ELSET, ELSET=%s\n' % (elset))
                write_n_int_per_line(intersect_elements, outfile, 8)
    
        # Write new node sets
        outfile.write('**\n')
        outfile.write('************\n')
        outfile.write('** NODE SETS\n')
        outfile.write('*************\n')
        for nset, nodes in layered_hexelem_nset_def.items():
            outfile.write('*NSET, NSET=%s\n' % (nset))
            write_n_int_per_line(nodes, outfile, 8)
    
    
        # Copy keywords that need not be changed
        outfile.write('**\n')
        outfile.write('*****************\n')
        outfile.write('** OTHER KEYWORDS\n')
        outfile.write('*****************\n')
        
        for keyword in keywords:
            parameters = getparameters(keyword)
            key = splitline(keyword[0])[0]
        
            if key in ['*ORIENTATION','*MATERIAL','*DENSITY','*ELASTIC','*FAIL STRESS']:
                for line in keyword:
                    outfile.write('%s\n' % (line))
                outfile.write('**\n')
    
            # Copy shell section keyword, but set offset parameter to zero
            elif key == '*SHELL SECTION':
                if 'OFFSET' in parameters:
                    parameters['OFFSET'] = '0.0'
                line = keyword_line('*SHELL SECTION', parameters)
                outfile.write('%s\n' % (line))
                for dataline in keyword[1:]:    # loop through datalines
                    outfile.write('%s\n' % (dataline))

# Write BECAS input files
#################################
    
    # init output dictionary
    shellexp_sections = {}
    
    if args.sections:
        status('writing BECAS input files', args.verbose)
        path_becas_out = os.path.join(os.getcwd(), args.becasdir)
        if os.path.isdir(path_becas_out):
            shutil.rmtree(path_becas_out)
            print(('Warning: %s existed and was deleted.' % (path_becas_out)))
    
        os.makedirs(path_becas_out)
        logfilepath = os.path.join(path_becas_out,'shellexpander_sections.log')
        logfile = open(logfilepath, 'w')
        i=0
        for elset_shell  in becas_elsets_shell:
            # init output dictionary for section
            msh2d = {}
            msh2d['s'] = None # cross section position along span
            msh2d['nl_2d'] = [] # Nodal points (node nr, x, y, z)
            msh2d['el_2d'] = []# Element number, node 1, n2, n3, ..., n8
            msh2d['emat']  = [] # Element nr, material nr, fiber angle, fiberplane angle
            msh2d['matprops'] = [] # material properties
            msh2d['failmat'] = [] # 
            msh2d['elsets'] = {} # elsets contained in mesh
            
            status('Processing section %s' % (elset_shell), args.verbose)
            becas_elements = []
            
            if not args.subelsets:
                for elset in elset_definitions.keys():
                    msh2d['elsets'][elset] = new_elset_definitions[elset + '_3D'] # return all elsets
                becas_elements = new_elset_definitions[elset_shell + '_3D']
            else:
                for elset in args.subelsets:
                    becas_elements.extend(new_elset_definitions[elset + '_3D'])
                    msh2d['elsets'][elset] = new_elset_definitions[elset + '_3D']
            becas_nodes = elset2nset(becas_elements, becas_element_definitions)
            
            radial_coords = [new_nodal_coordinates[node][2] for node in becas_nodes]
            mean_radial_coord = sum(radial_coords) / len(radial_coords)
            msh2d['s'] = mean_radial_coord
    
            if args.centerline:
                pos_error = abs(1 - (cline_coords[i][2]/mean_radial_coord))
                if pos_error > 0.02:
                    print('WARNING: Mean z-coordiante of section %s' %(elset_shell))
                    print('and z-coordinate of origin of corresponding local')
                    print('coordinate system differ by %g%%.' %(pos_error*100))
            
            path_section = os.path.join(path_becas_out, elset_shell)
            os.makedirs(path_section)
            
            logfile.write('%s   %g   %s\n' % (elset_shell, mean_radial_coord, path_section))
    
            # Write nodal coordinates for BECAS 
            outfile = open(os.path.join(path_section, 'N2D.in'), 'w')
            for nodenumber in becas_nodes:
                coord = new_nodal_coordinates[nodenumber]
                if args.centerline:
                    coord = coord - cline_coords[i][0:3]
                    coord = np.dot(csys_rot_mat[i],coord)
                # Only write the frist two coordinates!
                outfile.write('%d  %14.8e  %14.8e\n' % (nodenumber, coord[0], coord[1]))  
                msh2d['nl_2d'].append([nodenumber, coord[0], coord[1]])
            outfile.close()
    
            # Write element definitions for BECAS 
            outfile = open(os.path.join(path_section, 'E2D.in'), 'w')
            for elementnumber in becas_elements:
                nodes = becas_element_definitions[elementnumber]
                el_2d = []
                outfile.write('%d  ' % (elementnumber)) 
                el_2d.append(elementnumber)
                for nodenumber in nodes: 
                    outfile.write('%d  ' % (nodenumber)) 
                    el_2d.append(nodenumber)
                if len(nodes) == 4:
                    outfile.write('0  0  0  0')  # fill up with zeros if quad4
                    el_2d.extend([0,  0,  0,  0])
                outfile.write('\n') 
                msh2d['el_2d'].append(el_2d)
            outfile.close()
    
            # Write material assignment for BECAS 
            outfile = open(os.path.join(path_section, 'EMAT.in'), 'w')
            for elementnumber in becas_elements:
                materialnumber = material_number_of_element[elementnumber]
                tangent = element_tangent[elementnumber]
                # tangents need to be transformed too
                if args.centerline:
                    tangent = np.dot(csys_rot_mat[i],tangent)
                fpa = np.arctan2(tangent[1], tangent[0]) * 180.0/np.pi  # in degree!
                orientation = orientation_of_element[elementnumber]
                outfile.write('%d  %d  %g  %g\n' % (elementnumber, materialnumber, orientation, fpa))
                msh2d['emat'].append([elementnumber, materialnumber, orientation, fpa])
            outfile.close()
    
    
            # Write file with material data for BECAS 
            outfile = open(os.path.join(path_section, 'MATPROPS.in'), 'w')
            sorted_material_numbers = sorted(material_names.keys())
            for material_number in sorted_material_numbers:
                material_name = material_names[material_number]
                prop = material_properties[material_name]
                outfile.write('%14.6e  %14.6e  %14.6e  %14.6e  %14.6e  %14.6e  %g  %g  %g  %14.6e\n' % 
                        ( prop['E1'], prop['E2'], prop['E3'], 
                          prop['G12'], prop['G13'], prop['G23'], 
                          prop['nu12'], prop['nu13'], prop['nu23'],  
                          prop['rho'] ))
                msh2d['matprops'].append([prop['E1'], prop['E2'], prop['E3'], 
                          prop['G12'], prop['G13'], prop['G23'], 
                          prop['nu12'], prop['nu13'], prop['nu23'],  
                          prop['rho']])
            outfile.close()
    
    
            # Write file with strength data for BECAS 
            outfile = open(os.path.join(path_section, 'FAILMAT.in'), 'w')
            for material_number in sorted_material_numbers:
                material_name = material_names[material_number]
                prop = material_properties[material_name]
                # deal with the failure criterion switch:
                becas_fc = 1  # default 
                if material_name.endswith('MAXSTRAIN'): becas_fc = 1
                elif material_name.endswith('MAXSTRESS'): becas_fc = 2
                elif material_name.endswith('TSAIWU'): becas_fc = 3
    
                outfile.write('%d  ' % (becas_fc)) # failure criterion selection flag
                failmat = []
                failmat.append(becas_fc)
                for label in ['Xt' , 'Yt' , 'Yt' , 'S' , 'S' , 'S' , 'Xc' , 'Yc' , 'Yc',  
                              'Xet', 'Yet', 'Yet', 'Se', 'Se', 'Se', 'Xec', 'Yec', 'Yec']:  
                    if label in prop:  # If the value was defined
                        outfile.write('%14.6e ' % (prop[label]))  # Write it
                        failmat.append(prop[label])
                    else:
                        outfile.write('%14.6e ' % (0.0))  # Default is zero!
                        failmat.append(0.0)
                outfile.write('\n')
                msh2d['failmat'].append(failmat)
            outfile.close()
    
            i = i + 1
            
            # make np arrays
            
            msh2d['nl_2d'] = np.array(msh2d['nl_2d']) 
            msh2d['el_2d'] = np.array(msh2d['el_2d']) 
            msh2d['emat']  = np.array(msh2d['emat']) 
            msh2d['matprops'] = np.array(msh2d['matprops']) 
            msh2d['failmat'] = np.array(msh2d['failmat']) 
            shellexp_sections[elset_shell] = msh2d
            
        logfile.close()
    
    status('FINISHED', args.verbose)
    
    return shellexp_sections

def run_shellexpander():

    args = parse_command_line()
    main(args)

if __name__ == '__main__':

    # Parse Command Line
    args = parse_command_line()
    main(args)

