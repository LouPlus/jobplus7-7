import scrapy

class LiePinS(scrapy.Spider):
    name = 'paliepin'
    start_urls = ['https://www.liepin.com/']

    def parse(self, response):
        for i in response.css('li.clearfix'):    
            if i == 0:
                continue
        
            url = i.css('p.job-title a::attr(href)').extract_first()
            
            request = scrapy.Request('https:'+url, callback=self.parse_detail)
            yield request
            
    
    def parse_detail(self, response):
            yield{
                'degree':response.css('div.job-qualifications span::text').extract()[0], 
                'work_year':response.css('div.job-qualifications span::text').extract()[1], 
                'welfare':response.css('div.tag-list span::text').extract(),
                'industry':response.css('ul.new-compintro a::text').extract_first().strip(),
                'size':response.css('ul.new-compintro li::text').extract()[2].strip(),
                'address':response.css('ul.new-compintro li::text').extract()[3].strip(),
                'logo':response.css('div.company-logo img::attr(src)').extract_first(),
                'job':response.css('div.title-info h1::text').extract_first(),
                'salary':response.css('div.job-title-left p::text').extract_first().strip(),
                'name':response.css('div.title-info a::attr(title)').extract_first(),
                'city':response.css('p.basic-infor a::text').extract_first()
            }
