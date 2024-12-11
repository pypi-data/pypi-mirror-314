# STM Reader
This is an example of STS (STS reader) in NOMAD. The prime purpose of the reader is to transform data from measurement files into community-defined concepts constructed by the SPM community which allows experimentalists to store, organize, search, analyze, and share experimental data (only within the [NOMAD](https://nomad-lab.eu/nomad-lab/) platform) among the scientific communities. The reader builds on the [NXsts](https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsts.html#nxsts) application definition and needs an experimental file, (here you do not need a config file, a typical mapping strutcture between the application concepts and raw data structure, and use the default config file provided by reader if raw file has the same structure as Generic 5e, Generic 4.5) and a eln file to transform the experimental data into the [NXsts](https://fairmat-nfdi.github.io/nexus_definitions/classes/contributed_definitions/NXsts.html#nxsts) application concepts.

## Supported File Formats and File Versions

- Can parse Scanning Tunneling Spectroscopy (STS) from
    - `.dat` file format from Nanonis:
        - Versions: Generic 5e, Generic 4.5