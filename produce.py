import streamlit as st

# 언어 설정
if 'language' not in st.session_state:
    st.session_state.language = 'ko'  # 기본 언어를 한국어로 설정

# 사이드바 메뉴
st.sidebar.title("메뉴")
menu = st.sidebar.radio("선택하세요:", ["앱 추가", "앱 삭제", "앱 수정", "앱 목록 보기", "앱 선택"])

# 언어 선택 드롭다운
language = st.sidebar.selectbox("언어를 선택하세요:", options=["ko", "en"],
                                  format_func=lambda x: "한국어" if x == "ko" else "English")
st.session_state.language = language  # 선택한 언어 저장

# 앱 제목
st.title(translations[st.session_state.language]['title'])

if menu == "앱 추가":
    # 앱 추가 입력란
    app_name_input = st.text_input(translations[st.session_state.language]['app_name'])
    app_description_input = st.text_area(translations[st.session_state.language]['app_description'])
    rating_input = st.select_slider(translations[st.session_state.language]['app_rating'], options=[1, 2, 3, 4, 5])
    comment_input = st.text_area(translations[st.session_state.language]['app_comment'])
    genre_input = st.selectbox(translations[st.session_state.language]['select_genre'], genre_options)

    # 앱 추가 버튼
    if st.button(translations[st.session_state.language]['add_app_button']):
        if app_name_input and app_description_input:
            if add_app(app_name_input, app_description_input, rating_input, comment_input, genre_input):
                st.success(translations[st.session_state.language]['app_added'].format(app_name=app_name_input))
            else:
                st.warning(translations[st.session_state.language]['app_exists'].format(app_name=app_name_input))
        else:
            st.warning("앱 이름과 설명을 입력하세요.")

elif menu == "앱 삭제":
    # 앱 삭제 입력란
    app_name_delete = st.selectbox(translations[st.session_state.language]['delete_app'],
                                    [app["name"] for app in st.session_state.app_list])

    # 앱 삭제 버튼
    if st.button(translations[st.session_state.language]['delete_app_button']):
        if app_name_delete:
            delete_app(app_name_delete)
            st.success(translations[st.session_state.language]['app_deleted'].format(app_name=app_name_delete))
        else:
            st.warning("삭제할 앱을 선택하세요.")

elif menu == "앱 수정":
    # 앱 수정 입력란
    app_name_update = st.selectbox(translations[st.session_state.language]['update_app'],
                                    [app["name"] for app in st.session_state.app_list])
    new_rating_input = st.select_slider(translations[st.session_state.language]['update_rating'], options=[1, 2, 3, 4, 5])
    new_genre_input = st.selectbox(translations[st.session_state.language]['update_genre'], genre_options)

    # 앱 수정 버튼
    if st.button(translations[st.session_state.language]['update_app_button']):
        if app_name_update:
            update_app(app_name_update, new_rating_input, new_genre_input)
            st.success(translations[st.session_state.language]['app_updated'].format(app_name=app_name_update))
        else:
            st.warning("수정할 앱을 선택하세요.")

elif menu == "앱 목록 보기":
    # 현재 저장된 앱 목록 표시
    st.subheader(translations[st.session_state.language]['saved_apps'])
    if st.session_state.app_list:
        app_df = pd.DataFrame(st.session_state.app_list)
        st.dataframe(app_df)  # Streamlit에서 데이터프레임을 테이블로 보여줍니다.
    else:
        st.write(translations[st.session_state.language]['no_apps'])

elif menu == "앱 선택":
    # 앱 선택 및 세부 정보 보기
    if st.session_state.app_list:
        selected_app = st.selectbox("앱을 선택하세요:", [app["name"] for app in st.session_state.app_list])

        if st.button("앱 세부 정보 보기"):
            app_details = next((app for app in st.session_state.app_list if app["name"] == selected_app), None)
            if app_details:
                show_app_details(app_details)
    else:
        st.write(translations[st.session_state.language]['no_apps'])
