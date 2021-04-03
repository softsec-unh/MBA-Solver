sspam-mba-linear:
	python2 sspam-evaluation.py ../dataset/pldi_dataset_linear_MBA.txt linear.MBA.SSPAM.result.txt

sspam-mba-poly:
	python2 sspam-evaluation.py ../dataset/pldi_dataset_poly_MBA.txt poly.MBA.SSPAM.result.txt

sspam-mba-nonpoly:
	python2 sspam-evaluation.py ../dataset/pldi_dataset_nonpoly_MBA.txt nonpoly.MBA.SSPAM.result.txt

sspam-simplify:	
	@echo "----------------------sspam simplify linear MBA samples-------------------"
	@make sspam-mba-linear
	@echo "----------------------sspam simplify linear MBA samples completion---------"
	@echo "----------------------sspam simplify poly MBA samples----------------------"
	@make sspam-mba-poly
	@echo "----------------------sspam simplify poly MBA samples completion-----------"
	@echo "----------------------sspam simplify nonpoly MBA samples--------------------"
	@make sspam-mba-nonpoly
	@echo "----------------------sspam simplify nonpoly MBA samples completion---------"

