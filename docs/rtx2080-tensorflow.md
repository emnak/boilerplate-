# How to use RTX2080 GPUs with Tensorflow

If you use Tensorflow on the Sicara GPU, you need to use the step 
`SetGPUConfig` at the beginning of your pipeline 
(see the [example pipeline](pipelines/fashion-mnist-simple-cnn-pipeline.yaml)).
