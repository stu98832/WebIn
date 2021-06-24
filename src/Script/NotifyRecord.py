from datetime import datetime

class NotifyRecord:
    def __init__(self):
        self.ID = -1
        self.Title = ''
        self.Description = ''
        self.Content = ''
        self.UpdateTime = datetime(1970, 1, 1)
        self.IsRead = False
        self.Key = ''
    
    @staticmethod
    def FromDB(data):
        record = NotifyRecord()
        record.ID = data['id']
        record.Title = data['title']
        record.Description = data['desc']
        record.Content = data['content']
        record.UpdateTime = datetime.strptime(data['update_time'], '%Y:%m:%d %H:%M:%S')
        record.IsRead = str(data['is_read']) == '1'
        record.Key = data['key']
        return record