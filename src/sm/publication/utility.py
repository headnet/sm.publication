from BTrees.IOBTree import IOBTree
from BTrees.OOBTree import OOBTree

from DateTime import DateTime

from Persistence import Persistent

from zope.interface import implements

from sm.publication.interfaces import IOrderFormStorage


class OrderFormStorage(Persistent):
    implements(IOrderFormStorage)

    def __init__(self):
        self.storage = IOBTree()
        self.indeces = OOBTree()

    def getData(self, min_timestamp=None, max_timestamp=None):
        if min_timestamp and max_timestamp:
            indeces = self.indeces['timestamp'].keys(
                min=min_timestamp,
                max=max_timestamp
            )
        else:
            indeces = []

        result = []
        for i in indeces or self.storage.keys():
            data = self.storage[i]
            data.update({'id': i})

            result.append(data)

        return result

    def addToIndex(self, index, key, value):
        if index not in self.indeces:
            self.indeces[index] = OOBTree()

        self.indeces[index][key] = value

    def addOrder(self, order, title=''):
        if len(self.storage) == 0:
            new_key = 0
        else:
            new_key = self.storage.maxKey()
            new_key += 1

        new_dict = {}

        for key in order.keys():
            new_dict[key] = order[key]

        new_dict['timestamp'] = DateTime()
        new_dict['title'] = title

        self.storage[new_key] = new_dict

        self.addToIndex('timestamp', new_key, new_dict['timestamp'])
