import glob
import cdf2vtk as cdk

#Liste des fichiers à transformer
files = glob.glob('../010_mesonh/EXPNAM.ndom.SEGNAM.*[!000].nc')
#[!000] pour ignorer le premier fichier non lisible
#Liste des variables
var = ['THT','UT','VT','WT']
#Champs 3D
cdk.field2vtk(files,var)
#Modele de terrain
cdk.MNT(files[0])
