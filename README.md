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

## FM

### FastFM

The code to implement FastFM can be found in the [FastFM](./FastFM.ipynb) file

### DeepFM

The code for the data procesing as well as the model implementation can be found in the [DeepFM](./DeepFM/) folder.

### Results

The results for both DeepFM and FastFM can be found in [MetricasFM](./Metricas%20FM.ipynb)

