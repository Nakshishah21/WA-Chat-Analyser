import streamlit as st
import preprrocess, helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title('WA chat Analyzer')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprrocess.preprocess(data)


    # unique user perr chat
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user=st.sidebar.selectbox("show analysis", user_list)

    if st.sidebar.button("Show Analysis"):
        # Top Statistics
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

        st.title("Top Statistics")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(
                f"""
                <h3 style='font-size:25px;'>Total Messages</h3>
                <h1 style='font-size:40px; color:#00FFAA;'>{num_messages}</h1>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f"""
                <h3 style='font-size:25px;'>Total Words</h3>
                <h1 style='font-size:40px; color:#FFD700;'>{words}</h1>
                """,
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                f"""
                <h3 style='font-size:25px;'>Media Shared</h3>
                <h1 style='font-size:40px; color:#FF4B4B;'>{num_media_messages}</h1>
                """,
                unsafe_allow_html=True
            )

        with col4:
            st.markdown(
                f"""
                <h3 style='font-size:25px;'>Links Shared</h3>
                <h1 style='font-size:40px; color:#4DA6FF;'>{num_links}</h1>
                """,
                unsafe_allow_html=True
            )

        # Monthly Timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily Timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Activity Map
        st.title('Activity Map')

        col1, col2 = st.columns(2)

        with col1:
            st.header('Most Busy Day')
            busy_day = helper.week_activity_mapping(selected_user, df)

            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color="red")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header('Most Busy Month')
            busy_month = helper.month_activity_mapping(selected_user, df)

            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color="orange")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap=helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

    # findding busiest user
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df = helper.most_busy(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
   #WordCloud
        st.title("Word Cloud")
        df_wc=helper.create_wordcloud(selected_user,df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

    # most common words
        st.title("Common Words")
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title("Most Common Words")
        st.pyplot(fig)

    # emoji  Analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")
        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)


