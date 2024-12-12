import tests.test_middleware_utils
import tests.test_serialization_utils
import tests.test_concurrency_utils
import tests.test_network_utils
import tests.test_file_utils
import tests.test_image_utils
import tests.test_other_utils
import tests.test_dynamic_compose
import tests.test_ocr_utils
import tests.test_img_det


def global_test():
    tests.test_middleware_utils.tests()
    tests.test_serialization_utils.tests()
    tests.test_concurrency_utils.tests()
    tests.test_network_utils.tests()
    tests.test_file_utils.tests()
    tests.test_image_utils.tests()
    tests.test_other_utils.tests()
    tests.test_dynamic_compose.tests()
    tests.test_ocr_utils.tests()
    tests.test_img_det.tests()


if __name__ == '__main__':
    global_test()
