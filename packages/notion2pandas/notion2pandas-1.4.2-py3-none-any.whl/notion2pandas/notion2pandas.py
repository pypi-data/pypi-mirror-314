"""
notion2pandas: A Python package to integrate Notion databases with pandas DataFrames.

Notion2Pandas extends the notion-sdk-py library by Ramnes, enabling seamless data transfer
between Notion databases and pandas DataFrames with minimal code. With just a single line,
you can import a Notion database into a DataFrame or push updates from a DataFrame back to Notion.

Key Features:
- Easy import/export between Notion and pandas.
- Simplified Notion API interactions with robust error handling.
- Minimal setup, maximizing productivity for data analysis and manipulation.

Typical Usage:
    client = Notion2PandasClient(auth='your_notion_token')
    df = client.from_notion_DB_to_dataframe(database_id='your_database_id')

See the official Notion API documentation for more information: https://developers.notion.com/

Dependencies:
- notion_client
- pandas
"""

import time
import json
from dataclasses import dataclass
from typing import Callable, Tuple
import inspect

import pandas as pd

from notion_client import Client, APIErrorCode, APIResponseError
from notion_client.errors import HTTPResponseError, RequestTimeoutError
from notion_client.helpers import collect_paginated_api

from . import n2p_read_write


class NotionMaxAttemptsException(Exception):
    """
    Exception raised when the maximum number of network attempts
     to access a resource on Notion's servers is exceeded.

    Attributes:
        message (str): Description of the exception,
         detailing the failure after repeated network requests.
    """
    def __init__(self, m):
        self.message = m

    def __str__(self):
        return self.message


@dataclass
class RWFunction:
    """
    Represents a read-write function with metadata for handling Notion properties.

    Attributes:
        function (Callable): The function to be called for reading or writing data.
        num_params (int): The number of parameters the function accepts.
        need_column_name (bool): Indicates whether the function requires a column
                                  name as an argument.
        need_switcher (bool): Indicates whether the function requires a switcher
                              for processing the data.

    This class encapsulates properties of functions that interact with Notion
    data, allowing for dynamic handling based on the provided metadata.
    """
    function: Callable
    num_params: int
    need_column_name: bool
    need_switcher: bool


def _create_rw_tuple(read_func: Callable, write_func: Callable) -> Tuple[RWFunction, RWFunction]:
    return _create_rw_function(read_func), _create_rw_function(write_func)


def _create_rw_function(func: Callable) -> RWFunction:
    signature = inspect.signature(func)
    parameters = signature.parameters
    num_params = len(parameters)
    need_column_name = 'column_name' in parameters
    need_switcher = 'switcher' in parameters
    return RWFunction(
        function=func,
        num_params=num_params,
        need_column_name=need_column_name,
        need_switcher=need_switcher)


def _add_custom_columns(page_id, get_data_function, prop_dict, columns_dict):
    if len(columns_dict) > 0:
        notion_data = get_data_function(page_id)
        for column_name, function in columns_dict:
            prop_dict[column_name] = function(notion_data)


def _calculate_dict_hash(d):
    serialized_dict = json.dumps(d, sort_keys=True)
    return hash(serialized_dict)


class Notion2PandasClient(Client):
    """
    A client for interacting with Notion's API, extending the functionality of
    the base Client from the notion_client library.

    This class provides additional methods for retrieving and manipulating data
    within Notion, specifically tailored for integration with pandas DataFrames.

    Attributes:
        seconds_to_retry (int): The number of seconds to wait before retrying a
                                failed API request.
        max_attempts_executioner (int): The maximum number of attempts to make
                                         when executing API calls, useful for
                                         handling transient errors.
    """

    _ROW_HASH_KEY = 'Row_Hash'
    _ROW_PAGEID_KEY = 'PageID'

    # It's not in the official documentation,
    # but it seems there is a limit of 2700 API calls in 15 minutes.
    # https://notionmastery.com/pushing-notion-to-the-limits/#rate-limits
    # WIP
    _RATE_LIMIT_THRESHOLD = 900  # 60 * 15
    _CALLS_LIMIT_THRESHOLD = 2700

    def __init__(self, **kwargs):
        self.switcher = None
        self.seconds_to_retry = 30
        self.max_attempts_executioner = 3
        self.__set_n2p_arg(kwargs, 'secondsToRetry')
        self.__set_n2p_arg(kwargs, 'maxAttemptsExecutioner')

        super().__init__(**kwargs)

        self.read_only_columns = {"last_edited_time", "files", "created_time", "rollup",
                                  "unique_id", "last_edited_by", "button", "formula", "created_by"}

        self.switcher = {
            'title': _create_rw_tuple(n2p_read_write.title_read, n2p_read_write.title_write),
            'rich_text': _create_rw_tuple(n2p_read_write.rich_text_read,
                                          n2p_read_write.rich_text_write),
            'checkbox': _create_rw_tuple(n2p_read_write.checkbox_read,
                                         n2p_read_write.checkbox_write),
            'created_time': _create_rw_tuple(n2p_read_write.created_time_read,
                                             n2p_read_write.created_time_write),
            'number': _create_rw_tuple(n2p_read_write.number_read, n2p_read_write.number_write),
            'email': _create_rw_tuple(n2p_read_write.email_read, n2p_read_write.email_write),
            'url': _create_rw_tuple(n2p_read_write.url_read, n2p_read_write.url_write),
            'multi_select': _create_rw_tuple(n2p_read_write.multi_select_read,
                                             n2p_read_write.multi_select_write),
            'select': _create_rw_tuple(n2p_read_write.select_read,
                                       n2p_read_write.select_write),
            'date': _create_rw_tuple(n2p_read_write.date_read, n2p_read_write.date_write),
            'date_range': _create_rw_tuple(n2p_read_write.range_date_read,
                                           n2p_read_write.range_date_write),
            'files': _create_rw_tuple(n2p_read_write.files_read, n2p_read_write.files_write),
            'formula': _create_rw_tuple(n2p_read_write.formula_read, n2p_read_write.formula_write),
            'phone_number': _create_rw_tuple(n2p_read_write.phone_number_read,
                                             n2p_read_write.phone_number_write),
            'status': _create_rw_tuple(n2p_read_write.status_read, n2p_read_write.status_write),
            'unique_id': _create_rw_tuple(n2p_read_write.unique_id_read,
                                          n2p_read_write.unique_id_write),
            'created_by': _create_rw_tuple(n2p_read_write.created_by_read,
                                           n2p_read_write.created_by_write),
            'last_edited_time': _create_rw_tuple(n2p_read_write.last_edited_time_read,
                                                 n2p_read_write.last_edited_time_write),
            'string': _create_rw_tuple(n2p_read_write.string_read, n2p_read_write.string_write),
            'last_edited_by': _create_rw_tuple(n2p_read_write.last_edited_by_read,
                                               n2p_read_write.last_edited_by_write),
            'button': _create_rw_tuple(n2p_read_write.button_read, n2p_read_write.button_write),
            'relation': _create_rw_tuple(n2p_read_write.relation_read,
                                         n2p_read_write.relation_write),
            'rollup': _create_rw_tuple(n2p_read_write.rollup_read, n2p_read_write.rollup_write),
            'people': _create_rw_tuple(n2p_read_write.people_read, n2p_read_write.people_write)
        }

    def set_lambdas(self, key: str, new_read: Callable, new_write: Callable):
        """Generic method to update the read/write lambdas for a given key"""
        if key in self.switcher:
            self.switcher[key] = _create_rw_tuple(new_read, new_write)
        else:
            raise KeyError(f"'{key}' does not exist in read_write_lambdas")

    # Since Notion has introduced limits on requests to their APIs
    # (https://developers.notion.com/reference/request-limits),
    # this method can repeat the request to the Notion APIs at predefined time intervals
    # until a result is obtained or if the maximum limit of attempts is reached.

    def _notion_executor(self, api_to_call, **kwargs):
        attempts = self.max_attempts_executioner
        current_calls = 0
        while attempts > 0:
            try:
                result = api_to_call(**kwargs)
                current_calls += 1
                return result
            except HTTPResponseError as error:
                print('Caught exception: ' + str(error))
                attempts -= 1
                if isinstance(error, APIResponseError):
                    print('Error code: ' + error.code)
                    if error.code not in (APIErrorCode.InternalServerError,
                                          APIErrorCode.ServiceUnavailable):
                        print(error)
                        print(APIResponseError)
                        # raise APIErrorCode.ObjectNotFound
                else:
                    # Other error handling code
                    print(error)
                # Wait secondsToRetry before retry
                time.sleep(self.seconds_to_retry)
            except RequestTimeoutError as error:
                print('Caught exception: ' + str(error))
                attempts -= 1
            if attempts == 0:
                raise NotionMaxAttemptsException(
                    "NotionMaxAttemptsException") from None
            print('[_notionExecutor] Remaining attempts: ' + str(attempts))
        return None

    def get_database_columns(self, database_id):
        """
        Retrieves the columns (properties) of a Notion database.

        Args:
            database_id (str): The unique identifier of the Notion database.

        Returns:
            dict: The properties of the specified database,
             as retrieved from Notion.

        For more information, see the Notion API documentation:
        https://developers.notion.com/reference/retrieve-a-database
        """
        return self._notion_executor(
            self.databases.retrieve, **{'database_id': database_id})

    def create_page(self, parent_id, properties=None):
        """
        Creates a new page in the specified Notion parent page.

        Args:
            parent_id (str): The ID of the parent page where the new page will be created.
            properties (dict, optional): A dictionary of properties to set for the new page.

        Returns:
            str: The ID of the created page.

        For more information, see the Notion API documentation:
        https://developers.notion.com/reference/post-page
        """
        created_page = self._notion_executor(self.pages.create,
                                             **{'parent': {"database_id": parent_id},
                                                'properties': properties})
        return created_page.get('id')

    def _update_page(self, page_id, properties):
        updated_page = self._notion_executor(self.pages.update,
                                             **{'page_id': page_id,
                                                'properties': properties})
        return updated_page.get('id')

    def update_page(self, page_id, **kwargs):
        """
        Updates a specified Notion page with the provided attributes.

        Args:
            page_id (str): The ID of the page to update.
            **kwargs: Additional attributes to update for the page.

        Returns:
            str: The ID of the updated page.

        For more information, see the Notion API documentation:
        https://developers.notion.com/docs/patch-page
        """
        kwargs['page_id'] = page_id
        updated_page = self._notion_executor(self.pages.update, **kwargs)
        return updated_page.get('id')

    def retrieve_page(self, page_id):
        """
        Retrieves the details of a specified Notion page.

        Args:
            page_id (str): The ID of the page to retrieve.

        Returns:
            dict: The details of the requested page.

        For more information, see the Notion API documentation:
        https://developers.notion.com/reference/retrieve-a-page
        """
        return self._notion_executor(
            self.pages.retrieve, **{'page_id': page_id})

    def delete_page(self, page_id):
        """
        Deletes a specified Notion page.

        Args:
            page_id (str): The ID of the page to delete.

        For more information, see the Notion API documentation:
        https://developers.notion.com/reference/delete-a-block
        """
        self._notion_executor(
            self.blocks.delete, **{'block_id': page_id})

    def delete_rows_and_pages(self, df, rows_to_delete_indexes: list):
        """
        Deletes specified rows and their corresponding Notion pages from the given DataFrame.

        Args:
            df (DataFrame): The DataFrame containing the pages to delete.
            rows_to_delete_indexes (list): A list of row indices to delete
             from the DataFrame and Notion.

        For more information on page deletion, see the Notion API documentation:
        https://developers.notion.com/reference/delete-a-block
        """
        for row_index in rows_to_delete_indexes:
            page_id = df.loc[row_index, 'PageID']
            self.delete_page(page_id)
        df.drop(rows_to_delete_indexes, inplace=True)

    def retrieve_block(self, block_id):
        """
        Retrieves the details of a specified Notion block.

        Args:
            block_id (str): The ID of the block to retrieve.

        Returns:
            dict: The details of the requested block.

        For more information, see the Notion API documentation:
        https://developers.notion.com/reference/retrieve-a-block
        """
        return self._notion_executor(
            self.blocks.retrieve, **{'block_id': block_id})

    def retrieve_block_children_list(self, block_id):
        """
        Retrieves the children blocks of a specified Notion block.

        Args:
            block_id (str): The ID of the block whose children are to be retrieved.

        Returns:
            list: A list of children blocks under the specified block.

        For more information, see the Notion API documentation:
        https://developers.notion.com/reference/get-block-children
        """
        return self._notion_executor(
            self.blocks.children.list, **{'block_id': block_id})

    def update_block(self, block_id, field, field_value_updated):
        """
        Updates a specified field of a Notion block.

        Args:
            block_id (str): The ID of the block to update.
            field (str): The field to update in the block.
            field_value_updated (any): The new value for the specified field.

        Returns:
            dict: The updated block details.

        For more information, see the Notion API documentation:
        https://developers.notion.com/reference/update-a-block
        """
        return self._notion_executor(
            self.blocks.update,
            **{'block_id': block_id, field: field_value_updated})

    def __row_hash(self, row):
        row_dict = row.to_dict()
        if self._ROW_HASH_KEY in row_dict:
            del row_dict[self._ROW_HASH_KEY]
        return _calculate_dict_hash(row_dict)

    def __get_database_columns_and_types(self, database_id):
        columns = self.get_database_columns(database_id)
        if columns is None:
            return None
        return list(map(lambda notion_property:
                        (columns.get('properties').get(notion_property).get('name'),
                         columns.get('properties').get(notion_property).get('type')),
                        columns.get('properties')))

    def from_notion_DB_to_dataframe(self, database_id: str,  # pylint: disable=invalid-name
                                    filter_params=None):
        """
        Converts a Notion database into a pandas DataFrame.

        Args:
            database_id (str): The ID of the Notion database to retrieve.
            filter_params (dict, optional): Optional parameters to filter the database results.

        Returns:
            DataFrame: A pandas DataFrame containing the data from the specified Notion database.

        This method exists for backward compatibility with previous versions of the package.
        """
        return self.from_notion_DB_to_dataframe_kwargs(database_id, filter_params=filter_params)

    def from_notion_DB_to_dataframe_kwargs(self, database_id: str,  # pylint: disable=invalid-name
                                           **kwargs):
        """
        Converts a Notion database into a pandas DataFrame with additional parameters.

        Args:
            database_id (str): The ID of the Notion database to retrieve.
            **kwargs: Additional keyword arguments for filtering and selecting columns.
                - filter_params (dict, optional): Parameters to filter the database results.
                - columns_from_page (dict, optional): Mapping of columns to retrieve from the page.
                - columns_from_blocks (dict, optional):
                Mapping of columns to retrieve from the blocks.

        Returns:
            DataFrame: A pandas DataFrame containing the data from the specified Notion database.

        This method handles paginated results and retrieves properties from both pages and blocks.
        """
        if 'filter_params' not in kwargs or kwargs['filter_params'] is None:
            filter_params = {}
        else:
            filter_params = kwargs['filter_params']
        if 'columns_from_page' in kwargs:
            columns_from_page = list(kwargs['columns_from_page'].items())
        else:
            columns_from_page = []
        if 'columns_from_blocks' in kwargs:
            columns_from_blocks = list(kwargs['columns_from_blocks'].items())
        else:
            columns_from_blocks = []
        results = self._notion_executor(
            collect_paginated_api,
            **{'function': self.databases.query, **filter_params, "database_id": database_id})
        database_data = []
        for result in results:
            prop_dict = {}
            for notion_property in result.get("properties"):
                column_name = str(notion_property)
                prop_dict[str(notion_property)] = n2p_read_write.read_value_from_notion(
                    result.get("properties").get(notion_property), column_name, self.switcher)
            page_id = result.get("id")
            prop_dict[self._ROW_PAGEID_KEY] = page_id
            _add_custom_columns(page_id, self.retrieve_page, prop_dict, columns_from_page)
            _add_custom_columns(page_id, self.retrieve_block_children_list,
                                prop_dict, columns_from_blocks)
            database_data.append(prop_dict)
        df = pd.DataFrame(database_data)
        df[self._ROW_HASH_KEY] = df.apply(self.__row_hash, axis=1)
        return df

    def update_notion_DB_from_dataframe(self, database_id, df):  # pylint: disable=invalid-name
        """
        Updates a Notion database with data from a pandas DataFrame.

        Args:
            database_id (str): The ID of the Notion database to update.
            df (DataFrame): A pandas DataFrame containing the data to be written to the
            Notion database.

        This method iterates over the rows of the DataFrame, comparing each row's hash
        with the corresponding value in the Notion database. If the hashes differ, it
        updates the existing page or creates a new page if necessary.
        Read-only columns are ignored during the update process.

        The DataFrame is updated in place with the page IDs and hashes for each row
        after the operation.
        """
        columns = self.__get_database_columns_and_types(database_id)
        for index, row in df.iterrows():
            current_row_hash = self.__row_hash(row)
            if current_row_hash != row[self._ROW_HASH_KEY]:
                prop_dict = {}
                for column in columns:
                    column_name = column[0]
                    column_type = column[1]
                    if column_type in self.read_only_columns:
                        continue
                    prop_dict[column_name] = n2p_read_write.write_value_to_notion(
                        row[column_name], column_name, column_type, self.switcher)
                if row[self._ROW_PAGEID_KEY] != '':
                    self._update_page(row[self._ROW_PAGEID_KEY], prop_dict)
                    df.at[index, self._ROW_HASH_KEY] = current_row_hash
                else:
                    page_id = self.create_page(database_id, prop_dict)
                    df.at[index, self._ROW_PAGEID_KEY] = page_id
                    row[self._ROW_PAGEID_KEY] = page_id
                    df.at[index, self._ROW_HASH_KEY] = self.__row_hash(row)

    def __set_n2p_arg(self, kwargs, field_name):
        if field_name in kwargs:
            setattr(self, field_name, kwargs[field_name])
            del kwargs[field_name]
