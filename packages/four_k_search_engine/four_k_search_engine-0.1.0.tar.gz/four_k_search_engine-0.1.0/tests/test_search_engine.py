import logging

from four_k_search_engine_nosrednakram.LoadSearchData import LoadSearchData
from four_k_search_engine_nosrednakram.FilterSet import FilterSet
from four_k_search_engine_nosrednakram.Search import Search


#
# Run with the following prameters to see detailed logging feedback on the set.
#
# pytest -rP
#
logging.basicConfig(level=logging.INFO)
logging.getLogger('four_k_search_engine_nosrednakram.LoadSearchData').propagate = True
logging.getLogger('four_k_search_engine_nosrednakram.LoadSearchData').setLevel(logging.INFO)
logging.getLogger('four_k_search_engine_nosrednakram.FilterSet').propagate = True
logging.getLogger('four_k_search_engine_nosrednakram.FilterSet').setLevel(logging.INFO)
logging.getLogger('four_k_search_engine_nosrednakram.Search').propagate = True
logging.getLogger('four_k_search_engine_nosrednakram.Search').setLevel(logging.INFO)

TestData = [
    {"animal": "cat","name": "George","description": "king of the household", "feeder": "Mark",
     "Days": ["M", "W", "F"]},
    {"animal": "dog", "name": "Dottie", "description": "queen of the household", "feeder": "Nicki",
     "Days": ["M", "T", "W", "F"]},
    {"animal": "dog", "name": "Tigger", "description": "rogue Prince of the household", "feeder": "Mark",
     "Days": ["S", "W", "F"]},
    {"animal": "turtle", "name": "Mirtle", "description": "king of the aquarium", "feeder": "Nicki",
     "Days": ["T", "R", "U"]},
    {"animal": "fish", "name": "Mean Silver Dollar", "description": "king of the aquarium", "feeder": "Nicki",
     "Days": ["S", "S", "W"]},
    {"animal": "fish", "name": "Nice silver Dollar", "description": "chill fish", "feeder": "Nicki",
     "Days": ["S", "S", "W"]}
]




def test_loading_master_list():
    search_data = LoadSearchData(TestData,[])
    assert TestData == search_data.master_list


def test_loading_filter_options():
    search_data = LoadSearchData(TestData,["animal", "feeder"])
    assert "animal" in search_data.filter_options
    assert "feeder" in search_data.filter_options
    assert len(search_data.filter_options["animal"]) == 4
    assert len(search_data.filter_options["feeder"]) == 2
    assert "dog" in search_data.filter_options['animal']
    assert "Nicki" in search_data.filter_options['feeder']


def test_loading_master_index():
    search_data = LoadSearchData(TestData,[])
    assert len(search_data.master_index) == 6
    assert search_data.master_index[3] == 3

def test_filtering():
    search_data = LoadSearchData(TestData,["animal", "feeder"])
    filters = [
        {
            "field": "animal",
            "value": "dog",
            "include": True
        }
    ]
    filtered_list = FilterSet(search_data.master_index, search_data.master_list, filters).results
    assert len(filtered_list) == 2
    for rec in filtered_list:
        assert rec["animal"] == "dog"

    filters = [
        {
            "field": "animal",
            "value": "dog",
            "include": True
        },
        {
            "field": "feeder",
            "value": "Nicki",
            "include": True
        }
    ]
    filtered_list = FilterSet(search_data.master_index, search_data.master_list, filters).results
    assert len(filtered_list) == 1
    for rec in filtered_list:
        assert rec['feeder'] == "Nicki"

    search_data = LoadSearchData(TestData,["animal", "feeder"])
    filters = [
        {
            "field": "animal",
            "value": "dog",
            "include": False
        }
    ]
    filtered_list = FilterSet(search_data.master_index, search_data.master_list, filters).results
    assert len(filtered_list) == 4
    for rec in filtered_list:
        assert rec["animal"] != "dog"

def test_searching():
    search_data = LoadSearchData(TestData,[])
    searches = [
        {
            "field": "Shound Not Fail with Bad Key",
            "value": "silver"
        }
    ]
    search_results = Search(search_data.master_list, searches).results

    searches = [
        {
            "field": "name",
            "value": "silver"
        }
    ]
    search_results = Search(search_data.master_list, searches).results
    # We ignore case on string searches
    assert len(search_results) == 2
    for rec in search_results:
        assert rec["animal"] == "fish"

    searches = [
        {
            "field": "name",
            "value": "silver"
        },
        {
            "field": "description",
            "value": "CHILL"
        }
    ]
    search_results = Search(search_data.master_list, searches).results
    assert len(search_results) == 2

    searches = [
        {
            "field": "description",
            "value": "CHILL"
        }
    ]
    search_results = Search(search_data.master_list, searches).results
    assert len(search_results) == 1
    assert search_results[0]["description"] == "chill fish"
