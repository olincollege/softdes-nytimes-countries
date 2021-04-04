import pandas as pd
import matplotlib.pyplot as plt

def create_scatter_plot(country_name):
    """
    Display a scatter plot of hits per month for a country

    Args:
        country_name: a string that is the name of the country for which to
        visualize number of hits
    Returns:
        No return value
    """
    country_data = pd.read_csv(f'CountryData/{country_name}_data.csv')

    num_entries = len(country_data['MM-YYYY'])

    begin_date = country_data["MM-YYYY"][0]
    end_date = country_data["MM-YYYY"][num_entries - 1]

    plt.rc('axes', titlesize = 20)
    plt.rc('axes', labelsize = 15)
    plt.rc('xtick', labelsize = 10)
    plt.rc('ytick', labelsize = 10)

    plt.figure(figsize = (math.ceil(num_entries / 2), 5))
    plt.scatter(country_data['MM-YYYY'], country_data['Number of Hits'])

    plt.xticks(rotation = 45)

    plt.xlabel('Time Frame (MM-YYYY)')
    plt.ylabel('Number of Hits')
    plt.title(f'Number of Hits in NYTimes Articles per Month for ' \
              f'{country_name} from {begin_date} to {end_date}')

    plt.show()

def create_word_cloud_one_month(country_name, yearmonth):
    """
    Create a wordcloud based on the headlines collected about the country for
    the given month

    Args:
        country_name: a string representing the name of the country for which
        to create the wordcloud
        yearmonth: a string representing the month for which to get headlines,
        in YYYYMM format
    Returns:
        No return value
    """
    text = headline_list_to_string(country_name, yearmonth)
    num_words = len(text.split())

    background_flag_mask = np.array(Image.open(f"CountryFlags/{country_name}_flag.png"))

    wordcloud = WordCloud(mask=background_flag_mask, background_color="white",
                          stopwords = STOPWORDS, max_words = num_words).generate(text)
    colors = ImageColorGenerator(background_flag_mask)

    colored_cloud = wordcloud.recolor(color_func = colors)

    plt.figure(figsize = (20, 20))
    plt.axis('off')
    plt.imshow(colored_cloud)

def create_word_cloud_all(country_name):
    """
    Create a wordcloud based on all the headlines collected about the country

    Args:
        country_name: a string representing the name of the country for which
        to create the wordcloud
    Returns:
        No return value
    """
    text = all_headlines_in_string(country_name)
    num_words = len(text.split())

    background_flag_mask = np.array(Image.open(f"CountryFlags/{country_name}_flag.png"))

    wordcloud = WordCloud(mask=background_flag_mask, background_color="white",
                          stopwords = STOPWORDS, max_words = num_words).generate(text)
    colors = ImageColorGenerator(background_flag_mask)

    colored_cloud = wordcloud.recolor(color_func = colors)

    plt.figure(figsize = (20, 20))
    plt.axis('off')
    plt.imshow(colored_cloud)

def create_bubble_chart(country_name):
    """
    Create a bubble chart for a country based on number of hits and sentiment
    score over time

    Args:
        country_name: a string representing the name of the country for which
        to create a chart
    Returns:
        No return value
    """
    country_data = pd.read_csv(f"CountryData/{country_name}_data.csv")
    num_entries = len(country_data["Country Name"])

    plt.figure(figsize = (math.ceil(num_entries / 2), 5))
    plt.scatter(x = country_data["MM-YYYY"], y = country_data["Sentiment Score (-1 to 1)"],
                s = 10 * country_data["Number of Hits"], alpha = .5, color = 'purple')

    plt.xticks(rotation = 45)
    plt.xlabel("Time Frame (MM-YYYY)", size = 15)
    plt.ylabel("Sentiment Score (-1 to 1)", size = 15)

    begin_date = country_data["MM-YYYY"][0]
    end_date = country_data["MM-YYYY"][num_entries - 1]

    plt.title(f"New York Times Attention and Attitude Towards {country_name} from " \
              f"{begin_date} to {end_date}", size = 20)

    plt.show()
