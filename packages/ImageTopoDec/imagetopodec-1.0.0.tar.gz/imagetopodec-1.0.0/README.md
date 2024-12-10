# A library to process raster images using persistence homology


Example:

	import ImageTopoDec as bc
	import ImageTopoDec.barcode as bcc
	import ImageTopoDec.barplot as bcp
	import cv2


	img = cv2.imread('/Users/sam/Edu/bar/12/1.png', cv2.IMREAD_GRAYSCALE)

	cont = bc.barstruct()
	barc =  bcc.create_barcode(img, cont)

	cmp = barc.get_largest_component()
	img = bcc.combine_components_into_matrix(cmp, img.shape, img.dtype)
	# cv2.imshow("source",img)
	# cv2.waitKey(0)

	binmap = barc.segmentation(False)
	cv2.imshow("binmap", binmap)
	cv2.waitKey(1)

	filterd = barc.filter(100)
	cv2.imshow("filterd", filterd)
	cv2.waitKey(0)


	bcp.plot_barcode_lines(barc.item.getBarcodeLines(), 'test', True)

	exit(0)
