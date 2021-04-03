timeout = 5

stp-linear-before-simplify:
	python2 stp_check_before_simplify.py ../dataset/pldi_dataset_linear_MBA.txt $(timeout)

stp-poly-before-simplify:
	python2 stp_check_before_simplify.py ../dataset/pldi_dataset_poly_MBA.txt $(timeout)

stp-nonpoly-before-simplify:
	python2 stp_check_before_simplify.py ../dataset/pldi_dataset_nonpoly_MBA.txt $(timeout)

stp-linear-after-simplify:
	python2 stp_check_after_simplify.py ../dataset/pldi_dataset_linear_MBA.txt.simplify.txt $(timeout)

stp-poly-after-simplify:
	python2 stp_check_after_simplify.py ../dataset/pldi_dataset_poly_MBA.txt.simplify.txt $(timeout)

stp-nonpoly-after-simplify:
	python2 stp_check_after_simplify.py ../dataset/pldi_dataset_nonpoly_MBA.txt.simplify.txt $(timeout)

stp-linear-after-simplify-sspam:
	python2 stp_check_after_simplify_peertools.py ../sspam/linear.MBA.SSPAM.result.txt $(timeout)

stp-poly-after-simplify-sspam:
	python2 stp_check_after_simplify_peertools.py ../sspam/poly.MBA.SSPAM.result.txt $(timeout)

stp-nonpoly-after-simplify-sspam:
	python2 stp_check_after_simplify_peertools.py ../sspam/nonpoly.MBA.SSPAM.result.txt $(timeout)

stp-linear-after-simplify-syntia:
	python2 stp_check_after_simplify_peertools.py ../syntia/linear.64bit.result.txt $(timeout)

stp-poly-after-simplify-syntia:
	python2 stp_check_after_simplify_peertools.py ../syntia/poly.64bit.result.txt $(timeout)

stp-nonpoly-after-simplify-syntia:
	python2 stp_check_after_simplify_peertools.py ../syntia/nonpoly.64bit.result.txt $(timeout)


stp-solving-before-simplify-total:
	python3 total.py stp 0
stp-solving-before-simplify:
	@echo "--------------------stp solving linear MBA samples-------------------------"
	@make stp-linear-before-simplify
	@echo "--------------------stp solving linear MBA samples completion--------------"
	@echo "--------------------stp solving poly MBA samples---------------------------"
	@make stp-poly-before-simplify
	@echo "--------------------stp solving poly MBA samples completion----------------"
	@echo "--------------------stp solving nonpoly MBA samples------------------------"
	@make stp-nonpoly-before-simplify
	@echo "--------------------stp solving nonpoly MBA samples completion-------------"
	@echo "--------------------stp solving MBA samples before simplification-------------"
	@make stp-solving-before-simplify-total

stp-solving-mba-solver-total:
	python3 total.py stp 1 mba
stp-solving-mba-solver:
	@echo "--------------------stp solving linear MBA samples after MBA-Solver simplification--------------------------"
	@make stp-linear-after-simplify
	@echo "--------------------stp solving linear MBA samples after MBA-Solver simplification completion---------------"
	@echo "--------------------stp solving poly MBA samples after MBA-Solver simplification----------------------------"
	@make stp-poly-after-simplify
	@echo "--------------------stp solving poly MBA samples after MBA-Solver simplification completion-----------------"
	@echo "--------------------stp solving nonpoly MBA samples after MBA-Solver simplification-------------------------"
	@make stp-nonpoly-after-simplify
	@echo "--------------------stp solving nonpoly MBA samples after MBA-Solver simplification completion--------------"
	@echo "--------------------stp solving MBA samples after MBA-Solver simplification --------------"
	@make stp-solving-mba-solver-total

stp-solving-sspam-total:
	python3 total.py stp 1 sspam
stp-solving-sspam:
	@echo "--------------------stp solving linear MBA samples after SSPAM simplification--------------------------"
	@make stp-linear-after-simplify-sspam
	@echo "--------------------stp solving linear MBA samples after SSPAM simplification completion---------------"
	@echo "--------------------stp solving poly MBA samples after SSPAM simplification----------------------------"
	@make stp-poly-after-simplify-sspam
	@echo "--------------------stp solving poly MBA samples after SSPAM simplification completion-----------------"
	@echo "--------------------stp solving nonpoly MBA samples after SSPAM simplification-------------------------"
	@make stp-nonpoly-after-simplify-sspam
	@echo "--------------------stp solving nonpoly MBA samples after SSPAM simplification completion--------------"
	@echo "--------------------stp solving MBA samples after SSPAM simplification --------------"
	@make stp-solving-sspam-total

stp-solving-syntia-total:
	python3 total.py stp 1 syntia
stp-solving-syntia:
	@echo "--------------------stp solving linear MBA samples after Syntia simplification--------------------------"
	@make stp-linear-after-simplify-syntia
	@echo "--------------------stp solving linear MBA samples after Syntia simplification completion---------------"
	@echo "--------------------stp solving poly MBA samples after Syntia simplification----------------------------"
	@make stp-poly-after-simplify-syntia
	@echo "--------------------stp solving poly MBA samples after Syntia simplification completion-----------------"
	@echo "--------------------stp solving nonpoly MBA samples after Syntia simplification-------------------------"
	@make stp-nonpoly-after-simplify-syntia
	@echo "--------------------stp solving nonpoly MBA samples after Syntia simplification completion--------------"
	@echo "--------------------stp solving MBA samples after Syntia simplification --------------"
	@make stp-solving-syntia-total
