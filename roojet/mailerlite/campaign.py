import json


class Campaign(object):
    def __init__(self, **kwargs):
        defaults = {
            'unsubscribes': None,
            'uniqueOpens': None,
            'url': None,
            'bounces': None,
            'junk': None,
            'clicks': None,
            'started': None,
            'done': None,
            'total': None,
            'id': None,
            'opens': None,
            'subject': None,
        }

        for (param, default) in defaults.iteritems():
            setattr(self, param, kwargs.get(param, default))

    def __str__(self):
        return self.AsJsonString()

    def AsJsonString(self):
        return json.dumps(self.AsDict(), sort_keys=True)

    def AsDict(self):
        data = {}

        if self.unsubscribes:
            data['unsubscribes'] = self.unsubscribes
        if self.uniqueOpens:
            data['uniqueOpens'] = self.uniqueOpens
        if self.url:
            data['url'] = self.url
        if self.bounces:
            data['bounces'] = self.bounces
        if self.junk:
            data['junk'] = self.junk
        if self.clicks:
            data['clicks'] = self.clicks
        if self.started:
            data['started'] = self.started
        if self.done:
            data['done'] = self.done
        if self.total:
            data['total'] = self.total
        if self.id:
            data['id'] = self.id
        if self.opens:
            data['opens'] = self.opens
        if self.subject:
            data['subject'] = self.subject

        return data

    @staticmethod
    def _new_from_json_dict(data):
        return Campaign(
            unsubscribes=data.get('unsubscribes', None),
            uniqueOpens=data.get('uniqueOpens', None),
            url=data.get('url', None),
            bounces=data.get('bounces', None),
            junk=data.get('junk', None),
            clicks=data.get('clicks', None),
            started=data.get('started', None),
            done=data.get('done', None),
            total=data.get('total', None),
            id=data.get('id', None),
            opens=data.get('opens', None),
            subject=data.get('subject', None),
        )
