#!/usr/bin/env python

import requests
import json

import campaign
import subscriber_list
import subscriber


class Api(object):
    """
    Python interface to the mailerlite v1 API.

    Example:
        Create an instance of the Api class using your api key for auth:

            $ api = mailerlite.Api(api_key='your api key')

        Create a new list:

            $ example_list = api.create_list(name='Example List')

        Add a subscriber to example_list:

            $ new_subscriber = api.subscribe(
                  list_id=example_list.id,
                  email='rick@example.com',
                  name=None,
                  fields=None,
                  resubscribe=0
              )

        And then unsubscribe them:

            $ api.unsubscribe(email=new_subscriber.email)
    """

    def __init__(self, api_key):
        """
        Initialize a new mailerlite.api object.

        Args:
            api_key (str): Your mailerlite api_key.
        """
        self.api_key = api_key
        self.url = 'https://app.mailerlite.com/api/v1/'

    # Campaign endpoints

    def all_campaigns(self, limit=1000, page=1):
        """
        Get paginated details of all campaigns from your account.

        http://docs.mailerlite.com/pages/campaigns#getAll

        Args:
            limit (Optional[int]): The number of results per page.
            page (Optional[int]): Given limit=n, increasing this will view the
                next n results.

        Returns:
            A JSON response from the mailerlite API.
        """
        url = self._build_url('campaigns/')
        params = self._build_data({'limit': limit, 'page': page})
        response = self._get(url, params)

        return [campaign.Campaign._new_from_json_dict(x) for x in response['Results']]

    def campaign_details(self, campaign_id):
        """
        Get the details of a campaign.

        http://docs.mailerlite.com/pages/campaigns#get

        Args:
            campaign_id(str): The id of the campaign.

        Returns:
            A JSON response from the mailerlite API.
        """
        url = self._build_url('campaigns/{0}/'.format(campaign_id))
        params = self._build_data()
        response = self._get(url, params)

        return campaign.Campaign._new_from_json_dict(response)

    def campaign_recipients(self, campaign_id, limit=1000, page=1):
        """
        Get a paginated list of all campaign recipients for a given id.

        http://docs.mailerlite.com/pages/campaigns#getRecipients

        Args:
            campaign_id(str): The id of the campaign.
            limit (Optional[int]): The number of results per page.
            page (Optional[int]): Given limit=n, increasing this will view the
                next n results.

        Returns:
            A JSON response from the mailerlite API.
        """
        url = self._build_url('campaigns/{0}/recipients/'.format(campaign_id))
        params = self._build_data()
        response = self._get(url, params)

        return [subscriber.Subscriber._new_from_json_dict(x) for x in response['Results']]

    def campaign_opens(self, campaign_id, limit=1000, page=1):
        """
        Get a paginated list of all campaign opens for a given id.

        http://docs.mailerlite.com/pages/campaigns#getOpens

        Args:
            campaign_id(str): The id of te campaign.
            limit (Optional[int]): The number of results per page.
            page (Optional[int]): Given limit=n, increasing this will view the
                next n results.

        """
        url = self._build_url('campaigns/{0}/opens/'.format(campaign_id))
        params = self._build_data()
        response = self._get(url, params)

        return [subscriber.Subscriber._new_from_json_dict(x) for x in response['Results']]

    def campaign_clicks(self, campaign_id, limit=1000, page=1):
        """
        Get a paginated list of all campaign clicks for a given id.

        http://docs.mailerlite.com/pages/campaigns#getClicks

        Args:
            campaign_id(str): The id of te campaign.
            limit (Optional[int]): The number of results per page.
            page (Optional[int]): Given limit=n, increasing this will view the
                next n results.

        """
        url = self._build_url('campaigns/{0}/clicks/'.format(campaign_id))
        params = self._build_data()
        response = self._get(url, params)

        return [subscriber.Subscriber._new_from_json_dict(x) for x in response['Results']]

    def campaign_unsubscribes(self, campaign_id, limit=1000, page=1):
        """
        Get a paginated list of all campaign unsubscribes for a given id.

        http://docs.mailerlite.com/pages/campaigns#getUnsubscribes

        Args:
            campaign_id(str): The id of te campaign.
            limit (Optional[int]): The number of results per page.
            page (Optional[int]): Given limit=n, increasing this will view the
                next n results.

        """
        url = self._build_url(
            'campaigns/{0}/unsubscribes/'.format(campaign_id)
        )
        params = self._build_data()
        response = self._get(url, params)

        return [subscriber.Subscriber._new_from_json_dict(x) for x in response['Results']]

    def campaign_bounces(self, campaign_id, limit=1000, page=1):
        """
        Get a paginated list of all campaign bounces for a given id.

        http://docs.mailerlite.com/pages/campaigns#getBounces

        Args:
            campaign_id(str): The id of te campaign.
            limit (Optional[int]): The number of results per page.
            page (Optional[int]): Given limit=n, increasing this will view the
                next n results.

        """
        url = self._build_url('campaigns/{0}/bounces/'.format(campaign_id))
        params = self._build_data()
        response = self._get(url, params)

        return [subscriber.Subscriber._new_from_json_dict(x) for x in response['Results']]

    def campaign_spam_complaints(self, campaign_id, limit=1000, page=1):
        """
        Get a paginated list of all campaign spam complaints for a given id.

        http://docs.mailerlite.com/pages/campaigns#getJunk

        Args:
            campaign_id(str): The id of te campaign.
            limit (Optional[int]): The number of results per page.
            page (Optional[int]): Given limit=n, increasing this will view the
                next n results.

        """
        url = self._build_url('campaigns/{0}/junk/'.format(campaign_id))
        params = self._build_data()
        response = self._get(url, params)

        return [subscriber.Subscriber._new_from_json_dict(x) for x in response['Results']]

    # List endpoints

    def all_lists(self, limit=1000, page=1):
        """
        Get a paginated list of details for every list in your account.

        http://docs.mailerlite.com/pages/lists#getAll

        Args:
            limit (Optional[int]): The number of results per page.
            page (Optional[int]): Given limit=n, increasing this will view the
                next n results.

        Returns:
            A list of SubscriberList objects containig the response from the
            mailerlite API.
        """
        url = self._build_url('lists/')
        params = self._build_data({'limit': limit, 'page': page})
        response = self._get(url, params)

        return [subscriber_list.SubscriberList._new_from_json_dict(x) for x in response['Results']]

    def list_details(self, list_id):
        """
        Get the details of a list.

        http://docs.mailerlite.com/pages/lists#get

        Args:
            list_id(str): The id of the list.

        Returns:
            A SubscriberList object containing the response from the
            mailerlite API.
        """
        url = self._build_url('lists/')
        params = self._build_data({'id': list_id})
        response = self._get(url, params)

        return subscriber_list.SubscriberList._new_from_json_dict(
            response['Results'][0]
        )

    def create_list(self, list_name):
        """
        Create a new list.

        http://docs.mailerlite.com/pages/lists#post

        Args:
            list_name(str): The name for the new list.

        Returns:
            A SubscriberList object containing the response from the
            mailerlite API.
        """
        url = self._build_url('lists/')
        data = self._build_data({'name': list_name})
        response = self._post(url, data)
        return response['id']
#        return subscriber_list.SubscriberList._new_from_json_dict(
#            response['Results'][0]
#        )

    def update_list(self, list_id, new_list_name):
        """
        Changes the name of a list.

        http://docs.mailerlite.com/pages/lists#put

        Args:
            list_id(str): The ID of the list to update.
            new_list_name(str): The new name to assign to the list.

        Returns:
            A SubscriberList object containing the response from the
            mailerlite API.
        """
        url = self._build_url('lists/')
        data = self._build_data({'id': list_id, 'name': new_list_name})
        response = self._post(url, params)

        return subscriber_list.SubscriberList._new_from_json_dict(
            response['Results'][0]
        )

    def delete_list(self, list_id):
        """
        Delete a list.

        http://docs.mailerlite.com/pages/lists#delete

        Args:
            list_id(str): The ID of the list to delete.

        Returns:
            A SubscriberList object containing the response from the
            mailerlite API.
        """
        url = self._build_url('lists/')
        params = self._build_data({'id': list_id})
        response = self._delete(url, params)

        return subscriber_list.SubscriberList._new_from_json_dict(
            response['Results'][0]
        )

    def active_subscribers(self, list_id, limit=1000, page=1):
        """
        Returns a paginated list of all active subscribers for a given list.

        http://docs.mailerlite.com/pages/lists#getActive

        Args:
            list_id(str): The ID of the list to query on.
            limit(Optional[int]): The number of results per page.
            page(Optional[int]): Given limit=n, increasing this will view the
                next n results.

        Returns:
            A JSON response from the mailerlite API.
        """
        url = self._build_url('lists/{0}/active/'.format(list_id))
        params = self._build_data({'limit': limit, 'page': page})
        response = self._get(url, params)

        return [subscriber.Subscriber._new_from_json_dict(x) for x in response['Results']]

    def inactive_subscribers(self, list_id, limit=1000, page=1):
        """
        Returns a paginated list of all inactive subscribers for a given list.

        http://docs.mailerlite.com/pages/lists#getUnsubscribed

        Args:
            list_id(str): The ID of the list to query on.
            limit(Optional[int]): The number of results per page.
            page(Optional[int]): Given limit=n, increasing this will view the
                next n results.

        Returns:
            A JSON response from the mailerlite API.
        """
        url = self._build_url('lists/{0}/unsubscribed/'.format(list_id))
        params = self._build_data({'limit': limit, 'page': page})
        response = self._get(url, params)

        return [subscriber.Subscriber._new_from_json_dict(x) for x in response['Results']]

    def bounced_subscribers(self, list_id, limit=1000, page=1):
        """Get all bounced subscribers for a given list.

        http://docs.mailerlite.com/pages/lists#getBounced

        Args:
            list_id(str): The ID of the list to query on.
            limit(Optional[int]): The number of results per page.
            page(Optional[int]): Given limit=n, increasing this will view the
                next n results.

        Returns:
            A JSON response from the mailerlite API.
        """
        url = self._build_url('lists/{0}/bounced/'.format(list_id))
        params = self._build_data({'limit': limit, 'page': page})
        response = self._get(url, params)

        return [subscriber.Subscriber._new_from_json_dict(x) for x in response['Results']]

    # Subscriber endpoints

    def subscribe(self, list_id, email, name=None, fields=None, resubscribe=0):
        """Subscribe a user to a list.

        http://docs.mailerlite.com/pages/subscribers#post

        Args:
            list_id(str): The ID of the list to add a subscriber to.
            email(str): The email address of the new subscriber.
            name(Optional[str]): The name of the new subscriber.
            fields(Optional[dict]): A dictionary containing any custom fields.
                The default options are:
                    last_name
                    company
                    country
                    city
                    phone
                    state
                    zip
            resubscribe(Optional[bool]): Reactivates an existing subscriber,
                default 0.

        Returns:
            A JSON response from the mailerlite API.
        """
        url = self._build_url('subscribers/{0}/'.format(list_id))
        data = self._build_data({
            'id': list_id,
            'email': email,
            'name': name,
            'fields': fields,
            'resubscribe': resubscribe
        })
        response = self._post(url, data)
        return response
        #return subscriber.Subscriber._new_from_json_dict(response['Results'][0])

    def bulk_subscribe(self, list_id, subscribers, resubscribe=0):
        """Subscribe many users to a list.

        http://docs.mailerlite.com/pages/subscribers#postImport

        Args:
            list_id(str): The ID of the list to add a subscriber to.
            subscribers(dict): A dictionary containing many subscribers.
                Example:
                    {
                        {
                            'email': 'user@example.com',
                            'name': 'Rick',
                            'fields': {
                                'last_name': 'Grimes',
                                'company': 'Cynthiana Kentucky Police Dept.'
                            }
                            'resubscribe': 0
                        },
                        {
                            'email': 'user2@example.com',
                            'name': 'Carl',
                            'fields': {
                                'last_name': 'Grimes',
                                'company': 'N/A'
                            }
                            'resubscribe': 0
                        },
                    }
            resubscribe(Optional[bool]): Reactivates an existing subscriber,
                default 0.

        Returns:
            A list of subscriber objects containing all bad emails w/ a message
            giving the reason for rejection.
        """
        url = self._build_url('subscribers/{0}/import'.format(list_id))
        data = self._build_data({
            'id': list_id,
            'subscribers': subscribers,
            'resubscribe': resubscribe
        })
        response = self._post(url, data)

        return [subscriber.Subscriber._new_from_json_dict(x) for x in response['Results']]

    def subscriber_details(self, email, history=0):
        """Get the details of a subscriber.

        http://docs.mailerlite.com/pages/subscribers#get

        Args:
            email(str): The email address of the subscriber.
            history(Optional[bool]): Gets the history of campaigns and
                autoresponder emails received by the subscriber, default 0.

        Returns:
            A JSON response from the mailerlite API.
        """
        url = self._build_url('subscribers/')
        params = self._build_data({'email': email, 'history': history})
        response = self._get(url, params)

        return subscriber.Subscriber._new_from_json_dict(response['Results'][0])

    def delete_subscriber(self, list_id, email):
        """Remove a subscriber from a list.

        http://docs.mailerlite.com/pages/subscribers#delete

        Args:
            list_id(str): The id of the list to remove the user from.
            email(str): The email address of the subscriber to be removed.

        Returns:
            A JSON response from the mailerlite API.
        """
        url = self._build_url('subscribers/{0}/'.format(list_id))
        params = self._build_data({'email': email})
        response = self._delete(url, params)

        return subscriber.Subscriber._new_from_json_dict(response['Results'][0])

    def unsubscribe(self, email):
        """Unsubscribe a user from all campaigns.

        http://docs.mailerlite.com/pages/subscribers#postUnsubscribe

        Args:
            email(str): The email address of the subscriber to be unsubscribed.

        Returns:
            A JSON response from the mailerlite API.
        """
        url = self._build_url('subscribers/unsubscribe/')
        data = self._build_data({'email': email})
        response = self._post(url, data)

        return subscriber.Subscriber._new_from_json_dict(response)

    #######################################################################

    def _build_url(self, path):
        return '{0}{1}'.format(self.url, path)

    def _build_data(self, data={}):
        data['apiKey'] = self.api_key
        return data

    def _get(self, url, params):
        response = requests.get(url, params=params)
        return (json.loads(response.content))

    def _post(self, url, data):
        response = requests.post(url, data=data)
        return (json.loads(response.content))

    def _delete(self, url, params):
        response = requests.delete(url, params=params)
        return (json.loads(response.content))
