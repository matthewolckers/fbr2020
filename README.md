# Friend-based Ranking

Analysis of social networks and simulations for [Friend-based Ranking](https://arxiv.org/pdf/1807.05093.pdf), a paper by [Francis Bloch](https://www.sites.google.com/site/francisbloch1/) and [Matthew Olckers](https://www.matthewolckers.com/).

Code is written in Python using Jupyter Notebooks and is executed in three steps:


`extract_networks.ipynb` 

Extract the network data from India ([Banerjee et al, 2013](https://dataverse.harvard.edu/dataset.xhtml?persistentId=hdl:1902.1/21538)) and Indonesia ([Alatas et al, 2016](https://www.aeaweb.org/articles?id=10.1257/aer.20140705)) and calculate various network statistics. 

`figures.ipynb` 

Produce figures from the network data and save the figures as PDFs.

`homophily.ipynb` 

The homophily simulation and figure does not rely on the network data and is calculated in a separate notebook.

Each notebook is available as an html and PDF file to view the correct output of the code. You may also interact with the code online using [Binder](https://mybinder.org/).

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/matthewolckers/fbr2020/master)


## References

Banerjee, Abhijit; Chandrasekhar, Arun G.; Duflo, Esther; Jackson, Matthew O., 2013, "The Diffusion of Microfinance", https://doi.org/10.7910/DVN/U3BIHX, Harvard Dataverse, V9

Alatas, Vivi, Abhijit Banerjee, Arun G. Chandrasekhar, Rema Hanna, and Benjamin A. Olken. 2016. "Network Structure and the Aggregation of Information: Theory and Evidence from Indonesia." American Economic Review, 106 (7): 1663-1704. https://www.aeaweb.org/articles?id=10.1257/aer.20140705

