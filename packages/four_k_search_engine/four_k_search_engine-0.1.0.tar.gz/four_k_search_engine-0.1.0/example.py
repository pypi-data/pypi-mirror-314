#!/bin/env python
import json
from flask import Flask, jsonify

from four_k_search_engine_nosrednakram.LoadSearchData import LoadSearchData
from four_k_search_engine_nosrednakram.FilterSet import FilterSet
from four_k_search_engine_nosrednakram.Search import Search

with open('HPCharactersDataRaw.json') as search_json:
    search_dict = json.load(search_json)


SearchData = LoadSearchData(search_dict, ['Gender', 'Profession'])

app = Flask(__name__)

@app.route('/filter_options', methods=['GET'])
def query_subjects():
    if len(SearchData.filter_options) > 0:
        return json.dumps({'filter_options': SearchData.filter_options})
    else:
        return jsonify({'error': 'data not found'})

@app.route('/search', methods=['GET'])
def query_search():
    # filters = json.load(request.args.get('filters', type=str))
    filters = [{
                    "field": "Gender",
                    "value": "Female",
                    "include": True
              },
              {
                    "field": "Profession",
                    "value": "Auror",
                    "include": True
              }]
    filtered_list = FilterSet(SearchData.master_index, SearchData.master_list, filters).results
    # searches = json.load(request.args.get('searches',' type=str)
    searches = [{
                    "field": "Name",
                    "value": "tonk"
                }]
    # This is any match not exclusive match. Can change easy enough by looping hear and re-feeding the result
    # and next search filter. I think matching any substring search after filters may be desirable.
    if len(searches) > 0:
        filtered_list = Search(filtered_list, searches).results

    if len(filtered_list) > 0:
        return jsonify(filtered_list)
    else:
        return jsonify({'error': 'data not found'})


if __name__ == '__main__':
    app.run(debug=True)
