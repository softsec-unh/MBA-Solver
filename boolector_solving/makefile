timeout = 5

boolector-linear-before-simplify:
	python2 boolector_check_before_simplify.py ../dataset/pldi_dataset_linear_MBA.txt $(timeout)

boolector-poly-before-simplify:
	python2 boolector_check_before_simplify.py ../dataset/pldi_dataset_poly_MBA.txt $(timeout)

boolector-nonpoly-before-simplify:
	python2 boolector_check_before_simplify.py ../dataset/pldi_dataset_nonpoly_MBA.txt $(timeout)

boolector-linear-after-simplify:
	python2 boolector_check_after_simplify.py ../dataset/pldi_dataset_linear_MBA.txt.simplify.txt $(timeout)

boolector-poly-after-simplify:
	python2 boolector_check_after_simplify.py ../dataset/pldi_dataset_poly_MBA.txt.simplify.txt $(timeout)

boolector-nonpoly-after-simplify:
	python2 boolector_check_after_simplify.py ../dataset/pldi_dataset_nonpoly_MBA.txt.simplify.txt $(timeout)

boolector-linear-after-simplify-sspam:
	python2 boolector_check_after_simplify_peertools.py ../sspam/linear.MBA.SSPAM.result.txt $(timeout)

boolector-poly-after-simplify-sspam:
	python2 boolector_check_after_simplify_peertools.py ../sspam/poly.MBA.SSPAM.result.txt $(timeout)

boolector-nonpoly-after-simplify-sspam:
	python2 boolector_check_after_simplify_peertools.py ../sspam/nonpoly.MBA.SSPAM.result.txt $(timeout)

boolector-linear-after-simplify-syntia:
	python2 boolector_check_after_simplify_peertools.py ../syntia/linear.64bit.result.txt $(timeout)

boolector-poly-after-simplify-syntia:
	python2 boolector_check_after_simplify_peertools.py ../syntia/poly.64bit.result.txt $(timeout)

boolector-nonpoly-after-simplify-syntia:
	python2 boolector_check_after_simplify_peertools.py ../syntia/nonpoly.64bit.result.txt $(timeout)

boolector-solving-before-simplify-total:
	python3 total.py boolector 0
boolector-solving-before-simplify:
	@echo "--------------------boolector solving linear MBA samples-------------------------"
	@make boolector-linear-before-simplify
	@echo "--------------------boolector solving linear MBA samples completion--------------"
	@echo "--------------------boolector solving poly MBA samples---------------------------"
	@make boolector-poly-before-simplify
	@echo "--------------------boolector solving poly MBA samples completion----------------"
	@echo "--------------------boolector solving nonpoly MBA samples------------------------"
	@make boolector-nonpoly-before-simplify
	@echo "--------------------boolector solving nonpoly MBA samples completion-------------"
	@echo "--------------------boolector solving MBA samples before simplification-------------"
	@make boolector-solving-before-simplify-total

boolector-solving-mba-solver-total:
	python3 total.py boolector 1 mba
boolector-solving-mba-solver:
	@echo "--------------------boolector solving linear MBA samples after MBA-Solver simplification--------------------------"
	@make boolector-linear-after-simplify
	@echo "--------------------boolector solving linear MBA samples after MBA-Solver simplification completion---------------"
	@echo "--------------------boolector solving poly MBA samples after MBA-Solver simplification----------------------------"
	@make boolector-poly-after-simplify
	@echo "--------------------boolector solving poly MBA samples after MBA-Solver simplification completion-----------------"
	@echo "--------------------boolector solving nonpoly MBA samples after MBA-Solver simplification-------------------------"
	@make boolector-nonpoly-after-simplify
	@echo "--------------------boolector solving nonpoly MBA samples after MBA-Solver simplification completion--------------"
	@echo "--------------------boolector solving MBA samples after MBA-Solver simplification --------------"
	@make boolector-solving-mba-solver-total

boolector-solving-sspam-total:
	python3 total.py boolector 1 sspam
boolector-solving-sspam:
	@echo "--------------------boolector solving linear MBA samples after SSPAM simplification--------------------------"
	@make boolector-linear-after-simplify-sspam
	@echo "--------------------boolector solving linear MBA samples after SSPAM simplification completion---------------"
	@echo "--------------------boolector solving poly MBA samples after SSPAM simplification----------------------------"
	@make boolector-poly-after-simplify-sspam
	@echo "--------------------boolector solving poly MBA samples after SSPAM simplification completion-----------------"
	@echo "--------------------boolector solving nonpoly MBA samples after SSPAM simplification-------------------------"
	@make boolector-nonpoly-after-simplify-sspam
	@echo "--------------------boolector solving nonpoly MBA samples after SSPAM simplification completion--------------"
	@echo "--------------------boolector solving MBA samples after SSPAM simplification --------------"
	@make boolector-solving-sspam-total

boolector-solving-syntia-total:
	python3 total.py boolector 1 syntia
boolector-solving-syntia:
	@echo "--------------------boolector solving linear MBA samples after Syntia simplification--------------------------"
	@make boolector-linear-after-simplify-syntia
	@echo "--------------------boolector solving linear MBA samples after Syntia simplification completion---------------"
	@echo "--------------------boolector solving poly MBA samples after Syntia simplification----------------------------"
	@make boolector-poly-after-simplify-syntia
	@echo "--------------------boolector solving poly MBA samples after Syntia simplification completion-----------------"
	@echo "--------------------boolector solving nonpoly MBA samples after Syntia simplification-------------------------"
	@make boolector-nonpoly-after-simplify-syntia
	@echo "--------------------boolector solving nonpoly MBA samples after Syntia simplification completion--------------"
	@echo "--------------------boolector solving MBA samples after Syntia simplification --------------"
	@make boolector-solving-syntia-total
