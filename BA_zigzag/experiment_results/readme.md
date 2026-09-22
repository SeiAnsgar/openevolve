A ZigZag run needs a workload which is a model defined in a .onnx file and a cim-hardware description

was bedeutet was:
latency: result by zigzag, in cycles
energy: result by zigzag, in pAmp
opt_goal: attribute to optimize (latency or energy transfer(TODO!: or is it energy used? what exactly is energy))
time: how long it took the find a solution
//not that accurate but puts the different runtimes in perspective.
openevo runs with many runs can have relatively low runtimes if a big part of the iterations gets cannceled early because the generated program failed at a early validation check e.g. syntax error

LLM-Backend: which LLM got used for OpenEvovle to find new solutions
//model hosted by scads.ai, why take this model? -> in the selection, free to use (for me at least) The model is capable of the kind of task [cite]


inputs: 
[workload, hardware] -> [some_model.onnx, cim-hardware]

configuration:
    number_of_iterations:
    LLM_backend:



nb_spatial_mappings: //do i even need this? maybe its easier not to do so many zigzag runs, standard is 3(check if thats true). Most of the time it generates the same result

test_testname:
    workload:
    hardware:
    opt_goal:

    OpenEvolve:
        configuration:
            number_of_iterations:
            LLM_backend:
        metrics:
            energy:
            latency:
        time:

    ZigZag:
    configuration:
        nb_spatial_mappings:
    metrics:
            energy:
            latency:
        time: