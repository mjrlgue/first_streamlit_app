import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title("My parent new dinner")

streamlit.header('🍞Breakfast Menu')
streamlit.text('🥣 🐔 Omega 3 & Blueberry Oatmeal')
streamlit.text('🐔 Kale, Spinach & Rocket Smoothie')
streamlit.text('🥑🍞Hard-Boiled Free-Range Egg')


streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
streamlit.text(fruityvice_response)

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")

def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  if not fruit_choice:
    streamlit.write('The user entered ', fruit_choice)
  else:
    func = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(func)
    
except URLError as e:
  streamlit.error()



streamlit.stop()

streamlit.header("The fruit load contains:")

def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * from fruit_load_list")
    return my_cur.fetchall()

# add button to load fruits
if streamlit.button('Get fruit load'):
  snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list
  streamlit.dataframe(my_data_rows)





fruit_add = streamlit.text_input('What fruit would you like to add')
streamlit.write('Thanks for adding ', fruit_add)

my_cur.execute("insert into fruit_load_list values ('from streamlit')")
