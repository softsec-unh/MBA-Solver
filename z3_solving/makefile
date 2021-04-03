timeout = 5

z3-linear-before-simplify:
	python3 z3_check_before_simplify.py ../dataset/pldi_dataset_linear_MBA.txt $(timeout)

z3-poly-before-simplify:
	python3 z3_check_before_simplify.py ../dataset/pldi_dataset_poly_MBA.txt $(timeout)

z3-nonpoly-before-simplify:
	python3 z3_check_before_simplify.py ../dataset/pldi_dataset_nonpoly_MBA.txt $(timeout)

z3-linear-after-simplify:
	python3 z3_check_after_simplify.py ../dataset/pldi_dataset_linear_MBA.txt.simplify.txt $(timeout)

z3-poly-after-simplify:
	python3 z3_check_after_simplify.py ../dataset/pldi_dataset_poly_MBA.txt.simplify.txt $(timeout)

z3-nonpoly-after-simplify:
	python3 z3_check_after_simplify.py ../dataset/pldi_dataset_nonpoly_MBA.txt.simplify.txt $(timeout)

z3-linear-after-simplify-sspam:
	python3 z3_check_after_simplify_peertools.py ../sspam/linear.MBA.SSPAM.result.txt $(timeout)

z3-poly-after-simplify-sspam:
	python3 z3_check_after_simplify_peertools.py ../sspam/poly.MBA.SSPAM.result.txt $(timeout)

z3-nonpoly-after-simplify-sspam:
	python3 z3_check_after_simplify_peertools.py ../sspam/nonpoly.MBA.SSPAM.result.txt $(timeout)

z3-linear-after-simplify-syntia:
	python3 z3_check_after_simplify_peertools.py ../syntia/linear.64bit.result.txt $(timeout)

z3-poly-after-simplify-syntia:
	python3 z3_check_after_simplify_peertools.py ../syntia/poly.64bit.result.txt $(timeout)

z3-nonpoly-after-simplify-syntia:
	python3 z3_check_after_simplify_peertools.py ../syntia/nonpoly.64bit.result.txt $(timeout)

z3-solving-before-simplify-total:
	python3 total.py z3 0
z3-solving-before-simplify:
	@echo "--------------------z3 solving linear MBA samples-------------------------"
	@make z3-linear-before-simplify
	@echo "--------------------z3 solving linear MBA samples completion--------------"
	@echo "--------------------z3 solving poly MBA samples---------------------------"
	@make z3-poly-before-simplify
	@echo "--------------------z3 solving poly MBA samples completion----------------"
	@echo "--------------------z3 solving nonpoly MBA samples------------------------"
	@make z3-nonpoly-before-simplify
	@echo "--------------------z3 solving nonpoly MBA samples completion-------------"
	@echo "--------------------z3 solving MBA samples -------------------------------"
	@make z3-solving-before-simplify-total

z3-solving-mba-solver-total:
	python3 total.py z3 1 mba
z3-solving-mba-solver:
	@echo "--------------------z3 solving linear MBA samples after MBA-Solver simplification--------------------------"
	@make z3-linear-after-simplify
	@echo "--------------------z3 solving linear MBA samples after MBA-Solver simplification completion---------------"
	@echo "--------------------z3 solving poly MBA samples after MBA-Solver simplification----------------------------"
	@make z3-poly-after-simplify
	@echo "--------------------z3 solving poly MBA samples after MBA-Solver simplification completion-----------------"
	@echo "--------------------z3 solving nonpoly MBA samples after MBA-Solver simplification-------------------------"
	@make z3-nonpoly-after-simplify
	@echo "--------------------z3 solving nonpoly MBA samples after MBA-Solver simplification completion--------------"
	@echo "--------------------z3 solving MBA samples after MBA-Solver simplification --------------"
	@make z3-solving-mba-solver-total

z3-solving-sspam-total:
	python3 total.py z3 1 sspam
z3-solving-sspam:
	@echo "--------------------z3 solving linear MBA samples after SSPAM simplification--------------------------"
	@make z3-linear-after-simplify-sspam
	@echo "--------------------z3 solving linear MBA samples after SSPAM simplification completion---------------"
	@echo "--------------------z3 solving poly MBA samples after SSPAM simplification----------------------------"
	@make z3-poly-after-simplify-sspam
	@echo "--------------------z3 solving poly MBA samples after SSPAM simplification completion-----------------"
	@echo "--------------------z3 solving nonpoly MBA samples after SSPAM simplification-------------------------"
	@make z3-nonpoly-after-simplify-sspam
	@echo "--------------------z3 solving nonpoly MBA samples after SSPAM simplification completion--------------"
	@echo "--------------------z3 solving MBA samples after SSPAM simplification --------------"
	@make z3-solving-sspam-total

z3-solving-syntia-total:
	python3 total.py z3 1 syntia
z3-solving-syntia:
	@echo "--------------------z3 solving linear MBA samples after Syntia simplification--------------------------"
	@make z3-linear-after-simplify-syntia
	@echo "--------------------z3 solving linear MBA samples after Syntia simplification completion---------------"
	@echo "--------------------z3 solving poly MBA samples after Syntia simplification----------------------------"
	@make z3-poly-after-simplify-syntia
	@echo "--------------------z3 solving poly MBA samples after Syntia simplification completion-----------------"
	@echo "--------------------z3 solving nonpoly MBA samples after Syntia simplification-------------------------"
	@make z3-nonpoly-after-simplify-syntia
	@echo "--------------------z3 solving nonpoly MBA samples after Syntia simplification completion--------------"
	@echo "--------------------z3 solving MBA samples after Syntia simplification--------------"
	@make z3-solving-syntia-total
