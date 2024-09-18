from itemadapter import ItemAdapter
import mysql.connector


class SqlStorage:

    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='steam_data'
        )

        self.curr = self.conn.cursor()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        self.curr.execute(
            "INSERT INTO steamgen (title ,ram, size, discount, price, reviewnum, dlc, year, tag1, tag2, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (
                adapter.get('Title'),
                adapter.get('RAM'),
                adapter.get('Size'),
                adapter.get('Discount'),
                adapter.get('Price'),
                adapter.get('ReviewsNum'),
                adapter.get('DLC'),
                adapter.get('Year'),
                adapter.get('Tag_1'),
                adapter.get('Tag_2'),
                adapter.get('Image')
            )
        )
        return item

    def close_spider(self, spider):
        self.conn.commit()
        self.curr.close()
        self.conn.close()
