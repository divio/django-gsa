class FakeQuerySet(object):
    """Fake query set used for list_detail view.
    
    Implements just methods required for list_detail.
    """
    def __init__(self, items): 
        self.items = items
        
    def _clone(self): 
        return self    
    
    def __len__(self): 
        return len(self.items)
    
    def __getitem__(self, k): 
        return self.items[k]
