import requests
import logging
import json
import re
import time

from urllib.parse import urlencode


LOGIN_TOKEN_TIME_LIMIT = 60*30
GPT_3_5_TURBO = "gpt-3.5-turbo-0125"
GPT_4O_MINI = "gpt-4o-mini"
GPT_4_TURBO = "gpt-4-turbo"
GPT_4O = "gpt-4o"
CLAUDE_3_HAIKU = "claude-3-haiku-20240307"
CLAUDE_3_SONNET = "claude-3-sonnet-20240229"
CLAUDE_3_5_SONNET = "claude-3-5-sonnet-20240620"


class BadRequest(Exception):
    def __init__(self, message, code=None):
        self._code = code
        super().__init__(message)
    
    @property
    def code(self):
        return self._code


class DocumentNotCached(BadRequest):
    def __init__(self):
        super().__init__("Document has not been cached", 412)
        

class DocumentNotAvailable(BadRequest):
    def __init__(self):
        super().__init__("Document is unavailable or sealed", 403)


def aimethod(func):
    def wrapper(self, *args, **kwargs):
        # Use anthropic key if claude model is provided
        if "claude_model" in kwargs:
            kwargs["claude_model"] = kwargs["claude_model"] or CLAUDE_3_5_SONNET
            assert self.is_ai_api_key_valid(self._anthropic_api_key), "Valid Anthropic Key not set"
            kwargs["anthropic_key"] = self._anthropic_api_key
            return func(self, *args, **kwargs)
        
        # Otherwise use openai key
        kwargs["openai_model"] = kwargs.get("openai_model") or GPT_4O
        assert self.is_ai_api_key_valid(self._openai_api_key), "Valid OpenAI Key not set"
        kwargs["openai_key"] = self._openai_api_key
        return func(self, *args, **kwargs)
    return wrapper


class DocketAlarmClient:
    """
    Main client to interact with DocketAlarm API endpoints
    :param user: DocketAlarm user
    :param password: DocketAlarm password
    :param openai_api_key: OpenAI API key to use on VIDA Endpoints
    :param anthropic_api_key: Anthropic API key to use on VIDA Endpoints
    """
    URL = "https://www.docketalarm.com/api/v1/"

    def __init__(self, user: str, password: str, openai_api_key: str = "", anthropic_api_key: str = "") -> None:
        self._user = user
        self._password = password
        self._openai_api_key = openai_api_key
        self._anthropic_api_key = anthropic_api_key
        self._login_token = None
        self._login_token_time = None

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
            
    def __get_ai_key_on_params(self, params, **kwargs):
        """
        Add anthropic_key or openai_key to request param from kwargs.
        :param params: request params dictionary.
        """
        if "anthropic_key" in kwargs:
            assert "claude_model" in kwargs, "Claude model expected"
            params["anthropic_key"] = self._anthropic_api_key

        if "openai_key" in kwargs:
            assert "openai_model" in kwargs, "OpenAI model expected"
            params["openai_key"] = self._openai_api_key

    def _create_ai_request_params(self, basic_params: list[tuple], extra_keys: list[str], **kwargs) -> dict:
        """
        Arrange the request params for an ai endpoint.
        :param basic_params: Basic request params.
        :param extra_keys: keys to check if present on kwargs.
        """
        params = dict(basic_params + [(kw, kwargs[kw]) for kw in kwargs if kw in extra_keys])
        self.__get_ai_key_on_params(params, **kwargs)
        return params

    def get_login_token(self) -> str:
        """
        Get login token
        :return: token (str)
        """
        token_age = time.time() - self._login_token_time if self._login_token else None
        if token_age and token_age < LOGIN_TOKEN_TIME_LIMIT:
            self.logger.info("Current token age: %s minutes" % int(token_age//60))
            return self._login_token
        
        self.logger.info("Creating new login token")
        response = self._make_post_request("login/", {"username": self._user,
                                                      "password": self._password})
        
        if not response.get("success"):
            error = response.get('error')
            self.logger.warning("Bad request: %s" % error)
            raise BadRequest(f"error: {error}")
        
        self._login_token = response.get("login_token")
        self._login_token_time = time.time()
        return self._login_token
    
    def __make_request(self, endpoint: str, method: str,
                      data: dict = None, timeout: int = None):
        data = data or {}
        method = method.upper()
        params = {
            "method": method,
            "url": self.URL+endpoint,
            "timeout": timeout
        }

        if method == "POST":
            params["data"] = data

        response = requests.request(**params)
        if (status_code := response.status_code) != 200:
            error = f"status: {response.status_code}, text: {response.text}"
            self.logger.warning("Bad request: %s" % error)
            raise BadRequest(error, code=status_code)
        
        json_response = response.json()
        if not json_response.get("success", False):
            error = json.dumps(json_response)
            self.logger.warning("Bad request: %s" % error)
            raise BadRequest(error)
        
        return json_response
    
    def _make_post_request(self, endpoint: str, data: dict):
        return self.__make_request(endpoint, "POST", data)
    
    def _make_get_request(self, endpoint: str, params: dict = None, timeout: int = None):
        params = params or {}
        endpoint = f"{endpoint}?{urlencode(params)}"
        return self.__make_request(endpoint, "GET", timeout=timeout)

    def search(self, query: str, order: str, limit: int = 50,
               offset: int = 0, login_token: str = "", timeout=None) -> dict:
        """
        Perform a search on DocketAlarm API's search endpoint
        :param query: The DocketAlarm query to use.
        :param order: The order to get the results by.
        :param limit: the search limit, must be 50 or less.
        :param offset: Offset for the search, useful for pagination.
        :param login_token: Will be created if not provided
        :param timeout: The timeout for the request.
        :return: dictionary with json response
        """
        
        login_token = login_token or self.get_login_token()
        
        # Force limit to be at most 50
        limit = limit if isinstance(limit, int) and limit <= 50 else 50

        params = {"login_token": login_token, "q": query, "o": order, "limit": limit, "offset": offset}
        response = self._make_get_request("search/", params, timeout)
        
        return response

    def search_scroll(self, query:str, order:str, limit=50, offset=0, login_token="",
                      scroll_parallel=1, scroll_index=0, scroll="", timeout=None) -> dict:
        """
        Scroll search results on DocketAlarm API.
        If you need to scroll through many thousands or millions of records efficiently, the scroll API can help.
        It also supports parallel searches allowing you to make multiple requests at once.

        SET UP:
            Choose scroll_parallel to be large enough that the resulting threads do not exceed 5000 search results.
            If you do not want parallelism you can set this parameter to 1.
            Make a request per scroll_index, which is indexed from 0 to scroll_parallel - 1

            The response for each request will include a key "scroll" that will be used in subsequent calls.
        
        SCROLL:
            Include "scroll" in your inputs with the latest scroll response value for each setup request.
            You should not include offset, scroll_parallel or scroll_index, but if scroll is provided
            this methods will ignore those parameters.

            With each refresh of this call, more cases will load. Note that each thread will have a different
            scroll value and the scroll value will change with each call of scroll_index and scroll_parallel.

        :param query: The DocketAlarm query to use.
        :param order: The order to get the results by.
        :param limit: the search limit, must be 50 or less.
        :param offset: Offset for the search, useful for pagination.
        :param login_token: Will be created if not provided.
        :param scroll_parallel: number of parallel threads, or bins, to divide the search results into for scanning
        :param scroll_index: Individual thread, or bin, of the scroll_parallel threads indexed from 0 to scroll_parallel-1
        :param scroll: string produced for each thread when first setting scroll_index and scroll_parallel;
                       outputted as another field with key “scroll.” Pass this value into all subsequent calls          
        :param scroll_index: The index 
        :param timeout: The timeout for the request.
        :return: dictionary with json response
        """

        login_token = login_token or self.get_login_token()

        limit = limit if isinstance(limit, int) and limit <= 50 else 50

        params = {"login_token": login_token, "q": query, "o": order, "limit": limit}
        if scroll:
            params["scroll"] = scroll
        else:
            params["offset"] = offset
            params["scroll_parallel"] = scroll_parallel
            params["scroll_index"] = scroll_index
        
        response = self._make_get_request("search/", params, timeout)

        return response
    
    def get_docket(self, docket: str, court: str, **kwargs) -> dict:
        """
        Interact with the getdocket endpoint.
        :param docket: The docket number obtained from search.
        :param court: The court of the docket obtained from search
        :kwarg timeout: Timeout for the GET request.
        :key client_matter: The client matter for the API call.
        :key normalize: normalize option for getdocket endpoint.
        :key cached: Defaults to True, gets cached version of the docket
        :key login_token: If not provided it's auto generated
        :key check_is_pacer: Includes a boolean showing whether the
                               case is from a PACER court or not.
        :key add_documents_by_entries: Includes a list of all documents for
                                     each entry in the main response body 
        :return: dictionary with json response
        """
        timeout = kwargs.get("timeout")
        client_matter = kwargs.get("client_matter", "")
        extra_keys = ["normalize", "cached", "login_token", "check_is_pacer", "add_documents_by_entries"]
        basic_params = [("docket", docket), ("client_matter", client_matter), ("court", court)]
        params = dict(basic_params+[(key, kwargs.get(key)) for key in extra_keys if key in kwargs])

        if "cached" not in params:
            params["cached"] = True
        
        self.logger.info("Fetching docket using cached=%s" % params["cached"])
            
        if not params.get("login_token"):
            params["login_token"] = self.get_login_token()

        return self._make_get_request("getdocket/", params=params, timeout=timeout)
    
    def get_document_binary(self, doc_url: str, login_token: str = "", client_matter: str = "",
                            cached: bool = True, timeout: int = None) -> bytes:
        """
        Fetches the binary content of a pdf stored in DocketAlarm or directly from the court.
        :param doc_url: Url for the document.
        :param login_token: Token for DocketAlarm authentication.
        :param client_matter: The matter or client for the API call.
        :param cached: Boolean stating if desired to use cached version of the document or not.
        :param timeout: The timeout for the request.
        :return: document binary (bytes)
        """
        if not doc_url.endswith(".pdf") or not doc_url.startswith("https://www.docketalarm.com"):
            raise BadRequest("A DocketAlarm document URL must be provided")
        
        login_token = login_token or self.get_login_token()
        
        doc_url += f"?login_token={login_token}"
        if client_matter:
            doc_url += f"&client_matter={client_matter}"
        if cached:
            doc_url += "&cached"

        response = requests.get(doc_url, timeout=timeout)
        if (status_code := response.status_code) == 200:
            return response.content
        
        if status_code == 403:
            raise DocumentNotAvailable()
        
        if status_code == 412:
            raise DocumentNotCached()
        
        raise BadRequest(f"status: {status_code}, text: {response.text}", code=status_code)
    
    @aimethod
    def ask_docket(self, docket: str, court: str, question: str, output_format: dict,
                   target: str, client_matter: str = "", **kwargs) -> dict:
        """
        Interact with ask_docket endpoint.
        :param docket: The docket number as extracted from search.
        :param court: The court of the docket as extracted from search
        :param question: The question to ask the docket data.
        :param output_format: The output format of the desired response in natural language.
        :param target: The target for ask_docket, "dockets", "documents" or "both"
        :param client_matter:
        :key openai_model: Model to be used on openai interactions, by default uses gpt-4o
        :key claude_model: Model to be used on claude interactions, by default uses claude-3.5-sonnet
        :key cached: Gets cached version of the docket on the interaction, defaults to False.
        :key show_relevant: Gets relevant data used by ask_docket.
        :key login_token: If not provided is autogenerated
        :key timeout: The timeout for the request.
        :return: dictionary with json response
        """
        
        extra_keys = ["openai_model", "claude_model", "cached", "show_relevant", "login_token"]
        basic_params = [("docket", docket), ("client_matter", client_matter),
                        ("court", court), ("question", question),
                        ("output_format", output_format), ("target", target)]
        params = self._create_ai_request_params(basic_params, extra_keys, **kwargs)

        if "cached" not in params:
            params["cached"] = True
        
        self.logger.info("Executing ask_docket using cached=%s" % params["cached"])

        if not params.get("login_token"):
            params["login_token"] = self.get_login_token()

        timeout = kwargs.get("timeout")

        return self._make_get_request("VIDA/ask_docket/", params, timeout)

    @aimethod
    def case_matcher(self, **kwargs) -> dict:
        """
        Match a case from any arguments provided.
        Provide any keyword argument and will be used as inputs in case matcher except for the following
        :key openai_model: Model to be used on openai interactions, by default uses gpt-4o
        :key claude_model: Model to be used on claude interactions, by default uses claude-3.5-sonnet
        :key timeout: The timeout for the request.
        :kwargs: Provide any argument and will be used as inputs in case matcher
        :return: dict with result from case matcher and AI costs incurred
        """
        login_token = kwargs.get("login_token", self.get_login_token())
        client_matter = kwargs.get("client_matter", "")

        params = dict(login_token=login_token, client_matter=client_matter, **kwargs)

        timeout = None
        if "timeout" in params:
            timeout = params.pop("timeout")

        self.__get_ai_key_on_params(params, **kwargs)

        return self._make_get_request("VIDA/case_matcher/", params, timeout)
    
    @aimethod
    def smart_search(self, instructions: str, login_token: str = "", **kwargs) -> dict:
        """
        Return a query for DocketAlarm search based on instructions in natural language.
        :param instructions: Instructions to build a query by.
        :param login_token: If not provided will be auto-generated.
        :key openai_model: OpenAI model to be used when generating the query
        :key claude_model: Anthropic Claude model to be used when generating the query
        :key timeout: The timeout for the request.
        :return: dictionary with query and AI costs incurred.
        """
        login_token = login_token or self.get_login_token()
        extra_keys = ["openai_model", "claude_model"]
        basic_params = [("login_token", login_token), ("instructions", instructions)]

        params = self._create_ai_request_params(basic_params, extra_keys, **kwargs)

        timeout = kwargs.get("timeout")

        return self._make_get_request("VIDA/smart_search/", params, timeout)
    
    @aimethod
    def attorney_billing_rates(self, attorney_name: str, state: str = None, **kwargs) -> dict:
        """
        Extract attorney billing rates by name and state.
        :param attorney_name: The name of the attorney for which billing rates are to be extracted.
        :param state: The state of the attorney.
        :key openai_model: Model to be used on openai interactions, by default uses gpt-4o
        :key claude_model: Model to be used on claude interactions, by default uses claude-3.5-sonnet
        :key login_token: Auto generated by default.
        :key client_matter: Empty by default.
        :key timeout: The timeout for the request.
        :return: dictionary with result and AI costs incurred
        """
        extra_keys = ["openai_model", "claude_model", "login_token", "client_matter"]
        basic_params = [("attorney_name", attorney_name), ("state", state)]
        params = self._create_ai_request_params(basic_params, extra_keys, **kwargs)

        if not params.get("login_token"):
            params["login_token"] = self.get_login_token()
    
        if not params.get("client_matter"):
            params["client_matter"] = ""

        timeout = kwargs.get("timeout")

        return self._make_get_request("VIDA/attorney_billing_rates/", params, timeout)
    
    @aimethod
    def get_complaint_summary(self, docket: str, court: str, **kwargs) -> dict:
        """
        Get a summary of the legal complaint in the docket.
        :param docket: Docket number.
        :param court: The court of the docket.
        :key openai_model: The OpenAI model to be used on the API call.
        :key claude_model: The Anthropic Claude model to be used on the API call.
        :key login_token: Auto generated by default.
        :key cached: Bool stating if desired to use cached version of the docket.
        :key short: Extract a short complaint summary
        :key timeout: The timeout for the request.
        :return: dictionary with complaint summary and AI costs incurred
        """
        extra_keys = ["openai_model", "claude_model", "login_token", "cached", "short"]
        basic_params = [("docket", docket), ("court", court)]
        params = self._create_ai_request_params(basic_params, extra_keys, **kwargs)

        if not params.get("login_token"):
            params["login_token"] = self.get_login_token()
        
        timeout = kwargs.get("timeout")

        return self._make_get_request("VIDA/get_complaint_summary/", params, timeout)

    @aimethod
    def get_cause_of_action(self, docket: str, court: str, **kwargs) -> dict:
        """
        Get the causes of action from a legal complaint.
        :param docket: Docket number.
        :param court: The court of the docket.
        :key openai_model: Model to be used on openai interactions, by default uses gpt-4o
        :key claude_model: Model to be used on claude interactions, by default uses claude-3.5-sonnet
        :key login_token: Auto generated by default.
        :key cached: Bool stating if desired to use cached version of the docket.
        :key timeout: The timeout for the request.
        :return: Dictionary with cause of action and AI costs incurred
        """
        extra_keys = ["openai_model", "claude_model", "login_token", "cached"]
        basic_params = [("docket", docket), ("court", court)]
        params = self._create_ai_request_params(basic_params, extra_keys, **kwargs)

        if not params.get("login_token"):
            params["login_token"] = self.get_login_token()

        timeout = kwargs.get("timeout")
        
        return self._make_get_request("VIDA/get_cause_of_action/", params, timeout)

    @aimethod
    def entity_normalizer(self, entity, include_corp_group: bool = False,
                          search_limit: int = 10, login_token: str = "", **kwargs) -> dict:
        """
        Get a DocketAlarm query for the entity normalized
        :param entity: The entity to normalize.
        :param include_corp_group: Boolean stating if desired to include corporation group matches.
        :param search_limit: The internal search limit when optimizing. Must be between 10 and 50.
        :param login_token: If not provided is autogenerated.
        :key openai_model: Model to be used on openai interactions, by default uses gpt-4o
        :key claude_model: Model to be used on claude interactions, by default uses claude-3.5-sonnet
        :key timeout: The timeout for the request.
        :return: Dictionary with the query for the normalized entity
        """
        login_token = login_token or self.get_login_token()
        basic_params = [("entity", entity), ("login_token", login_token), ("search_limit", search_limit)]
        extra_keys = ["openai_model", "claude_model"]

        params = self._create_ai_request_params(basic_params, extra_keys, **kwargs)
        if include_corp_group:
            params["include_corporate_group"] = True

        timeout = kwargs.get("timeout")
        
        return self._make_get_request("VIDA/entity_normalizer/", params, timeout)
    
    @aimethod
    def area_of_law(self, case_type: str, **kwargs) -> dict:
        """
        Interact with the SALI tags endpoint "area of law"
        :param case_type: The case type or NOS code for the case.
        :key openai_model: The model for OpenAI interactions.
        :key claude_model: The model for Anthropic AI interactions.
        :key timeout: The timeout for the request.
        :key login_token: If not provided is generated during the call
        :return: Dictionary with response and SALI tag.
        """
        basic_params = [("case_type", case_type)]
        extra_keys = ["openai_model", "claude_model", "login_token"]

        params = self._create_ai_request_params(basic_params, extra_keys, **kwargs)

        if not params.get("login_token"):
            params["login_token"] = self.get_login_token()

        timeout = kwargs.get("timeout")

        return self._make_get_request("VIDA/area_of_law/", params, timeout)
    
    @aimethod
    def forum_and_venues(self, court: str, **kwargs) -> dict:
        """
        Interact with the SALI tags endpoint "forums and venues"
        :param court: The court for the case.
        :key openai_model: The model for OpenAI interactions.
        :key claude_model: The model for Anthropic AI interactions.
        :key timeout: The timeout for the request.
        :key login_token: If not provided is generated during the call
        :return: Dictionary with response and SALI tag.
        """
        basic_params = [("court", court)]
        extra_keys = ["openai_model", "claude_model", "login_token"]

        params = self._create_ai_request_params(basic_params, extra_keys, **kwargs)

        if not params.get("login_token"):
            params["login_token"] = self.get_login_token()

        timeout = kwargs.get("timeout")

        return self._make_get_request("VIDA/forum_and_venues/", params, timeout)

    @staticmethod
    def is_ai_api_key_valid(ai_api_key: str) -> bool:
        """
        Check if an OpenAI API key is valid or not.
        :param ai_api_key: The key to check.
        :return: bool
        """
        if not ai_api_key:
            return False
        
        pattern = re.compile(r'^(sk-|Bearer )?.+$')
        return bool(re.match(pattern, ai_api_key))
