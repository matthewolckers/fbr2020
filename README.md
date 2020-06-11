# Friend-based Ranking

Analysis of social networks and simulations for [Friend-based Ranking](https://arxiv.org/pdf/1807.05093.pdf), a paper by [Francis Bloch](https://www.sites.google.com/site/francisbloch1/) and [Matthew Olckers](https://www.matthewolckers.com/).

Code is written in Python using Jupyter Notebooks and is executed in three steps:


`extract_networks.ipynb`

Extract the network data from India ([Banerjee et al, 2013](https://doi.org/10.7910/DVN/U3BIHX)) and Indonesia ([Alatas et al, 2020](http://doi.org/10.3886/E119802V1)) and calculate various network statistics. 

`figures.ipynb`

Produce figures from the network data and save the figures as PDFs.

`homophily.ipynb`

The homophily simulation and figure does not rely on the network data and is calculated in a separate notebook.

Each notebook is available as an html and PDF file to view the correct output of the code. You may also interact with the code online using [Binder](https://mybinder.org/).

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/matthewolckers/fbr2020/master)


## References

Banerjee, Abhijit; Chandrasekhar, Arun G.; Duflo, Esther; Jackson, Matthew O., 2013, "The Diffusion of Microfinance", https://doi.org/10.7910/DVN/U3BIHX, Harvard Dataverse, V9.

Alatas, Vivi, Banerjee, Abhijit, Chandrasekhar, Arun, Hanna, Rema, and Olken, Benjamin. Data and Code for: Network Structure and the Aggregation of Information: Theory and Evidence from Indonesia. Nashville, TN: American Economic Association [publisher], 2020. Ann Arbor, MI: Inter-university Consortium for Political and Social Research [distributor], 2020-06-08. https://doi.org/10.3886/E119802V1
