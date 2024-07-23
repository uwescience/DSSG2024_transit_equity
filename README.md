# DSSG2024_transit_equity
Transit equity public code and documentation

Website Link: [DSSG2024_transit_equity](https://uwescience.github.io/DSSG2024_transit_equity/)

## Environment Setup

To set up a Conda environment using the environment.yaml file, follow these steps:

1. Open a terminal or command prompt.
2. Navigate to the directory where the environment.yaml file is located. In this repository, it would be the root folder.

    Note: Switch to the main branch.

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

2. Navigate to the root of this repository.

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
    
    Generally, you would want to provide the dotenv path while loading the environment. For example:
    ```python
    path_to_env = '<path_to_env_file>'
    load_dotenv(dotenv_path=path_to_env)
    ```

4. You can now access the environment variables in your code using `os.getenv('VARIABLE_NAME')`.

    Remember to add the `.env` file to your `.gitignore` to keep your sensitive information secure.


## Example Usage

Once the Python environment has been setup, and the env file is loaded, you can import a method and utilize it:

1. Import the necessary modules/methods in your Python code:

    ```python
    from transit_equity.utils.db_helpers import get_automap_base_with_views
    ```

2. Call the method function with the required arguments:

    ```python
    from sqlalchemy import create_engine
    engine = create_engine('postgresql://user:password@localhost:5432/dbname')
    Base = get_automap_base_with_views(engine=engine, schema='orca')
    print(type(Base))   # <class 'sqlalchemy.ext.automap.AutomapBase'>
    ```
