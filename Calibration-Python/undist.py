# You should replace these 3 lines with the output in calibration step
DIM=(1920, 1080)
K=np.array([[1087.7517088403981, 0.0, 921.1974163971402], [0.0, 1100.0717302685962, 543.3721306287408], [0.0, 0.0, 1.0]])
D=np.array([[0.0474937696880302], [-1.2257225826964717], [2.856438084251032], [-2.0954783152258365]])
def undistort(img_path):
    img = cv2.imread(img_path)
    h,w = img.shape[:2]
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    cv2.imshow("undistorted", undistorted_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
if __name__ == '__main__':
    for p in sys.argv[1:]:
        undistort(p)
