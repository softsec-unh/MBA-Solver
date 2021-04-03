# MBA-Solver Code and Dataset

MBA-Solver is a tool to make MBA expressions easier for SMT solving.

## How to Build

### MBA-Solver

MBA-Solver is written in Python 3.6. It relies on ast, numpy, sympy, astparse
libraries, which can be easily installed by `pip3 install ast numpy astparse
sympy`.

### Solvers and their Python interface
The following solvers are supported. MBA-Solver uses python interface
to communicate with the solvers.

1. Z3: [GitHub Link](https://github.com/Z3Prover/z3)  
   Python interface: `pip3 install z3-solver`
2. Boolector: [GitHub Link](https://github.com/boolector/boolector)  
   Python interface: [Link](https://boolector.github.io/docs/index.html)
3. STP: [Github Link](https://github.com/stp/stp)  
   Python interface: [Link](https://stp.readthedocs.io/en/latest/#python-usage)

## Source Files
1. tools/svector_simplify.py: simplify linear MBA sub-expression
2. tools/truthtable_search_simplify.py: simplify poly MBA sub-expression
3. mba-simplifier/pldi_dataset_simplify_*.py: split MBA expression and apply the corresponding simplification (linear, poly, nonpoly) to them.

## Step-by-Step Instructions
### Dataset
The folder "full-dataset" contains the compete dataset: 1000 linear MBA expression, 1000 poly MBA expression, and 1000 nonpoly MBA expression.

To facilitate the artifact evaluation, the folder "dataset" include a sub-dataset: 21 linear MBA expression, 21 poly MBA expression, and 20 nonpoly MBA expression.

If you would like to run on the full-dataset, please rename "full-dataset" to "dataset".

### Quick Demo

Run `make quick-demo` will first use Z3 to solve the original MBA, then use MBA-Solver to simplify them, and then use Z3 to solve the simplified MBA.

### Simplify MBA

Run MBA-Solver: `make mba-solver-simplify-mba`.

Functions for analyzing and manipulating MBA expressions are in the "tools" folder. The simplification results are stored in the "dataset" folder.

## SMT Solving

Each script will print out the number of correctly simplified cases (True), incorrectly simplified cases (False), Timeout cases and total number.

### Timeout

The timeout can be configured at the beginning of the makefiles under boolector_solving, stp_solving, and z3_solving. The default timeout is set to 5 seconds for quick evaluation. The evaluation in our paper is set to one hour. Please note that, running with shorter timeout may reduce the ratio of solved cases in peer tools.

### Z3
1. Solve original MBA: `make z3-solving-original`.
2. Solve MBA after simplification by MBA-Solver: `make z3-solving-mba-solver-simplify`.
3. Solve MBA after simplification by SSPAM: `make z3-solving-sspam-simplify`.
4. Solve MBA after simplification by Syntia: `make z3-solving-syntia-simplify`.

Run `make z3` will run these four experiments in a batch.

### Boolector
1. Solve original MBA: `make boolector-solving-original`.
2. Solve MBA after simplification by MBA-Solver: `make boolector-solving-mba-solver-simplify`.
3. Solve MBA after simplification by SSPAM: `make boolector-solving-sspam-simplify`.
4. Solve MBA after simplification by Syntia: `make boolector-solving-syntia-simplify`.

Run `make boolector` will run these four experiments in a batch.

### STP
1. Solve original MBA: `make stp-solving-original`.
2. Solve MBA after simplification by MBA-Solver: `make stp-solving-mba-solver-simplify`.
3. Solve MBA after simplification by SSPAM: `make stp-solving-sspam-simplify`.
4. Solve MBA after simplification by Syntia: `make stp-solving-syntia-simplify`.

Run `make stp` will run these four experiments in a batch.

## Peer tools

1. SSPAM: [GitHub Link](https://github.com/quarkslab/sspam/blob/master/README.md).
2. Syntia: [GitHub link](https://github.com/RUB-SysSec/syntia/blob/master/README.md).

Running peer tools may take around 18 hours on the subset. To save time, we have already include the simplified result from these tools. So you do not have to run the commands in this section.

Run SSPAM on MBA dataset: `make sspam-simplify-mba`.

Run Syntia on MBA dataset: `make syntia-simplify-mba`.
