import sqlalchemy
from sqlalchemy import create_engine, inspect
import contextily as cx
import geopandas
from matplotlib import pyplot as plt
import pandas as pd
from geodatasets import get_path



def known_tables_in_schema(engine):
    """
    This function prints all the known tables,views and 
    materialized views in an engine
    --
    schema: str
    """
    inspector = inspect(engine)
    schemas = inspector.get_schema_names()
    for schema in schemas:
        for table_name in inspector.get_table_names(schema=schema):
            print( table_name)

        for view in inspector.get_view_names(schema=schema):
            print( view)

        for m_view in inspector.get_materialized_view_names(schema=schema):
            print( m_view)

        print(f'\n')


def check_weird_in_coordinates(df, lat_col= 'device_lat1', long_col = 'device_lng1', weird_lat = 40, weird_long = -120):
  """
  This function checks if the coordinates in a df have weird things like very unlike locations

  Parameter
    ---------
    df: pd.DataFrame, The dataframe to check,
    lat_col: numeric, The column name for latitude,
    long_col: numeric, The column name for longitude

  """
  check_wrd = df[df[long_col] > weird_long, df[lat_col] < weird_lat]
  print(f'The shape is {df.shape} and the weird shape is at least {check_wrd.shape}')
  print(f'The min and max for lat is {min(df[lat_col])}, {max(df[lat_col])}.')
  print(f'The min and max for long is {min(df[long_col])}, {max(df[long_col])}')


def create_gdf_from_df(df, lat_col, lon_col, crs = "EPSG:4326", to_crs = "EPSG:3857"):
    """
    Function to create a geopandas dataframe from a pandas dataframe
    input: df: pandas dataframe
    lat_col: str: column name for latitude
    lon_col: str: column name for longitude
    crs: str: coordinate reference system
    output: gdf: geopandas dataframe
    """
    df['time_of_day'] = df['hour'].apply(categorize_time)
    gdf = geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(df[lon_col], df[lat_col]))
    gdf.crs = crs
    gdf = gdf.to_crs(to_crs)
    gdf.head(5)
    return gdf


def subset_plot(df, col_name:str, graph_name:str):
    """
    This function will plot based on the subset of column names.
    The input will be the dataframe (for mapping purpose, geopandas dataframe) 
    and the column that will need subdivision (as string) 
    """
    for col_subset in df[col_name].unique():
        print(col_subset)
        subset = df[df[col_name] == col_subset ]
        fig, ax = plt.subplots(1, 1, figsize = (20, 10))
        ax = subset.plot(figsize=(10, 10), alpha=0.001,
                            ax = ax,
                            markersize=1
                            )
        cx.add_basemap(ax, source=cx.providers.CartoDB.Positron)
        ax.set_title(f'{graph_name} map in {col_subset}', fontdict = {'fontsize': '20', 'fontweight' : '4'})
        
    # gdf_morning = gdf_stmt_transactions_clean[df_stmt_transactions_clean['time_of_day']=='Morning']


### This is the function to get the results of query and print
def get_results(session, query):
    """
    This function will get the results of a query and print it.

    Parameters:
    ----------
    session: sqlalchemy.orm.session.Session, The session object to use
    query: str, The query to execute
    
    """

    try:
        with session.begin():
            # Execute the query
            result = session.execute(query).fetchall()
            # Process results here
            # for row in result:
            #     print(row)
            print('result get fetched')
            return result
    except SQLAlchemyError as e:
        print('hi there- rollback')
         # Rollback the transaction in case of error
        session.rollback()  
        print(f"Error: {e}")
    finally:
        session.close()  # Ensure the session is closed properly
