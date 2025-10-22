import os

from pymilvus.model.dense import OnnxEmbeddingFunction

# TODO validate its parrallel
class DefaultParallel(OnnxEmbeddingFunction):
    def __init__(self):
        super().__init__("GPTCache/paraphrase-albert-onnx", "GPTCache/paraphrase-albert-small-v2")
        import onnxruntime
        from huggingface_hub import hf_hub_download
        sess_options = onnxruntime.SessionOptions()
        sess_options.execution_mode = onnxruntime.ExecutionMode.ORT_PARALLEL
        sess_options.intra_op_num_threads = os.cpu_count()//2  # 控制单个算子的并行度
        sess_options.graph_optimization_level = onnxruntime.GraphOptimizationLevel.ORT_ENABLE_ALL
        self.ort_session = onnxruntime.InferenceSession(
            hf_hub_download(repo_id=self.model_name, filename="model.onnx"), sess_options)