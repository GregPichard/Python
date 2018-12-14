import eikon
eikon.set_app_key('638fa3bbb90349d5a97dc60c1c0cc4b0b5646846')
eikon.get_news_headlines('R:LHAG.DE', date_from='2018-01-01T00:00:00', date_to='2018-12-13T18:00:00')

df = eikon.get_timeseries(["MSFT.O"],
                          start_date="2018-01-01",
                          end_date="2018-12-13")
df
