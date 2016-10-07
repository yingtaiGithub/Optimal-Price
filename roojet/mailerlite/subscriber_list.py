class SubscriberList(object):
    def __init__(self, **kwargs):
        defaults = {
            'updated': None,
            'bounced': None,
            'name': None,
            'unsubscribed': None,
            'date': None,
            'total': None,
            'id': None,
            'date': None,
        }

        for (param, default) in defaults.iteritems():
            setattr(self, param, kwargs.get(param, default))

    def __str__(self):
        return self.AsJsonString()

    def AsJsonString(self):
        return json.dumps(self.AsDict(), sort_keys=True)

    def AsDict(self):
        data = {}

        if self.updated:
            data['updated'] = self.updated
        if self.bounced:
            data['bounced'] = self.bounced
        if self.name:
            data['name'] = self.name
        if self.unsubscribed:
            data['unsubscribed'] = self.unsubscribed
        if self.total:
            data['total'] = self.total
        if self.id:
            data['id'] = self.id
        if self.date:
            data['date'] = self.date

        return data

    @staticmethod
    def _new_from_json_dict(data):
        return SubscriberList(
            updated=data.get('updated', None),
            bounced=data.get('bounced', None),
            name=data.get('name', None),
            unsubscribed=data.get('unsubscribed', None),
            total=data.get('total', None),
            id=data.get('id', None),
            date=data.get('date', None),
        )
