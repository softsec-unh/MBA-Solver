linear-simplify:
	python3 pldi_dataset_simplify_linear.py ../dataset/pldi_dataset_linear_MBA.txt

poly-simplify:
	python3 pldi_dataset_simplify_poly.py ../dataset/pldi_dataset_poly_MBA.txt

nonpoly-simplify:
	python3 pldi_dataset_simplify_nonpoly.py ../dataset/pldi_dataset_nonpoly_MBA.txt

mba-solver-simplify: 
	@echo "-----------MBA-Solver simplify linear MBA samples------------------"
	@make linear-simplify
	@echo "-----------MBA-Solver simplify linear MBA samples completion-------"
	@echo "-----------MBA-Solver simplify poly MBA samples--------------------"
	@make poly-simplify
	@echo "-----------MBA-Solver simplify poly MBA samples completion---------"
	@echo "-----------MBA-Solver simplify nonpoly MBA samples-----------------"
	@make nonpoly-simplify
	@echo "-----------MBA-Solver simplify nonpoly MBA samples completion------"
