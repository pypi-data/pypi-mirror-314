# coding = utf-8
# @Time    : 2024-12-10  12:42:42
# @Author  : zhaosheng@nuaa.edu.cn
# @Describe: Pickable session for VAD.

import os
from functools import partial
import onnxruntime as ort

class PickableSession:
    """
    This is a wrapper to make the current InferenceSession class pickable.
    """
    def __init__(self, onnx_path=None):
        # if onnx_path is None, load $DGUARD_MODEL_PATH/dguard_vad.onnx as default
        if onnx_path is None:
            DGUARD_MODEL_PATH = os.environ.get("DGUARD_MODEL_PATH")
            if not DGUARD_MODEL_PATH:
                raise ValueError("Please set the environment variable DGUARD_MODEL_PATH or specify the onnx_path.")
            onnx_path = os.path.join(DGUARD_MODEL_PATH, "dguard_vad.onnx")
        opts = ort.SessionOptions()
        opts.inter_op_num_threads = 1
        opts.intra_op_num_threads = 1
        opts.log_severity_level = 3
        self.model_path = onnx_path
        self.init_session = partial(ort.InferenceSession, sess_options=opts, providers=["CPUExecutionProvider"])
        self.sess = self.init_session(self.model_path)

    def run(self, *args):
        return self.sess.run(None, *args)

    def __getstate__(self):
        return {"model_path": self.model_path}

    def __setstate__(self, values):
        self.model_path = values["model_path"]
        self.sess = self.init_session(self.model_path)

vad_session = PickableSession()
