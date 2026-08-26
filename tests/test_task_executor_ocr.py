import sys
import threading
import types
import unittest
from unittest.mock import patch

import cv2  # Keep OpenCV loaded while patch.dict restores fake OCR modules.
import numpy as np

import ok.task.TaskExecutor as task_executor_module
from ok.task.TaskExecutor import TaskExecutor


class TestTaskExecutorOCR(unittest.TestCase):
    @staticmethod
    def make_executor(use_npu=True):
        executor = TaskExecutor.__new__(TaskExecutor)
        executor.config = {
            'ocr': {
                'default': {
                    'lib': 'onnxocr',
                    'params': {'use_npu': use_npu},
                },
            },
        }
        executor._ocr_lib = {}
        executor._ocr_lib_lock = threading.Lock()
        executor._ocr_init_results = {}
        return executor

    @staticmethod
    def fake_onnxocr(ocr_side_effect=None):
        instances = []

        class FakeONNXPaddleOcr:
            def __init__(self, **kwargs):
                self.kwargs = kwargs
                self.frames = []
                instances.append(self)

            def ocr(self, frame):
                self.frames.append(frame)
                if ocr_side_effect is not None:
                    raise ocr_side_effect
                return [[('box', ('okscript', 0.99))]]

        package = types.ModuleType('onnxocr')
        module = types.ModuleType('onnxocr.onnx_paddleocr')
        module.ONNXPaddleOcr = FakeONNXPaddleOcr
        package.onnx_paddleocr = module
        return instances, {
            'onnxocr': package,
            'onnxocr.onnx_paddleocr': module,
        }

    def test_npu_ocr_runs_generated_frame_smoke_test(self):
        executor = self.make_executor(use_npu=True)
        instances, modules = self.fake_onnxocr()

        with patch.dict(sys.modules, modules):
            result = executor._create_ocr_lib('default')

        self.assertIs(result, instances[0])
        self.assertEqual([True], [instance.kwargs['use_npu'] for instance in instances])
        self.assertEqual(1, len(instances[0].frames))
        frame = instances[0].frames[0]
        self.assertIsInstance(frame, np.ndarray)
        self.assertEqual((160, 640, 3), frame.shape)
        self.assertLess(frame.min(), 255)
        self.assertIn('use_npu=True', executor._ocr_init_results['default'])
        self.assertIn('okscript', executor._ocr_init_results['default'])

    def test_failed_npu_ocr_falls_back_to_non_npu_instance(self):
        executor = self.make_executor(use_npu=True)
        instances, modules = self.fake_onnxocr(RuntimeError('NPU unavailable'))

        with patch.dict(sys.modules, modules):
            result = executor._create_ocr_lib('default')

        self.assertIs(result, instances[1])
        self.assertEqual([True, False], [instance.kwargs['use_npu'] for instance in instances])
        self.assertEqual(1, len(instances[0].frames))
        self.assertEqual(0, len(instances[1].frames))
        self.assertIn('use_npu=False', executor._ocr_init_results['default'])
        self.assertIn('NPU unavailable', executor._ocr_init_results['default'])

    def test_disabled_npu_skips_smoke_test(self):
        executor = self.make_executor(use_npu=False)
        instances, modules = self.fake_onnxocr()

        with patch.dict(sys.modules, modules):
            result = executor._create_ocr_lib('default')

        self.assertIs(result, instances[0])
        self.assertEqual([False], [instance.kwargs['use_npu'] for instance in instances])
        self.assertEqual([], instances[0].frames)
        self.assertEqual('use_npu=False', executor._ocr_init_results['default'])

    def test_default_init_finish_log_includes_npu_test_result(self):
        executor = self.make_executor(use_npu=True)
        executor._ocr_lib['default'] = object()
        executor._ocr_init_results['default'] = 'use_npu=True, test_ocr=okscript'

        with patch.object(task_executor_module.logger, 'info') as info:
            executor._init_default_ocr()

        finish_log = info.call_args_list[-1].args[0]
        self.assertIn('default ocr init end', finish_log)
        self.assertIn('use_npu=True, test_ocr=okscript', finish_log)


if __name__ == '__main__':
    unittest.main()
