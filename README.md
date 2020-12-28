# web_selenium
Automated Test interface and web page data consistency

nosetests -s 执行并捕获输出

nosetests  –h查看所有nose相关命令

输出简单报告：

  安装nose-html-reporting
  
  pip install nose-html-reporting
  
  运行参数：
  
  --with-html	
  
    Enable plugin HtmlOutput: Output test results as pretty html.
    
  --html-file=FILE
  
    Path to html file to store the report in. Default is nosetests.html in the working directory
    
  --html-report-template=FILE
  
    Path to jinja2 file to get the report template from. Default is templates/report.html from the package working directory
    
  --with-xunit
  
    输出xml格式
