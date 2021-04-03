linear-program-synthesis-64:testmcts.py
	python2 testmcts.py 64 ../dataset/pldi_dataset_linear_MBA.txt linear.syntia.64bit.middle.json 

linear-json-transformation-64:
	python2 transformation.py linear.syntia.64bit.middle.json linear.64bit.middle.txt

linear-syntia-evaluation-64:linear-program-synthesis-64 linear-json-transformation-64
	python2 syntia-evaluation.py 64 linear.64bit.middle.txt linear.64bit.result.txt 

poly-program-synthesis-64:testmcts.py
	python2 testmcts.py 64 ../dataset/pldi_dataset_poly_MBA.txt poly.syntia.64bit.middle.json 

poly-json-transformation-64:
	python2 transformation.py poly.syntia.64bit.middle.json poly.64bit.middle.txt

poly-syntia-evaluation-64:poly-program-synthesis-64 poly-json-transformation-64
	python2 syntia-evaluation.py 64 poly.64bit.middle.txt poly.64bit.result.txt 

nonpoly-program-synthesis-64:testmcts.py
	python2 testmcts.py 64 ../dataset/pldi_dataset_nonpoly_MBA.txt nonpoly.syntia.64bit.middle.json 

nonpoly-json-transformation-64:
	python2 transformation.py nonpoly.syntia.64bit.middle.json nonpoly.64bit.middle.txt

nonpoly-syntia-evaluation-64:nonpoly-program-synthesis-64 nonpoly-json-transformation-64
	python2 syntia-evaluation.py 64 nonpoly.64bit.middle.txt nonpoly.64bit.result.txt 

syntia-simplify:
	@echo "------------syntia simplify linear MBA samples-------------------"
	@make linear-syntia-evaluation-64
	@echo "------------syntia simplify linear MBA samples completion--------"
	@echo "------------syntia simplify poly MBA samples-------------------"
	@make poly-syntia-evaluation-64
	@echo "------------syntia simplify poly MBA samples completion--------"
	@echo "------------syntia simplify nonpoly MBA samples-------------------"
	@make nonpoly-syntia-evaluation-64
	@echo "------------syntia simplify nonpoly MBA samples completion--------"
