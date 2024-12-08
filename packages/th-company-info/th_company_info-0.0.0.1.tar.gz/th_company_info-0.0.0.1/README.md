# th-company-info
This is a educational library for getting data of company info from page dataforthai.com and return as a json respone.

## Installation
```
pip install th-company-info
```

## Usage

```
from th_company_info.scraper import th_company_info

try:
    tax_id = "0107542000011"  # Replace with a valid 13-digit tax ID
    data = th_company_info(tax_id)
    print(data)
except Exception as e:
    print(f"An error occurred: {e}")

```

## Response
```
{
    "tax_id": "0107542000011",
    "name_th": "บริษัท ซีพี ออลล์ จำกัด (มหาชน)",
    "name_en": "CP ALL PUBLIC COMPANY LIMITED",
    "description": "ดำเนินกิจการร้านค้าสะดวกซื้อ เพื่อจำหน่ายสินค้าอุปโภค-บริโภคหมวดธุรกิจ : ร้านสะดวกซื้อ/มินิมาร์ท",
    "status": "ยังดำเนินกิจการอยู่",
    "registered_date": "12 มีนาคม 2542",
    "registered_capital": "8,986,296,048 บาท",
    "address": "313 อาคารซี.พี.ทาวเวอร์ ชั้นที่ 24 ถนนสีลม แขวงสีลม เขตบางรัก กรุงเทพมหานคร 10500",
    "website": "www.cpall.co.th",
    "stock_symbol": "CPALL"
}
```

## Author
Grassroot Engineer
