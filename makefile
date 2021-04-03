quick-demo: z3-solving-original mba-solver-simplify-mba z3-solving-mba-solver-simplify

boolector: boolector-solving-original boolector-solving-mba-solver-simplify boolector-solving-sspam-simplify boolector-solving-syntia-simplify

stp: stp-solving-original stp-solving-mba-solver-simplify stp-solving-sspam-simplify stp-solving-syntia-simplify

z3: z3-solving-original z3-solving-mba-solver-simplify z3-solving-sspam-simplify z3-solving-syntia-simplify

boolector-solving-original:
	@cd boolector_solving && make boolector-solving-before-simplify
boolector-solving-mba-solver-simplify:
	@cd boolector_solving && make boolector-solving-mba-solver
boolector-solving-sspam-simplify:
	@cd boolector_solving && make boolector-solving-sspam
boolector-solving-syntia-simplify:
	@cd boolector_solving && make boolector-solving-syntia

stp-solving-original:
	@cd stp_solving && make stp-solving-before-simplify
stp-solving-mba-solver-simplify:
	@cd stp_solving && make stp-solving-mba-solver
stp-solving-sspam-simplify:
	@cd stp_solving && make stp-solving-sspam
stp-solving-syntia-simplify:
	@cd stp_solving && make stp-solving-syntia

z3-solving-original:
	@cd z3_solving && make z3-solving-before-simplify
z3-solving-mba-solver-simplify:
	@cd z3_solving && make z3-solving-mba-solver
z3-solving-sspam-simplify:
	@cd z3_solving && make z3-solving-sspam
z3-solving-syntia-simplify:
	@cd z3_solving && make z3-solving-syntia

mba-solver-simplify-mba:
	@cd ./mba-simplifier && make mba-solver-simplify

sspam-simplify-mba:
	@cd ./sspam && make sspam-simplify

syntia-simplify-mba:
	@cd ./syntia && make syntia-simplify
