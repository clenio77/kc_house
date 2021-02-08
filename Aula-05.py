import pandas as pd
import streamlit as st
import plotly.express as px


def main():
    #functions
    @st.cache(allow_output_mutation=True)
    def get_data(path):
        df = pd.read_csv(path)
        df['date'] = pd.to_datetime(df['date'])
        return df

    df = get_data('./datasets/dados.csv')
    #df.drop(df.columns[[0]], axis=1, inplace=True)


    # Categorizing the Level column
    def add_level(df):
        for i in range(len(df)):
            if (df.loc[i, 'price'] > 0) & (df.loc[i, 'price'] < 321950):
                df.loc[i, 'level'] = 'nivel_0'
            elif (df.loc[i, 'price'] > 321950) & (df.loc[i, 'price'] < 450000):
                df.loc[i, 'level'] = 'nivel_1'
            elif (df.loc[i, 'price'] > 450000) & (df.loc[i, 'price'] < 645000):
                df.loc[i, 'level'] = 'nivel_2'
            else:
                df.loc[i, 'level'] = 'nivel_3'

    #Map interactive
    def map_interative(df):
        #houses = df[['id', 'lat', 'long', 'price', 'level']]
        fig = px.scatter_mapbox(houses,
                                lat='lat',
                                lon='long',
                                color='level',
                                size='price',
                                # color_continuous_scale=px.colors.cyclical.IceFire,
                                size_max=15,
                                zoom=10)
        fig.update_layout(mapbox_style='open-street-map')
        fig.update_layout(height=600, margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
        st.plotly_chart(fig)
        #st.write(fig)

    activities = ["EDA", "Plots", "Questions"]
    choice = st.sidebar.selectbox("Select Activities", activities)

    #st.title('Class 05 - Analisys House Rocket Company!')
    st.markdown("<h1 style='text-align: center; color:blue;'>Class 05 - Analisys House Rocket Company!</h1>",unsafe_allow_html=True)

    if choice == 'EDA':
        #st.subheader("**Exploratory Data Analysis**")
        st.markdown("<h1 style='text-align: center;fonte-size:20px;'>Exploratory Data Analysis</h1>",unsafe_allow_html=True)
        #df = st.file_uploader("Upload a Dataset", type=["csv", "txt"])
        #df = get_data('./datasets/dados.csv')
        st.write(df.head())

        if st.sidebar.checkbox("Number Of Rows and Columns"):
            st.write('{} linhas  e  {} colunas.'.format(df.shape[0],df.shape[1]))

        if st.sidebar.checkbox("Show Columns"):
            all_columns = df.columns.to_list()
            st.write(all_columns)

        if st.sidebar.checkbox("Summary"):
            st.write(df.describe())

        if st.sidebar.checkbox("Verify null rows"):
            lista_nulos = df.isnull().sum()
            st.write(lista_nulos)

        if st.sidebar.checkbox("Deleting null lines"):
            df.dropna()
            st.write(df.isnull().any().sum())

        if st.sidebar.checkbox("Verify data duplicated"):
            st.write(df.duplicated().sum())

        if st.sidebar.checkbox("Show Selected Columns"):
            all_columns = df.columns.to_list()
            selected_columns = st.multiselect("Select Columns", all_columns)
            new_df = df[selected_columns]
            st.dataframe(new_df)

    elif choice == 'Plots':
        #st.subheader("Data Visualization Dashboard and Maps")
        st.markdown("<h1 style='text-align: center; color:blue; font-size: 22px;'>Data Visualization Dashboard and Maps</h1>", unsafe_allow_html=True)
        if st.sidebar.checkbox("Interactive Map by Property Price"):
            st.markdown("<h2 style='text-align: center; color:black; font-size: 18px;'>Map by Property Type!</h2>",unsafe_allow_html=True)
            #st.subheader('**Map for Level!** ')
            houses = df[['id', 'lat', 'long', 'price', 'level']].copy()
            fig = px.scatter_mapbox(
                houses,
                lat='lat',
                lon='long',
                #color='level',
                size='price',
                color_continuous_scale=px.colors.cyclical.IceFire,
                size_max=15,
                zoom=10
            )

            fig.update_layout(mapbox_style='open-street-map')
            fig.update_layout(height=900, margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
            st.plotly_chart(fig)


        if st.sidebar.checkbox("Adding Interactive Filters"):
            houses = df[['id', 'lat', 'long', 'price', 'level', 'is_waterfront']]
            #df['is_waterfront'] = df['waterfront'].apply(lambda x: 'yes' if x == 1 else 'no')
            # Select the type you want to view:
            selector = st.sidebar.radio(
                "Select the type you want to view:",
                ("Is_waterFront", "No_waterFront"),
            )
            if selector == "Is_waterFront":
                houses['is_waterfront'] = df['is_waterfront'] == 'yes'
            elif selector == "No_waterFront":
                houses['is_waterFront'] = df['is_waterfront'] == 'no'
            st.plotly_chart(houses)
            #add_filter_interactive(df)


        if st.sidebar.checkbox("Map for Price"):
            st.markdown("<h2 style='text-align: center; color:black; font-size: 18px;'>Map by Price!</h2>",unsafe_allow_html=True)
            #is_check = st.sidebar.checkbox('Display Map for Price')
            #houses = df[['id', 'lat', 'long', 'price', 'level']]
            price_min = int(df['price'].min())
            price_max = int(df['price'].max())
            price_avg = int(df['price'].mean())

            price_slider = st.sidebar.slider('Price Range',
                                             price_min,
                                             price_max,
                                             price_avg)

            houses = df[df['price'] < price_slider][['id', 'lat', 'long', 'price','level']]
            fig = px.scatter_mapbox(
                houses,
                lat='lat',
                lon='long',
                color='price',
                size='level',
                #color_continuous_scale=px.colors.cyclical.IceFire,
                size_max=15,
                zoom=10)
            fig.update_layout(mapbox_style='open-street-map')
            fig.update_layout(height=600, margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
            st.plotly_chart(fig)
            # st.write(fig)

        if st.sidebar.checkbox("Map for Number Bedrooms"):
            st.markdown("<h2 style='text-align: center; color:black; font-size: 18px;'>Map by Number Bedrooms!</h2>",unsafe_allow_html=True)
            houses = df[['id', 'lat', 'long', 'price', 'level','bedrooms']]
            bedrooms_min = int(df['bedrooms'].min())
            bedrooms_max = int(df['bedrooms'].max())
            bedrooms_avg = int(df['bedrooms'].mean())

            bedrooms_slider = st.sidebar.slider('Bedrooms range',
                                             bedrooms_min,
                                             bedrooms_max,
                                             bedrooms_avg)

            houses = df[df['bedrooms'] < bedrooms_slider][['id', 'lat', 'long', 'price','level','bedrooms']]
            fig = px.scatter_mapbox(houses,
                                    lat='lat',
                                    lon='long',
                                    color='price',
                                    size='bedrooms',
                                    #color_continuous_scale=px.colors.cyclical.IceFire,
                                    size_max=15,
                                    zoom=10)
            fig.update_layout(mapbox_style='open-street-map')
            fig.update_layout(height=600, margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
            st.plotly_chart(fig)
            #st.write(fig)

    elif choice == 'Questions':
        st.markdown("<h1 style='text-align: center; color:black; font-size: 36px;'>Questions!</h1>",unsafe_allow_html=True)
        #st.title("Questions")
        #df = st.file_uploader("Upload a Dataset", type=["csv", "txt", "xlsx"])
        #df = get_data('./datasets/dados.csv')
        # if df is not None:
        #     df = pd.read_csv(df)
        #     st.dataframe(df.head())


        if st.sidebar.checkbox("1. How many properties per level?"):
            st.markdown("<h2 style='text-align: left; color:black; font-size: 26px;font-family:serif;'>How many properties for level?</h2>",unsafe_allow_html=True)
            st.write('**Nivel 0:** preço entre R$ 0.00 e R$ 321.950 = **{}**'.format(df[df['level'] == 'nivel_0'].shape[0]))
            st.write('**Nivel 1:** preço entre R$ 321.950 e R$ 450.000 = **{}**.'.format(df[df['level'] == 'nivel_1'].shape[0]))
            st.write('**Nivel 2:** preço entre R$ 450.000 e R$ 645.000 = **{}**'.format(df[df['level'] == 'nivel_2'].shape[0]))
            st.write('**Nivel 3:** preço acima de  R$ 645.000 = **{}**'.format(df[df['level'] == 'nivel_3'].shape[0]))


        if st.sidebar.checkbox("What is the average size of the living room of the buildings by size?"):
            st.markdown("<h2 style='text-align: left; color:black; font-size: 26px;font-family: serif;'>What is the average size of the living room of the buildings by size?</h2>",unsafe_allow_html=True)
            size_0 = df[(df['sqft_living'] > 0) & (df['sqft_living'] < 1427)]
            size_1 = df[(df['sqft_living'] >= 1427) & (df['sqft_living'] < 1910)]
            size_2 = df[(df['sqft_living'] >= 1910) & (df['sqft_living'] < 2550)]
            size_3 = df[df['sqft_living'] >= 2550]
            st.write('A média do tamanha das salas de estar dos imóveis de size_0 é {:.02f}'.format(
                size_0.sqft_living.mean()))
            st.write('A média do tamanho das salas de estar dos imóveis de Size_1 é {:.02f}'.format(
                size_1.sqft_living.mean()))
            st.write('A média do tamanho das salas de estar dos imóveis de Size_2 é {:.02f}'.format(
                size_2.sqft_living.mean()))
            st.write('A média do tamanho das salas de estar dos imóveis de Size_3 é {:.02f}'.format(
                size_3.sqft_living.mean()))





            




    #read data
    # @st.cache(allow_output_mutation=True)
    # def get_data(path):
    #     data = pd.read_csv(path)
    #     #data['date'] = pd.to_datetime(data['date'])
    #     return data
    #
    #
    # # load data
    # data = get_data('./datasets/dados.csv')
    #
    # #view Data
    # st.dataframe(data)


if __name__ == '__main__':
    main()