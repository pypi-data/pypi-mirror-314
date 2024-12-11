# nsys2prv: Translate NVIDIA Nsight Systems traces to Paraver traces

_nsys2prv_ is a Python package that parses and interprets the exported data of an NVIDIA Nsight Systems[^1] trace and converts it to Paraver semantics in order to browse the trace with Paraver.  Paraver is a tool by the Performance Tools team at BSC, and is a parallel trace visualization system allowing for large scale trace execution analysis. Paraver can be obtained at [https://tools.bsc.es/downloads](https://tools.bsc.es/downloads).

The Nsight Systems traces should include GPU kernel activity, and also translate information about CUDA runtime, OpenACC constructs, MPI runtime, GPU metrics and NVTX regions. It supports reports of multiple processes and threads, but right now it still does not support merging multiple reports into one trace.

## How it works
This tool relies on the export functionality of `nsys`. The data collection consists of a mix of the `nsys stats` predefined scripts, and a manual parsing of the _.sqlite_ exported format data.  The following figure summarizes the translation workflow:
![translation workflow](docs/translate-workflow.png)

More details on the workflow and the data parsing logic can be read on the [wiki pages](https://pm.bsc.es/gitlab/beppp/nsys2prv/-/wikis/Home).

## Installation

_nsys2prv_ is distributed as a PyPI package and thus can be installed with `pip`. The following requirements for the package to work will be installed automatically by `pip`:
- python > 3.11
- pandas > 2.2.2
- sqlalchemy
- tqdm

Additionally, it requires an installation of NIDIA Nsight Systems in your _PATH_ to extract the data. Alternatively, you can set the NSYS_HOME environment variable.  It is required that the version of Nsight Systems is always greater than the one used to obtain the trace. It is recommended at least the version 23.11.

To install the package just use `pip` globally or create a vitual environment:
```bash
pip install --global nsys2prv
# or
python -m venv ./venv
source ./venv/bin/activate
pip install nsys2prv
```

## Basic usage
To translate a trace from Nsight Systems you need the _.nsys-rep_ report file that `nsys profile` outputs. This serves as input to `nsys2prv`.
```bash
nsys2prv -t what,to,translate source.nsys-rep output-prv-name
```

Currently, the translator needs that the user manually specifies the different programming models information to translate using the `--trace,-t` flag. By default it always extracts kernel execution information, so it is mandatory that the nsys report contains GPU activity. Future releases will automatically detect the information that is available in the report and make this flag optional.  The accepted value for the flag is a comma-separated list with any of the following categories:  
- `cuda_api_trace`: CUDA API calls
- `nvtx_pushpop_trace`: The developer defined NVTX Push/Pop regions
- `nvtx_startend_trace`: The developer defined NTXT Start/End regions
- `gpu_metrics`: The sampling events of hardware metrics for the GPUs
- `mpi_event_trace`: The MPI calls
- `openacc`: The OpenACC constructs

Finally, the `output-prv-name.prv` trace can be opened with Paraver and analyzed.

## Further documentation
For documentation about trace analysis and config files (CFGs) provided, please refer to the [wiki pages](https://pm.bsc.es/gitlab/beppp/nsys2prv/-/wikis/Home).

## Bug reporting and contribution
A list of the current bugs and features targeted can be seen in the GitLab repository. The project is still currently under initial development and is expecting a major code refactoring and changes in the command line interface (CLI).  As it is a tool to support and enable performance analysts' work, new use cases or petitions for other programming model information support are always welcomed. Please contact marc.clasca@bsc.es or beppp@bsc.es for any of those requests, recommendations, or contribution ideas.


[^1]: https://developer.nvidia.com/nsight-systems