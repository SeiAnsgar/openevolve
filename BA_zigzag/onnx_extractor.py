import onnx
from onnx import shape_inference

def extract_layer_info(onnx_path):
    # load_external_data=False verhindert das Suchen/Laden der .external Datei
    model = onnx.load(onnx_path, load_external_data=False)
    
    try:
        model = shape_inference.infer_shapes(model)
    except Exception as e:
        print(f"Hinweis bei Shape Inference: {e}")
        
    graph = model.graph
    
    # Value infos & initializers für Shape-Lookup
    value_shapes = {}
    for vi in list(graph.value_info) + list(graph.input) + list(graph.output):
        type_proto = vi.type.tensor_type
        if type_proto.HasField('shape'):
            shape = [dim.dim_value for dim in type_proto.shape.dim]
            value_shapes[vi.name] = shape

    for tensor in graph.initializer:
        value_shapes[tensor.name] = list(tensor.dims)

    print("WORKLOAD STRUCTURE (ResNet18 Layer Dimensions):")
    print("| Layer Name | Type | K (Out Ch) | C (In Ch) | Image Size (OX x OY) | Kernel (FX x FY) |")
    print("|---|---|---|---|---|---|")

    layer_idx = 1
    for node in graph.node:
        if node.op_type in ["Conv", "Gemm"]:
            name = node.name if node.name else f"{node.op_type}_{layer_idx}"
            
            if node.op_type == "Conv":
                # Weights: [K, C, FY, FX]
                w_shape = value_shapes.get(node.input[1], [0,0,0,0])
                # Output Y: [B, K, OY, OX]
                out_shape = value_shapes.get(node.output[0], [0,0,0,0])
                
                K = w_shape[0] if len(w_shape) > 0 and w_shape[0] != 0 else "?"
                C = w_shape[1] if len(w_shape) > 1 and w_shape[1] != 0 else "?"
                FY, FX = (w_shape[2], w_shape[3]) if len(w_shape) > 3 else ("?", "?")
                OY, OX = (out_shape[2], out_shape[3]) if len(out_shape) > 3 else ("?", "?")
                
                print(f"| {name} | Conv | {K} | {C} | {OX}x{OY} | {FX}x{FY} |")
                
            elif node.op_type == "Gemm":
                # Weights: [K, C]
                w_shape = value_shapes.get(node.input[1], [0,0])
                K = w_shape[0] if len(w_shape) > 0 and w_shape[0] != 0 else "?"
                C = w_shape[1] if len(w_shape) > 1 and w_shape[1] != 0 else "?"
                print(f"| {name} | Gemm | {K} | {C} | N/A (Vector) | N/A |")
                
            layer_idx += 1

if __name__ == "__main__":
    extract_layer_info("zigzag_inputs/models/mobilenetv2.onnx")