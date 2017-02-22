#!/usr/bin/env python

import __main__
__main__.pymol_argv = [ 'pymol', '-qc'] # Quiet and no GUI

from optparse import OptionParser
from os import system, listdir, path
import zipfile

import pymol


def runBlender(pwrml, pout):

    cmd = "blender --background --python command3D.py -- " + str(pwrml) + " " + str(pout)
    print "run blender"
    print cmd
    system(cmd)

    lfilout = [path.dirname(pout) + "/" + i for i in listdir(path.dirname(pout))]
    #print lfilout

    ppng = pout + ".png"
    pobj = pout + ".obj"
    pmtl = pout + ".mtl"

    if not ppng in lfilout or not pobj in lfilout or not pmtl in lfilout:
        print "ERROR -> BLENDER CONVERSION - Check the WRML file"
        return []

    else:
        pzip = pout + ".zip"
        zipmodel = zipfile.ZipFile(pzip, "w")
        zipmodel.write(ppng, arcname=ppng.split("/")[-1])
        zipmodel.write(pobj, arcname=pobj.split("/")[-1])
        zipmodel.write(pmtl, arcname=pmtl.split("/")[-1])
        zipmodel.close()

        return [pobj, pmtl, ppng, pzip]



def PDBtoWRL(pfilinPDB, pseopt = 1):

    pfilinWRL = pfilinPDB[:-4] + ".wrl"

    pymol.finish_launching()

    pymol.cmd.load(pfilinPDB, "lig")
    pymol.cmd.hide(representation="line")
    pymol.cmd.show(representation="stick")
    pymol.cmd.set("valence", 1)
    pymol.cmd.set("stick_quality", 500)
    pymol.cmd.color("cyan", "elem c")
    pymol.cmd.save(pfilinWRL)
    if pseopt == 1:
        pymol.cmd.save(pfilinPDB[:-4] + ".pse")

    pymol.cmd.quit()


    return pfilinWRL




def main():
    #arg_protein
    use = "%prog [-i file .pdb or .sdf] [-w file in wrml] [-o path out name] [-h help]\n\n" \
          "Dependencies: \n" \
          "- Blender 2.76\n" \
          "- pymol 1.7.x\n" \
          "\n\n" \
          "Exemples:\n" \
          "1. With wrl file\n" \
          "- ./main.py -w myfile.wrl -o model3D\n\n" \
          "2. With a sdf or a pdb file\n" \
          "./main.py -i myligand.sdf -o model3D\n" \
          "./main.py -i myligand.pdb -o model3D\n"
    parser = OptionParser(usage=use)


    parser.add_option("-i","--input", dest="pfilin", default="0", help="File of structure in .pdb or .sdf format")
    parser.add_option("-w","--wrl", dest="pwrl", default="0", help="wrl file only for model conversion")
    parser.add_option("-o","--output", dest="pout", default="0", help="Name and path for output 3D object")

    (options, args) = parser.parse_args()

    pfilin = options.pfilin
    pwrl = options.pwrl
    pout = options.pout
    #dependancy = options.dependancy

    if pout == "0":
        print "ERROR -> Use a correct output file"
        return

    # case if WRML is im input
    if pwrl != "0":
        lfilout = runBlender(pwrl, pout)
        if len(lfilout) == 4:
            print "Model 3D is generated -> " + lfilout[-1]
            return
        else:
            print "ERROR -> No model 3D generated, please check your input files and paths"

    elif pfilin != "0":
        print pfilin

        filetype = path.splitext(pfilin)[1]
        print filetype
        if filetype != ".sdf" and filetype != ".pdb":
            print "ERROR -> File type in input not supported, please use pdb or sdf format"
            return
        #elif filetype == "sdf":
        #    cmdconvert = "babel " + pfilin + " " + pfilin[:-4] + "pdb"
        #    system(cmdconvert)
        #    pfilin = pfilin[:-4] + "pdb"

        # convert PDB to WRL
        pwrl = PDBtoWRL(pfilin)
        lfilout = runBlender(pwrl, pout)
        if len(lfilout) == 4:
            print "Model 3D is generated -> " + lfilout[-1]
            return
        else:
            print "ERROR -> No model 3D generated, please check your input files and paths"


main()


#PDBtoWRL("/home/aborrel/3D_model/lig.pdb")


