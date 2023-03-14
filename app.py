"""
@author: Soumil Baldota
"""
import os
import json
import streamlit as st
import plotly
import pandas as pd
import numpy as np
import pandas as pd
import re
from textblob import TextBlob
from wordcloud import WordCloud
import seaborn as sns
import matplotlib.pyplot as plt
import cufflinks as cf
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.io as pio
import nltk
nltk.download('vader')
from nltk.sentiment.vader import SentimentIntensityAnalyzer


constraints = ['#B34D22', '#EBE00C', '#1FEB0C', '#0C92EB', '#EB0CD5']
def categorical_variable_summary(df, column_name):
  fig = make_subplots(rows = 1, cols = 2, 
                      subplot_titles = ('Countplot', 'Percentage'),
                      specs = [[{"type" : "xy"}, {'type' : 'domain'}]])
  
  fig.add_trace(go.Bar(y = df[column_name].value_counts().values.tolist(),
                       x = [str(i) for i in df[column_name].value_counts().index],
                       text = df[column_name].value_counts().values.tolist(),
                       textfont = dict(size = 14),
                       name = column_name,
                       textposition = 'auto',
                       showlegend = False,
                       marker = dict(color = constraints,
                                     line = dict(color = '#DBE6EC',
                                                 width = 1))),
                row = 1, col = 1)
  
  fig.add_trace(go.Pie(labels = df[column_name].value_counts().keys(),
                       values = df[column_name].value_counts().values,
                       textfont = dict(size = 18),
                       textposition = 'auto',
                       showlegend = False,
                       name = column_name,
                       marker = dict(colors = constraints)),
                row = 1, col = 2)
  
  fig.update_layout(title = {'text' : column_name, 'y' : 0.9, 'x' : 0.5,
                             'xanchor' : 'center', 'yanchor' : 'top'},
                    template = 'plotly_white')
  
  return fig

def analyser(car = 'a', dataset = 'a'):

	print(os.path.join(dataset, f"{car}.json"))
	a = rf"./{dataset}/{car}.json"
	f = open(a)
	data = json.load(f)
	l = []

	for k,v in data.items():
		for j in v:
			l.append((j, int(k)))

	df = pd.DataFrame(l, columns = ['reviews', 'overall'])
	rt = lambda x : re.sub("[^a-zA-Z]", ' ', str(x))
	df["reviews"] = df["reviews"].map(rt)
	df["reviews"] = df["reviews"].str.lower()

	#creating an instance of SentimentIntensityAnalyzer
	sent_analyzer = SentimentIntensityAnalyzer()

	df[['polarity', 'subjectivity']] = df['reviews'].apply(lambda Text:pd.Series(TextBlob(Text).sentiment))
	#polarity sends the mood and ranges between 0 and 1 - more towards 1, it is positive and towards 0, it is negative

	for index, row in df['reviews'].iteritems():
	  score = sent_analyzer.polarity_scores(row)

	  neg = score['neg']
	  neu = score['neu']
	  pos = score['pos']

	  if neg > pos:
	    df.loc[index, 'sentiment'] = "Negative"
	  elif pos > neg:
	    df.loc[index, 'sentiment'] = "Positive"
	  else:
	    df.loc[index, 'sentiment'] = "Neutral"

	return [categorical_variable_summary(df, 'overall'),
					categorical_variable_summary(df, 'sentiment')
					]

def main():
	st.title('Mahindra Data Analysis')

	car = st.selectbox('Select name of the car',
							[
							"thar","scorpio","xuv700",
							"scorpio-classic","xuv300",
							"bolero","bolero-neo","xuv400-ev",
							"kuv-100-nxt","alturas-g4","marazzo"
							]
						)
	dataset = st.selectbox('Select dataset to analyse',
						[
							"cardekho",
							"carwale"
						]
						)

	if(st.button('analyse')):
		plots = analyser(dataset = dataset,car = car)
		st.plotly_chart(plots[0], 
			use_container_width=True)
		st.plotly_chart(plots[1], 
			use_container_width=True)
		# analyser()
if __name__ == '__main__':
    main()