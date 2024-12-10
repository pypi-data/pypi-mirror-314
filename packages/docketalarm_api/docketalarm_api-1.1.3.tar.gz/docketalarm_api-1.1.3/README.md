# DocketAlarmAPI
API Wrapper for DocketAlarm.
# Table of Contents
1. [Installation and usage](#usage)
2. [Get Login Token](#get_login_token)
3. [Search](#search)
4. [Scroll](#search_scroll)
5. [Get Docket](#get_docket)
6. [Get Document](#get_document_binary)
7. [Ask Docket](#ask_docket)
8. [Case Matcher](#case_matcher)
9. [Smart Search](#smart_search)
10. [Attorney Billing Rates](#attorney_billing_rates)
11. [Get Complaint Summary](#get_complaint_summary)
12. [Get Cause of Action](#get_cause_of_action)
13. [Area of Law](#area_of_law)
14. [Forum and Venues](#forum_and_venues)

# usage
Use `pip install docketalarm_api` to install this library.  
To use the DocketAlarmClient you'll need your DocketAlarm user and password, and if desired to interact with OpenAI powered endpoints, an OpenAI API Key.  
Import and initialize the client as follows:
```
from docketalarm_api import DocketAlarmClient

da_client = DocketAlarmClient(<your-docketalarm-user>, <your-docketalarm-password>, <your-openai-api-key>, <your-anthropic-api-key>)
```

## Without AI keys
You can initialize the client without an OpenAI API key or an Anthropic API key, but you will not be able
to interact with AI endpoints.
```
from docketalarm_api import DocketAlarmClient

da_client = DocketAlarmClient(<your-docketalarm-user>, <your-docketalarm-password>)
```

## With OpenAI key only
You can initialize the client with only an OpenAI API key as follows:
```
from docketalarm_api import DocketAlarmClient, GPT_4O_MINI

da_client = DocketAlarmClient(<your-docketalarm-user>, <your-docketalarm-password>, <your-openai-api-key>)
```
In this case you will be able to interact with AI endpoints directly without having to explicitly specify a model
(GPT_4O is used as default) but you can import some models as in the example.

## With Anthropic key only
You can also initialize the client with only an Anthropic API key as follows:
```
from docketalarm_api import DocketAlarmClient, CLAUDE_3_5_SONNET

da_client = DocketAlarmClient(<your-docketalarm-user>, <your-docketalarm-password>, anthropic_api_key=<your-anthropic-api-key>)
```

## IMPORTANT
When using both keys or only an Anthropic API key you will have to **explicitly** provide
the **claude_model** param/keyword argument to be used on the call, if it's desired to use Claude.

An AI method will attempt to use the OpenAI key by default

You can import different models from the "*docketalarm_api*" module:

GPT_3_5_TURBO, GPT_4_TURBO, GPT_4O_MINI, GPT_4O, CLAUDE_3_HAIKU, CLAUDE_3_SONNET, CLAUDE_3_5_SONNET

# General Endpoints
These are methods available directly to your DocketAlarm user through a `DocketAlarmClient` instance.

## get_login_token
Get authentication token from DocketAlarm.  

**Example**:

```
    login_token = da_client.get_login_token()
```

## search
Perform a search on DocketAlarm API's search endpoint.  

| Parameter    | Description                                         |
|--------------|-----------------------------------------------------|
| query        | The DocketAlarm query to use.                       |
| order        | The order to get the results by.                    |
| limit        | The search limit, must be 50 or less.               |
| offset       | Offset for the search, useful for pagination.       |
| login_token  | Will be created if not provided.                    |
| return       | Dictionary with JSON response.                      |

**Example**:

```
    response = da_client.search("is:docket AND is:state", "random", limit=10)
    search_results = response["search_results"]
```

## search_scroll
Perform a scroll search on DocketAlarm API.  

| Parameter       | Description                                                                                                                                                                 |
|-----------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| query           | The DocketAlarm query to use.                                                                                                                                               |
| order           | The order to get the results by.                                                                                                                                            |
| limit           | The search limit, must be 50 or less.                                                                                                                                       |
| offset          | Offset for the search, useful for pagination.                                                                                                                               |
| login_token     | Will be created if not provided.                                                                                                                                            |
| scroll_parallel | Number of parallel threads, or bins, to divide the search results into for scanning                                                                                         |
| scroll_index    | Individual thread, or bin, of the scroll_parallel threads indexed from 0 to scroll_parallel-1                                                                               |
| scroll          | String produced for each thread when first setting scroll_index and scroll_parallel outputted as another field with key “scroll.” Pass this value into all subsequent calls |
| return          | Dictionary with JSON response.                                                                                                                                              |

**Example**:

```
    # SET UP
    response_index_0 = da_client.search_scroll(query="is:docket from:-7days court:(California)",
                                               order="-date_filed", scroll_parallel=2, scroll_index=0)
    
    response_index_1 = da_client.search_scroll(query="is:docket from:-7days court:(California)",
                                               order="-date_filed", scroll_parallel=2, scroll_index=1)
                                        
    search_results = response_index_0["search_results"] + response_index_1["search_results"]
    
    # SCROLLING
    scrolling_index_0 = da_client.search_scroll(query="is:docket from:-7days court:(California)",
                                         order="-date_filed", scroll=response_index_0["scroll"])
    
    search_results.extend(scrolling_index_0.get("search_results", []))

    scrolling_index_1 = da_client.search_scroll(query="is:docket from:-7days court:(California)",
                                         order="-date_filed", scroll=response_index_1["scroll"])
    
    
    search_results.extend(scrolling_index_1.get("search_results", []))
    
    # Could loop until no more results in any of the responses.
    # Make sure to always use the previous call's scroll value as a scroll parameter
```

## get_docket
Interact with getdocket endpoint, fetching a docket by court and docket number.  

| Parameter                | Description                                                 |
|--------------------------|-------------------------------------------------------------|
| docket                   | The docket number obtained from search.                     |
| court                    | The court of the docket obtained from search.               |
| timeout                  | Timeout for the GET request.                                |
| client_matter            | The client matter for the API call.                         |
| normalize                | Normalize option for getdocket endpoint.                    |
| cached                   | Defaults to True, gets cached version of the docket.        |
| login_token              | If not provided it's auto-generated.                        |
| check_is_pacer           | Include a boolean stating if the case is from a PACER court |
| add_documents_by_entries | Include a list of all documents per entry on the response   |
| return                   | Dictionary with JSON response.                              |

**Example**:

```
    docket_data = da_client.get_docket(docket="JC205-106", court="Texas State, Grayson County, Justice of the Peace 2")
```

## get_document_binary
Fetches the binary content of a pdf stored in DocketAlarm or directly from the court.  

| Parameter     | Description                                                              |
|---------------|--------------------------------------------------------------------------|
| doc_url       | URL for the document.                                                    |
| login_token   | Token for OpenAI authentication.                                         |
| client_matter | The matter or client for the API call.                                   |
| cached        | Boolean stating if desired to use cached version of the document or not. |
| return        | Document binary (bytes).                                                 |

**Example**:

```
    document_bytes = da_client.get_document_binary(
        'https://www.docketalarm.com/cases/Arkansas_State_Faulkner_County_Circuit_Court/23DR-98-821/OCSE_V_JOHN_TAYLOR/docs/28082014_OTHER_0.pdf'
    )
```

# AI Endpoints

These methods require the use of an AI API key, supplied when initializing the instance.
This AI API key can be an OpenAI API key or an Anthropic API key.

Remember that when it's desired to interact with an AI endpoint using Claude, the **claude_model** param has to be provided

## ask_docket
Interact with DocketAlarm's ask_docket OpenAI endpoint.  

| Parameter     | Description                                                              |
|---------------|--------------------------------------------------------------------------|
| docket        | The docket number as extracted from search.                              |
| court         | The court of the docket as extracted from search.                        |
| question      | The question to ask to the docket data.                                  |
| output_format | The output format of the desired response in natural language.           |
| target        | The target for ask_docket, "docket", "documents" or "both".              |
| openai_model  | Model to be used on OpenAI interactions, defaults to gpt-4o.             |
| claude_model  | Model to be used on Claude interactions, defaults to claude-3.5-sonnet   |
| cached        | Gets cached version of the docket on the interaction, defaults to False. |
| show_relevant | Gets relevant data used by ask_docket.                                   |
| login_token   | If not provided, it is autogenerated.                                    |
| timeout       | The timeout for the request.                                             |
| return        | Dictionary with JSON response.                                           |

**Examples**:

Using OpenAI
```
    response = da_client.ask_docket(docket='JC205-106', court='Texas State, Grayson County, Justice of the Peace 2',
                                    question='is the case pre or post discovery stages?',
                                    output_format='Enum["pre" or "post" or "unknown"]',
                                    target="docket", cached = True)

    openai_answer = response["from_dockets"]["openai_answer"]
```

Using Claude
```
    from docketalarm_api import CLAUDE_3_5_SONNET
    
    
    response = da_client.ask_docket(docket='JC205-106', court='Texas State, Grayson County, Justice of the Peace 2',
                                    question='is the case pre or post discovery stages?',
                                    output_format='Enum["pre" or "post" or "unknown"]',
                                    target="docket", cached=True, claude_model=CLAUDE_3_5_SONNET)

    claude_answer = response["from_dockets"]["claude_answer"]
```

## case_matcher
Match a case from any input provided using DocketAlarm's OpenAI powered case_matcher endpoint.  

| Parameter     | Description                                                            |
|---------------|------------------------------------------------------------------------|
| openai_model  | Model to be used on OpenAI interactions, defaults to gpt-4o.           |
| claude_model  | Model to be used on Claude interactions, defaults to claude-3.5-sonnet |
| timeout       | The timeout for the request.                                           |
| kwargs        | Provide any argument and it will be used as inputs in case matcher.    |
| return        | Dictionary with result from case matcher and AI costs incurred.        |

**Examples**:

Using OpenAI
```
    from docketalarm_api import GPT_4_TURBO
    
    
    response = da_client.case_matcher(openai_model=GPT_4_TURBO,
                                      description="A PACER case involving Cloud Systems HoldCo in California")
    case_link = response["result"]["Link"]
```

Using Claude
```
    from docketalarm_api import CLAUDE_3_5_SONNET
    
    
    response = da_client.case_matcher(claude_model=CLAUDE_3_5_SONNET,
                                      description="A PACER case involving Cloud Systems HoldCo in California")
    case_link = response["result"]["Link"]
```

## smart_search
Return a query for DocketAlarm search based on instructions in natural language  

| Parameter     | Description                                                            |
|---------------|------------------------------------------------------------------------|
| instructions  | Instructions to build a query by.                                      |
| openai_model  | Model to be used on OpenAI interactions, defaults to gpt-4o.           |
| claude_model  | Model to be used on Claude interactions, defaults to claude-3.5-sonnet |
| login_token   | If not provided, it will be auto-generated.                            |
| timeout       | The timeout for the request.                                           |
| return        | Dictionary with query and AI costs incurred.                           |

**Examples**:

Using OpenAI:
```
    response = da_client.smart_search(
        instructions="Cases involving Ford Motor in New York, that span from December 2014 to june 2019"
    )
    query = response["query"]
```

Using Claude:
```
    from docketalarm_api import CLAUDE_3_5_SONNET


    response = da_client.smart_search(
        instructions="Cases involving Ford Motor in New York, that span from December 2014 to june 2019",
        claude_model=CLAUDE_3_5_SONNET
    )
    query = response["query"]
```

## attorney_billing_rates
Extract attorney billing rates by name and state.  

| Parameter     | Description                                                            |
|---------------|------------------------------------------------------------------------|
| attorney_name | The name of the attorney for which billing rates are to be extracted.  |
| state         | The state of the attorney.                                             |
| openai_model  | Model to be used on OpenAI interactions, defaults to gpt-4o.           |
| claude_model  | Model to be used on Claude interactions, defaults to claude-3.5-sonnet |
| login_token   | Auto-generated by default.                                             |
| client_matter | Empty by default.                                                      |
| timeout       | The timeout for the request.                                           |
| return        | Dictionary with result and AI costs incurred.                          |

**Examples**

Using OpenAI:
```
    response = da_client.attorney_billing_rates(attorney_name="ashley marshal",
                                                state="connecticut")
    attorney_data = response["result"]
```

Using Claude:
```
    from docketalarm_api import CLAUDE_3_5_SONNET
    
    
    response = da_client.attorney_billing_rates(attorney_name="ashley marshal",
                                                state="connecticut",
                                                claude_model=CLAUDE_3_5_SONNET)
    attorney_data = response["result"]
```

## get_complaint_summary
Get a summary of the legal complaint in the docket.  

| Parameter       | Description                                                            |
|-----------------|------------------------------------------------------------------------|
| docket          | Docket number.                                                         |
| court           | The court of the docket.                                               |
| openai_model    | Model to be used on OpenAI interactions, defaults to gpt-4o.           |
| claude_model    | Model to be used on Claude interactions, defaults to claude-3.5-sonnet |
| login_token     | Auto-generated by default.                                             |
| cached          | Bool stating if desired to use cached version of the docket.           |
| short           | Extract a short complaint summary.                                     |
| timeout         | The timeout for the request.                                           |
| return          | Dictionary with result and AI costs incurred.                          |

**Examples**:

Using OpenAI:
```
    from docketalarm_api import GPT_4O
    
    
    response = da_client.get_complaint_summary(docket="JC205-106", court="Texas State, Grayson County, Justice of the Peace 2",
                                            short=True, openai_model=GPT_4O, cached=True)
    openai_answer = response["openai_answer"]
```

Using Claude:
```
    from docketalarm_api import CLAUDE_3_5_SONNET
    
    
    response = da_client.get_complaint_summary(docket="JC205-106", court="Texas State, Grayson County, Justice of the Peace 2",
                                               short=True, claude_model=CLAUDE_3_5_SONNET, cached=True)
    claude_answer = response["claude_answer"]
```

## get_cause_of_action
Get the causes of action from a legal complaint.  

| Parameter       | Description                                                            |
|-----------------|------------------------------------------------------------------------|
| docket          | Docket number.                                                         |
| court           | The court of the docket.                                               |
| openai_model    | Model to be used on OpenAI interactions, defaults to gpt-4o.           |
| claude_model    | Model to be used on Claude interactions, defaults to claude-3.5-sonnet |
| login_token     | Auto-generated by default.                                             |
| cached          | Bool stating if desired to use cached version of the docket.           |
| timeout         | The timeout for the request.                                           |
| return          | Dictionary with result and AI costs incurred.                          |

**Examples**:

Using OpenAI:
```
    from docketalarm_api import GPT_4O
    
    
    response = da_client.get_cause_of_action(docket="JC205-106", court="Texas State, Grayson County, Justice of the Peace 2",
                                            openai_model=GPT_4O, cached=True)
    openai_answer = response["openai_answer"]
```

Using Claude:
```
    from docketalarm_api import CLAUDE_3_5_SONNET
    
    
    response = da_client.get_cause_of_action(docket="JC205-106", court="Texas State, Grayson County, Justice of the Peace 2",
                                            claude_model=CLAUDE_3_5_SONNET, cached=True)
    claude_answer = response["claude_answer"]
```

## entity_normalizer
Get a DocketAlarm query for the entity normalized  

| Parameter          | Description                                                            |
|--------------------|------------------------------------------------------------------------|
| entity             | The entity to normalize.                                               |
| include_corp_group | Boolean stating if desired to include corporation group matches.       |
| search_limit       | The internal search limit when optimizing. Must be between 10 and 50.  |
| login_token        | If not provided, it is autogenerated.                                  |
| openai_model       | Model to be used on OpenAI interactions, defaults to gpt-4o.           |
| claude_model       | Model to be used on Claude interactions, defaults to claude-3.5-sonnet |
| timeout            | The timeout for the request.                                           |
| return             | Dictionary with result and AI costs incurred.                          |

**Examples**:

Using OpenAI:
```
    response = da_client.entity_normalizer(entity="Apple", search_limit=20,
                                           include_corp_group=True)
    query = response["query"]
```

Using Claude:
```
    from docketalarm_api import CLAUDE_3_5_SONNET
    
    
    response = da_client.entity_normalizer(entity="Apple", search_limit=20,
                                           include_corp_group=True,
                                           claude_model=CLAUDE_3_5_SONNET)
    query = response["query"]
```

## area_of_law
Get the area of law SALI tag from a provided case type or NOS code.

| Parameter    | Description                                                            |
|--------------|------------------------------------------------------------------------|
| case_type    | The case type or NOS code from the docket                              |
| openai_model | Model to be used on OpenAI interactions, defaults to gpt-4o.           |
| claude_model | Model to be used on Claude interactions, defaults to claude-3.5-sonnet |
| timeout      | The timeout for the request.                                           |
| login_token  | If not provided, it is autogenerated.                                  |
| return       | Dictionary with result and AI costs incurred.                          |

**Examples**:

Using OpenAI:
```
    response = da_client.area_of_law("Design - D23/262000")
    tag = response["tag"]
```

Using Claude:
```
    from docketalarm_api import CLAUDE_3_HAIKU
    
    
    response = da_client.area_of_law("Design - D23/262000", claude_model=CLAUDE_3_HAIKU)
    tag = response["tag"]
```

## forum_and_venues
Get the forum and venues SALI tag from a provided court.

| Parameter    | Description                                                            |
|--------------|------------------------------------------------------------------------|
| court        | The court from the docket                                              |
| openai_model | Model to be used on OpenAI interactions, defaults to gpt-4o.           |
| claude_model | Model to be used on Claude interactions, defaults to claude-3.5-sonnet |
| timeout      | The timeout for the request.                                           |
| login_token  | If not provided, it is autogenerated.                                  |
| return       | Dictionary with result and AI costs incurred.                          |

**Examples**:

Using OpenAI:
```
    response = da_client.forum_and_venues("U.S. Patent Application")
    tag = response["tag"]
```

Using Claude:
```
    from docketalarm_api import CLAUDE_3_HAIKU
    
    
    response = da_client.forum_and_venues("U.S. Patent Application", claude_model=CLAUDE_3_HAIKU)
    tag = response["tag"]
```