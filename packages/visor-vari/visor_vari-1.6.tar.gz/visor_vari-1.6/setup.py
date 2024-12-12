
from setuptools import setup

with open("README.rst", "r", encoding="utf-8") as hoja:
    long_description = hoja.read()

setup(
        name= "visor_vari",
        version= "1.6",
        author= "El Señor es el único eterno. Que la ciencia lo honre a Él.",
        author_email= "from.colombia.to.all@gmail.com",

        description= "Permite la visualización de grandes conjuntos de datos en sistemas (software) complejos",
        long_description=long_description,
        long_description_content_type="text/x-rst",
        
        license="Mozilla Public License 2.0 (MPL 2.0)",
        license_files=("license.txt",),
        
        packages= ["visor_vari", "visor_vari.readme_visor"],
        
        package_data={
            '': ['license.txt'],
        },
        include_package_data= True,
        #url="https://github.com/Metal-Alcyone-zero/",
        classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        ],
        
        python_requires= ">=3.11.3"
        #install_requires=['Tkinter'],
)

