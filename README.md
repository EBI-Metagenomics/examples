# Microbiome Informatics - API and service usage examples

The MGnify REST API [https://www.ebi.ac.uk/metagenomics/api/latest/](https://www.ebi.ac.uk/metagenomics/api/latest/) provides an easy-to-use set of top level resources, such as studies, samples, runs, experiment-types, biomes and annotations, that let user access metagenomics data in [JSON format](https://en.wikipedia.org/wiki/JSON) (JSON is an standard format for data interchange and file format). Retrieving the data is as simple as sending an HTTP request. The API return JSON objects with a defined schema that contains the resource type, associated object identifier (id) and a set of attributes. Where appropriate, relationships and links are provided to other resources.

We have utilized an interactive documentation framework ([Swagger UI](https://swagger.io/tools/swagger-ui/)) to visualize and simplify interaction with the API’s resources via an HTML interface. Detailed explanations of the purpose of all resources, along with many examples, are provided to guide end-users. Documentation on how to use the endpoints is available at [https://www.ebi.ac.uk/metagenomics/api/docs/](https://www.ebi.ac.uk/metagenomics/api/docs/).

## Repo structure

This repo contains MGnify API examples and [ENA](https://www.ebi.ac.uk/ena) examples. 

### MGnify

Please refer to [mgnify/README.md](mgnify/README.md)

### ENA

Please refer to [ena/README.md](ena/README.md)