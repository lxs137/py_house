from sf_record_spider.Pipelines.mysql import MySQLConnectorSF
from scrapy.exceptions import DropItem
import re
from datetime import date
from sf_record_spider.items import SellItem,RentItem
class SFDataBasePipeline(object):

    def process_item(self, item, spider):
        if isinstance(item, SellItem):
            insert_dict = {}
            if item['community_id']:
                insert_dict['code'] = item['code']

                time_str = item['release_time']
                time_str = ''.join(time_str.split())
                time_str = re.sub('[^0-9]', '-', time_str)
                time_list = time_str.split('-')
                insert_dict['release_time'] = date(int(time_list[0]), int(time_list[1]), int(time_list[2]))

                insert_dict['price_all'] = item['price_all']
                insert_dict['price_per'] = item['price_per']
                insert_dict['first_pay'] = item.get('first_pay')
                insert_dict['month_pay'] = item.get('month_pay')
                insert_dict['floor'] = item.get('floor')
                insert_dict['area_build'] = item['area_build']
                insert_dict['direction'] = item.get('direction')
                insert_dict['decoration'] = item.get('decoration')
                insert_dict['house_model'] = item.get('house_model')
                insert_dict['build_time'] = item.get('build_time')
                insert_dict['house_structure'] = item.get('house_structure')
                insert_dict['house_type'] = item.get('house_type')
                insert_dict['property_type'] = item.get('property_type')
                MySQLConnectorSF.insert_sell_info(insert_dict, item['community_id'])
            else:
                raise DropItem('SellItem: Missing community_info_id.')
        elif isinstance(item, RentItem):
            insert_dict = {}
            if item['community_id']:
                insert_dict['code'] = item['code']
                time_list = item.get('update_time').split('/')
                insert_dict['update_time'] = date(int(time_list[0]), int(time_list[1]), int(time_list[2]))
                insert_dict['price'] = item['price']
                insert_dict['rate'] = item['rate']
                insert_dict['pay_type'] = item.get('pay_type')
                insert_dict['house_type'] = item.get('house_type')
                insert_dict['house_model'] = item.get('house_model')
                insert_dict['area_build'] = item.get('area_build')
                if insert_dict['area_build'] == None and insert_dict['house_type'] != None:
                    insert_dict['area_build'] = int(float(re.search('[0-9]+', insert_dict['house_type']).group()))
                insert_dict['floor'] = item.get('floor')
                insert_dict['direction'] = item.get('direction')
                insert_dict['decoration'] = item.get('decoration')
                insert_dict['support_bed'] = item.get('support_bed')
                insert_dict['support_furniture'] = item.get('support_furniture')
                insert_dict['support_gas'] = item.get('support_gas')
                insert_dict['support_warm'] = item.get('support_warm')
                insert_dict['support_network'] = item.get('support_network')
                insert_dict['support_tv'] = item.get('support_tv')
                insert_dict['support_condition'] = item.get('support_condition')
                insert_dict['support_fridge'] = item.get('support_fridge')
                insert_dict['support_wash'] = item.get('support_wash')
                insert_dict['support_water'] = item.get('support_water')
                MySQLConnectorSF.insert_rent_info(insert_dict, item['community_id'])
            else:
                raise DropItem('RentItem: Missing community_info_id.')

