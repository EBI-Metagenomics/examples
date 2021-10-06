# Microbiome Informatics - API and service usage examples

The MGnify REST API [https://www.ebi.ac.uk/metagenomics/api/latest/](https://www.ebi.ac.uk/metagenomics/api/latest/) provides an easy-to-use set of top level resources, such as studies, samples, runs, experiment-types, biomes and annotations, that let user access metagenomics data in [JSON format](https://en.wikipedia.org/wiki/JSON) (JSON is an standard format for data interchange and file format). Retrieving the data is as simple as sending an HTTP request. The API return JSON objects with a defined schema that contains the resource type, associated object identifier (id) and a set of attributes. Where appropriate, relationships and links are provided to other resources.

We have utilized an interactive documentation framework ([Swagger UI](https://swagger.io/tools/swagger-ui/)) to visualize and simplify interaction with the API’s resources via an HTML interface. Detailed explanations of the purpose of all resources, along with many examples, are provided to guide end-users. Documentation on how to use the endpoints is available at [https://www.ebi.ac.uk/metagenomics/api/docs/](https://www.ebi.ac.uk/metagenomics/api/docs/).

We also have [general documentation for the MGnify resource](https://emg-docs.readthedocs.io) as a whole.

## Quick start
### Online examples in RStudio, for users of [R](https://www.r-project.org) 
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/EBI-metagenomics/examples/binder?urlpath=rstudio)

### Online examples in Jupyter, for users of [Python](https://www.python.org)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/EBI-metagenomics/examples/binder)

## Repo structure

This repo contains MGnify API examples and [ENA](https://www.ebi.ac.uk/ena) examples. 

### MGnify

Please refer to [mgnify/README.md](mgnify/README.md)

### ENA

Please refer to [ena/README.md](ena/README.md)

Contributors
============

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/olatarkowska"><img src="https://avatars3.githubusercontent.com/u/1065155?v=4" width="100px;" alt=""/><br /><sub><b>Ola Tarkowska</b></sub></a><br /><a href="https://github.com/EBI-Metagenomics/emg-toolkit/commits?author=olatarkowska" title="Code">💻</a><a href="https://github.com/EBI-Metagenomics/EMG-docs/commits/master?author=olatarkowska">📖</a></td>
    <td align="center"><a href="https://github.com/mberacochea"><img src="https://avatars3.githubusercontent.com/u/1123897?v=4" width="100px;" alt=""/><br /><sub><b>Martin Beracochea</b></sub></a><br /><a href="https://github.com/EBI-Metagenomics/emg-toolkit/commits?author=mberacochea" title="Code">💻</a></td>
  </tr>
</table>

<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!

Contact
=======

If the documentation do not answer your questions, please [contact us](https://www.ebi.ac.uk/support/metagenomics).