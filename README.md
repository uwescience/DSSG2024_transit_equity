# DSSG2024_transit_equity
Transit equity public code and documentation

Website Link: [DSSG2024_transit_equity](https://uwescience.github.io/DSSG2024_transit_equity/)

## Environment Setup

To set up a Conda environment using the environment.yaml file, follow these steps:

1. Open a terminal or command prompt.
2. Navigate to the directory where the environment.yaml file is located. In this case, it would be the root folder.
3. Run the following command to create the Conda environment:

    ```
    conda env create -f environment.yaml
    ```

    This command will read the environment.yaml file and create a new Conda environment with the specified dependencies.

4. Once the environment is created, activate it by running the following command:

    ```
    conda activate orca
    ```
    (If the name in environment.yaml has been changed, update the above environment name accordingly)

5. You can now proceed with running your notebooks or any other tasks within the activated Conda environment.

Remember to deactivate the environment when you're done by running `conda deactivate`.


## Installing Package Locally

(This section assumes that the conda environmet has been set up in the way given in [here](#environment-setup))

1. Activate the environment set up in [here](#environment-setup)

2. Navigate to the root.

3. Run the following command to install the `transit-equity` package in interactive mode without dependencies:

    ```
    pip install --no-deps -e .
    ```

Extra context given in the discussion thread of the [Pull Request 4](https://github.com/uwescience/DSSG2024_transit_equity/pull/4)


## Using dotenv

To use dotenv for managing environment variables, follow these steps:
1. Create a `.env` file in the root folder of your project.

2. Add your environment variables to the `.env` file in the following format: `VARIABLE_NAME=VALUE`.

    Refer to [.env.example](.env.example) to know which environment variables to add to .env


3. In your Python code, import the `dotenv` module and load the environment variables from the `.env` file using the following code:

    ```python
    from dotenv import load_dotenv

    load_dotenv()
    ```
    
    If your code is present inside a subdirectly, update the sys path accordingly. For example:
    ```python
    parent_dir = os.path.dirname(os.getcwd())
    if parent_dir not in sys.path:
        sys.path.append(parent_dir)
    
    from utils.connect import get_automap_base_with_views
    ```

4. You can now access the environment variables in your code using `os.getenv('VARIABLE_NAME')`.

    Remember to add the `.env` file to your `.gitignore` to keep your sensitive information secure.

