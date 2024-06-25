import scrapy

import scrapy

class MySpider(scrapy.Spider):
    name = "scrapydown"

    def __init__(self, url=None, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        if not url:
            raise ValueError("A target URL must be provided")
        self.start_urls = [url]

    def parse(self, response):
        try:
            # Extract input fields
            input_fields = response.css('input[type="text"], input[type="email"], input[type="password"], input[type="number"], input[type="url"], input[type="tel"], input[type="search"], input[type="date"], input[type="time"], input[type="datetime-local"], input[type="month"], input[type="week"]')
            for field in input_fields:
                yield {
                    'type': 'input',
                    'name': field.attrib.get('name'),
                    'value': field.attrib.get('value', ''),
                    'placeholder': field.attrib.get('placeholder', '')
                }

            # Extract textarea fields
            textarea_fields = response.css('textarea')
            for field in textarea_fields:
                yield {
                    'type': 'textarea',
                    'name': field.attrib.get('name'),
                    'value': field.css('::text').get(),
                    'placeholder': field.attrib.get('placeholder', '')
                }

            # Extract select fields
            select_fields = response.css('select')
            for field in select_fields:
                options = field.css('option')
                options_list = [{'value': option.attrib.get('value', ''), 'text': option.css('::text').get()} for option in options]
                yield {
                    'type': 'select',
                    'name': field.attrib.get('name'),
                    'options': options_list
                }

            # Follow links to the next pages
            next_page = response.css('a.next::attr(href)').get()
            if next_page is not None:
                yield response.follow(next_page, self.parse)
        except Exception as e:
            self.logger.error(f"Error parsing response: {e}")
