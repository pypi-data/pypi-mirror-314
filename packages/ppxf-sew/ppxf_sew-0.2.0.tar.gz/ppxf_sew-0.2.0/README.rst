
**pPXF-SEW: A full-spectrum fitting method of stellar population Synthesis based on ''Equivalent Widths spectrum'' without attenuation curve prior based on pPXF**

Description
===========

This ``pPXF-SEW`` package contains a Python implementation of the stellar 
population Synthesis based on ``Equivalent Widths spectrum`` (``SEW``) 
method and the Penalized PiXel-Fitting (``pPXF``) method. It uses 
full-spectrum fitting with SED to extract stellar and gas kinematics, 
the stellar population, as well as the dust attenuation curve of stars
and galaxies, without a prior attenuation curve. The kinematics are derived
from the ``pPXF`` method, while the stellar population and attenuation curve
are derived from the ``SEW`` method.

The ``SEW`` method was described in Lu (2025) (in prep.).

The ``pPXF`` method was originally described in `Cappellari & Emsellem (2004)
<https://ui.adsabs.harvard.edu/abs/2004PASP..116..138C>`_
and was substantially upgraded in subsequent years, particularly in
`Cappellari (2017) <https://ui.adsabs.harvard.edu/abs/2017MNRAS.466..798C>`_.

Installation
------------

Install with::

    pip install ppxf-sew

Without write access to the global ``site-packages`` directory, use::

    pip install --user ppxf-sew

To upgrade to the latest version, use::

    pip install --upgrade ppxf-sew

Usage Examples
--------------

To learn how to use the ``pPXF-SEW`` package, run the examples as 
Jupyter Notebooks in the ``ppxf-sew/example`` directory. 
It can be found within the main ``pPXF-SEW`` package installation folder 
inside `site-packages <https://stackoverflow.com/a/46071447>`_.

###########################################################################

License
-------

Other/Proprietary License

Copyright (c) 2024 Jiafeng Lu

This software is provided as is with no warranty. You may use it for
non-commercial purposes and modify it for personal or internal use, as long
as you include this copyright and disclaimer in all copies. You may not
redistribute the code.

