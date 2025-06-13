# springserve-python
Python Library for accessing the Springserve API

For more information on using the API, please refer to our Wiki:

https://wiki.springserve.com/display/SSD/API+-+Getting+Started

Installation

-------------

To install from source:

    python setup.py install

To install from pip:

    pip install springserve


To use the [Reporting API](https://springserve.atlassian.net/wiki/spaces/SSD/pages/1588035603/Reporting+API)
with this package, also install [pandas](https://pypi.org/project/pandas/).

Usage
-----------

### Configuration: Using Link ###

Springserve is using link to handle it's configuration.  Link is a way to
centrally configure your database, api handles. It has support for Springserve
api connections.  For more, see the link documentation.  https://link-docs.readthedocs.org/en/latest/

Link will be installed when you install springserve

To configure link for springserve:

Open ipython and run the following. This will edit your link.config.  By default this will be ~/.link/link.config.
You can change this directory location by setting the environment variable  LNK_DIR

Run the following to set up your config:

		In [1]: import springserve

		In [2]: springserve.setup_config()
		Enter a user name: {enter email here}
		Enter password:
		Would you like write[Y/n] y
		writing config to: /Users/{username}/.link/link.config
		done: refreshing config

### Configuration: In Code ####

You can now configure your username and password directly in code instead of
using link.  Here is an example: 

		In [1]: import springserve

		In [2]: springserve.set_credentials(user='blah@blah.com', password="mypassword")

### Configuration: Token Injection ####

If you have many users and you want to store their tokens and inject the token
in for each call you can do that using set_token. Here is an example: 

		In [1]: import springserve

		In [2]: springserve.set_token('56385e9ae7ef6cc35e5c34153f479b858')


### Tab Completion and IPython ###

The python library was built to work seamlessly with tools like IPython. IPython
is an interactive shell that is well suited for adhoc data analysis as well as
general python debugging. One of it's best features is tab completion and
documentation

		In [1]: import springserve

		In [2]: springserve.<tab>

			springserve.API    springserve.demand_tags   springserve.domain_lists  springserve.raw_get springserve.supply_tags

		# see documentation on the get function of supply_tags
		In [3]: springserve.supply_tags.get?

        Signature: springserve.supply_tags.get(path_param=None, reauth=False, **query_params)
        Docstring:
        Make a get request to this api service.  Allows you to pass in arbitrary query paramaters.

        Examples::

            # get all supply_tags
            tags = springserve.supply_tags.get()

            for tag in tags:
                print tag.id, tag.name

            # get one supply tag
            tag = springserve.supply_tag.get(1)
            print tag.id, tag.name

            # get by many ids
            tags = springserve.supply_tags.get(ids=[1,2,3])

            # get users that are account_contacts (ie, using query string # params)
            users = springserve.users.get(account_contact=True)
        File:      /usr/local/lib/python2.7/site-packages/springserve/__init__.py
        Type:      instancemethod

		# get a supply_tag by it's id
		In [4]: tag = springserve.supply_tags.get(1234)

		# see what fields exist on the supply_tag
		In [5]: tag.<tab>

		tag.active                 tag.domain_list_ids        tag.player_size_targeting
		tag.supply_partner_id
		tag.allowed_player_sizes   tag.domain_targeting       tag.rate
		tag.supply_type
		tag.country_codes          tag.id                     tag.raw
		tag.country_targeting      tag.name                   tag.save
		tag.demand_tag_priorities  tag.payment_terms          tag.supply_group_id

		# see the contents of a field
		In [5]: tag.name
		Out[7]: "My Test Tag"

		# change the contents and save it
		In [6]: tag.name = "My New Test Tag"
		In [7]: resp = tag.save()

In addition to working with single responses.  This simple interface makes it
easy to make calls that will return more than one result.


		In [8]: tags = springserve.demand_tags.get()

		In [9]: for tag in tags:
		...:     print tag.name
		...:

		My Tag 1
		My Tag 2

### SpringServe Reporting ###

Below is the documentation for and an example of using SpringServe reporting.
This module requires the `pandas` package to be installed.

        In [10]: springserve.reports.run?
        Signature: springserve.reports.run(start_date=None, end_date=None, interval=None,
        dimensions=None, account_id=None, **kwargs)
        Docstring:
        parameter     options (if applicable)  notes
        ===================================================
        start_date:  "2015-12-01 00:00:00" or "2015-12-01"
        end_date:    "2015-12-02 00:00:00" or "2015-12-01"
        interval:    "hour", "day", "cumulative"
        timezone:    "UTC", "America/New_York"   defaults to America/New_York
        date_range:  Today, Yesterday, Last 7 Days   date_range takes precedence over
        start_date/end_date
        dimensions:  supply_tag_id, demand_tag_id, detected_domain, declared_domain,
        demand_type, supply_type, supply_partner_id, demand_partner_id, supply_group
        domain is only available when using date_range of Today, Yesterday, or Last 7 Days

        the following parameters act as filters; pass an array of values (usually IDs)
        =================================================================================

        supply_tag_ids:  [22423,22375, 25463]
        demand_tag_ids:  [22423,22375, 25463]
        detected_domains:         ["nytimes.com", "weather.com"]
        declared_domains:         ["nytimes.com", "weather.com"]
        supply_types     ["Syndicated","Third-Party"]
        supply_partner_ids:  [30,42,41]
        supply_group_ids:    [13,15,81]
        demand_partner_ids:  [3,10,81]
        demand_types:    ["Vast Only","FLASH"]

        In[11]: report = springserve.reports.run(state_date="2016-09-19", end_date="2016-09-19",
        dimensions=["supply_tag_id"], declared_domains=["nytimes.com", "weather.com"])

        In[12]: report.ok
        Out[12]: True

        Getting next pages of your report
        =================================================================================

        In[11]: report = springserve.reports.run(state_date="2016-09-19", end_date="2016-09-19",
        dimensions=["supply_tag_id"], declared_domains=["nytimes.com", "weather.com"])

        In[11]: report_df = report.to_dataframe()

        In[12]: report.get_next_page()
        Out[12]: True

        This method returns True if it got the next page and False if not, indicating that you
        are already at the last page.
        Note that if you call get_next_page this overwrite the current data and when you call
        to_dataframe the results will only contain the data from the last page you got.

        In[12]: report.get_all_pages()
        Out[12]:

        This method gets all the remaining pages of the report (so if you're currently at page 2 it
        will get page 2 onwards, if you're at page 1 it will get everything) then if you call to_dataframe
        on the report you will get all the data. Note that if this is a very large report it's best
        to get one page at a time so you don't run out of memory.

