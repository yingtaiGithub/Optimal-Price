class Subscriber(object):
    def __init__(self, **kwargs):
        defaults = {
            'email': None,
            'name': None,
            'date': None,
            'groups': None,
            'fields': None,
            'campaigns': None,
            'link': None,
            'reason': None,
            'sent': None,
            'opened': None,
            'clicked': None,
            'message': None,
        }

        for (param, default) in defaults.iteritems():
            setattr(self, param, kwargs.get(param, default))

    def __str__(self):
        return self.AsJsonString()

    def AsJsonString(self):
        return json.dumps(self.AsDict(), sort_keys=True)

    def AsDict(self):
        data = {}

        if self.email:
            data['email'] = self.email
        if self.name:
            data['name'] = self.name
        if self.date:
            data['date'] = self.date
        if self.groups:
            data['groups'] = self.groups
        if self.fields:
            data['fields'] = self.fields
        if self.campaigns:
            data['campaigns'] = self.campaigns
        if self.link:
            data['link'] = self.link
        if self.reason:
            data['reason'] = self.reason
        if self.sent:
            data['sent'] = self.sent
        if self.opened:
            data['opened'] = self.opened
        if self.clicked:
            data['clicked'] = self.clicked
        if self.message:
            data['message'] = self.message

        return data

    @staticmethod
    def _new_from_json_dict(data):
        return Subscriber(
            email=data.get('email', None),
            name=data.get('name', None),
            date=data.get('date', None),
            groups=data.get('groups', None),
            fields=data.get('fields', None),
            campaigns=data.get('campaigns', None),
            link=data.get('link', None),
            reason=data.get('reason', None),
            sent=data.get('sent', None),
            opened=data.get('opened', None),
            clicked=data.get('clicked', None),
            message=data.get('message', None),
        )
