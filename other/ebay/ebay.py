#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import time
from xml.dom.minidom import parse
import xml.dom.minidom
from lxml.etree import HTML
import json

def get_api(itemId):
    url = "https://api.ebay.com/ws/api.dll"

    # payload = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<GetItemRequest xmlns=\"urn:ebay:apis:eBLBaseComponents\">\n\t<RequesterCredentials>\n\t\t<eBayAuthToken>AgAAAA**AQAAAA**aAAAAA**E22gVw**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6wHl4egCJGFqAqdj6x9nY+seQ**dGUBAA**AAMAAA**IMs5d70hebXySsE+9A+0ep9JUniYq7cr/UcZ9qcsGp50qg8VZcpdhA2mq/FwZdDCBXwBFK2Y0A9nlxWpSI9ZrysRZXF5yOMmkDHB1FTG2mdoGkGYe8i3qKyx0XZs49RP8j946ZPiRow3JACEC4T6LseuJDNRClQMeoe8L9ypk3V5CXjkvojQnkHISMnqHgYv+vvybqXobPjdELWgnOE2/usn6xdvOoruXZjwiGLdWSaFQ9hkR8q2n3gjoK6jv/B7srA6FytS9MwYKnkOJHCFFOEstiek6wlv2uRdShlT3o8KNsHFX9UnVY0GKD9PqofvmWRv0jlDVX5s9afNXx/5UgZpL/VowYKXb53BT5YiHuwwMIdTb51dVwRk/dPK4If0zftw+2r/0Sj0rhPC7LBw17YlCAUZZ5x4/DZagj77VLXskwpLkolfhJ2nfbHy1hoHnZENWuA0pnTLoroI+ZXwVB2U0YLLGREbnCfoSod5Vswv5o59JfiKmrJEKdAIZ2dxIkcze65isawZRtzYD1fBl0x30KNp7BIXYTocywa91BG322wzTJKwp7wfXwrrUz1e1iXigM111HwyjLjJ13IbgSyTeqmPuOn2QcoI3cUzgWXZpFang1nKdH/AMasxX9gonYctjTGZHyHYksMtb7joYkZX9XTWKY3VCFft5EdJPpiYfy2qZGNtkftGICBCwnZ21vGEUDpfnVGZszeKK9OarvJMFDVh/MJAsew1WOZTYrIvW2ow9/hVCyuY1llrOHlo</eBayAuthToken>\n\t</RequesterCredentials>\n\t<ItemID>282651820547</ItemID>\n\t<IncludeTaxTable>true</IncludeTaxTable>\n\t<IncludeWatchCount>true</IncludeWatchCount>\n\t<IncludeItemSpecifics>true</IncludeItemSpecifics>\n</GetItemRequest>"
    body = '<?xml version="1.0" encoding="utf-8"?><GetItemRequest xmlns="urn:ebay:apis:eBLBaseComponents"><RequesterCredentials><eBayAuthToken>AgAAAA**AQAAAA**aAAAAA**E22gVw**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6wHl4egCJGFqAqdj6x9nY+seQ**dGUBAA**AAMAAA**IMs5d70hebXySsE+9A+0ep9JUniYq7cr/UcZ9qcsGp50qg8VZcpdhA2mq/FwZdDCBXwBFK2Y0A9nlxWpSI9ZrysRZXF5yOMmkDHB1FTG2mdoGkGYe8i3qKyx0XZs49RP8j946ZPiRow3JACEC4T6LseuJDNRClQMeoe8L9ypk3V5CXjkvojQnkHISMnqHgYv+vvybqXobPjdELWgnOE2/usn6xdvOoruXZjwiGLdWSaFQ9hkR8q2n3gjoK6jv/B7srA6FytS9MwYKnkOJHCFFOEstiek6wlv2uRdShlT3o8KNsHFX9UnVY0GKD9PqofvmWRv0jlDVX5s9afNXx/5UgZpL/VowYKXb53BT5YiHuwwMIdTb51dVwRk/dPK4If0zftw+2r/0Sj0rhPC7LBw17YlCAUZZ5x4/DZagj77VLXskwpLkolfhJ2nfbHy1hoHnZENWuA0pnTLoroI+ZXwVB2U0YLLGREbnCfoSod5Vswv5o59JfiKmrJEKdAIZ2dxIkcze65isawZRtzYD1fBl0x30KNp7BIXYTocywa91BG322wzTJKwp7wfXwrrUz1e1iXigM111HwyjLjJ13IbgSyTeqmPuOn2QcoI3cUzgWXZpFang1nKdH/AMasxX9gonYctjTGZHyHYksMtb7joYkZX9XTWKY3VCFft5EdJPpiYfy2qZGNtkftGICBCwnZ21vGEUDpfnVGZszeKK9OarvJMFDVh/MJAsew1WOZTYrIvW2ow9/hVCyuY1llrOHlo</eBayAuthToken></RequesterCredentials><ItemID>{itemId}</ItemID><IncludeTaxTable>true</IncludeTaxTable><IncludeWatchCount>true</IncludeWatchCount><IncludeItemSpecifics>true</IncludeItemSpecifics></GetItemRequest>'
    headers = {
        'X-EBAY-API-COMPATIBILITY-LEVEL': "967",
        'X-EBAY-API-DEV-NAME': "2049a9dd-15bc-430c-92c8-1184afa2904e",
        'X-EBAY-API-APP-NAME': "kaidenxu-Analytic-PRD-c246ab0a7-42d9aad7",
        'X-EBAY-API-CERT-NAME': "PRD-246ab0a79154-d85b-43f4-97e9-47b7",
        'X-EBAY-API-CALL-NAME': "GetItem",
        'X-EBAY-API-SITEID': "0",
        'Content-Type': "text/xml",
        'cache-control': "no-cache",
    }
    data = body.format(itemId=itemId)
    response = requests.request("POST", url, data=data, headers=headers)

    print(response.text)
    with open('myxml.xml','w') as f:
        f.write(response.text)

    DOMTree = xml.dom.minidom.parse('myxml.xml')
    collection = DOMTree.documentElement

    ItemList = collection.getElementsByTagName("Item")
    # print(ItemList)
    for myeitem in ItemList:
        Craw_date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        Craw_ebaysite = '0'
        Crawitemid = itemId
        Country_value = myeitem.getElementsByTagName("Country")[0].childNodes[0].data
        Currency_value = myeitem.getElementsByTagName("Currency")[0].childNodes[0].data
        ItemID_value = itemId
        ConvertedStartPrice_value = myeitem.getElementsByTagName("ListingDetails")[0].getElementsByTagName("ConvertedStartPrice")[0].childNodes[0].data
        StartTime_value = myeitem.getElementsByTagName("ListingDetails")[0].getElementsByTagName("StartTime")[0].childNodes[0].data
        EndTime_value = myeitem.getElementsByTagName("ListingDetails")[0].getElementsByTagName("EndTime")[0].childNodes[0].data
        ListingDuration_value = myeitem.getElementsByTagName("ListingDuration")[0].childNodes[0].data
        Location_value = myeitem.getElementsByTagName("Location")[0].childNodes[0].data
        CategoryID_value = myeitem.getElementsByTagName("PrimaryCategory")[0].getElementsByTagName("CategoryID")[0].childNodes[0].data
        CategoryName_value = myeitem.getElementsByTagName("PrimaryCategory")[0].getElementsByTagName("CategoryName")[0].childNodes[0].data
        QuantitySold_value = myeitem.getElementsByTagName("SellingStatus")[0].getElementsByTagName("QuantitySold")[0].childNodes[0].data
        ShipToLocations_value = myeitem.getElementsByTagName("ShipToLocations")[0].childNodes[0].data
        Title_value = myeitem.getElementsByTagName("Title")[0].childNodes[0].data
        VATPercent_value = ''
        SubTitle_value = myeitem.getElementsByTagName("SubTitle")[0].childNodes[0].data if myeitem.getElementsByTagName("SubTitle") else ''
        ShippingService_value = myeitem.getElementsByTagName("ShippingDetails")[0].getElementsByTagName("ShippingServiceOptions")[0].getElementsByTagName("ShippingService")[0].childNodes[0].data
        ShippingServiceCost_value = myeitem.getElementsByTagName("ShippingDetails")[0].getElementsByTagName("ShippingServiceOptions")[0].getElementsByTagName("ShippingServiceCost")[0].childNodes[0].data
        ShippingServiceAdditionalCost_value = myeitem.getElementsByTagName("ShippingDetails")[0].getElementsByTagName("ShippingServiceOptions")[0].getElementsByTagName("ShippingServiceAdditionalCost")[0].childNodes[0].data
        ShippingServicePriority_value = myeitem.getElementsByTagName("ShippingDetails")[0].getElementsByTagName("ShippingServiceOptions")[0].getElementsByTagName("ShippingServicePriority")[0].childNodes[0].data
        ExpeditedService_value = myeitem.getElementsByTagName("ShippingDetails")[0].getElementsByTagName("ShippingServiceOptions")[0].getElementsByTagName("ExpeditedService")[0].childNodes[0].data
        ShippingTimeMin_value = ''
        ShippingTimeMax_value = ''
        Street1_value = ''
        CityName_value = ''
        CountryName_value = ''
        VATSite_value = ''
        VATID_value = ''
        sku_value = myeitem.getElementsByTagName("SKU")[0].childNodes[0].data
        CurrentPrice_value = myeitem.getElementsByTagName("SellingStatus")[0].getElementsByTagName("CurrentPrice")[0].childNodes[0].data
        ListingStatus_value = myeitem.getElementsByTagName("SellingStatus")[0].getElementsByTagName("ListingStatus")[0].childNodes[0].data
        Site_value = myeitem.getElementsByTagName("Site")[0].childNodes[0].data
        HitCount_value = myeitem.getElementsByTagName("HitCount")[0].childNodes[0].data
        eBayPlus_value = myeitem.getElementsByTagName("eBayPlus")[0].childNodes[0].data
        eBayPlusEligible_value = myeitem.getElementsByTagName("eBayPlusEligible")[0].childNodes[0].data
        Adult_value = myeitem.getElementsByTagName("ListingDetails")[0].getElementsByTagName("Adult")[0].childNodes[0].data
        ListingType_value = myeitem.getElementsByTagName("ListingType")[0].childNodes[0].data
        taxtable = ''
        SellInfo_FeedbackScore_value = myeitem.getElementsByTagName("Seller")[0].getElementsByTagName("FeedbackScore")[0].childNodes[0].data
        SellInfo_PositiveFeedbackPercent_value = myeitem.getElementsByTagName("Seller")[0].getElementsByTagName("PositiveFeedbackPercent")[0].childNodes[0].data
        SellInfo_NewUser_value = myeitem.getElementsByTagName("Seller")[0].getElementsByTagName("NewUser")[0].childNodes[0].data
        SellInfo_RegistrationDate_value = myeitem.getElementsByTagName("Seller")[0].getElementsByTagName("RegistrationDate")[0].childNodes[0].data
        SellInfo_Site_value = myeitem.getElementsByTagName("Seller")[0].getElementsByTagName("Site")[0].childNodes[0].data
        SellInfo_Status_value = myeitem.getElementsByTagName("Seller")[0].getElementsByTagName("Status")[0].childNodes[0].data
        SellInfo_UserID_value = myeitem.getElementsByTagName("Seller")[0].getElementsByTagName("UserID")[0].childNodes[0].data
        SellInfo_UserIDLastChanged_value = myeitem.getElementsByTagName("Seller")[0].getElementsByTagName("UserIDChanged")[0].childNodes[0].data
        SellInfo_StoreURL_value = myeitem.getElementsByTagName("Seller")[0].getElementsByTagName("SellerInfo")[0].getElementsByTagName("StoreURL")[0].childNodes[0].data
        SellInfo_TopRatedSeller_value = myeitem.getElementsByTagName("Seller")[0].getElementsByTagName("SellerInfo")[0].getElementsByTagName("TopRatedSeller")[0].childNodes[0].data if myeitem.getElementsByTagName("Seller")[0].getElementsByTagName("SellerInfo")[0].getElementsByTagName("TopRatedSeller") else ''
        GalleryURL = myeitem.getElementsByTagName("PictureDetails")[0].getElementsByTagName("GalleryURL")[0].childNodes[0].data
        CategoryID_value2 = myeitem.getElementsByTagName("PrimaryCategory")[0].getElementsByTagName("CategoryID")[0].childNodes[0].data
        CategoryName_value2 = myeitem.getElementsByTagName("PrimaryCategory")[0].getElementsByTagName("CategoryName")[0].childNodes[0].data



        obj = {
            "Craw_date": Craw_date,
            "Craw_ebaysite": Craw_ebaysite,
            "Crawitemid": Crawitemid,
            "Country_value": Country_value,
            "Currency_value": Currency_value,
            "ItemID_value": ItemID_value,
            "ConvertedStartPrice_value": ConvertedStartPrice_value,
            "StartTime_value": StartTime_value,
            "EndTime_value": EndTime_value,
            "ListingDuration_value": ListingDuration_value,
            "Location_value": Location_value,
            "CategoryID_value": CategoryID_value,
            "CategoryName_value": CategoryName_value,
            "QuantitySold_value": QuantitySold_value,
            "ShipToLocations_value": ShipToLocations_value,
            "Title_value": Title_value,
            "VATPercent_value": VATPercent_value,
            "SubTitle_value": SubTitle_value,
            "ShippingService_value": ShippingService_value,
            "ShippingServiceCost_value": ShippingServiceCost_value,
            "ShippingServiceAdditionalCost_value": ShippingServiceAdditionalCost_value,
            "ShippingServicePriority_value": ShippingServicePriority_value,
            "ExpeditedService_value": ExpeditedService_value,
            "ShippingTimeMin_value": ShippingTimeMin_value,
            "ShippingTimeMax_value": ShippingTimeMax_value,
            "Street1_value": Street1_value,
            "CityName_value": CityName_value,
            "CountryName_value": CountryName_value,
            "VATSite_value": VATSite_value,
            "VATID_value": VATID_value,
            "sku_value": sku_value,
            "CurrentPrice_value": CurrentPrice_value,
            "ListingStatus_value": ListingStatus_value,
            "Site_value": Site_value,
            "HitCount_value": HitCount_value,
            "eBayPlus_value": eBayPlus_value,
            "eBayPlusEligible_value": eBayPlusEligible_value,
            "Adult_value": Adult_value,
            "ListingType_value": ListingType_value,
            "taxtable": taxtable,
            "SellInfo_FeedbackScore_value": SellInfo_FeedbackScore_value,
            "SellInfo_PositiveFeedbackPercent_value": SellInfo_PositiveFeedbackPercent_value,
            "SellInfo_NewUser_value": SellInfo_NewUser_value,
            "SellInfo_RegistrationDate_value": SellInfo_RegistrationDate_value,
            "SellInfo_Site_value": SellInfo_Site_value,
            "SellInfo_Status_value": SellInfo_Status_value,
            "SellInfo_UserID_value": SellInfo_UserID_value,
            "SellInfo_UserIDLastChanged_value": SellInfo_UserIDLastChanged_value,
            "SellInfo_StoreURL_value": SellInfo_StoreURL_value,
            "SellInfo_TopRatedSeller_value": SellInfo_TopRatedSeller_value,
            "GalleryURL": GalleryURL,
            "CategoryID_value2": CategoryID_value2,
            "CategoryName_value2": CategoryName_value2,
        }
        print(json.dumps(obj))
        save_res = Craw_date+'||'+Craw_ebaysite+'||'+Crawitemid+'||'+Country_value+'||'+Currency_value+'||'+ItemID_value+'||'+ConvertedStartPrice_value+'||'+StartTime_value+'||'+EndTime_value+'||'+ListingDuration_value+'||'+Location_value+'||'+CategoryID_value+'||'+CategoryName_value+'||'+QuantitySold_value+'||'+ShipToLocations_value+'||'+Title_value+'||'+VATPercent_value+'||'+SubTitle_value+'||'+ShippingService_value+'||'+ShippingServiceCost_value+'||'+ShippingServiceAdditionalCost_value+'||'+ShippingServicePriority_value+'||'+ExpeditedService_value+'||'+ShippingTimeMin_value+'||'+ShippingTimeMax_value+'||'+Street1_value+'||'+CityName_value+'||'+CountryName_value+'||'+VATSite_value+'||'+VATID_value+'||'+sku_value+'||'+CurrentPrice_value+'||'+ListingStatus_value+'||'+Site_value+'||'+HitCount_value+'||'+eBayPlus_value+'||'+eBayPlusEligible_value+'||'+Adult_value+'||'+ListingType_value+'||'+taxtable+'||'+SellInfo_FeedbackScore_value+'||'+SellInfo_PositiveFeedbackPercent_value+'||'+SellInfo_NewUser_value+'||'+SellInfo_RegistrationDate_value+'||'+SellInfo_Site_value+'||'+SellInfo_Status_value+'||'+SellInfo_UserID_value+'||'+SellInfo_UserIDLastChanged_value+'||'+SellInfo_StoreURL_value+'||'+SellInfo_TopRatedSeller_value+'||'+GalleryURL+'||'+CategoryID_value2+'||'+CategoryName_value2
        save_res = save_res.replace('\n','').replace(',','，').replace('||',',')+'\n'
        with open('results.csv','a') as f:
            f.write(save_res)


def start(url):
    response = requests.get(url)
    # print(response.text)
    html = HTML(response.text)
    itemId = html.xpath('string(//div[@id="descItemNumber"])')
    print(itemId)
    get_api(itemId)

if __name__ == '__main__':
    with open('results.csv','w') as f:
        save_res = 'Craw_date,Craw_ebaysite,Crawitemid,Country_value,Currency_value,ItemID_value,ConvertedStartPrice_value,StartTime_value,EndTime_value,ListingDuration_value,Location_value,CategoryID_value,CategoryName_value,QuantitySold_value,ShipToLocations_value,Title_value,VATPercent_value,SubTitle_value,ShippingService_value,ShippingServiceCost_value,ShippingServiceAdditionalCost_value,ShippingServicePriority_value,ExpeditedService_value,ShippingTimeMin_value,ShippingTimeMax_value,Street1_value,CityName_value,CountryName_value,VATSite_value,VATID_value,sku_value,CurrentPrice_value,ListingStatus_value,Site_value,HitCount_value,eBayPlus_value,eBayPlusEligible_value,Adult_value,ListingType_value,taxtable,SellInfo_FeedbackScore_value,SellInfo_PositiveFeedbackPercent_value,SellInfo_NewUser_value,SellInfo_RegistrationDate_value,SellInfo_Site_value,SellInfo_Status_value,SellInfo_UserID_value,SellInfo_UserIDLastChanged_value,SellInfo_StoreURL_value,SellInfo_TopRatedSeller_value,GalleryURL,CategoryID_value2,CategoryName_value2\n'
        f.write(save_res)

    item_list = []
    with open('urls.txt') as f:
        results = f.readlines()
        for res in results:
            item_list.append(res.strip())

    for url in item_list:
        start(url)