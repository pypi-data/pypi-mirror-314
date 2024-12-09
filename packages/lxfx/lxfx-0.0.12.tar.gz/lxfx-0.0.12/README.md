# lxfx

Predicting the forex and stock markets is notoriously challenging due to their inherent complexity and the multitude of factors that influence price movements. These markets are influenced by a diverse array of elements, including economic indicators, geopolitical events, market sentiment, and even natural disasters. The sheer volume of data and the rapid pace at which market conditions can change make it difficult to develop models that can consistently predict market behavior with high accuracy.

The forex market, for instance, is affected by interest rates, inflation, political stability, and economic performance of countries, among other factors. Similarly, the stock market is influenced by corporate earnings, industry performance, investor sentiment, and macroeconomic trends. The interplay of these factors creates a dynamic and often unpredictable environment.

`lxfx` aims to address these challenges by providing a robust framework for experimenting with various methods and models. The library is designed to handle both technical and fundamental data, allowing users to incorporate a wide range of information into their analysis. By leveraging advanced models such as LSTM, GRU, RNN, WaveNets, and Transformers, `lxfx` enables users to explore different approaches and techniques to improve prediction accuracy.

The major target of `lxfx` is to empower users to experiment with different methods and data sources, providing the flexibility to test and refine their models. Whether you are using technical indicators, fundamental data, or a combination of both, `lxfx` offers the tools needed to build sophisticated models and evaluate their performance. The library's comprehensive suite of functionalities ensures that users can create robust and efficient pipelines, making it easier to tackle the complexities of forex and stock market prediction.

By employing state-of-the-art techniques and continuously refining models based on new data, `lxfx` helps users push the boundaries of what is possible in market prediction. While no model can guarantee perfect accuracy, the ability to experiment with different methods and data sources increases the likelihood of developing models that can provide valuable insights and improve decision-making in the financial markets.

## Experiment Management with XFX Projects

One of the standout features of `lxfx` is its ability to manage experiments as individual projects, referred to as XFX projects. This functionality allows users to save all experimental data, including configurations, model parameters, training logs, and results, in a structured manner. By organizing experiments as projects, `lxfx` provides a comprehensive overview of how different models perform under various conditions.

### Key Benefits of XFX Projects

- **Comprehensive Experiment Tracking**: Each XFX project captures detailed information about the experiment, including the data used, model configurations, training parameters, and evaluation metrics. This ensures that all aspects of the experiment are documented and can be reviewed at any time.
- **Reproducibility**: By saving all experimental data, XFX projects make it easy to reproduce experiments. Users can rerun experiments with the same settings or modify parameters to explore different scenarios, ensuring that results are consistent and comparable.
- **Performance Comparison**: XFX projects enable users to compare the performance of different models and configurations side by side. This helps in identifying the best-performing models and understanding the impact of various factors on model accuracy.
- **Visualization and Analysis**: With built-in tools for visualizing training progress, prediction results, and evaluation metrics, XFX projects provide valuable insights into model performance. Users can generate plots and charts to analyze how models behave over time and under different conditions.
- **Collaboration**: XFX projects facilitate collaboration by providing a standardized format for sharing experimental data. Team members can easily share their projects, review each other's work, and build upon previous experiments.

### How to Create and Manage XFX Projects

Creating an XFX project is straightforward. Users can define a project by specifying the configuration file, model type, and other relevant parameters. Once the project is set up, `lxfx` handles the rest, automatically saving all experimental data and providing tools for managing and analyzing the project.


## Overview
`lxfx` is a comprehensive library designed to streamline the process of working with time series data and developing machine learning and deep learning models. This library aims to enhance productivity by reducing the need to write repetitive code, allowing you to focus on experimentation and model training using PyTorch.

## Key Features

- **Time Series Analysis**: Simplifies the steps involved in time series data analysis.
- **Machine Learning and Deep Learning**: Facilitates the creation and training of models with PyTorch.
- **Integration with Popular Libraries**: Seamlessly integrates with well-known libraries and data types such as NumPy arrays, PyTorch tensors, and Pandas DataFrames.

## Benefits

- **Efficiency**: Speeds up workflows by providing reusable classes and functions.
- **Flexibility**: Offers the ability to use provided classes as-is or customize them to fit specific needs.
- **Consistency**: Ensures that objects remain compatible with standard libraries, making it easy to incorporate `lxfx` into existing projects.

With `lxfx`, you can create robust and efficient pipelines with minimal code, making it an ideal tool for both beginners and experienced practitioners in the field of time series analysis and machine learning.

## Project Status

`lxfx` is currently in the alpha stage. This means that the project is still under active development and may undergo significant changes. Users are encouraged to experiment with the library and provide feedback, but should be aware that some features may not be fully stable or complete. Contributions and suggestions are welcome to help improve the library as it evolves.

## Use Cases

`lxfx` is designed to address a variety of time series problems, with a particular focus on forecasting in the stock and forex markets. However, the library is versatile enough to be applied to a wide range of time series analysis tasks, excluding NLP (Natural Language Processing) for now. Support for NLP will be added in the near future.

### Stock Market Forecasting

- **Data Loading**: Easily load and preprocess stock market data.
- **Feature Engineering**: Generate relevant features for stock price prediction.
- **Model Training**: Train advanced models such as LSTM, GRU, and Transformers to predict stock prices.
- **Evaluation**: Evaluate model performance using various metrics and visualization tools.

### Forex Market Forecasting

- **Data Loading**: Seamlessly load and preprocess forex market data.
- **Feature Engineering**: Create features that capture the dynamics of forex price movements.
- **Model Training**: Utilize state-of-the-art models to forecast forex prices.
- **Evaluation**: Assess model accuracy and visualize predictions.

### General Time Series Analysis

- **Data Loading**: Load time series data from various sources.
- **Feature Engineering**: Extract meaningful features for time series analysis.
- **Model Training**: Implement and train models for tasks such as anomaly detection, trend analysis, and more.
- **Evaluation**: Use built-in tools to evaluate and visualize model results.

`lxfx` provides a comprehensive toolkit for tackling time series problems, making it a valuable resource for both financial market forecasting and general time series analysis. The library's flexibility ensures that it can be adapted to meet the needs of different projects and applications.

## Installation
## Installation

The `lxfx` library is available on PyPI, making it easy to install using `pip`. Follow the instructions below to install the library.

### Method 1: Install from PyPI

1. **Install the `lxfx` Library**:
   Use `pip` to install the latest version of `lxfx` directly from PyPI.
   ```bash
   pip install lxfx
   ```

### Method 2: Install from Source

If you prefer to install the library from the source, you can clone the repository from GitHub.

1. **Clone the Repository**:
   Clone the `lxfx` repository to your local machine.
   ```bash
   git clone https://github.com/yourusername/lxfx.git
   cd lxfx
   ```

2. **Create a Virtual Environment** (optional but recommended):
   It is a good practice to create a virtual environment to manage your project dependencies.
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the Dependencies**:
   Use the `requirements.txt` file to install all necessary dependencies.
   ```bash
   pip install -r requirements.txt
   ```

4. **Install the `lxfx` Library**:
   Finally, install the `lxfx` library.
   ```bash
   pip install .
   ```

After completing these steps, the `lxfx` library should be installed and ready to use in your projects. You can verify the installation by running:

# Usage

## Configuration

The `lxfx` library uses a configuration file in JSON format to set up various components and parameters. Below are configurations for the different models so far available:

### FCBlock Configuration

| Parameter                  | Value   |
|----------------------------|---------|
| **in_features**            | `null`  |
| **hidden_size**            | `null`  |
| **out_size**               | `null`  |
| **nature**                 | `"lstm"`|
| **dropout**                | `0.2`   |
| **num_layers**             | `1`     |
| **bidirectional**          | `false` |
| **activation**             | `"tanh"`|
| **use_batch_norm**         | `false` |
| **pass_block_hidden_state**| `false` |

### FxFCModel Configuration

| Parameter                  | Value   |
|----------------------------|---------|
| **num_features**           | `null`  |
| **block_type**             | `"lstm"`|
| **out_features**           | `1`     |
| **units**                  | `null`  |
| **num_layers**             | `1`     |
| **is_encoder**             | `false` |
| **encoder_latent_dim**     | `null`  |
| **is_decoder**             | `false` |
| **out_units**              | `null`  |
| **activation**             | `"tanh"`|
| **bidirectional**          | `false` |
| **pass_states**            | `false` |
| **use_batch_norm**         | `false` |
| **pass_block_hidden_state**| `false` |
| **decoder_out_features**   | `null`  |

**Comments**:
- The length of the units array is equal to the number of fxfc blocks.
- The number of out_units MUST be equal to the number of units.
- Once the out_units is set, then pass_block_hidden_states must be false because the first layer shall have a hidden state whose shape is different from the next layer's hidden state shape.
- use_batch_norm is a MUST if the data is forex data.

### FxFCEncoder Configuration

| Parameter          | Value   |
|--------------------|---------|
| **num_features**   | `null`  |
| **block_type**     | `null`  |
| **units**          | `null`  |
| **out_units**      | `null`  |
| **num_layers**     | `1`     |
| **activation**     | `"tanh"`|
| **latent_dim**     | `null`  |
| **use_batch_norm** | `false` |
| **bidirectional**  | `false` |
| **is_attentive**       | `false`|

### FxFCDecoder Configuration

| Parameter            | Value   |
|----------------------|---------|
| **latent_dim**       | `null`  |
| **target_features**  | `1`     |
| **block_type**       | `null`  |
| **units**            | `null`  |
| **out_units**        | `null`  |
| **num_layers**       | `1`     |
| **activation**       | `"tanh"`|
| **use_batch_norm**   | `false` |
| **initialize_weights**| `false`|
| **initializer_method**| `null` |
| **is_attentive**       | `false`|

### FxFCAutoEncoder Configuration

| Parameter                  | Value          |
|----------------------------|----------------|
| **num_features**           | `null`         |
| **target_features**        | `1`            |
| **future_pred_length**     | `1`            |
| **block_types**            | `["lstm", "lstm"]`|
| **units**                  | `[null, null]` |
| **out_units**              | `[null, null]` |
| **num_layers**             | `[1, 1]`       |
| **activations**            | `["tanh", "tanh"]`|
| **latent_dim**             | `32`           |
| **dropout**                | `[0.2, 0.2]`   |
| **bidirectional**          | `[false, false]`|
| **use_batch_norm**         | `[false, false]`|
| **pass_states**            | `[false, false]` |
| **pass_block_hidden_state**| `[false, false]`|
| **is_attentive**           | `[true, true]`  |

**Comments**:
- Once the out_units is set, then pass_block_hidden_states must be false because the first layer shall have a hidden state whose shape is different from the next layer's hidden state shape.

### TimeSeriesDatasetManager Configuration

| Parameter              | Value          |
|------------------------|----------------|
| **file_path**          | `null`         |
| **future_pred_length** | `1`            |
| **targetIndices**      | `null`         |
| **target_names**       | `null`         |
| **drop_names**         | `null`         |
| **date_col**           | `null`         |
| **sequence_length**    | `5`            |
| **test_sequence_length**| `2`           |
| **is_autoregressive**  | `false`        |
| **stride**             | `1`            |
| **scaler_feature_range**| `[0, 1]`      |
| **transform**          | `null`         |
| **use_default_scaler** | `true`         |
| **split_criterion**    | `[0.7, 0.15, 0.15]`|
| **batchsize**          | `null`         |
| **is_fx**              | `false`        |
| **transform_targets**  | `true`         |
| **index_col**          | `null`         |
| **manual_seed**        | `null`         |
| **test_stride**        | `null`         |

### ModelTrainer Configuration

| Parameter          | Value   |
|--------------------|---------|
| **loss_fn**        | `null`  |
| **optmizer**       | `null`  |
| **epochs**         | `3`     |
| **accuracy_fn**    | `null`  |
| **lr**             | `0.001` |
| **project_path**   | `null`  |
| **is_logging**     | `true`  |
| **resume**         | `false` |
| **targets_transformed**| `false`|

### TensorInitializer Configuration

| Parameter | Value |
|-----------|-------|
| **method**| `null`|
