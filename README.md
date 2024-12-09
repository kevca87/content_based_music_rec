# Effect of tracks metadata representations in Content Based Automatic Playlist Continuation

**To scrap the dataset**
1. Create a `.env` file with the tokens of the APIs (in the root dir of the project) (An example could be found in sample.env)
2. Run the following command
    ```
    py .\scrap_dataset.py -s <s> -e <e>
    ```

    `s` is the start index of `unique_tracks` list
    `e` is the end index of `unique_tracks` list

    By default the script needs an output directory created named `data_ignored/tracks_dataset`, you can specify the directory by using the flag `-o`

## Dataset partition
The process of train and challenge dataset partition could be found in [data_partition](./data_partition.ipynb) file

## Embeddings creation
The process of embedding creation could be found in the [content_embedding_creation](./content_embedding_creation.ipynb) file

## SASRec
The code to implement SASRec & $SASRec_C$ and the results of the experiments can be found in the [SASRec](./SASRec/) folder

## FM

### FastFM

The code to implement FastFM can be found in the [FastFM](./FastFM.ipynb) file

### DeepFM

The code for the data procesing as well as the model implementation can be found in the [DeepFM](./DeepFM/) folder.

### Results

The results for both DeepFM and FastFM can be found in [MetricasFM](./Metricas%20FM.ipynb)

## Uso de ChatGPT
https://chatgpt.com/share/67576291-7920-800e-8963-fea495cb8e51

https://chatgpt.com/share/675762a8-6c64-800e-9846-7c8e65ed28af

https://chatgpt.com/share/675763c2-9ab4-8012-9766-69ab6c9df8c0

https://chatgpt.com/share/675766e4-59ac-8005-b72c-f55392358850