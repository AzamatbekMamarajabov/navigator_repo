"""This file is for views, main operations are done here"""
import csv
import logging

from datetime import datetime
from django.shortcuts import render
from django.views.generic import FormView
from django.http import HttpResponse

import requests

from .forms import SearchForm
from .constants import GITHUB_API, LOG_FILE, GlobalVariable  # BITBUCKET_API


GLOBAL_VARIABLE = GlobalVariable()


class HomeSearchView(FormView):  # pylint: disable=too-many-ancestors
    """This class is for home search view, by this views repositories are searched"""
    template_name = 'home.html'
    form_class = SearchForm
    logging.basicConfig(filename=LOG_FILE,
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)

    def get(self, request, *args, **kwargs):

        if request.method == 'GET' and 'search_term' in request.GET:

            query = request.GET.get('search_term', '')

            res = search_term(query)
            form = self.form_class(request.GET)
            names, dates, commits_query = github_parsing(res)
            commit_message, committer = commits_parsing(commits_query)

            data = names, dates, commit_message, committer
            GLOBAL_VARIABLE.set_current_data(data)
            logging.info(" GET request is working")
            return render(
                request, self.template_name, {
                    'form': form, 'names': names,
                    'dates': dates,
                    'commit_message': commit_message,
                    'committer': committer,
                })
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST)
        if form.is_valid():
            query = form.cleaned_data['search']
            res = search_term(query)

            names, dates, commits_query = github_parsing(res)

            commit_message, committer = commits_parsing(commits_query)
            data = names, dates, commit_message, committer

            GLOBAL_VARIABLE.set_current_data(data)
            return render(
                request, self.template_name, {
                    'form': form, 'names': names,
                    'dates': dates,
                    'commit_message': commit_message,
                    'committer': committer,
                })

        return render(request, self.template_name, {'form': form})


def search_term(query):
    """This funtion is used for getting requests from github or bitbucket accordingly"""
    results = {}
    logging.info("GET request search query is working")
    try:
        results = requests.get(
            GITHUB_API+query+'&per_page=10&sort=updated&order=desc')
        logging.info("GET request search query is working by github api")
    except requests.ConnectionError as exception:
        return f'{exception}'
    return results


def github_parsing(query):
    """This funtion is used for making parsing on github query"""
    logging.info("GET request github parsing is working")
    host = 'github'
    GLOBAL_VARIABLE.set_host_name(host)
    json_all = query.json()
    json_items = json_all['items']
    clear_list_name = []
    clear_list_created_at = []
    clear_list_commits_url = []

    for items in json_items:
        clear_list_name += {items['name']}
        clear_list_created_at += {items['updated_at']}
        clear_list_commits_url += {items['commits_url']}

    return clear_list_name, clear_list_created_at, clear_list_commits_url


def commits_parsing(query):
    """This funtion is used for making parsing on query taken from github commits """
    logging.info("GET request commit parsing is working")
    results = {}
    list_of_commits = []
    clear_list_message = []
    clear_list_committer = []
    json_commits = {}
    json_all = {}
    for single_query in query:
        list_of_commits += {single_query[:-6]}

        try:
            results = requests.get(single_query[:-6])
        except requests.ConnectionError as exception:
            return f'{exception}'

        json_all = results.json()[0]

        json_commits = json_all['commit']
        clear_list_message += {json_commits['message']}
        clear_list_committer += {json_commits['committer']['name']}

    return clear_list_message, clear_list_committer


def csv_download_view(request):
    """This funtion is used for downloading result as a csv file """
    logging.info(" CSV file download is working")
    now = datetime.now()
    timestamp = now.strftime("%Y_%m_%d")
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="results_' + \
        GLOBAL_VARIABLE.get_host_name()+'_'+timestamp+'.csv"'

    writer = csv.writer(response)
    list_of_cd = list(GLOBAL_VARIABLE.get_current_data())

    for i in range(10):
        rows = [sub_list[i] for sub_list in list_of_cd]
        writer.writerow(rows)

    return response
