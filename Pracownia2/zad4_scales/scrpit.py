def test():
    scale_test("scale11")
    scale_test("scale12")
    scale_test("scale13")
    scale_test("scale14")
    scale_test("scale15")

def scale_test(file_name):
    with open(file_name) as f1:
        with open("scale1") as f2:
            nums2 = [int(l.strip()) for l in f2.readlines()[:21]]
            nums1 = [int(l.strip()) for l in f1.readlines()[:21]]
            print([abs(a - b) for a, b in zip(nums1, nums2)])

test()
